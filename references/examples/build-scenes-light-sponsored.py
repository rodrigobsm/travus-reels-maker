# Example: sponsored health reel, LIGHT theme (clean-light preset). Talking head + b-roll + product hero scene.
# Brand and product names are placeholders: swap the logo, cutout and texts for the real sponsor.
# Gera compositions/*.html. Tempos relativos ao inicio de cada cena (inicios em build-index.py).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_scenes import *

INK, GREEN, GSOFT, CORAL, CREAM, GOLD = "#15211B", "#1F9D63", "#E3F3EA", "#E8553D", "#F7F3EA", "#B89B55"

LIGHT = """
    .P-card { display: inline-block; font-size: 58px; background: #fff; border-radius: 30px; padding: 24px 36px 20px; box-shadow: 0 18px 50px rgba(21,33,27,0.20); font-family: "Montserrat", sans-serif; font-weight: 900; color: #15211B; white-space: nowrap; text-align: center; line-height: 1.08; }
    .P-pill { display: inline-block; border-radius: 999px; padding: 14px 30px 12px; font-family: "Montserrat", sans-serif; font-weight: 900; white-space: nowrap; box-shadow: 0 12px 34px rgba(21,33,27,0.18); }
    .P-pg { background: #1F9D63; color: #fff; }
    .P-pc { background: #D2442C; color: #fff; }
    .P-pw { background: #fff; color: #15211B; }
    .P-pi { background: #15211B; color: #fff; }
    .P-g { color: #1F9D63; } .P-c { color: #E8553D; } .P-gold { color: #B89B55; }
    .P-sub { display: block; font-family: "Montserrat", sans-serif; font-weight: 700; font-size: 34px; color: #4B5A52; margin-top: 10px; }
    .P-veil { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(255,255,255,0) 40%, rgba(255,255,255,0.10) 70%, rgba(255,255,255,0.0) 100%); }
"""

ICO = {
    "check": '<svg viewBox="0 0 24 24" style="width:%dpx;height:%dpx;vertical-align:middle"><circle cx="12" cy="12" r="11" fill="#1F9D63"/><path d="M7 12.5l3.2 3.2L17.5 8.5" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "x": '<svg viewBox="0 0 24 24" style="width:%dpx;height:%dpx;vertical-align:middle"><circle cx="12" cy="12" r="11" fill="#E8553D"/><path d="M8 8l8 8M16 8l-8 8" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/></svg>',
    "us": '<svg viewBox="0 0 30 20" style="width:%dpx;height:%dpx;vertical-align:middle;border-radius:4px"><rect width="30" height="20" fill="#fff"/><g fill="#B22234"><rect y="0" width="30" height="1.54"/><rect y="3.08" width="30" height="1.54"/><rect y="6.15" width="30" height="1.54"/><rect y="9.23" width="30" height="1.54"/><rect y="12.3" width="30" height="1.54"/><rect y="15.4" width="30" height="1.54"/><rect y="18.46" width="30" height="1.54"/></g><rect width="13" height="10.77" fill="#3C3B6E"/></svg>',
    "br": '<svg viewBox="0 0 30 20" style="width:%dpx;height:%dpx;vertical-align:middle;border-radius:4px"><rect width="30" height="20" fill="#009C3B"/><path d="M15 2.2 L27.6 10 L15 17.8 L2.4 10 Z" fill="#FFDF00"/><circle cx="15" cy="10" r="4.6" fill="#002776"/></svg>',
    "lab": '<svg viewBox="0 0 24 24" style="width:%dpx;height:%dpx;vertical-align:middle" fill="none" stroke="#1F9D63" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3"/><path d="M7.5 15h9"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" style="width:%dpx;height:%dpx;vertical-align:middle" fill="none" stroke="#1F9D63" stroke-width="2.2" stroke-linejoin="round"><path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" style="width:%dpx;height:%dpx;vertical-align:middle"><path d="M4 4h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H10l-5 4v-4H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z" fill="#1F9D63"/><circle cx="8" cy="11" r="1.4" fill="#fff"/><circle cx="12" cy="11" r="1.4" fill="#fff"/><circle cx="16" cy="11" r="1.4" fill="#fff"/></svg>',
    "plane": '<svg viewBox="0 0 24 24" style="width:%dpx;height:%dpx;vertical-align:middle" fill="none" stroke="#fff" stroke-width="2.2" stroke-linejoin="round"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/></svg>',
}


def ico(name, size):
    return ICO[name] % (size, size if name not in ("us", "br") else int(size * 2 / 3))


