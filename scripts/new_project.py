#!/usr/bin/env python3
"""Creates the folder of a new reel and its HyperFrames project, already themed from the video brief.

  python new_project.py --name "GTA6-No-AI" [--brief brief.json] [--root <projects folder>] [--skip-init]

- Folder: <projects>/<name>/ with reels-project/ (HyperFrames), broll-originals/, music-candidates/, voiceover/
- brief.json: the answers of the per-video questions (references/video-brief.md). Missing keys fall back to
  the creator defaults in config.json. The merged brief is saved as <name>/brief.json.
- Writes reels-project/reel.config.json (theme, palette, captions, language) and the :root theme in index.html.
- Removes the fixed title (titleBar = none) and the captions track (captions.mode = none) from index.html.
"""
import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import config  # noqa: E402

SKILL = os.path.dirname(HERE)
TEMPLATE = os.path.join(SKILL, "assets", "template")
PALETTES = json.load(io.open(os.path.join(TEMPLATE, "scripts", "palettes.json"), encoding="utf-8"))

ap = argparse.ArgumentParser()
ap.add_argument("--name", required=True, help="short topic name, no accents (it becomes the folder name)")
ap.add_argument("--brief", help="JSON with this video's answers")
ap.add_argument("--root", help="projects folder (default: config paths.projects)")
ap.add_argument("--skip-init", action="store_true", help="do not run `hyperframes init` (template only)")
a = ap.parse_args()

cfg = config.load()
brief = config._merge(cfg["defaults"], json.load(io.open(a.brief, encoding="utf-8")) if a.brief else {})
brief.setdefault("language", cfg["creator"]["language"])

name = re.sub(r"[^A-Za-z0-9._-]+", "-", a.name).strip("-")
folder = os.path.join(os.path.expanduser(a.root or cfg["paths"]["projects"]), name)
proj = os.path.join(folder, "reels-project")
for sub in ("broll-originals", "music-candidates", "voiceover"):
    os.makedirs(os.path.join(folder, sub), exist_ok=True)

if not os.path.exists(os.path.join(proj, "hyperframes.json")) and not a.skip_init:
    r = subprocess.run("npx --yes hyperframes init reels-project --non-interactive --skip-transcribe --skip-skills --resolution portrait",
                       cwd=folder, shell=True)
    if r.returncode != 0:
        print("WARN hyperframes init failed; continuing with the template only")
os.makedirs(proj, exist_ok=True)
shutil.copytree(TEMPLATE, proj, dirs_exist_ok=True)

# theme
theme = brief.get("theme", "bold-dark")
if theme not in PALETTES:  # "brand": the creator's colors on top of a dark or light base
    theme = brief.get("brandBase", "bold-dark")
pal = dict(PALETTES[theme])
pal.update(brief.get("palette") or {})
lang = str(brief["language"]).split("-")[0].lower()
reel_cfg = {
    "duration": None,
    "language": lang,
    "theme": theme,
    "palette": brief.get("palette") or {},
    "keywords": [],
    "captions": brief.get("captions") or {},
}
io.open(os.path.join(proj, "reel.config.json"), "w", encoding="utf-8").write(json.dumps(reel_cfg, ensure_ascii=False, indent=2) + "\n")

idx_path = os.path.join(proj, "index.html")
idx = io.open(idx_path, encoding="utf-8").read()
root_css = """/* THEME (rewritten by scripts/new_project.py from reel.config.json -> theme/palette) */
      :root {
        --ground: %(ground)s;
        --ink: %(ink)s;
        --alert: %(alert)s;
        --alert-text: %(alertText)s;
        --accent: %(accent)s;
        --cool: %(cool)s;
        --ok: %(ok)s;
        --card: %(card)s;
        --card-ink: %(cardInk)s;
        --shade: %(scrim)s;
        --gold: var(--accent);
        --font-display: "League Gothic", sans-serif;
        --font-body: "Montserrat", sans-serif;
        --font-mono: "JetBrains Mono", monospace;
      }
      /* END THEME */""" % pal
idx = re.sub(r"/\* THEME.*?/\* END THEME \*/", lambda m: root_css, idx, flags=re.S)
idx = idx.replace('<html lang="en">', '<html lang="%s">' % brief["language"])
if brief.get("titleBar") == "none":
    idx = re.sub(r"\n\s*<!-- FIXED TITLE.*?-->\n\s*<div id=\"title\"[^\n]*</div>", "", idx, flags=re.S)
if (brief.get("captions") or {}).get("mode") == "none":
    idx = re.sub(r"\n\s*<!-- CAPTIONS.*?-->\n\s*<div id=\"captions\"[^\n]*</div>", "", idx, flags=re.S)
io.open(idx_path, "w", encoding="utf-8", newline="\n").write(idx)

io.open(os.path.join(folder, "brief.json"), "w", encoding="utf-8").write(json.dumps(brief, ensure_ascii=False, indent=2) + "\n")
print("project:", proj)
print("brief:  ", os.path.join(folder, "brief.json"))
print("theme:  ", reel_cfg["theme"], "| captions:", json.dumps(reel_cfg["captions"], ensure_ascii=False))
print("next: put the raw video in reels-project/assets/ (SDR, see SKILL.md) and replace __DUR__ / __TITLE_DUR__ in index.html")
