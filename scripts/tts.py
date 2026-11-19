#!/usr/bin/env python3
"""Voiceover with the creator's cloned voice. Provider comes from config.json -> voice.provider.

  python tts.py check                                  # voice + balance (no credit spent)
  python tts.py generate voice_script.json OUT_DIR     # one MP3 per segment in OUT_DIR
  python tts.py generate voice_script.json OUT_DIR --only 03   # redo only the segment whose file starts with "03"

voice_script.json:
  {"speed": 1.08, "temperature": 0.85,
   "segments": [{"file": "01 Hook", "text": "[excited, talking to a friend] ..."}, ...]}
  ("velocidade"/"temperatura"/"trechos"/"arquivo"/"texto" are accepted too.)

Providers
- fish        Fish Audio, model s2.1-pro by default. Free-form tags in [brackets] at the start of each sentence.
              API credit is billed apart from the website plan: https://fish.audio/app/developers/billing
              HTTP 402 = no API credit.
- elevenlabs  ElevenLabs, model eleven_v3 by default (supports [audio tags]). With any other model the
              [tags] are stripped, because older models would read them out loud.
Secrets: fish_api_key / elevenlabs_api_key (secrets_store.py). Voice id: config voice.voiceId.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import config  # noqa: E402
from secrets_store import read  # noqa: E402

CFG = config.load()["voice"]
PROVIDER = CFG["provider"]


def http(method, url, headers, body=None):
    data = None
    if body is not None:
        headers = dict(headers, **{"Content-Type": "application/json"})
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.read(), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        raise SystemExit("ERROR %s %s %s: %s" % (PROVIDER, e.code, url.split("?")[0], e.read()[:400].decode("utf-8", "replace")))


def voice_id():
    v = CFG.get("voiceId")
    if not v:
        raise SystemExit("set the voice id first:  python config.py set voice.voiceId <id>")
    return v


# ---------------------------------------------------------------- Fish Audio
FISH = "https://api.fish.audio"


def fish_headers(model=None):
    h = {"Authorization": "Bearer " + read("fish_api_key")}
    if model:
        h["model"] = model
    return h


def fish_check():
    m = json.loads(http("GET", FISH + "/model/" + voice_id(), fish_headers())[0])
    print("voice:", m.get("title"), "| state:", m.get("state"), "| languages:", m.get("languages"), "| visibility:", m.get("visibility"))
    if m.get("visibility") == "public":
        print("TIP: your cloned voice is PUBLIC on Fish Audio; consider making it private.")
    c = json.loads(http("GET", FISH + "/wallet/self/api-credit", fish_headers())[0])
    print("API credit:", c.get("credit"))


def fish_tts(text, speed, temperature):
    body = {"text": text, "reference_id": voice_id(), "format": "mp3", "mp3_bitrate": 192, "sample_rate": 44100,
            "latency": "normal", "normalize": True, "temperature": temperature, "top_p": 0.7,
            "prosody": {"speed": speed, "volume": 0, "normalize_loudness": True}}
    return http("POST", FISH + "/v1/tts", fish_headers(CFG.get("model") or "s2.1-pro"), body)


# ---------------------------------------------------------------- ElevenLabs
EL = "https://api.elevenlabs.io"


def el_headers():
    return {"xi-api-key": read("elevenlabs_api_key")}


def el_check():
    v = json.loads(http("GET", EL + "/v1/voices/" + voice_id(), el_headers())[0])
    print("voice:", v.get("name"), "| category:", v.get("category"))
    s = json.loads(http("GET", EL + "/v1/user/subscription", el_headers())[0])
    print("characters used:", s.get("character_count"), "/", s.get("character_limit"), "| tier:", s.get("tier"))


def el_tts(text, speed, temperature):
    model = CFG.get("model") or "eleven_v3"
    if not model.startswith("eleven_v3"):
        text = re.sub(r"\[[^\]]*\]\s*", "", text)
    text = text.replace("[emphasis] ", "")  # emphasis comes from punctuation/caps on ElevenLabs
    body = {"text": text, "model_id": model,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.35, "speed": max(0.7, min(1.2, speed))}}
    return http("POST", EL + "/v1/text-to-speech/%s?output_format=mp3_44100_128" % voice_id(), el_headers(), body)


# ---------------------------------------------------------------- common
def generate(script_path, out_dir, only=None):
    s = json.load(open(script_path, encoding="utf-8"))
    segs = s.get("segments") or s.get("trechos")
    speed0 = s.get("speed", s.get("velocidade", CFG.get("speed", 1.0)))
    temp0 = s.get("temperature", s.get("temperatura", CFG.get("temperature", 0.8)))
    os.makedirs(out_dir, exist_ok=True)
    fn = {"fish": fish_tts, "elevenlabs": el_tts}[PROVIDER]
    sent = 0
    for seg in segs:
        name = seg.get("file") or seg.get("arquivo")
        text = seg.get("text") or seg.get("texto")
        if only and not name.startswith(only):
            continue
        audio, ctype = fn(text, seg.get("speed", seg.get("velocidade", speed0)), seg.get("temperature", seg.get("temperatura", temp0)))
        if "json" in ctype or len(audio) < 2000:
            raise SystemExit("ERROR unexpected response for %s: %s" % (name, audio[:300]))
        dest = os.path.join(out_dir, name + ".mp3")
        open(dest, "wb").write(audio)
        sent += len(text.encode("utf-8"))
        print("ok", dest, "(%d KB)" % (len(audio) // 1024))
    print("text bytes sent:", sent)


if __name__ == "__main__":
    if PROVIDER not in ("fish", "elevenlabs"):
        raise SystemExit("voice.provider is '%s'. Choose one in the setup (fish | elevenlabs) or record the voiceover yourself." % PROVIDER)
    if len(sys.argv) >= 2 and sys.argv[1] == "check":
        {"fish": fish_check, "elevenlabs": el_check}[PROVIDER]()
    elif len(sys.argv) >= 4 and sys.argv[1] == "generate":
        only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
        generate(sys.argv[2], sys.argv[3], only)
    else:
        raise SystemExit(__doc__)
