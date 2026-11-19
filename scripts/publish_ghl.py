#!/usr/bin/env python3
"""Schedules (or publishes now) one vertical video on the GoHighLevel / LeadConnector Social Planner:
Instagram Reel, Facebook Reel, TikTok and YouTube Short, in a single post.

NEVER run this without the creator having given the date and time IN THIS CONVERSATION.

  python publish_ghl.py --video final.mp4 --cover cover.png --caption post-caption.txt \
      --when "2026-11-20 09:00" --yt-title "Title #shorts" [--networks instagram,facebook,tiktok,youtube] [--dry-run]
  python publish_ghl.py ... --when now          # immediate publish

--when     "YYYY-MM-DD HH:MM" in config publish.timezone, or "now". Refuses past times and times before
           publish.earliestHour.
--caption  UTF-8 .txt with the final post caption (at most rules.maxHashtags hashtags).
--cover    PNG/JPG; converted to a 1080x1920 JPG under 2 MB.
Credentials: secret ghl_token (secrets_store.py) + config publish.ghl.locationId / publish.ghl.userId.
Writes publish_ghl.json (body + response) next to the video.

Lessons learned (do not undo):
- The time is converted here with zoneinfo. Never compute it in a shell (`TZ=... date` in Git Bash returns UTC).
- GHL creates one child post per network; the real status lives in the children. Never PUT a new
  scheduleDate on an existing post and never delete/recreate without listing the day's posts first:
  that produced duplicates on Instagram and TikTok.
- "Publish now" is status "published" without scheduleDate (GHL refuses schedules ~2 min ahead).
  The response is only {"message": "Created Post"}: that is SUCCESS, never repeat the POST.
- The cover is stored in the post's top-level `thumbnail`; media[0].thumbnail comes back empty (normal).
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import config  # noqa: E402
from secrets_store import read  # noqa: E402

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:  # Python < 3.9
    raise SystemExit("Python 3.9+ required")

CFG = config.load()
PUB = CFG["publish"]
try:
    TZ = ZoneInfo(PUB["timezone"])
except ZoneInfoNotFoundError:
    raise SystemExit("this Python has no time-zone data: python -m pip install tzdata")
API = "https://services.leadconnectorhq.com"

ap = argparse.ArgumentParser()
ap.add_argument("--video", required=True)
ap.add_argument("--cover", required=True)
ap.add_argument("--caption", required=True)
ap.add_argument("--when", required=True, help='"YYYY-MM-DD HH:MM" in %s, or "now"' % PUB["timezone"])
ap.add_argument("--yt-title", required=True, help="YouTube Short title (max 100 characters)")
ap.add_argument("--networks", default=",".join(PUB["networks"]))
ap.add_argument("--dry-run", action="store_true", help="build the body and stop (no upload, no post)")
a = ap.parse_args()

TOKEN = read("ghl_token")
LOC, USER = PUB["ghl"]["locationId"], PUB["ghl"]["userId"]
if not LOC or not USER:
    raise SystemExit("set publish.ghl.locationId and publish.ghl.userId with config.py")
HDR = ["-H", "Authorization: Bearer " + TOKEN, "-H", "Version: 2021-07-28", "-H", "Accept: application/json"]


def curl(args, timeout=120):
    r = subprocess.run(["curl", "-sS", "-m", str(timeout)] + args, capture_output=True, text=True, encoding="utf-8")
    try:
        return json.loads(r.stdout)
    except ValueError:
        sys.exit("ERROR GHL response: " + (r.stdout or r.stderr)[:500])


def now_local():
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M")


# 1) time
NOW = a.when.strip().lower() == "now"
when_utc = None
if not NOW:
    local = datetime.strptime(a.when, "%Y-%m-%d %H:%M").replace(tzinfo=TZ)
    if local <= datetime.now(timezone.utc):
        sys.exit("ERROR time in the past: %s (now it is %s %s)" % (a.when, now_local(), PUB["timezone"]))
    if local.hour < PUB.get("earliestHour", 0):
        sys.exit("ERROR before %02d:00: %s" % (PUB["earliestHour"], a.when))
    when_utc = local.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
print("now in %s: %s | publish: %s" % (PUB["timezone"], now_local(), "IMMEDIATE" if NOW else a.when))

# 2) caption and title
caption = open(a.caption, encoding="utf-8").read().strip()
tags = [w for w in caption.split() if w.startswith("#")]
if len(tags) > CFG["rules"]["maxHashtags"]:
    sys.exit("ERROR the caption has %d hashtags; the limit is %d" % (len(tags), CFG["rules"]["maxHashtags"]))
if len(a.yt_title) > 100:
    sys.exit("ERROR YouTube title longer than 100 characters")

# 3) connected accounts
acc = curl(HDR + ["%s/social-media-posting/%s/accounts" % (API, LOC)])["results"]["accounts"]
by_net = {}
for x in acc:
    if not x.get("deleted") and not x.get("isExpired"):
        by_net.setdefault(x["platform"], x["id"])
nets = [n.strip() for n in a.networks.split(",") if n.strip()]
missing = [n for n in nets if n not in by_net]
if missing:
    sys.exit("ERROR no valid connected account for: %s (connected: %s)" % (missing, list(by_net)))

# 4) cover as 1080x1920 JPG
tmpd = tempfile.mkdtemp()
cover = os.path.join(tmpd, "cover.jpg")
subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-i", a.cover,
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920", "-q:v", "3", cover], check=True)
if os.path.getsize(cover) > 2_000_000:
    sys.exit("ERROR cover is still larger than 2 MB")

body = {"accountIds": [by_net[n] for n in nets], "userId": USER, "createdBy": USER, "type": "reel", "summary": caption,
        "media": [{"url": "VIDEO_URL", "type": "video/mp4", "thumbnail": "COVER_URL"}]}
if NOW:
    body["status"] = "published"
else:
    body["status"], body["scheduleDate"] = "scheduled", when_utc
if "instagram" in nets:
    body["instagramPostDetails"] = {"type": "reel", "showOnFeed": True}
if "facebook" in nets:
    body["facebookPostDetails"] = {"type": "reel"}
if "tiktok" in nets:
    body["tiktokPostDetails"] = {"privacyLevel": "PUBLIC_TO_EVERYONE", "enableComment": True, "enableDuet": True,
                                 "enableStitch": True, "promoteOtherBrand": False, "promoteYourBrand": False, "videoDisclosure": False}
if "youtube" in nets:
    body["youtubePostDetails"] = {"title": a.yt_title, "type": "short", "privacyLevel": "public"}

if a.dry_run:
    print(json.dumps(body, ensure_ascii=False, indent=1))
    sys.exit(0)


# 5) upload to the Media Library (GHL publishes from these URLs)
def upload(path, name):
    j = curl(HDR + ["-X", "POST", API + "/medias/upload-file", "-F", "file=@" + path, "-F", "name=" + name, "-F", "hosted=false"], 600)
    url = j.get("url") or sys.exit("ERROR upload %s: %s" % (path, j))
    head = subprocess.run(["curl", "-sSIL", "-m", "60", url], capture_output=True, text=True).stdout
    size = [l for l in head.splitlines() if l.lower().startswith("content-length")]
    if not size or int(size[-1].split(":")[1]) != os.path.getsize(path):
        sys.exit("ERROR uploaded file does not match the local one: " + url)
    print("UPLOAD", os.path.basename(path), "->", url)
    return url


stem = os.path.splitext(os.path.basename(a.video))[0].lower().replace(" ", "-")
body["media"][0]["url"] = upload(a.video, "reel_%s.mp4" % stem)
body["media"][0]["thumbnail"] = upload(cover, "reel_%s_cover.jpg" % stem)

# 6) create the post (ONE call: never repeat the POST on an ambiguous answer, list the posts instead)
bf = os.path.join(tmpd, "body.json")
json.dump(body, open(bf, "w", encoding="utf-8"), ensure_ascii=False)
res = curl(HDR + ["-X", "POST", "%s/social-media-posting/%s/posts" % (API, LOC), "-H", "Content-Type: application/json", "--data-binary", "@" + bf])
out = os.path.join(os.path.dirname(os.path.abspath(a.video)), "publish_ghl.json")
json.dump({"body": body, "response": res}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
post = (res.get("results") or {}).get("post")


def children():
    """GHL creates one post per network; the real status of each network is in them, not in the parent."""
    q = {"skip": "0", "limit": "40", "includeUsers": "false", "type": "all",
         "fromDate": datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00.000Z"), "toDate": "2099-01-01T00:00:00.000Z"}
    lf = os.path.join(tmpd, "list.json")
    json.dump(q, open(lf, "w", encoding="utf-8"))
    ps = curl(HDR + ["-X", "POST", "%s/social-media-posting/%s/posts/list" % (API, LOC), "-H", "Content-Type: application/json", "--data-binary", "@" + lf])
    net = {v: k for k, v in by_net.items()}
    return [(net.get((p.get("accountIds") or [""])[0], "?"), p["_id"], p.get("status"), p.get("publishedAt"))
            for p in (ps.get("results") or {}).get("posts", [])
            if (p.get("summary") or "").strip() == caption and len(p.get("accountIds") or []) == 1 and not p.get("deleted")]


if NOW:
    if not (res.get("success") and "Created" in str(res.get("message"))):
        sys.exit("ERROR publishing: " + json.dumps(res, ensure_ascii=False)[:800])
    fs = []
    for _ in range(24):  # up to ~10 min
        time.sleep(25)
        fs = children()
        print(datetime.now(TZ).strftime("%H:%M:%S"), " | ".join("%s=%s" % (n, s) for n, _, s, _ in fs))
        if fs and all(s in ("published", "failed", "error") for _, _, s, _ in fs):
            break
    json.dump({"body": body, "response": res, "per_network": fs}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("log:", out)
    sys.exit(0)

if not post:
    sys.exit("ERROR creating the post (do NOT retry before listing the day's posts): " + json.dumps(res, ensure_ascii=False)[:800])

# 7) verify what was stored
chk = curl(HDR + ["%s/social-media-posting/%s/posts/%s" % (API, LOC, post["_id"])])["results"]["post"]
print("OK", post["_id"], chk["status"], chk["scheduleDate"], "| networks:", ",".join(nets), "| accounts:", len(chk["accountIds"]))
print("cover stored:", "yes" if chk.get("thumbnail") else "NO (check the preview in the Social Planner)")
for k in ("instagramPostDetails", "facebookPostDetails", "tiktokPostDetails", "youtubePostDetails"):
    if k in body and not chk.get(k):
        print("WARN", k, "did not come back stored")
print("log:", out)
