# Scene library for 1080x1920 reels (HyperFrames motion graphics).
# Usage, in scripts/build-scenes.py:   from reel_scenes import *
# Each scene(...) writes compositions/<name>.html (static HTML you can still edit by hand).
#
# SIDE SAFE ZONE: in full screen on tall phones, Instagram zooms the reel and crops ~97 px on each
# side. Nothing readable may cross SAFE_X. Centered texts (.P-big / .P-tag / .P-kicker) are measured
# with the real font and shrunk automatically to fit SAFE_W.
#
# THEME: colors come from reel.config.json -> "palette" (written by scripts/new_project.py).
# Use C["ink"], C["accent"], C["alert"]... in your own scene CSS so the same scene works in dark and light.
import html as _html
import io
import json
import os
import re

from fontTools.ttLib import TTFont

W, H = 1080, 1920
SAFE_X = 130  # minimum side margin
SAFE_W = W - 2 * SAFE_X  # 820
SAFE_TOP = 186  # below the Instagram top bar
CAPTION_Y = 1436  # caption center (low position); keep scene text above ~1330

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

# Preset palettes live in scripts/palettes.json (shared with build-captions.cjs and new_project.py).
# reel.config.json picks one with "theme" and may override any key in "palette".
PALETTES = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "palettes.json"), encoding="utf-8"))


def _load_palette():
    cfg_path = os.path.join(ROOT, "reel.config.json")
    cfg = {}
    if os.path.exists(cfg_path):
        cfg = json.load(io.open(cfg_path, encoding="utf-8"))
    pal = dict(PALETTES.get(cfg.get("theme", "bold-dark"), PALETTES["bold-dark"]))
    pal.update(cfg.get("palette") or {})
    return pal


C = _load_palette()
_g = C["ground"].lstrip("#")
DARK = (0.2126 * int(_g[0:2], 16) + 0.7152 * int(_g[2:4], 16) + 0.0722 * int(_g[4:6], 16)) / 255 < 0.5  # True for dark themes

FONT_FILES = {
    "display": "LeagueGothic.woff2",
    "body": "Montserrat-900.woff2",
    "mono": "JetBrainsMono-700.woff2",
}
_fonts = {}