def cardrow(id, start, dur, top, html, track=0, extra=""):
    return clip(id, start, dur, top, '<span id="%s-in" class="P-card">%s</span>' % (id, html), track, extra)


def pillrow(id, start, dur, top, html, cls="P-pw", size=36, track=0, extra=""):
    return clip(id, start, dur, top, '<span id="%s-in" class="P-pill %s" style="font-size:%dpx">%s</span>' % (id, cls, size, html), track, extra)


def fs(text, size, maxw=740):
    """font-size Montserrat 900 que cabe em maxw (zona segura 820 - padding)."""
    return fit(text, "body", size, maxw)


def box(id, start, dur, left, top, w, h, inner, track=0, extra=""):
    return ('    <div id="%s" class="clip" data-start="%s" data-duration="%s" data-track-index="%d" '
            'style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx" %s>%s</div>\n') % (id, start, dur, track, left, top, w, h, extra, inner)


UP = '      tl.fromTo("%s", { y: 50, opacity: 0, scale: 0.94 }, { y: 0, opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }, %s);\n'
BOUNCE = '      tl.fromTo("%s", { scale: 0.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.42, ease: "back.out(2.2)" }, %s);\n'
OUT = '      tl.to("%s", { y: -20, opacity: 0, duration: 0.2, ease: "power2.in" }, %s);\n'
NUDGE = '      tl.to("%s", { scale: 1.07, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1 }, %s);\n'

# ---------------------------------------------------------------- HOOK (0 - 7.2)
t1 = "BARRIGA INCHADA"
scene("hook", LIGHT + """
    #hook-title-in { font-size: %dpx; padding: 26px 40px 22px; }
    #hook-title-in .P-g { display: block; font-size: 1.12em; margin-top: 6px; }
""" % fs(t1, 84),
    cardrow("hook-title", 0, 7.0, 210, t1 + '<span class="P-g">NOS EUA? ' + ico("us", 70) + '</span>')
    + pillrow("hook-a", 3.17, 1.55, 1190, "INCHADA", "P-pc", 40, 1)
    + pillrow("hook-b", 3.91, 0.81, 1270, "ESTUFADA", "P-pc", 40, 2, CZ)
    + pillrow("hook-c1", 4.75, 2.25, 1170, ico("check", 40) + " COMENDO BEM", "P-pw", 34, 3)
    + pillrow("hook-c2", 5.56, 1.44, 1240, ico("check", 40) + " MALHANDO", "P-pw", 34, 4)
    + pillrow("hook-c3", 6.1, 0.9, 1310, ico("check", 40) + " DORMINDO DIREITO", "P-pw", 34, 5, CZ),
    '      tl.fromTo("#hook-title-in", { scale: 1.12 }, { scale: 1, duration: 0.5, ease: "expo.out" }, 0);\n'
    + NUDGE % ("#hook-title-in", 3.2)
    + BOUNCE % ("#hook-a-in", 3.19) + BOUNCE % ("#hook-b-in", 3.93)
    + OUT % ("#hook-a-in", 4.55) + OUT % ("#hook-b-in", 4.55)
    + UP % ("#hook-c1-in", 4.77) + UP % ("#hook-c2-in", 5.58) + UP % ("#hook-c3-in", 6.12)
    + OUT % ("#hook-title-in", 6.8))

# ---------------------------------------------------------------- FRESCURA (7.2 - 10.4)
scene("fresc", LIGHT,
    pillrow("fresc-a", 0.52, 1.0, 1200, ico("x", 42) + " NÃO É FRESCURA", "P-pw", 40)
    + pillrow("fresc-b", 1.54, 1.66, 1200, ico("lab", 44) + " TEM ESTUDO", "P-pg", 44, 1),
    BOUNCE % ("#fresc-a-in", 0.54) + OUT % ("#fresc-a-in", 1.36) + BOUNCE % ("#fresc-b-in", 1.56))

