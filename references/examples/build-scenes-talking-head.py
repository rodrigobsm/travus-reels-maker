# Example: TALKING-HEAD reel (face on camera) with b-roll and motion-graphics scenes (bold-dark preset).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_scenes import *

# ---------- BINANCE (3.2s) ----------
scene("binance", """
    #binance-logo-in img { width: 250px; height: 250px; border-radius: 50%; box-shadow: 0 0 0 10px #f3ba2f, 0 30px 80px rgba(243,186,47,0.45); }
""",
    '    <div class="P-scrim" data-layout-allow-occlusion></div>\n'
    + clip("binance-k", 0, 3.2, 452, '<span id="binance-k-in" class="P-kicker">INCIDENTE <i>01</i>/04</span>')
    + clip("binance-logo", 0, 3.2, 560, '<span id="binance-logo-in"><img src="assets/logos/binance.svg" alt="Binance" /></span>', 1)
    + clip("binance-name", 0.15, 3.05, 858, '<span id="binance-name-in" class="P-big" style="font-size: 190px">BINANCE</span>', 2)
    + clip("binance-tag", 1.2, 2.0, 1076, '<span id="binance-tag-in" class="P-tag" style="font-size: 112px">ATAQUE BILIONÁRIO</span>', 3),
    RISE % ("#binance-k-in", 0.05) + POP % ("#binance-logo-in", 0.05) + RISE % ("#binance-name-in", 0.2) + SLAM % ("#binance-tag-in", -3, -3, 1.2)
    + '      tl.to("#binance-logo-in", { rotation: 360, duration: 0.7, ease: "power3.inOut" }, 1.1);\n'
    + '      tl.to("#binance-tag-in", { x: 10, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }, 1.48);\n')

# ---------- PHP (5.6s) ----------
sites = ""
sitejs = ""
for i, (u, t) in enumerate([("loja-online.com", 3.78), ("portal-noticias.com", 4.08), ("sistema-interno.com", 4.38)]):
    y = 620 + i * 190
    sites += ('    <div id="php-site%d" class="clip php-site" data-start="3.1" data-duration="2.5" data-track-index="%d" style="top: %dpx">'
              '<div id="php-site%d-in" class="php-card"><span class="php-dots"><i></i><i></i><i></i></span><span class="php-url">%s</span>'
              '<span class="php-state"><b id="php-on%d" class="php-on">ONLINE</b><b id="php-off%d" class="php-off">503 · FORA DO AR</b></span></div></div>\n') % (i, 5 + i, y, i, u, i, i)
    sitejs += '      tl.fromTo("#php-site%d-in", { x: %d, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, ease: "power3.out" }, %s);\n' % (i, 300 if i % 2 else -300, 3.1 + i * 0.08)
    sitejs += '      tl.set("#php-on%d", { opacity: 0 }, %s); tl.set("#php-off%d", { opacity: 1 }, %s);\n' % (i, t, i, t)
    sitejs += '      tl.fromTo("#php-site%d-in", { borderColor: "rgba(255,255,255,0.25)" }, { borderColor: "#ff2d3a", duration: 0.1, immediateRender: false }, %s);\n' % (i, t)
    sitejs += '      tl.to("#php-site%d-in", { x: 14, duration: 0.045, yoyo: true, repeat: 5, ease: "none" }, %s);\n' % (i, t)
