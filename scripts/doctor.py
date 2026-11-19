#!/usr/bin/env python3
"""Checks everything travus-reels-maker needs and prints how to fix what is missing.

  python doctor.py            # tools + Python packages + config + secrets of the chosen providers
Exit code 1 when a REQUIRED item is missing.
"""
import importlib.util
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config  # noqa: E402
import secrets_store  # noqa: E402

rows = []
missing_required = False


def add(name, ok, detail, fix, required=True):
    global missing_required
    rows.append(("OK " if ok else ("MISSING" if required else "optional"), name, detail, "" if ok else fix))
    if required and not ok:
        missing_required = True


def version(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120, shell=(os.name == "nt"))
        return (r.stdout or r.stderr).strip().splitlines()[0] if r.returncode == 0 else None
    except Exception:
        return None


node = version(["node", "--version"])
add("node >= 18", bool(node) and int(node.lstrip("v").split(".")[0]) >= 18, node or "-", "install Node.js 18+ (https://nodejs.org)")
hf = version(["npx", "--yes", "hyperframes", "--version"]) if node else None
add("hyperframes CLI", bool(hf), hf or "-", "npx hyperframes --version (needs internet the first time)")
for tool in ("ffmpeg", "ffprobe"):
    add(tool, bool(shutil.which(tool)), shutil.which(tool) or "-", "install FFmpeg and put it on PATH (https://ffmpeg.org/download.html)")
add("curl", bool(shutil.which("curl")), shutil.which("curl") or "-", "install curl (only needed for publishing)", required=False)
add("yt-dlp", bool(shutil.which("yt-dlp")), shutil.which("yt-dlp") or "-",
    "optional, for official trailers/clips you have the right to use: pip install yt-dlp", required=False)

for mod, pkg in (("fontTools", "fonttools"), ("brotli", "brotli")):
    add("python: " + pkg, importlib.util.find_spec(mod) is not None, "", "python -m pip install " + pkg)
try:
    from zoneinfo import ZoneInfo

    ZoneInfo("America/New_York")
    tz_ok = True
except Exception:
    tz_ok = False
add("python: tzdata", tz_ok, "", "python -m pip install tzdata (needed for scheduling)", required=False)
add("python: keyring", importlib.util.find_spec("keyring") is not None, secrets_store.backend(),
    "python -m pip install keyring (secure API-key storage; Windows falls back to DPAPI)", required=(os.name != "nt"))

cfg = config.load()
add("config", os.path.exists(config.PATH) and cfg.get("setupDone"), config.PATH, "run the first-time setup (the skill asks the questions)")
vp = cfg["voice"]["provider"]
if vp in ("fish", "elevenlabs"):
    key = "fish_api_key" if vp == "fish" else "elevenlabs_api_key"
    add("secret: " + key, bool(secrets_store.read(key, required=False)), "", "python scripts/secrets_store.py set " + key)
    add("voice id", bool(cfg["voice"]["voiceId"]), cfg["voice"]["voiceId"] or "-", "python scripts/config.py set voice.voiceId <id>")
if cfg["publish"]["provider"] == "ghl":
    add("secret: ghl_token", bool(secrets_store.read("ghl_token", required=False)), "", "python scripts/secrets_store.py set ghl_token")
    add("ghl locationId", bool(cfg["publish"]["ghl"]["locationId"]), "", "python scripts/config.py set publish.ghl.locationId <id>")

w = max(len(r[1]) for r in rows)
for st, name, detail, fix in rows:
    print("%-8s %-*s  %s%s" % (st, w, name, detail, ("   -> " + fix) if fix else ""))
sys.exit(1 if missing_required else 0)
