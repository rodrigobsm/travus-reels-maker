#!/usr/bin/env python3
"""Google Gemini API for reels: AI video shots (avatar or b-roll) and images (covers, b-roll).

  python gemini.py check
  python gemini.py video --prompt prompt.txt --out shot.mp4 [--avatar] [--refs a.png b.png] [--duration 8] [--aspect 9:16] [--resolution 1080p]
  python gemini.py image --prompt prompt.txt --out cover.png [--thumb] [--input face.png ...] [--aspect 9:16] [--size 2K]

- Secret: gemini_api_key (secrets_store.py). Models and avatar come from config.json -> "gemini" / "avatar".
- Video uses the Interactions API (POST /v1beta/interactions) with gemini-omni-1.2-flash by default.
  The Veo 3.1 predictLongRunning API was shut down on 2026-10-22.
- --avatar adds the reference images from config avatar.refsDir (max 3). The API cannot load an avatar
  saved in the Gemini app by its name: the references ARE the avatar. Describe their role in the prompt
  ("the man in the reference images").
- --thumb uses gemini.thumbModel (best text rendering) instead of gemini.imageModel.
- Prompts are files (UTF-8) so they can be reviewed and versioned next to the project.
Writes <out>.json with the request (without image data) and the raw response metadata.
"""
import argparse
import base64
import glob
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import config  # noqa: E402
from secrets_store import read  # noqa: E402

API = "https://generativelanguage.googleapis.com/v1beta"
CFG = config.load()
GEM = CFG.get("gemini", {})
AV = CFG.get("avatar", {})


def call(method, path, body=None, timeout=900, raw=False):
    headers = {"x-goog-api-key": read("gemini_api_key"), "Api-Revision": "2026-05-20"}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    url = path if path.startswith("http") else API + path
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            out = r.read()
            return out if raw else json.loads(out)
    except urllib.error.HTTPError as e:
        msg = e.read()[:800].decode("utf-8", "replace")
        hint = ""
        if e.code == 429 and "Free Tier" in msg:
            hint = ("\nHINT: image and video models have a 0 quota on the Gemini API free tier. Enable billing for this key's project "
                    "(aistudio.google.com -> Billing / ai.dev/rate-limit). Until then, make covers with HyperFrames.")
        raise SystemExit("ERROR Gemini %s %s: %s%s" % (e.code, path.split("?")[0], msg, hint))


def image_part(path):
    mt = mimetypes.guess_type(path)[0] or "image/png"
    return {"type": "image", "mime_type": mt, "data": base64.b64encode(open(path, "rb").read()).decode()}


def find_media(obj, kind):
    """Return (bytes or None, uri or None) for the first video/image block in the response."""
    stack = [obj]
    while stack:
        x = stack.pop()
        if isinstance(x, dict):
            mt = str(x.get("mime_type") or x.get("mimeType") or "")
            if (x.get("type") == kind or mt.startswith(kind + "/")) and (x.get("data") or x.get("uri")):
                return (base64.b64decode(x["data"]) if x.get("data") else None), x.get("uri")
            stack.extend(x.values())
        elif isinstance(x, list):
            stack.extend(x)
    return None, None