scene("php", """
    #php-logo-in { background: #777bb4; border-radius: 40px; padding: 34px 70px 30px; box-shadow: 0 30px 80px rgba(119,123,180,0.5); }
    #php-logo-in img { width: 300px; height: 150px; display: block; }
    .php-site { position: absolute; left: 130px; width: 820px; height: 160px; }
    .php-card { position: absolute; inset: 0; border-radius: 26px; background: rgba(10,13,20,0.9); border: 3px solid rgba(255,255,255,0.25); display: flex; align-items: center; padding: 0 26px; gap: 18px; }
    .php-dots { display: flex; gap: 8px; }
    .php-dots i { width: 14px; height: 14px; border-radius: 50%; background: #3a4150; }
    .php-url { font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 28px; color: #c9d2e3; flex: 1; text-align: left; }
    .php-state { position: relative; width: 290px; height: 60px; }
    .php-state b { position: absolute; right: 0; top: 0; font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 26px; line-height: 60px; padding: 0 18px; border-radius: 12px; white-space: nowrap; }
    .php-on { background: #1fd17a; color: #04130b; }
    .php-off { background: #ff2d3a; color: #fff; opacity: 0; }
""",
    '    <div class="P-scrim" data-layout-allow-occlusion></div>\n'
    + clip("php-k", 0, 3.05, 452, '<span id="php-k-in" class="P-kicker">INCIDENTE <i>02</i>/04</span>')
    + clip("php-crit", 0.5, 2.55, 560, '<span id="php-crit-in" class="P-tag" style="font-size: 96px">FALHAS CRÍTICAS</span>', 1)
    + clip("php-logo", 1.7, 1.35, 740, '<span id="php-logo-in"><img src="assets/logos/php.svg" alt="PHP" /></span>', 2)
    + clip("php-zero", 2.4, 0.65, 1000, '<span id="php-zero-in" class="P-big" style="font-size: 250px">ZERO-DAY</span>', 3)
    + clip("php-k2", 3.1, 2.5, 452, '<span id="php-k2-in" class="P-kicker">RESULTADO</span>', 4)
    + sites
    + clip("php-down", 4.5, 1.1, 1206, '<span id="php-down-in" class="P-big" style="font-size: 92px">VÁRIOS SITES <span style="color:#ff2d3a">FORA DO AR</span></span>', 8, CZ),
    RISE % ("#php-k-in", 0.05) + SLAM % ("#php-crit-in", -2, -2, 0.5) + POP % ("#php-logo-in", 1.7) + SLAM % ("#php-zero-in", 0, 0, 2.4)
    + '      tl.to("#php-zero-in", { x: 12, duration: 0.045, yoyo: true, repeat: 5, ease: "none" }, 2.66);\n'
    + RISE % ("#php-k2-in", 3.1) + sitejs + RISE % ("#php-down-in", 4.5))

# ---------- MICROSOFT (2.15s) ----------
scene("msft", """
    #msft-logo-in { background: #fff; border-radius: 48px; padding: 44px; box-shadow: 0 30px 80px rgba(0,0,0,0.6); }
    #msft-logo-in img { width: 170px; height: 170px; display: block; }
    .msft-day { font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 46px; color: #fff; border: 4px solid #ff2d3a; border-radius: 16px; padding: 14px 30px; margin: 0 12px; background: rgba(255,45,58,0.18); }
""",
    '    <div class="P-scrim" data-layout-allow-occlusion></div>\n'
    + clip("msft-k", 0, 2.15, 452, '<span id="msft-k-in" class="P-kicker">INCIDENTE <i>03</i>/04</span>')
    + clip("msft-logo", 0, 2.15, 548, '<span id="msft-logo-in"><img src="assets/logos/microsoft.svg" alt="Microsoft" /></span>', 1)
    + clip("msft-name", 0.1, 2.05, 842, '<span id="msft-name-in" class="P-big" style="font-size: 170px">MICROSOFT</span>', 2)
    + clip("msft-tag", 0.5, 1.65, 1030, '<span id="msft-tag-in" class="P-tag" style="font-size: 112px">FORA DO AR</span>', 3)
    + clip("msft-days", 1.1, 1.05, 1200, '<span id="msft-d1" class="msft-day">QUINTA</span><span id="msft-d2" class="msft-day">SEXTA</span>', 4, CZ),
    RISE % ("#msft-k-in", 0.03) + POP % ("#msft-logo-in", 0.03) + RISE % ("#msft-name-in", 0.12) + SLAM % ("#msft-tag-in", -3, -3, 0.5)
    + POP % ("#msft-d1", 1.1) + POP % ("#msft-d2", 1.42)
    + '      tl.to("#msft-logo-in", { opacity: 0.25, duration: 0.06, yoyo: true, repeat: 5, ease: "none" }, 0.55);\n')