# ---------------------------------------------------------------- ESTUDO (10.4 - 19.85)  [b-roll laboratorio + bacteria]
scene("study", LIGHT + """
    #study-dots { position: absolute; left: 190px; top: 900px; width: 700px; height: 150px; }
    .study-dot { position: absolute; width: 56px; height: 56px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #7DDBA8, #1F9D63); box-shadow: 0 6px 18px rgba(31,157,99,0.45); }
""",
    pillrow("study-k", 1.34, 8.1, 520, ico("lab", 40) + " REVISTA CELL · 2018", "P-pw", 36)
    + cardrow("study-a", 2.0, 2.4, 640, 'IMIGRANTES<br/><span class="P-g">NOS EUA</span>', 1)
    + cardrow("study-b", 4.05, 5.4, 640, 'PERDEM <span class="P-c">BACTÉRIAS</span><br/>DO INTESTINO', 2)
    + box("study-dots", 4.05, 5.4, 190, 900, 700, 150, ''.join('<i id="study-d%d" class="study-dot" style="left:%dpx;top:%dpx"></i>' % (i, 40 + i * 110, 30 + (i % 2) * 40) for i in range(6)), 3)
    + pillrow("study-c", 7.75, 1.7, 1110, "AS BACTÉRIAS BOAS", "P-pg", 42, 4),
    UP % ("#study-k-in", 1.36) + UP % ("#study-a-in", 2.03) + OUT % ("#study-a-in", 3.9)
    + UP % ("#study-b-in", 4.07)
    + ''.join('      tl.fromTo("#study-d%d", { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }, %s);\n' % (i, round(4.2 + i * 0.08, 2)) for i in range(6))
    + ''.join('      tl.to("#study-d%d", { scale: 0.2, opacity: 0.15, duration: 0.35, ease: "power2.in" }, %s);\n' % (i, round(5.4 + i * 0.25, 2)) for i in (1, 4))
    + BOUNCE % ("#study-c-in", 7.79))

# ---------------------------------------------------------------- DO BRASIL (19.85 - 25.5)  [b-roll aviao]
scene("brasil", LIGHT + """
    #brasil-route-in { display: inline-flex; align-items: center; gap: 30px; background: #fff; border-radius: 30px; padding: 26px 40px; box-shadow: 0 18px 50px rgba(21,33,27,0.2); }
    #brasil-route-in i { display: block; width: 210px; height: 8px; border-radius: 4px; background: repeating-linear-gradient(90deg, #1F9D63 0 18px, transparent 18px 30px); }
    .brasil-dot { position: absolute; width: 40px; height: 40px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #7DDBA8, #1F9D63); }
""",
    cardrow("brasil-a", 0.6, 4.9, 560, 'AS BACTÉRIAS BOAS<br/><span class="P-g">QUE VOCÊ TROUXE</span>', 0)
    + clip("brasil-route", 1.0, 4.5, 820, '<span id="brasil-route-in">' + ico("br", 120) + '<i></i>' + ico("us", 120) + '</span>', 1)
    + box("brasil-dots", 2.4, 3.1, 330, 1000, 420, 80, ''.join('<b id="brasil-d%d" class="brasil-dot" style="left:%dpx;top:%dpx"></b>' % (i, i * 95, (i % 2) * 30) for i in range(5)), 2)
    + pillrow("brasil-x", 4.66, 0.84, 1120, "DESAPARECEM", "P-pc", 52, 3),
    UP % ("#brasil-a-in", 0.6) + UP % ("#brasil-route-in", 1.0)
    + ''.join('      tl.fromTo("#brasil-d%d", { x: -160, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power2.out" }, %s);\n' % (i, round(2.4 + i * 0.1, 2)) for i in range(5))
    + ''.join('      tl.to("#brasil-d%d", { scale: 0, opacity: 0, duration: 0.3, ease: "power2.in" }, %s);\n' % (i, round(3.9 + i * 0.12, 2)) for i in range(5))
    + BOUNCE % ("#brasil-x-in", 4.68) + NUDGE % ("#brasil-x-in", 5.1))

# ---------------------------------------------------------------- POR QUE (25.5 - 27.55)
scene("why", LIGHT,
    pillrow("why-a", 1.15, 0.9, 1200, "POR QUÊ?", "P-pi", 44),
    BOUNCE % ("#why-a-in", 1.17))

# ---------------------------------------------------------------- CAUSAS (27.55 - 39.9)  [b-roll torneira, pao, cereal]
CAUSES = [("1", "ÁGUA CLORADA", "mata as bactérias boas (e as ruins)", 0.3, 3.4),
          ("2", "TRIGO DIFERENTE", "não tem jeito", 3.66, 1.74),
          ("3", "ULTRAPROCESSADOS", "emulsificantes destroem o muco", 5.82, 6.53)]
cz = ""
cj = ""
for i, (n, tit, sub, t, d) in enumerate(CAUSES):
    cz += cardrow("causes-c%d" % i, t, d, 620, '<span class="causes-n">%s</span>%s<span class="P-sub">%s</span>' % (n, tit, sub), i, )
    cj += UP % ("#causes-c%d-in" % i, t + 0.02)
