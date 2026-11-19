#!/usr/bin/env python3
"""Creator config for travus-reels-maker (no secrets here: those live in secrets_store.py).

  python config.py status                    # "configured" (exit 0) or "not-configured" (exit 1)
  python config.py path                      # where the config lives
  python config.py init                      # writes the defaults if there is no config yet
  python config.py show                      # prints the whole config
  python config.py get defaults.theme
  python config.py set creator.handle "@me"  # value is parsed as JSON when possible (true, 0.2, ["a","b"])
  python config.py set setupDone true

Location: $TRAVUS_REELS_HOME/config.json, default ~/.travus-reels/config.json
"""
import copy
import io
import json
import os
import sys

HOME = os.environ.get("TRAVUS_REELS_HOME") or os.path.join(os.path.expanduser("~"), ".travus-reels")
PATH = os.path.join(HOME, "config.json")

DEFAULTS = {
    "version": 1,
    "setupDone": False,
    "creator": {
        "name": "",            # shown nowhere unless the creator asks; used for the README of each project
        "handle": "",          # @handle for the CTA ("follow @handle")
        "niche": "",           # e.g. "AI for business", "health and weight loss"
        "audience": "",        # e.g. "Brazilians living in the US"
        "language": "pt-BR",   # language of the videos, captions and post copy
        "voiceStyle": "",      # one line on how the creator talks, e.g. "friendly, direct, no jargon"
    },
    "paths": {"projects": os.path.join(os.path.expanduser("~"), "Reels")},
    "defaults": {
        "source": "ask",                 # talking-head | voiceover | topic | hybrid | ask
        "editStyle": "auto",             # auto | classic | editorial-canvas | product-kinetic | terminal-neon | cinematic-3d
        "theme": "bold-dark",            # bold-dark | clean-light | neon-retro | brand
        "palette": {},                   # overrides for the theme (accent, alert, ink, ground...)
        "captions": {"mode": "word", "style": "outline", "position": "low", "uppercase": True},
        "titleBar": "whole",             # whole | hook | none
        "duration": "45-60",             # 15-30 | 30-45 | 45-60 | 60-90 | story-58
        "pace": "dynamic",               # calm | dynamic | frantic
        "jumpCuts": "aggressive",        # aggressive | light | none
        "punchIns": True,
        "broll": "stock",                # stock | official | motion-only | none
        "brollLayout": "mix",            # mix (alternate full screen and split screen) | full | split
        "logos": True,
        "music": {"enabled": True, "style": "tech", "volume": 0.2},   # tech | corporate | lofi | cinematic | synthwave | upbeat
        "sfx": "subtle",                 # subtle | punchy | none
        "narrationTone": "friendly",     # friendly | journalistic | didactic | hype
        "cta": {"type": "question", "keyword": ""},  # comment-keyword | question | follow | link-in-bio | none
        "deliverables": ["mp4", "phone-copy", "cover", "post-caption"],
        "phoneCopyMaxMB": 30,
    },
    "rules": {
        "bannedOpeners": [],             # first words a reel must never start with
        "maxHashtags": 5,                # Instagram accepts at most 5
        "fixedHashtags": [],
        "captionFooter": "",             # text appended to every post caption (e.g. "Follow @me for more")
        "approveScript": True,           # stop for script approval when generating from a topic
        "approveNarration": True,        # send the full narration before editing
    },
    "voice": {
        "provider": "none",              # none | fish | elevenlabs
        "voiceId": "",                   # cloned voice / reference id (not a secret)
        "model": "",                     # fish: s2.1-pro | elevenlabs: eleven_v3 (empty = provider default)
        "speed": 1.08,
        "temperature": 0.85,
    },
    "gemini": {                          # Google Gemini API (secret: gemini_api_key)
        "videoModel": "gemini-omni-1.2-flash",   # AI video (Veo 3.1 API was shut down on 2026-10-22)
        "imageModel": "gemini-nano-banana-2.1",  # b-roll images
        "thumbModel": "gemini-3-pro-image",      # covers/thumbnails (best text rendering)
        "resolution": "1080p",
    },
    "avatar": {                          # the creator's AI avatar for generated talking-head shots
        "name": "",                      # label only (e.g. the avatar's name in the Gemini app); the API cannot load it by name
        "refsDir": os.path.join(HOME, "avatar"),  # 1-3 reference images of the avatar (face, framing, outfit)
        "description": "",               # one line: look, clothes, setting it usually appears in
        "voice": "fish",                 # fish = narrate with the cloned voice | model = let the video model speak
    },
    "publish": {
        "provider": "manual",            # manual | ghl
        "timezone": "America/New_York",
        "networks": ["instagram", "facebook", "tiktok", "youtube"],
        "earliestHour": 8,
        "ghl": {"locationId": "", "userId": ""},
    },
}


def _merge(base, over):
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        out[k] = _merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def load():
    if not os.path.exists(PATH):
        return copy.deepcopy(DEFAULTS)
    return _merge(DEFAULTS, json.load(io.open(PATH, encoding="utf-8")))


def save(cfg):
    os.makedirs(HOME, exist_ok=True)
    io.open(PATH, "w", encoding="utf-8").write(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")


def get(cfg, dotted):
    cur = cfg
    for part in dotted.split("."):
        cur = cur[part]
    return cur


def set_(cfg, dotted, value):
    parts = dotted.split(".")
    cur = cfg
    for part in parts[:-1]:
        cur = cur.setdefault(part, {})
    cur[parts[-1]] = value


def _parse(v):
    try:
        return json.loads(v)
    except ValueError:
        return v


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    if a[0] == "path":
        print(PATH)
    elif a[0] == "status":
        ok = os.path.exists(PATH) and load().get("setupDone")
        print("configured" if ok else "not-configured")
        sys.exit(0 if ok else 1)
    elif a[0] == "init":
        if os.path.exists(PATH):
            print("exists:", PATH)
        else:
            save(copy.deepcopy(DEFAULTS))
            print("created:", PATH)
    elif a[0] == "show":
        print(json.dumps(load(), ensure_ascii=False, indent=2))
    elif a[0] == "get" and len(a) == 2:
        v = get(load(), a[1])
        print(json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v)
    elif a[0] == "set" and len(a) == 3:
        cfg = load()
        set_(cfg, a[1], _parse(a[2]))
        save(cfg)
        print("set", a[1], "=", json.dumps(get(cfg, a[1]), ensure_ascii=False))
    else:
        raise SystemExit(__doc__)