# ---------- FAA (4s) ----------
scene("faa", """
    #faa-logo-in img { width: 270px; height: 270px; display: block; border-radius: 50%; background: #fff; box-shadow: 0 0 0 8px #fff, 0 30px 80px rgba(0,0,0,0.6); }
""",
    '    <div class="P-scrim" data-layout-allow-occlusion></div>\n'
    + clip("faa-k", 0, 4, 452, '<span id="faa-k-in" class="P-kicker">INCIDENTE <i>04</i>/04</span>')
    + clip("faa-logo", 0, 4, 552, '<span id="faa-logo-in"><img src="assets/logos/faa.svg" alt="FAA" /></span>', 1)
    + clip("faa-name", 0.45, 3.55, 876, '<span id="faa-name-in" class="P-big" style="font-size: 118px">SISTEMA AÉREO DOS EUA</span>', 2)
    + clip("faa-zero", 3.05, 0.95, 1212, '<span id="faa-zero-in" class="P-tag" style="font-size: 76px">NENHUM AVIÃO DECOLANDO</span>', 3, CZ),
    RISE % ("#faa-k-in", 0.03) + POP % ("#faa-logo-in", 0.03) + RISE % ("#faa-name-in", 0.45) + SLAM % ("#faa-zero-in", -2, -2, 3.05))

# ---------- LINK (3.95s, sobre a fala) ----------
chips = ""
linkjs = ""
for i, (bg, f, alt, sz) in enumerate([("#f3ba2f", "binance", "Binance", 96), ("#777bb4", "php", "PHP", 96), ("#ffffff", "microsoft", "Microsoft", 96), ("#ffffff", "faa", "FAA", 122)]):
    chips += ('    <div id="link-c%d" class="clip link-chip" data-start="0" data-duration="3.95" data-track-index="%d" style="top: %dpx">'
              '<div id="link-c%d-in" class="link-body" style="background: %s"><img src="assets/logos/%s.svg" alt="%s" style="width:%dpx;height:%dpx" /></div></div>\n') % (i, i + 1, 440 + i * 178, i, bg, f, alt, sz, sz)
    linkjs += '      tl.fromTo("#link-c%d-in", { x: -240, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: "back.out(1.6)" }, %s);\n' % (i, round(0.05 + i * 0.07, 2))
    linkjs += '      tl.to("#link-c%d-in", { scale: 1.16, duration: 0.13, ease: "power2.out", yoyo: true, repeat: 1 }, %s);\n' % (i, round(2.3 + i * 0.16, 2))
    linkjs += '      tl.to("#link-c%d-in", { x: -260, opacity: 0, duration: 0.22, ease: "power2.in" }, %s);\n' % (i, round(3.62 + i * 0.03, 2))
scene("link", """
    .link-chip { position: absolute; left: 130px; width: 150px; height: 150px; }
    .link-body { opacity: 0; position: absolute; inset: 0; border-radius: 36px; display: flex; align-items: center; justify-content: center; box-shadow: 0 18px 40px rgba(0,0,0,0.55), 0 0 0 4px rgba(255,255,255,0.9); }
    .link-body img { object-fit: contain; }
    #link-line { position: absolute; left: 197px; top: 470px; width: 16px; height: 620px; }
    #link-line-in { position: absolute; inset: 0; background: #ff2d3a; border-radius: 8px; box-shadow: 0 0 30px rgba(255,45,58,0.9); }
""",
    '    <div id="link-line" class="clip" data-start="2.2" data-duration="1.75" data-track-index="0"><div id="link-line-in"></div></div>\n' + chips,
    linkjs
    + '      tl.fromTo("#link-line-in", { scaleY: 0, transformOrigin: "50% 0%" }, { scaleY: 1, duration: 0.6, ease: "power2.inOut" }, 2.22);\n'
    + '      tl.to("#link-line-in", { opacity: 0, duration: 0.2, ease: "none" }, 3.6);\n')