scene("causes", LIGHT + """
    .causes-n { display: inline-block; width: 70px; height: 70px; line-height: 74px; border-radius: 50%%; background: #E8553D; color: #fff; font-size: 40px; margin-right: 20px; vertical-align: middle; }
    #causes-c0-in, #causes-c1-in, #causes-c2-in { font-size: %dpx; }
    #causes-sh-in { display: inline-flex; align-items: center; gap: 14px; }
""" % fs("3ULTRAPROCESSADOS", 66, 650),
    pillrow("causes-k", 0.05, 12.3, 500, "POR QUE ISSO ACONTECE", "P-pi", 32, 3)
    + cz
    + pillrow("causes-sh", 10.0, 2.35, 900, ico("shield", 44) + " A PROTEÇÃO DO INTESTINO", "P-pw", 36, 4),
    UP % ("#causes-k-in", 0.08) + cj + BOUNCE % ("#causes-sh-in", 10.02)
    + '      tl.to("#causes-sh-in", { opacity: 0.35, duration: 0.3, ease: "none" }, 11.2);\n')

# ---------------------------------------------------------------- INFLAMADO (39.9 - 45.7)
scene("inflam", LIGHT,
    pillrow("inflam-a", 0.7, 5.1, 1150, "CORPO INFLAMADO", "P-pc", 50)
    + pillrow("inflam-b", 2.83, 2.97, 1260, "INTESTINO PRESO?", "P-pw", 36, 1, CZ)
    + pillrow("inflam-c", 4.01, 1.79, 1260, "METABOLISMO?", "P-pw", 36, 2, CZ),
    BOUNCE % ("#inflam-a-in", 0.73) + NUDGE % ("#inflam-a-in", 1.3)
    + UP % ("#inflam-b-in", 2.85) + OUT % ("#inflam-b-in", 3.85) + UP % ("#inflam-c-in", 4.03))

# ---------------------------------------------------------------- O QUE AJUDA (45.7 - 49.45)
tq = "O QUE AJUDA A"
scene("science", LIGHT + "    #science-a-in { font-size: %dpx; }\n" % fs("RECONSTRUIR?", 70),
    cardrow("science-a", 0.6, 3.15, 1050, tq + '<br/><span class="P-g">RECONSTRUIR?</span>'),
    UP % ("#science-a-in", 0.62) + NUDGE % ("#science-a-in", 2.0))

# ---------------------------------------------------------------- SOLUCOES (49.45 - 63.55)  [b-roll smoothie, legumes, gengibre]
SOL = [("GLUTAMINA", "combustível das células do intestino", 0.33), ("FIBRAS PREBIÓTICAS", "alimentam as bactérias boas", 4.45),
       ("CÚRCUMA + GENGIBRE", "modulam a inflamação", 9.42)]
srows = ""
sj = ""
for i, (tit, sub, t) in enumerate(SOL):
    srows += box("solve-r%d" % i, t, round(14.1 - t, 2), 130, 640 + i * 190, 820, 166,
                 '<div id="solve-r%d-in" class="solve-item"><span class="solve-n">%d</span><div><b>%s</b><em>%s</em></div></div>' % (i, i + 1, tit, sub), 1 + i)
    sj += '      tl.fromTo("#solve-r%d-in", { x: 400, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, %s);\n' % (i, t)
    sj += '      tl.fromTo("#solve-r%d-in .solve-n", { backgroundColor: "#CFE8DA" }, { backgroundColor: "#1F9D63", duration: 0.2, ease: "none", immediateRender: false }, %s);\n' % (i, t + 0.4)
scene("solve", LIGHT + """
    .solve-item { position: absolute; inset: 0; background: rgba(255,255,255,0.96); border-radius: 28px; box-shadow: 0 16px 44px rgba(21,33,27,0.18); display: flex; align-items: center; gap: 24px; padding: 0 30px; }
    .solve-n { flex: 0 0 auto; width: 82px; height: 82px; border-radius: 50%; color: #fff; font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 44px; line-height: 86px; text-align: center; }
    .solve-item b { display: block; font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 40px; color: #15211B; white-space: nowrap; }
    .solve-item em { display: block; font-style: normal; font-family: "Montserrat", sans-serif; font-weight: 700; font-size: 28px; color: #4B5A52; margin-top: 6px; white-space: nowrap; }
""",
    pillrow("solve-k", 0.05, 14.05, 520, "O QUE A CIÊNCIA MOSTRA", "P-pg", 34)
    + srows,
    UP % ("#solve-k-in", 0.06) + sj)