def strip_data(obj):
    if isinstance(obj, dict):
        return {k: ("<%d bytes base64>" % len(v) if k == "data" and isinstance(v, str) and len(v) > 200 else strip_data(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [strip_data(v) for v in obj]
    return obj


def save(kind, res, out, body):
    data, uri = find_media(res, kind)
    if data is None and uri:
        if "files/" in uri and not uri.startswith("http"):
            uri = API + "/" + uri.split("v1beta/")[-1]
        for _ in range(120):  # files can take a while to become ACTIVE
            meta = call("GET", uri.split("?")[0].replace(":download", "")) if "files/" in uri else {}
            if meta.get("state") in (None, "ACTIVE"):
                break
            if meta.get("state") == "FAILED":
                raise SystemExit("ERROR generation failed: %s" % json.dumps(meta)[:500])
            time.sleep(5)
        dl = uri if (":download" in uri or "alt=media" in uri) else uri + (":download?alt=media" if "files/" in uri else "")
        data = call("GET", dl, raw=True)
    if not data:
        raise SystemExit("ERROR no %s in the response: %s" % (kind, json.dumps(strip_data(res))[:1200]))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    open(out, "wb").write(data)
    json.dump({"request": strip_data(body), "response": strip_data(res)}, open(out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ok", out, "(%d KB)" % (len(data) // 1024))


def avatar_refs(extra):
    refs = list(extra or [])
    if not refs:
        d = os.path.expanduser(AV.get("refsDir", ""))
        refs = sorted(glob.glob(os.path.join(d, "*.png")) + glob.glob(os.path.join(d, "*.jpg")) + glob.glob(os.path.join(d, "*.jpeg")))
    if not refs:
        raise SystemExit("no avatar reference images: put 1-3 images in %s (see references/ai-video.md)" % AV.get("refsDir"))
    return refs[:3]


def cmd_check(_a):
    names = {m["name"].split("/")[-1] for m in call("GET", "/models?pageSize=1000").get("models", [])}
    for label, mid in (("video", GEM.get("videoModel")), ("image", GEM.get("imageModel")), ("thumb", GEM.get("thumbModel"))):
        print("%-6s %-28s %s" % (label, mid, "OK" if mid in names else "NOT LISTED (check the model id / access)"))
    d = os.path.expanduser(AV.get("refsDir", ""))
    n = len(glob.glob(os.path.join(d, "*.*"))) if os.path.isdir(d) else 0
    print("avatar %-28s %d reference image(s) in %s" % (AV.get("name") or "-", n, d))


def cmd_video(a):
    prompt = open(a.prompt, encoding="utf-8").read().strip()
    parts = []
    if a.avatar or a.refs:
        parts = [image_part(p) for p in avatar_refs(a.refs)]
    body = {"model": a.model or GEM.get("videoModel", "gemini-omni-1.2-flash"),
            "input": parts + [{"type": "text", "text": prompt}] if parts else prompt,
            "response_format": {"type": "video", "aspect_ratio": a.aspect, "resolution": a.resolution or GEM.get("resolution", "1080p"),
                                "duration": "%ss" % a.duration}}
    print("generating video (%s, %ss, %s, %d reference image(s))..." % (body["model"], a.duration, a.aspect, len(parts)))
    save("video", call("POST", "/interactions", body), a.out, body)


def cmd_image(a):
    prompt = open(a.prompt, encoding="utf-8").read().strip()
    parts = [image_part(p) for p in (a.input or [])]
    model = a.model or (GEM.get("thumbModel") if a.thumb else GEM.get("imageModel")) or "gemini-nano-banana-2.1"
    body = {"model": model, "input": parts + [{"type": "text", "text": prompt}],
            "response_format": {"type": "image", "aspect_ratio": a.aspect, "image_size": a.size}}
    print("generating image (%s, %s, %s)..." % (model, a.aspect, a.size))
    save("image", call("POST", "/interactions", body), a.out, body)


ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
sub.add_parser("check")
v = sub.add_parser("video")
v.add_argument("--prompt", required=True)
v.add_argument("--out", required=True)
v.add_argument("--avatar", action="store_true", help="use the avatar reference images from the config")
v.add_argument("--refs", nargs="*", help="explicit reference images (max 3)")
v.add_argument("--duration", type=int, default=8, help="3-15 seconds")
v.add_argument("--aspect", default="9:16")
v.add_argument("--resolution")
v.add_argument("--model")
i = sub.add_parser("image")
i.add_argument("--prompt", required=True)
i.add_argument("--out", required=True)
i.add_argument("--thumb", action="store_true", help="use the thumbnail model (best text rendering)")
i.add_argument("--input", nargs="*", help="input images (face photo, product, style reference)")
i.add_argument("--aspect", default="9:16")
i.add_argument("--size", default="2K", help="1K | 2K | 4K (uppercase K)")
i.add_argument("--model")
args = ap.parse_args()
{"check": cmd_check, "video": cmd_video, "image": cmd_image}[args.cmd](args)