# ---------- DEPENDÊNCIA (3.2s) ----------
scene("dep", """
    #dep-bar { position: absolute; left: 130px; top: 980px; width: 820px; height: 74px; }
    #dep-track { position: absolute; inset: 0; border-radius: 37px; border: 4px solid rgba(255,255,255,0.8); background: rgba(6,8,13,0.6); overflow: hidden; }
    #dep-fill { position: absolute; left: 0; top: 0; width: 100%; height: 100%; background: linear-gradient(90deg, #5b7cff 0%, #ffd60a 55%, #ff2d3a 100%); }
""",
    '    <div class="P-scrim" data-layout-allow-occlusion></div>\n'
    + clip("dep-k", 0, 3.2, 500, '<span id="dep-k-in" class="P-kicker">O QUE CONECTA TUDO</span>')
    + clip("dep-l1", 0.35, 2.85, 620, '<span id="dep-l1-in" class="P-big" style="font-size: 150px">NOSSA</span>', 1)
    + clip("dep-l2", 0.75, 2.45, 760, '<span id="dep-l2-in" class="P-big" style="font-size: 200px; color: #ffd60a">DEPENDÊNCIA</span>', 2)
    + '    <div id="dep-bar" class="clip" data-start="1.0" data-duration="2.2" data-track-index="3"><div id="dep-track"><div id="dep-fill"></div></div></div>\n'
    + clip("dep-max", 1.75, 1.45, 1110, '<span id="dep-max-in" class="P-tag" style="font-size: 84px">NUNCA FOI TÃO GRANDE</span>', 4),
    RISE % ("#dep-k-in", 0.05) + RISE % ("#dep-l1-in", 0.35) + SLAM % ("#dep-l2-in", 0, 0, 0.75)
    + '      tl.fromTo("#dep-track", { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "none" }, 1.0);\n'
    + '      tl.fromTo("#dep-fill", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 1.0, ease: "power2.in" }, 1.05);\n'
    + SLAM % ("#dep-max-in", -2, -2, 1.8)
    + '      tl.to("#dep-track", { x: 10, duration: 0.045, yoyo: true, repeat: 7, ease: "none" }, 2.05);\n')

# ---------- IA (3.95s) ----------
pins = "".join('<i class="ai-pin" style="left:-68px;top:%dpx"></i><i class="ai-pin" style="right:-68px;top:%dpx"></i>' % (y, y) for y in (110, 200, 290, 380))
scene("ai", """
    #ai-chip { position: absolute; left: 290px; top: 520px; width: 500px; height: 500px; }
    #ai-chip-in { position: absolute; inset: 0; border-radius: 70px; border: 8px solid #5b7cff; background: rgba(8,12,30,0.78); box-shadow: 0 0 90px rgba(91,124,255,0.65), inset 0 0 60px rgba(91,124,255,0.35); display: flex; align-items: center; justify-content: center; }
    #ai-chip-in span { font-family: "League Gothic", sans-serif; font-size: 400px; line-height: 1; color: #fff; letter-spacing: 0.02em; padding-top: 30px; }
    .ai-pin { position: absolute; width: 60px; height: 14px; background: #5b7cff; border-radius: 7px; }
""",
    '    <div class="P-scrim" data-layout-allow-occlusion></div>\n'
    + clip("ai-k", 0, 3.95, 440, '<span id="ai-k-in" class="P-kicker">E AGORA... INTELIGÊNCIA ARTIFICIAL</span>')
    + '    <div id="ai-chip" class="clip" data-start="0.3" data-duration="3.65" data-track-index="1"><div id="ai-chip-in">' + pins + '<span>IA</span></div></div>\n'
    + clip("ai-l1", 1.7, 2.25, 1066, '<span id="ai-l1-in" class="P-tag" style="font-size: 120px">MUDOU O JOGO</span>', 2)
    + clip("ai-l2", 3.0, 0.95, 1226, '<span id="ai-l2-in" class="P-big" style="font-size: 74px">DA SEGURANÇA DIGITAL</span>', 3, CZ),
    RISE % ("#ai-k-in", 0.05)
    + '      tl.fromTo("#ai-chip-in", { scale: 0.2, opacity: 0, rotation: -25 }, { scale: 1, opacity: 1, rotation: 0, duration: 0.55, ease: "back.out(1.7)" }, 0.3);\n'
    + '      tl.to("#ai-chip-in", { scale: 1.06, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 3 }, 0.95);\n'
    + SLAM % ("#ai-l1-in", -3, -3, 1.72) + RISE % ("#ai-l2-in", 3.0))