# ---------------------------------------------------------------- PRODUTO NA MAO (63.55 - 76.3)
scene("product", LIGHT + """
    #product-logo-in { display: inline-flex; align-items: center; gap: 22px; }
    #product-logo-in img { width: 150px; height: 92px; display: block; }
    #product-logo-in b { font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 38px; color: #15211B; }
    #product-logo-in b span { color: #8A7233; }
""",
    pillrow("product-a", 1.4, 2.6, 1180, ico("check", 40) + " ESSA FÓRMULA ENTREGA", "P-pg", 38)
    + pillrow("product-b", 2.62, 3.1, 1270, "USO HÁ +1 MÊS", "P-pw", 34, 1, CZ)
    + cardrow("product-logo", 5.85, 6.9, 1110, '<span id="product-logo-in"><img src="assets/logos/brand.svg" alt="Brand" /><b>MARCA PARCEIRA<br/><span>DO BRASIL</span></b></span>', 2)
    + pillrow("product-us", 9.38, 3.37, 1300, "AGORA NOS EUA " + ico("us", 54), "P-pi", 36, 3, CZ),
    BOUNCE % ("#product-a-in", 1.42) + OUT % ("#product-a-in", 3.8) + UP % ("#product-b-in", 2.7) + OUT % ("#product-b-in", 5.5)
    + UP % ("#product-logo-in", 5.89) + BOUNCE % ("#product-us-in", 9.4))

# ---------------------------------------------------------------- HERO DO PRODUTO (76.3 - 82.6)
BEN = [("COLÁGENO", 0.53, 130, 1180), ("VITAMINA C", 1.25, 560, 1180), ("ALTÍSSIMO PADRÃO", 2.73, 130, 1280)]
bh = ""
bj = ""
for i, (txt, t, left, top) in enumerate(BEN):
    w = 820 if left == 130 and i == 2 else 390
    bh += box("hero-b%d" % i, t, round(6.3 - t, 2), left, top, w, 84, '<div id="hero-b%d-in" class="hero-ben">%s %s</div>' % (i, ico("check", 40), txt), 3 + i)
    bj += BOUNCE % ("#hero-b%d-in" % i, t + 0.02)
scene("hero", LIGHT + """
    #hero-bg { position: absolute; inset: 0; background: radial-gradient(700px 700px at 50% 42%, #FFFFFF 0%, #F7F3EA 60%, #EFE8D8 100%); }
    #hero-can { position: absolute; left: 240px; top: 470px; width: 600px; height: 750px; }
    #hero-can img { width: 600px; height: 750px; object-fit: contain; display: block; }
    #hero-name-in { font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 92px; color: #15211B; letter-spacing: -0.01em; }
    #hero-name-in span { color: #B89B55; }
    #hero-logo-in img { width: 200px; height: 122px; display: block; }
    .hero-ben { position: absolute; inset: 0; border-radius: 999px; background: #fff; box-shadow: 0 12px 34px rgba(21,33,27,0.16); display: flex; align-items: center; justify-content: center; gap: 12px; font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 34px; color: #15211B; }
    #hero-gut-in { box-shadow: 0 16px 50px rgba(31,157,99,0.45); }
""",
    '    <div id="hero-bg" data-layout-allow-occlusion></div>\n'
    + clip("hero-logo", 0, 6.3, 210, '<span id="hero-logo-in" style="display:inline-block"><img src="assets/logos/brand.svg" alt="Brand" /></span>', 0)
    + clip("hero-name", 0.05, 6.25, 350, '<span id="hero-name-in">PRODUTO<span>X</span></span>', 1)
    + box("hero-can", 0, 6.3, 240, 470, 600, 750, '<div id="hero-can-in"><img src="assets/img/product-cutout.png" alt="Product" /></div>', 2, "data-layout-allow-overflow data-layout-allow-occlusion")
    + bh
    + pillrow("hero-gut", 5.3, 1.0, 1080, "FOCO TOTAL: INTESTINO", "P-pg", 44, 7),
    '      tl.fromTo("#hero-bg", { opacity: 0 }, { opacity: 1, duration: 0.25, ease: "none" }, 0);\n'
    + '      tl.fromTo("#hero-can-in", { y: 120, scale: 0.85, opacity: 0, rotation: -6 }, { y: 0, scale: 1, opacity: 1, rotation: 0, duration: 0.55, ease: "back.out(1.6)" }, 0.05);\n'
    + '      tl.to("#hero-can-in", { y: -14, duration: 1.2, ease: "sine.inOut", yoyo: true, repeat: 3 }, 0.6);\n'
    + UP % ("#hero-logo-in", 0.05) + UP % ("#hero-name-in", 0.12) + bj
    + BOUNCE % ("#hero-gut-in", 5.32))