def text_width(text, font="display", size=100, ls=0.0):
    """Width in px of `text` in the project font (ls = letter-spacing in em)."""
    if font not in _fonts:
        f = TTFont(os.path.join(ROOT, "assets", "fonts", FONT_FILES[font]))
        _fonts[font] = (f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    cmap, hmtx, upm = _fonts[font]
    adv = 0
    for ch in text:
        g = cmap.get(ord(ch))
        adv += hmtx[g][0] if g else upm * 0.5
    return adv / upm * size + ls * size * len(text)


def fit(text, font="display", size=100, maxw=SAFE_W, ls=0.0):
    """Largest font-size <= size at which `text` fits in maxw."""
    while size > 28 and text_width(text, font, size, ls) > maxw:
        size -= 2
    return size


_a = C["scrimAlpha"]
BASE = """
    #root { position: absolute; inset: 0; }
    .P-scrim { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(%(scrim)s,%(a0)s) 0%%, rgba(%(scrim)s,%(a1)s) 42%%, rgba(%(scrim)s,%(a2)s) 100%%); }
    .P-row { position: absolute; left: 0; width: 1080px; text-align: center; line-height: 1; white-space: nowrap; }
    .P-row > * { display: inline-block; }
    .P-kicker { font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: 0.2em; color: %(cardInk)s; padding: 12px 22px 11px; border: 2px solid rgba(%(shadow)s,0.35); border-radius: 999px; background: %(card)s; }
    .P-kicker i { font-style: normal; color: %(alertText)s; }
    .P-big { font-family: "League Gothic", sans-serif; text-transform: uppercase; color: %(ink)s; letter-spacing: 0.015em; }
    .P-tag { font-family: "League Gothic", sans-serif; text-transform: uppercase; color: #fff; background: %(alert)s; padding: 14px 34px 6px; border-radius: 8px; letter-spacing: 0.02em; box-shadow: 0 18px 50px rgba(%(shadow)s,0.30); }
    .P-card { display: inline-block; font-size: 58px; background: %(card)s; color: %(cardInk)s; border-radius: 30px; padding: 24px 36px 20px; box-shadow: 0 18px 50px rgba(%(shadow)s,0.22); font-family: "Montserrat", sans-serif; font-weight: 900; white-space: nowrap; }
""" % dict(C, a0=_a[0], a1=_a[1], a2=_a[2])

# class -> (font, letter-spacing em, total horizontal padding, default size)
_KIND = {"big": ("display", 0.015, 0, None), "tag": ("display", 0.02, 68, None), "kicker": ("mono", 0.2, 48, 30)}
_SPAN = re.compile(r'<span id="([^"]+)" class="P-(big|tag|kicker)"(?: style="([^"]*)")?>(.*?)</span></div>')


def _autofit(body, pads):
    def sub(m):
        sid, kind, style, inner = m.group(1), m.group(2), m.group(3) or "", m.group(4)
        font, ls, pad, default = _KIND[kind]
        pad += pads.get(sid, 0)
        fs = re.search(r"font-size:\s*(\d+)px", style)
        size = int(fs.group(1)) if fs else default
        if size is None:
            return m.group(0)
        lines = [_html.unescape(re.sub(r"<[^>]+>", "", ln)).upper() for ln in re.split(r"<br\s*/?>", inner)]
        new = min(fit(ln, font, size, SAFE_W - 10 - pad, ls) for ln in lines)
        if new != size:
            print("  safe-zone fit: %s %dpx -> %dpx" % (sid, size, new))
            style = re.sub(r"font-size:\s*\d+px", "font-size: %dpx" % new, style) if fs else ("font-size: %dpx; " % new + style).strip()
        st = ' style="%s"' % style if style else ""
        return '<span id="%s" class="P-%s"%s>%s</span></div>' % (sid, kind, st, inner)

    return _SPAN.sub(sub, body)


def scene(name, css, body, js, pads=None):
    """Writes compositions/<name>.html. `P-` becomes `<name>-` in css/body/js.
    NEVER name a class `<name>-row` (or `P-row` in your css): clip() already uses P-row.
    pads: {span_id: extra horizontal padding in px} for spans with their own background."""
    body = _autofit(body, pads or {})
    s = "<template>\n  <style>" + (BASE + css).replace("P-", name + "-") + "  </style>\n"
    s += '  <div id="root" data-composition-id="%s" data-width="1080" data-height="1920">\n' % name
    s += body.replace("P-", name + "-")
    s += "  </div>\n  <script>\n    (function () {\n      const tl = gsap.timeline({ paused: true });\n"
    s += js.replace("P-", name + "-")
    s += '      window.__timelines["%s"] = tl;\n    })();\n  </script>\n</template>\n' % name
    io.open(os.path.join(ROOT, "compositions", name + ".html"), "w", encoding="utf-8", newline="\n").write(s)


def clip(id, start, dur, top, inner, track=0, extra=""):
    """Timed centered line (times relative to the scene start)."""
    return '    <div id="%s" class="clip P-row" data-start="%s" data-duration="%s" data-track-index="%d" style="top: %dpx" %s>%s</div>\n' % (id, start, dur, track, top, extra, inner)


# Ready tweens: SLAM % (selector, rot_from, rot_to, t) | RISE % (selector, t) | POP % (selector, t) | SHAKE % (selector, t)
SLAM = '      tl.fromTo("%s", { scale: 2.2, opacity: 0, rotation: %s }, { scale: 1, opacity: 1, rotation: %s, duration: 0.28, ease: "expo.out" }, %s);\n'
RISE = '      tl.fromTo("%s", { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, %s);\n'
POP = '      tl.fromTo("%s", { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)" }, %s);\n'
SHAKE = '      tl.to("%s", { x: 12, duration: 0.045, yoyo: true, repeat: 5, ease: "none" }, %s);\n'
CZ = "data-layout-allow-caption-zone"  # for a scene's last line that touches the caption band
SCRIM = '    <div class="P-scrim" data-layout-allow-occlusion></div>\n'  # tints the b-roll behind the scene (dark or light)