# ---------- TOOLKIT (6.1s) ----------
tk = ""
tkjs = ""
for i, (txt, t) in enumerate([("automatizar tarefas", 0.6), ("encontrar vulnerabilidades", 2.33), ("criar ataques", 3.63)]):
    n = len(txt)
    tk += ('    <div id="toolkit-ln%d" class="clip toolkit-ln" data-start="%s" data-duration="%s" data-track-index="%d" style="top: %dpx">'
           '<span class="toolkit-pr">&gt;</span><span id="toolkit-tx%d" class="toolkit-tx">%s</span><span id="toolkit-ok%d" class="toolkit-ok">OK</span></div>\n') % (i, t, round(6.1 - t, 2), 3 + i, 760 + i * 122, i, txt, i)
    tkjs += '      tl.fromTo("#toolkit-tx%d", { clipPath: "inset(0 100%% 0 0)" }, { clipPath: "inset(0 0%% 0 0)", duration: %s, ease: "steps(%d)" }, %s);\n' % (i, round(n * 0.028, 2), n, t)
    tkjs += '      tl.fromTo("#toolkit-ok%d", { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)" }, %s);\n' % (i, round(t + n * 0.028 + 0.1, 2))
scene("toolkit", """
    #toolkit-win { position: absolute; left: 130px; top: 520px; width: 820px; height: 500px; }
    #toolkit-win-in { position: absolute; inset: 0; border-radius: 30px; background: rgba(7,10,16,0.92); border: 3px solid rgba(255,255,255,0.22); box-shadow: 0 40px 100px rgba(0,0,0,0.7); overflow: hidden; }
    #toolkit-bar { height: 84px; background: #161b26; display: flex; align-items: center; padding: 0 30px; gap: 12px; }
    #toolkit-bar i { width: 22px; height: 22px; border-radius: 50%; }
    #toolkit-bar span { font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 28px; color: #8b97ad; margin-left: 20px; }
    #toolkit-head { position: absolute; left: 166px; top: 644px; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 34px; color: #ffd60a; white-space: nowrap; }
    .toolkit-ln { position: absolute; left: 166px; width: 760px; height: 70px; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 38px; line-height: 70px; color: #fff; white-space: nowrap; }
    .toolkit-pr { color: #1fd17a; margin-right: 18px; }
    .toolkit-tx { display: inline-block; }
    .toolkit-ok { display: inline-block; margin-left: 18px; font-size: 28px; line-height: 44px; padding: 0 12px; border-radius: 8px; background: #1fd17a; color: #04130b; vertical-align: middle; }
""",
    '    <div class="P-scrim" data-layout-allow-occlusion></div>\n'
    + clip("toolkit-k", 0, 6.1, 440, '<span id="toolkit-k-in" class="P-kicker">POUCO CONHECIMENTO <i>+</i> IA</span>')
    + '    <div id="toolkit-win" class="clip" data-start="0" data-duration="6.1" data-track-index="1"><div id="toolkit-win-in"><div id="toolkit-bar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i><span>agente-ia — terminal</span></div></div></div>\n'
    + '    <div id="toolkit-head" class="clip" data-start="0.2" data-duration="5.9" data-track-index="2"><span id="toolkit-head-in" style="display:inline-block">$ hoje qualquer um consegue:</span></div>\n'
    + tk
    + clip("toolkit-tag", 5.25, 0.85, 1196, '<span id="toolkit-tag-in" class="P-tag" style="font-size: 80px">MUITO MAIS SOFISTICADOS</span>', 7, CZ),
    RISE % ("#toolkit-k-in", 0.05)
    + '      tl.fromTo("#toolkit-win-in", { y: 120, opacity: 0, scale: 0.92 }, { y: 0, opacity: 1, scale: 1, duration: 0.45, ease: "power3.out" }, 0);\n'
    + '      tl.fromTo("#toolkit-head-in", { opacity: 0 }, { opacity: 1, duration: 0.15, ease: "none" }, 0.25);\n'
    + tkjs + SLAM % ("#toolkit-tag-in", -2, -2, 5.27))