# ---------------------------------------------------------------- SINTOMAS (82.6 - 90.35)
SY = [("VIVE INCHADO", 3.78), ("INTESTINO IRREGULAR", 4.83), ("PELE QUE NÃO MELHORA", 6.36)]
sy = ""
syj = ""
for i, (txt, t) in enumerate(SY):
    sy += box("sympt-r%d" % i, t, round(7.75 - t, 2), 130, 1000 + i * 100, 820, 84, '<div id="sympt-r%d-in" class="sympt-item"><span class="sympt-box"></span>%s</div>' % (i, txt), 2 + i)
    syj += '      tl.fromTo("#sympt-r%d-in", { x: -300, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, ease: "power3.out" }, %s);\n' % (i, t)
    syj += '      tl.to("#sympt-r%d-in .sympt-box", { backgroundColor: "#E8553D", duration: 0.15, ease: "none" }, %s);\n' % (i, t + 0.3)
scene("sympt", LIGHT + """
    .sympt-item { position: absolute; inset: 0; border-radius: 22px; background: rgba(255,255,255,0.96); box-shadow: 0 12px 34px rgba(21,33,27,0.16); display: flex; align-items: center; gap: 20px; padding: 0 28px; font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 36px; color: #15211B; white-space: nowrap; }
    .sympt-box { width: 44px; height: 44px; border-radius: 12px; border: 4px solid #E8553D; background: #fff; flex: 0 0 auto; }
""",
    pillrow("sympt-k", 1.4, 6.35, 900, "BRASILEIRO NOS EUA " + ico("us", 54), "P-pi", 34, 1) + sy,
    UP % ("#sympt-k-in", 1.45) + syj)

# ---------------------------------------------------------------- CTA (90.35 - fim)
CTA = 9.45
scene("cta", LIGHT + """
    #cta-card-in { display: inline-block; background: #fff; border-radius: 34px; padding: 30px 44px 26px; box-shadow: 0 22px 60px rgba(21,33,27,0.25); text-align: center; }
    #cta-card-in small { display: flex; align-items: center; justify-content: center; gap: 16px; font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 44px; color: #15211B; }
    #cta-card-in b { display: block; font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 104px; line-height: 1.05; color: #1F9D63; letter-spacing: -0.01em; margin-top: 8px; }
    #cta-bf-in { display: inline-flex; align-items: center; gap: 16px; }
    #cta-bf-in i { font-style: normal; background: #15211B; color: #fff; border-radius: 12px; padding: 10px 18px 8px; font-size: 32px; }
    #cta-arrow svg { width: 120px; height: 120px; display: block; }
""",
    clip("cta-card", 0.85, CTA - 0.85, 820, '<span id="cta-card-in"><small>%s COMENTA</small><b>“INTESTINO”</b></span>' % ico("chat", 60), 0)
    + pillrow("cta-bf", 3.6, CTA - 3.6, 1140, '<span id="cta-bf-in">' + ico("plane", 40).replace('stroke="#fff"', 'stroke="#15211B"') + ' LINK NO DIRECT <i>BLACK FRIDAY</i></span>', "P-pw", 34, 1)
    + box("cta-arrow", 1.0, CTA - 1.0, 830, 1230, 120, 120, '<div id="cta-arrow-in"><svg viewBox="0 0 100 100"><path d="M20 20 Q70 25 78 75 M60 66 L78 80 L92 60" fill="none" stroke="#1F9D63" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg></div>', 2, CZ),
    '      tl.fromTo("#cta-card-in", { y: 80, scale: 0.8, opacity: 0 }, { y: 0, scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }, 0.87);\n'
    + NUDGE % ("#cta-card-in", 1.85) + UP % ("#cta-bf-in", 3.62)
    + '      tl.fromTo("#cta-arrow-in", { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "none" }, 1.0);\n'
    + '      tl.to("#cta-arrow-in", { x: 10, y: 10, duration: 0.35, ease: "sine.inOut", yoyo: true, repeat: 11 }, 1.2);\n'
    + NUDGE % ("#cta-card-in", 8.05))
print("ok")