# ---------- HANDS (4.4s) ----------
scene("hands", """
    #hands-a-in { color: #5b7cff; text-shadow: 0 0 60px rgba(91,124,255,0.7); }
    #hands-b-in { color: #ff2d3a; text-shadow: 0 0 60px rgba(255,45,58,0.8); }
""",
    '    <div class="P-scrim" data-layout-allow-occlusion></div>\n'
    + clip("hands-k", 0.2, 4.2, 470, '<span id="hands-k-in" class="P-kicker">A IA ESTÁ NAS MÃOS DE</span>')
    + clip("hands-a", 1.55, 2.85, 600, '<span id="hands-a-in" class="P-big" style="font-size: 190px">QUEM CONSTRÓI</span>', 1)
    + clip("hands-e", 2.75, 1.65, 812, '<span id="hands-e-in" class="P-big" style="font-size: 96px">E TAMBÉM DE</span>', 2)
    + clip("hands-b", 3.55, 0.85, 930, '<span id="hands-b-in" class="P-big" style="font-size: 200px">QUEM DESTRÓI</span>', 3),
    RISE % ("#hands-k-in", 0.2) + SLAM % ("#hands-a-in", 0, 0, 1.57) + RISE % ("#hands-e-in", 2.75) + SLAM % ("#hands-b-in", 0, 0, 3.57)
    + '      tl.to("#hands-a-in", { opacity: 0.35, duration: 0.2, ease: "none" }, 3.57);\n'
    + '      tl.to("#hands-b-in", { x: 14, skewX: 8, duration: 0.045, yoyo: true, repeat: 7, ease: "none" }, 3.86);\n')

# ---------- CHECKLIST (8.9s) ----------
CK = [("ATUALIZE OS SISTEMAS", 0.08), ("AUTENTICAÇÃO EM 2 ETAPAS", 1.0), ("BACKUPS SEMPRE DISPONÍVEIS", 3.45), ("REVISE QUEM TEM ACESSO", 6.2)]
# largura útil do texto no card: 820 - bordas/padding/caixa/número/gaps
CK_FS = min(fit(t, "display", 74, 820 - 190, 0.02) for t, _ in CK)
ck = ""
ckjs = ""
for i, (txt, t) in enumerate(CK):
    ck += ('    <div id="check-r%d" class="clip check-row" data-start="%s" data-duration="%s" data-track-index="%d" style="top: %dpx"><div id="check-r%d-in" class="check-card">'
           '<span class="check-box"><svg viewBox="0 0 60 60"><path id="check-p%d" d="M13 31 L26 44 L48 17" fill="none" stroke="#04130b" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="60" stroke-dashoffset="60"/></svg></span>'
           '<span class="check-n">0%d</span><span class="check-t">%s</span></div></div>\n') % (i, t, round(8.9 - t, 2), 2 + i, 600 + i * 158, i, i, i + 1, txt)
    ckjs += '      tl.fromTo("#check-r%d-in", { x: 420, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, %s);\n' % (i, t)
    ckjs += '      tl.fromTo("#check-r%d-in .check-box", { backgroundColor: "rgba(255,255,255,0.08)" }, { backgroundColor: "#1fd17a", duration: 0.18, ease: "none", immediateRender: false }, %s);\n' % (i, round(t + 0.5, 2))
    ckjs += '      tl.fromTo("#check-p%d", { strokeDashoffset: 60 }, { strokeDashoffset: 0, duration: 0.28, ease: "power2.out", immediateRender: false }, %s);\n' % (i, round(t + 0.55, 2))
    ckjs += '      tl.to("#check-r%d-in", { scale: 1.04, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1 }, %s);\n' % (i, round(t + 0.55, 2))
scene("check", """
    .check-row { position: absolute; left: 130px; width: 820px; height: 134px; }
    .check-card { position: absolute; inset: 0; border-radius: 28px; background: rgba(8,11,18,0.9); border: 3px solid rgba(255,255,255,0.22); display: flex; align-items: center; padding: 0 24px; gap: 16px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
    .check-box { width: 64px; height: 64px; border-radius: 18px; border: 4px solid #1fd17a; background: rgba(255,255,255,0.08); flex: 0 0 auto; display: flex; align-items: center; justify-content: center; }
    .check-box svg { width: 50px; height: 50px; }
    .check-n { font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 30px; color: #8b97ad; }
    .check-t { font-family: "League Gothic", sans-serif; font-size: %dpx; line-height: 1; color: #fff; letter-spacing: 0.02em; white-space: nowrap; padding-top: 8px; }
""" % CK_FS + """
""",
    '    <div class="P-scrim" data-layout-allow-occlusion></div>\n'
    + clip("check-k", 0, 8.9, 436, '<span id="check-k-in" class="P-kicker">TEM UM NEGÓCIO? <i>NÃO ESPERE</i></span>')
    + clip("check-h", 0, 8.9, 500, '<span id="check-h-in" class="P-big" style="font-size: 84px; color: #ffd60a">FAÇA ISSO AGORA</span>', 1)
    + ck,
    RISE % ("#check-k-in", 0.0) + RISE % ("#check-h-in", 0.0) + ckjs)

# ---------- END (6.63s, sobre a fala) ----------
scene("end", """
    #end-shade { position: absolute; left: 0; top: 0; width: 1080px; height: 560px; background: linear-gradient(180deg, rgba(4,6,10,0.86) 0%, rgba(4,6,10,0.62) 55%, rgba(4,6,10,0) 100%); }
    #end-q-in { color: #0a0c12; background: #fff; padding: 16px 34px 6px; border-radius: 10px; }
    #end-arrow { position: absolute; left: 490px; top: 404px; width: 100px; height: 100px; }
    #end-arrow svg { width: 100px; height: 100px; display: block; }
""",
    '    <div id="end-shade" data-layout-allow-occlusion></div>\n'
    + clip("end-q0", 0.2, 2.75, 200, '<span id="end-q0-in" class="P-big" style="font-size: 92px">A IA VAI MUDAR<br/>A SEGURANÇA DIGITAL?</span>', 0, "data-layout-allow-overlap")
    + clip("end-big", 3.05, 1.15, 196, '<span id="end-big-in" class="P-big" style="font-size: 230px; color: #ff2d3a">JÁ MUDOU.</span>', 1)
    + clip("end-c1", 4.26, 2.37, 196, '<span id="end-c1-in" class="P-tag" style="font-size: 76px">COMENTA AQUI EMBAIXO</span>', 2)
    + clip("end-q", 4.5, 2.13, 304, '<span id="end-q-in" class="P-big" style="font-size: 96px">VOCÊ ESTÁ PREPARADO?</span>', 3)
    + '    <div id="end-arrow" class="clip" data-start="4.9" data-duration="1.73" data-track-index="4"><div id="end-arrow-in"><svg viewBox="0 0 100 100"><path d="M50 12 V78 M22 52 L50 82 L78 52" fill="none" stroke="#ffd60a" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>\n',
    RISE % ("#end-q0-in", 0.2)
    + '      tl.to("#end-q0-in", { opacity: 0, y: -40, duration: 0.15, ease: "power2.in" }, 2.8);\n'
    + SLAM % ("#end-big-in", -2, -2, 3.07)
    + '      tl.to("#end-big-in", { x: 12, duration: 0.045, yoyo: true, repeat: 5, ease: "none" }, 3.36);\n'
    + SLAM % ("#end-c1-in", -2, -2, 4.28) + POP % ("#end-q-in", 4.52)
    + '      tl.fromTo("#end-arrow-in", { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.25, ease: "power2.out" }, 4.92);\n'
    + '      tl.to("#end-arrow-in", { y: 22, duration: 0.28, ease: "sine.inOut", yoyo: true, repeat: 4 }, 5.2);\n',
    pads={"end-q-in": 68})
print("ok")
