# Example: VOICEOVER-ONLY reel (no face), 100% motion graphics over darkened b-roll (bold-dark preset).
# Padrões: logo + etiqueta "DE GRAÇA" · chips de concorrentes com $$$ e cadeado · ícone de mudo · nome em destaque com anel ·
# chat genérico riscado com X · nuvem desenhada com computador dentro + 3 chips · terminal de tarefas · celular fechando o app +
# painel "TRABALHANDO..." · comparação em 3 cards com preço · alvo com flecha · corrida com barras e logos · grade de pessoas acendendo ·
# cards de dados/contas · CTA com pergunta, balão e botão SEGUIR -> SEGUINDO.
# ATENÇÃO: não use a classe ".<cena>-row" no CSS da cena: clip() já usa "P-row" e as regras colidem.
# Cenas do reels "Muse, a IA gratis da Meta". Gera compositions/*.html via reel_scenes.py.
# Tempos relativos ao inicio de cada cena (o index.html posiciona as cenas na fala).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_scenes import *

GREEN = "#1fd17a"

# Chip de logo (logos oficiais em assets/logos, nunca redesenhados)
CHIP = """
    .P-chip { display: flex; align-items: center; justify-content: center; border-radius: 30%; box-shadow: 0 18px 40px rgba(0,0,0,0.55), 0 0 0 4px rgba(255,255,255,0.9); }
    .P-chip img { display: block; object-fit: contain; }
"""
LOGO = {
    "meta": ("meta.svg", "Meta", "#ffffff", 0.74, 0.5),
    "chatgpt": ("chatgpt.svg", "ChatGPT", "#ffffff", 0.62, 0.62),
    "grok": ("grok.svg", "Grok", "#0b0b0d", 0.6, 0.6),
}


def chip(id, which, size):
    f, alt, bg, w, h = LOGO[which]
    return ('<div id="%s" class="P-chip" style="width:%dpx;height:%dpx;background:%s">'
            '<img src="assets/logos/%s" alt="%s" style="width:%dpx;height:%dpx" /></div>') % (id, size, size, bg, f, alt, int(size * w), int(size * h))


def box(id, start, dur, left, top, w, h, inner, track=0, extra=""):
    """Caixa posicionada a mao (respeitar left>=130 e left+w<=950 para o que e legivel)."""
    return ('    <div id="%s" class="clip" data-start="%s" data-duration="%s" data-track-index="%d" '
            'style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx" %s>%s</div>\n') % (id, start, dur, track, left, top, w, h, extra, inner)


def fadeout(sel, t):
    return '      tl.to("%s", { opacity: 0, y: -30, duration: 0.18, ease: "power2.in" }, %s);\n' % (sel, t)


def pulse(sel, t, s=1.1):
    return '      tl.to("%s", { scale: %s, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1 }, %s);\n' % (sel, s, t)


# ---------------------------------------------------------------- HOOK (0 - 4.94)
scene("hook", CHIP + """
    #hook-meta-in { display: inline-block; background: #fff; border-radius: 40px; padding: 28px 54px; box-shadow: 0 30px 90px rgba(0,130,251,0.55), 0 0 0 5px rgba(255,255,255,0.9); }
    #hook-meta-in img { width: 220px; height: 147px; display: block; }
    #hook-free-in { color: #04130b; background: #1fd17a; box-shadow: 0 18px 60px rgba(31,209,122,0.55); }
    .hook-price { position: absolute; left: 0; top: 0; width: 100%; text-align: center; }
    .hook-price span { display: inline-block; font-family: "League Gothic", sans-serif; font-size: 70px; line-height: 1; color: #fff; background: #ff2d3a; padding: 10px 26px 2px; border-radius: 8px; letter-spacing: 0.04em; box-shadow: 0 14px 40px rgba(255,45,58,0.5); }
    .hook-lock { position: absolute; right: -24px; top: -24px; width: 72px; height: 72px; border-radius: 50%; background: #ff2d3a; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 0 5px rgba(6,8,13,0.95); }
    .hook-lock svg { width: 40px; height: 40px; }
""",
    SCRIM
    + clip("hook-meta", 0, 4.94, 452, '<span id="hook-meta-in"><img src="assets/logos/meta.svg" alt="Meta" /></span>')
    + clip("hook-free", 1.9, 3.04, 700, '<span id="hook-free-in" class="P-tag" style="font-size: 160px">DE GRAÇA</span>', 1)
    + box("hook-c1", 3.25, 1.69, 300, 950, 170, 170, chip("hook-c1-in", "chatgpt", 170) + '<span id="hook-l1" class="hook-lock"><svg viewBox="0 0 24 24"><rect x="5" y="11" width="14" height="10" rx="2" fill="#fff"/><path d="M8 11V8a4 4 0 0 1 8 0v3" fill="none" stroke="#fff" stroke-width="2.6"/></svg></span>', 2, "data-layout-allow-overflow")
    + box("hook-c2", 3.35, 1.59, 610, 950, 170, 170, chip("hook-c2-in", "grok", 170) + '<span id="hook-l2" class="hook-lock"><svg viewBox="0 0 24 24"><rect x="5" y="11" width="14" height="10" rx="2" fill="#fff"/><path d="M8 11V8a4 4 0 0 1 8 0v3" fill="none" stroke="#fff" stroke-width="2.6"/></svg></span>', 3, "data-layout-allow-overflow")
    + box("hook-p1", 3.85, 1.09, 245, 1140, 280, 90, '<div id="hook-p1-in" class="hook-price"><span>$$$</span></div>', 4)
    + box("hook-p2", 3.95, 0.99, 555, 1140, 280, 90, '<div id="hook-p2-in" class="hook-price"><span>$$$</span></div>', 5)
    + clip("hook-k", 3.3, 1.64, 1244, '<span id="hook-k-in" class="P-kicker">OS CONCORRENTES <i>COBRAM</i></span>', 6, CZ),
    '      tl.fromTo("#hook-meta-in", { scale: 1.18 }, { scale: 1, duration: 0.5, ease: "expo.out" }, 0);\n'
    + pulse("#hook-meta-in", 1.08, 1.12)
    + SLAM % ("#hook-free-in", -4, -3, 1.9)
    + '      tl.to("#hook-free-in", { scale: 1.08, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1 }, 2.5);\n'
    + '      tl.fromTo("#hook-c1-in", { y: 160, opacity: 0, rotation: -12 }, { y: 0, opacity: 1, rotation: 0, duration: 0.4, ease: "back.out(1.8)" }, 3.25);\n'
    + '      tl.fromTo("#hook-c2-in", { y: 160, opacity: 0, rotation: 12 }, { y: 0, opacity: 1, rotation: 0, duration: 0.4, ease: "back.out(1.8)" }, 3.35);\n'
    + RISE % ("#hook-k-in", 3.3)
    + SLAM % ("#hook-p1-in span", -6, -4, 3.88) + SLAM % ("#hook-p2-in span", 6, 4, 3.98)
    + '      tl.fromTo("#hook-l1", { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(3)" }, 4.45);\n'
    + '      tl.fromTo("#hook-l2", { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(3)" }, 4.55);\n'
    + SHAKE % ("#hook-c1-in", 4.62) + SHAKE % ("#hook-c2-in", 4.66))

# ---------------------------------------------------------------- QUASE NINGUEM (4.94 - 6.62)
scene("quiet", """
    #quiet-mute { position: absolute; left: 440px; top: 960px; width: 200px; height: 200px; }
    #quiet-mute-in { position: absolute; inset: 0; border-radius: 50%; background: rgba(6,8,13,0.7); border: 5px solid rgba(255,255,255,0.85); display: flex; align-items: center; justify-content: center; }
    #quiet-mute-in svg { width: 120px; height: 120px; }
""",
    SCRIM
    + clip("quiet-a", 0, 1.68, 520, '<span id="quiet-a-in" class="P-big" style="font-size: 200px">QUASE NINGUÉM</span>')
    + clip("quiet-b", 0.62, 1.06, 740, '<span id="quiet-b-in" class="P-tag" style="font-size: 104px">TÁ FALANDO DISSO</span>', 1)
    + '    <div id="quiet-mute" class="clip" data-start="0.2" data-duration="1.48" data-track-index="2"><div id="quiet-mute-in"><svg viewBox="0 0 24 24"><path d="M3 9h4l5-4v14l-5-4H3z" fill="#fff"/><path d="M16 9l5 6M21 9l-5 6" stroke="#ff2d3a" stroke-width="2.4" stroke-linecap="round"/></svg></div></div>\n',
    SLAM % ("#quiet-a-in", 0, 0, 0.02)
    + SLAM % ("#quiet-b-in", -3, -2, 0.64)
    + POP % ("#quiet-mute-in", 0.2)
    + '      tl.to("#quiet-mute-in", { rotation: 8, duration: 0.09, yoyo: true, repeat: 5, ease: "sine.inOut" }, 0.7);\n')

# ---------------------------------------------------------------- MUSE (6.62 - 9.48)
scene("muse", CHIP + """
    #muse-name-in { color: #fff; letter-spacing: 0.06em; text-shadow: 0 0 40px rgba(120,150,255,0.95), 0 0 120px rgba(91,124,255,0.75); }
    #muse-ring { position: absolute; left: 190px; top: 470px; width: 700px; height: 700px; }
    #muse-ring-in { position: absolute; inset: 0; border-radius: 50%; border: 6px solid rgba(120,150,255,0.7); box-shadow: 0 0 80px rgba(91,124,255,0.6), inset 0 0 80px rgba(91,124,255,0.35); }
    #muse-by-in { display: inline-flex; align-items: center; gap: 26px; }
    #muse-by-in b { font-family: "League Gothic", sans-serif; font-weight: 400; font-size: 96px; color: #fff; line-height: 1; padding-top: 10px; letter-spacing: 0.02em; }
""",
    SCRIM
    + clip("muse-k", 0, 2.86, 452, '<span id="muse-k-in" class="P-kicker">EU TÔ FALANDO DO</span>')
    + '    <div id="muse-ring" class="clip" data-start="0.6" data-duration="2.26" data-track-index="1" data-layout-allow-occlusion><div id="muse-ring-in"></div></div>\n'
    + clip("muse-name", 0.62, 2.24, 600, '<span id="muse-name-in" class="P-big" style="font-size: 400px">MUSE</span>', 2)
    + clip("muse-sub", 0.96, 1.9, 1010, '<span id="muse-sub-in" class="P-big" style="font-size: 84px">A NOVA INTELIGÊNCIA ARTIFICIAL</span>', 3)
    + clip("muse-by", 2.34, 0.52, 1112, '<span id="muse-by-in">' + chip("muse-by-chip", "meta", 120) + '<b>DA META</b></span>', 4, CZ),
    RISE % ("#muse-k-in", 0.02)
    + '      tl.fromTo("#muse-name-in", { scale: 1.9, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "expo.out" }, 0.62);\n'
    + '      tl.fromTo("#muse-ring-in", { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.6, ease: "power3.out" }, 0.6);\n'
    + '      tl.to("#muse-ring-in", { scale: 1.06, opacity: 0.6, duration: 1.6, ease: "sine.inOut" }, 1.2);\n'
    + RISE % ("#muse-sub-in", 0.96)
    + POP % ("#muse-by-in", 2.34))

# ---------------------------------------------------------------- NAO E CHATBOT (9.48 - 12.05)
scene("chatbot", """
    #chatbot-win-in { position: absolute; inset: 0; border-radius: 34px; background: rgba(12,15,22,0.94); border: 3px solid rgba(255,255,255,0.22); box-shadow: 0 40px 100px rgba(0,0,0,0.7); overflow: hidden; }
    #chatbot-bar { height: 80px; background: #161b26; display: flex; align-items: center; padding: 0 30px; gap: 14px; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 28px; color: #8b97ad; }
    #chatbot-bar i { width: 22px; height: 22px; border-radius: 50%; background: #3a4150; }
    .chatbot-b { position: absolute; max-width: 600px; font-family: "Montserrat", sans-serif; font-weight: 700; font-size: 34px; line-height: 1.25; padding: 22px 28px; border-radius: 28px; }
    .chatbot-bot { left: 30px; background: #232a38; color: #e6ebf5; border-bottom-left-radius: 8px; }
    .chatbot-me { right: 30px; background: #5b7cff; color: #fff; border-bottom-right-radius: 8px; }
    #chatbot-x { position: absolute; left: 290px; top: 470px; width: 500px; height: 500px; }
    #chatbot-x svg { width: 500px; height: 500px; display: block; }
    .chatbot-strike { position: absolute; left: -16px; right: -16px; top: 44%; height: 18px; background: #ff2d3a; border-radius: 9px; box-shadow: 0 0 30px rgba(255,45,58,0.8); }
""",
    SCRIM
    + '    <div id="chatbot-win" class="clip" data-start="0" data-duration="2.57" data-track-index="0" style="position:absolute;left:130px;top:470px;width:820px;height:480px"><div id="chatbot-win-in">'
      '<div id="chatbot-bar"><i></i><i></i><i></i><span>chatbot</span></div>'
      '<div id="chatbot-b1" class="chatbot-b chatbot-bot" style="top:112px">Olá! Como posso ajudar?</div>'
      '<div id="chatbot-b2" class="chatbot-b chatbot-me" style="top:222px">Responde minha pergunta</div>'
      '<div id="chatbot-b3" class="chatbot-b chatbot-bot" style="top:332px">Claro! Aqui está...</div>'
      '</div></div>\n'
    + '    <div id="chatbot-x" class="clip" data-start="0.38" data-duration="2.19" data-track-index="1" data-layout-allow-occlusion><svg viewBox="0 0 100 100"><path id="chatbot-x1" d="M14 14 L86 86" pathLength="1" stroke="#ff2d3a" stroke-width="13" stroke-linecap="round" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/><path id="chatbot-x2" d="M86 14 L14 86" pathLength="1" stroke="#ff2d3a" stroke-width="13" stroke-linecap="round" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/></svg></div>\n'
    + clip("chatbot-esq", 0.4, 1.27, 1010, '<span id="chatbot-esq-in" class="P-tag" style="font-size: 130px">ESQUECE</span>', 2)
    + clip("chatbot-more", 1.67, 0.9, 1010, '<span id="chatbot-more-in" class="P-big" style="font-size: 150px; position: relative">MAIS UM CHATBOT<i id="chatbot-st" class="chatbot-strike"></i></span>', 3),
    '      tl.fromTo("#chatbot-win-in", { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: "power3.out" }, 0);\n'
    + '      ["#chatbot-b1", "#chatbot-b2", "#chatbot-b3"].forEach(function (s, i) { tl.fromTo(s, { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.22, ease: "back.out(2)" }, 0.04 + i * 0.12); });\n'
    + '      tl.to("#chatbot-x1", { strokeDashoffset: 0, duration: 0.16, ease: "power2.out" }, 0.4);\n'
    + '      tl.to("#chatbot-x2", { strokeDashoffset: 0, duration: 0.16, ease: "power2.out" }, 0.52);\n'
    + '      tl.to("#chatbot-win-in", { opacity: 0.4, scale: 0.96, duration: 0.25, ease: "power2.out" }, 0.45);\n'
    + SLAM % ("#chatbot-esq-in", -4, -3, 0.4)
    + SHAKE % ("#chatbot-esq-in", 0.7)
    + RISE % ("#chatbot-more-in", 1.67)
    + '      tl.fromTo("#chatbot-st", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.25, ease: "power3.out" }, 1.95);\n')

# ---------------------------------------------------------------- COMPUTADOR NA NUVEM (12.05 - 17.19)
ICON_GLOBE = '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><circle cx="12" cy="12" r="9.5"/><ellipse cx="12" cy="12" rx="4.2" ry="9.5"/><path d="M2.5 12h19M4.5 7h15M4.5 17h15"/></svg>'
ICON_MEM = '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5" fill="#fff"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/></svg>'
ICON_PLUS = '<svg viewBox="0 0 24 24" fill="none" stroke="#06080d" stroke-width="3.4" stroke-linecap="round"><path d="M12 4v16M4 12h16"/></svg>'
cchips = ""
cjs = ""
for i, (lab, icon, t, gold) in enumerate([("NAVEGADOR", ICON_GLOBE, 3.85, False), ("MEMÓRIA", ICON_MEM, 4.24, False), ("E TUDO", ICON_PLUS, 4.45, True)]):
    style = "background:#ffd60a;color:#06080d;border-color:#ffd60a" if gold else ""
    cchips += box("cloud-c%d" % i, round(t, 2), round(5.14 - t, 2), 130 + i * 280, 1010, 260, 170,
                  '<div id="cloud-c%d-in" class="cloud-chip" style="%s">%s<b>%s</b></div>' % (i, style, icon, lab), 4 + i)
    cjs += '      tl.fromTo("#cloud-c%d-in", { y: 90, scale: 0.7, opacity: 0 }, { y: 0, scale: 1, opacity: 1, duration: 0.32, ease: "back.out(2)" }, %s);\n' % (i, t)
scene("cloud", """
    #cloud-icon { position: absolute; left: 230px; top: 560px; width: 620px; height: 440px; }
    #cloud-icon svg { width: 620px; height: 620px; display: block; margin-top: -110px; }
    .cloud-chip { position: absolute; inset: 0; border-radius: 30px; background: rgba(8,11,18,0.9); border: 3px solid rgba(255,255,255,0.3); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); color: #fff; }
    .cloud-chip svg { width: 66px; height: 66px; }
    .cloud-chip b { font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 32px; letter-spacing: 0.02em; }
""",
    SCRIM
    + clip("cloud-k", 0, 5.14, 452, '<span id="cloud-k-in" class="P-kicker">O MUSE TEM <i>LITERALMENTE</i></span>')
    + '    <div id="cloud-icon" class="clip" data-start="0.1" data-duration="5.04" data-track-index="1"><svg viewBox="0 0 24 24">'
      '<path id="cloud-path" d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" pathLength="1" fill="rgba(91,124,255,0.16)" stroke="#fff" stroke-width="0.7" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1"/>'
      '<g id="cloud-pc"><rect x="7.6" y="11.2" width="8" height="5.2" rx="0.6" fill="#0b1020" stroke="#ffd60a" stroke-width="0.55"/><path d="M9.6 13.1h4M9.6 14.5h2.6" stroke="#5b7cff" stroke-width="0.5" stroke-linecap="round"/><path d="M11.6 16.4v1.3M9.9 17.8h3.4" stroke="#ffd60a" stroke-width="0.55" stroke-linecap="round"/></g>'
      '</svg></div>\n'
    + clip("cloud-pcl", 1.64, 2.18, 1000, '<span id="cloud-pcl-in" class="P-big" style="font-size: 116px">UM COMPUTADOR DEDICADO</span>', 2)
    + clip("cloud-tag", 2.85, 0.97, 1124, '<span id="cloud-tag-in" class="P-tag" style="font-size: 96px">SÓ SEU, NA NUVEM</span>', 3)
    + cchips,
    RISE % ("#cloud-k-in", 0.02)
    + '      tl.to("#cloud-path", { strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut" }, 0.1);\n'
    + '      tl.fromTo("#cloud-pc", { opacity: 0, scale: 0.3, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.4)" }, 1.66);\n'
    + '      tl.fromTo("#cloud-icon svg", { scale: 1 }, { scale: 1.06, duration: 3.5, ease: "none", immediateRender: false }, 1.6);\n'
    + RISE % ("#cloud-pcl-in", 1.64)
    + SLAM % ("#cloud-tag-in", -3, -2, 2.87)
    + fadeout("#cloud-pcl-in", 3.62) + fadeout("#cloud-tag-in", 3.62)
    + cjs)

# ---------------------------------------------------------------- TAREFAS (17.19 - 20.26)
tk = ""
tkjs = ""
for i, (txt, t) in enumerate([("pesquisar", 0.66), ("organizar", 1.31), ("resolver uma tarefa", 2.19)]):
    n = len(txt)
    tk += ('    <div id="tasks-ln%d" class="clip tasks-ln" data-start="%s" data-duration="%s" data-track-index="%d" style="top: %dpx">'
           '<span class="tasks-pr">&gt;</span><span id="tasks-tx%d" class="tasks-tx">%s</span><span id="tasks-ok%d" class="tasks-ok">OK</span></div>\n') % (i, t, round(3.07 - t, 2), 3 + i, 770 + i * 110, i, txt, i)
    tkjs += '      tl.fromTo("#tasks-tx%d", { clipPath: "inset(0 100%% 0 0)" }, { clipPath: "inset(0 0%% 0 0)", duration: %s, ease: "steps(%d)" }, %s);\n' % (i, round(n * 0.025, 2), n, t)
    tkjs += '      tl.fromTo("#tasks-ok%d", { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.22, ease: "back.out(3)" }, %s);\n' % (i, round(t + n * 0.025 + 0.12, 2))
scene("tasks", """
    #tasks-win { position: absolute; left: 130px; top: 540px; width: 820px; height: 560px; }
    #tasks-win-in { position: absolute; inset: 0; border-radius: 30px; background: rgba(7,10,16,0.93); border: 3px solid rgba(255,255,255,0.22); box-shadow: 0 40px 100px rgba(0,0,0,0.7); overflow: hidden; }
    #tasks-bar { height: 84px; background: #161b26; display: flex; align-items: center; padding: 0 30px; gap: 12px; }
    #tasks-bar i { width: 22px; height: 22px; border-radius: 50%; }
    #tasks-bar span { font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 28px; color: #8b97ad; margin-left: 20px; }
    #tasks-head { position: absolute; left: 170px; top: 660px; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 34px; color: #ffd60a; white-space: nowrap; }
    .tasks-ln { position: absolute; left: 170px; width: 760px; height: 80px; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 46px; line-height: 80px; color: #fff; white-space: nowrap; }
    .tasks-pr { color: #1fd17a; margin-right: 20px; }
    .tasks-tx { display: inline-block; }
    .tasks-ok { display: inline-block; margin-left: 20px; font-size: 30px; line-height: 48px; padding: 0 14px; border-radius: 8px; background: #1fd17a; color: #04130b; vertical-align: middle; }
""",
    SCRIM
    + clip("tasks-k", 0, 3.07, 452, '<span id="tasks-k-in" class="P-kicker">VOCÊ PEDE <i>E ELE FAZ</i></span>')
    + '    <div id="tasks-win" class="clip" data-start="0" data-duration="3.07" data-track-index="1"><div id="tasks-win-in"><div id="tasks-bar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i><span>muse — tarefas</span></div></div></div>\n'
    + '    <div id="tasks-head" class="clip" data-start="0.15" data-duration="2.92" data-track-index="2"><span id="tasks-head-in" style="display:inline-block">$ você pede:</span></div>\n'
    + tk,
    RISE % ("#tasks-k-in", 0.02)
    + '      tl.fromTo("#tasks-win-in", { y: 120, opacity: 0, scale: 0.92 }, { y: 0, opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }, 0);\n'
    + '      tl.fromTo("#tasks-head-in", { opacity: 0 }, { opacity: 1, duration: 0.15, ease: "none" }, 0.2);\n'
    + tkjs)

# ---------------------------------------------------------------- FECHA O APP (20.26 - 25.78)
scene("closeapp", """
    #closeapp-phone-in { position: absolute; inset: 0; border-radius: 64px; background: #05070b; border: 12px solid #2a2f3a; box-shadow: 0 40px 100px rgba(0,0,0,0.8), 0 0 0 3px rgba(255,255,255,0.25); overflow: hidden; }
    #closeapp-notch { position: absolute; left: 50%; top: 18px; width: 120px; height: 34px; margin-left: -60px; border-radius: 17px; background: #000; z-index: 3; }
    #closeapp-home { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 20px; background: linear-gradient(160deg, #1b2240 0%, #0a0d16 70%); }
    #closeapp-home b { font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 30px; color: #8b97ad; letter-spacing: 0.12em; }
    #closeapp-home svg { width: 96px; height: 96px; }
    #closeapp-app { position: absolute; inset: 0; background: #0f1320; border-radius: 52px; padding: 90px 30px 0; }
    #closeapp-app h4 { font-family: "League Gothic", sans-serif; font-weight: 400; font-size: 76px; color: #fff; line-height: 1; letter-spacing: 0.06em; text-shadow: 0 0 30px rgba(91,124,255,0.9); }
    .closeapp-task { margin-top: 26px; height: 74px; border-radius: 18px; background: #1b2132; display: flex; align-items: center; padding: 0 20px; gap: 14px; font-family: "Montserrat", sans-serif; font-weight: 700; font-size: 30px; color: #c9d2e3; }
    .closeapp-task i { width: 26px; height: 26px; border-radius: 50%; background: #1fd17a; flex: 0 0 auto; }
    #closeapp-card-in { position: absolute; inset: 0; border-radius: 32px; background: rgba(8,11,18,0.93); border: 3px solid rgba(91,124,255,0.6); box-shadow: 0 0 80px rgba(91,124,255,0.35), 0 40px 100px rgba(0,0,0,0.6); overflow: hidden; }
    #closeapp-head { position: absolute; left: 34px; top: 30px; right: 34px; display: flex; align-items: center; gap: 18px; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 30px; color: #c9d2e3; }
    #closeapp-head svg { width: 56px; height: 56px; }
    #closeapp-live { margin-left: auto; font-size: 28px; color: #04130b; background: #1fd17a; border-radius: 8px; padding: 6px 12px; }
    #closeapp-work { position: absolute; left: 34px; top: 120px; display: flex; align-items: center; gap: 26px; }
    #closeapp-spin { width: 90px; height: 90px; border-radius: 50%; border: 10px solid rgba(255,255,255,0.15); border-top-color: #5b7cff; border-right-color: #5b7cff; }
    #closeapp-work b { font-family: "League Gothic", sans-serif; font-weight: 400; font-size: 110px; line-height: 1; color: #fff; padding-top: 10px; letter-spacing: 0.02em; }
    #closeapp-track { position: absolute; left: 34px; right: 34px; top: 262px; height: 30px; border-radius: 15px; background: rgba(255,255,255,0.12); overflow: hidden; }
    #closeapp-fill { position: absolute; inset: 0; background: linear-gradient(90deg, #5b7cff, #1fd17a); }
    .closeapp-log { position: absolute; left: 34px; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 30px; color: #8b97ad; white-space: nowrap; }
    .closeapp-log em { font-style: normal; color: #1fd17a; }
""",
    SCRIM
    + clip("closeapp-k", 0, 2.2, 452, '<span id="closeapp-k-in" class="P-kicker">E PODE ATÉ <i>FECHAR O APP</i></span>')
    + '    <div id="closeapp-phone" class="clip" data-start="0" data-duration="2.42" data-track-index="1" style="position:absolute;left:350px;top:530px;width:380px;height:720px"><div id="closeapp-phone-in"><span id="closeapp-notch"></span>'
      '<div id="closeapp-home" data-layout-allow-overlap data-layout-allow-occlusion><svg viewBox="0 0 24 24" fill="none" stroke="#8b97ad" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="3" width="7" height="7" rx="2"/><rect x="3" y="14" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/></svg><b>APP FECHADO</b></div>'
      '<div id="closeapp-app" data-layout-allow-overlap data-layout-allow-occlusion><h4>MUSE</h4><div class="closeapp-task"><i></i>pesquisar</div><div class="closeapp-task"><i></i>organizar</div><div class="closeapp-task"><i style="background:#ffd60a"></i>resolver</div></div>'
      '</div></div>\n'
    + clip("closeapp-k2", 2.22, 3.3, 452, '<span id="closeapp-k2-in" class="P-kicker">E ELE <i>CONTINUA</i></span>', 2)
    + '    <div id="closeapp-card" class="clip" data-start="2.22" data-duration="3.3" data-track-index="3" style="position:absolute;left:130px;top:540px;width:820px;height:440px"><div id="closeapp-card-in">'
      '<div id="closeapp-head"><svg viewBox="0 0 24 24"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" fill="rgba(91,124,255,0.3)" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg><span>muse · nuvem</span><span id="closeapp-live">ONLINE</span></div>'
      '<div id="closeapp-work"><div id="closeapp-spin"></div><b>TRABALHANDO...</b></div>'
      '<div id="closeapp-track"><div id="closeapp-fill"></div></div>'
      '<div id="closeapp-g1" class="closeapp-log" style="top:322px"><em>✓</em> pesquisando</div>'
      '<div id="closeapp-g2" class="closeapp-log" style="top:368px"><em>✓</em> organizando</div>'
      '</div></div>\n'
    + clip("closeapp-solo", 3.47, 2.05, 1020, '<span id="closeapp-solo-in" class="P-tag" style="font-size: 140px">SOZINHO</span>', 4)
    + clip("closeapp-sub", 3.8, 1.72, 1196, '<span id="closeapp-sub-in" class="P-big" style="font-size: 64px">MESMO SEM VOCÊ CONVERSAR COM ELE</span>', 5, CZ),
    RISE % ("#closeapp-k-in", 0.02)
    + '      tl.fromTo("#closeapp-phone-in", { y: 200, opacity: 0, rotation: -6 }, { y: 0, opacity: 1, rotation: 0, duration: 0.45, ease: "power3.out" }, 0);\n'
    + '      tl.to("#closeapp-app", { y: -520, scale: 0.55, opacity: 0, duration: 0.45, ease: "power3.in" }, 0.7);\n'
    + '      tl.fromTo("#closeapp-home b", { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "none" }, 1.15);\n'
    + '      tl.to("#closeapp-phone-in", { x: -620, rotation: -14, opacity: 0, duration: 0.35, ease: "power2.in" }, 2.05);\n'
    + RISE % ("#closeapp-k2-in", 2.22)
    + '      tl.fromTo("#closeapp-card-in", { x: 700, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 2.22);\n'
    + '      tl.to("#closeapp-spin", { rotation: 1440, duration: 3.3, ease: "none" }, 2.22);\n'
    + '      tl.fromTo("#closeapp-fill", { scaleX: 0.04, transformOrigin: "0% 50%" }, { scaleX: 0.92, duration: 3.1, ease: "power1.inOut" }, 2.4);\n'
    + '      tl.fromTo("#closeapp-g1", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.25, ease: "power2.out" }, 2.8);\n'
    + '      tl.fromTo("#closeapp-g2", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.25, ease: "power2.out" }, 3.6);\n'
    + SLAM % ("#closeapp-solo-in", -4, -3, 3.49)
    + SHAKE % ("#closeapp-solo-in", 3.8)
    + RISE % ("#closeapp-sub-in", 3.8))

# ---------------------------------------------------------------- COMPARACAO (25.78 - 39.76)
rows = ""
rjs = ""
for i, (lg, name, sub, t, pill, tp, pstyle) in enumerate([
        ("chatgpt", "DOTS", "CHATGPT", 1.1, "PLANOS<br/>MAIS CAROS", 4.49, "font-size:50px;line-height:0.95"),
        ("grok", "GROK BOT", "GROK", 5.4, "US$ 30/MÊS", 7.29, "font-size:60px"),
        ("meta", "MUSE", "META", 9.75, "GRÁTIS", 11.02, "font-size:104px;background:#1fd17a;color:#04130b;box-shadow:0 16px 50px rgba(31,209,122,0.55)")]):
    top = 540 + i * 236
    rows += ('    <div id="cmp-r%d" class="clip cmp-row" data-start="%s" data-duration="%s" data-track-index="%d" style="top:%dpx"><div id="cmp-r%d-in" class="cmp-card">'
             '%s<b class="cmp-name">%s</b><span class="cmp-sub">%s</span>'
             '<span id="cmp-p%d" class="cmp-pill" style="%s">%s</span></div></div>\n') % (i, t, round(13.98 - t, 2), 1 + i, top, i, chip("cmp-chip%d" % i, lg, 150), name, sub, i, pstyle, pill)
    rjs += '      tl.fromTo("#cmp-r%d-in", { x: %d, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, %s);\n' % (i, -500 if i % 2 == 0 else 500, t)
    rjs += SLAM % ("#cmp-p%d" % i, -6, -4, tp)
scene("cmp", CHIP + """
    .cmp-row { position: absolute; left: 130px; width: 820px; height: 210px; }
    .cmp-card { position: absolute; inset: 0; border-radius: 32px; background: rgba(8,11,18,0.9); border: 3px solid rgba(255,255,255,0.22); box-shadow: 0 24px 60px rgba(0,0,0,0.55); }
    .cmp-card .cmp-chip-pos { position: absolute; }
    .cmp-name { position: absolute; left: 212px; top: 46px; font-family: "League Gothic", sans-serif; font-weight: 400; font-size: 92px; line-height: 1; color: #fff; letter-spacing: 0.02em; white-space: nowrap; }
    .cmp-sub { position: absolute; left: 216px; top: 152px; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: 0.18em; color: #8b97ad; }
    .cmp-pill { position: absolute; right: 26px; top: 50%; margin-top: -55px; min-height: 110px; display: flex; align-items: center; justify-content: center; text-align: center; font-family: "League Gothic", sans-serif; text-transform: uppercase; color: #fff; background: #ff2d3a; padding: 10px 22px 2px; border-radius: 10px; letter-spacing: 0.03em; box-shadow: 0 16px 44px rgba(255,45,58,0.45); white-space: nowrap; }
    #cmp-chip0, #cmp-chip1, #cmp-chip2 { position: absolute; left: 30px; top: 30px; }
    #cmp-note-in { font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 32px; color: #c9d2e3; letter-spacing: 0.08em; }
""",
    SCRIM
    + clip("cmp-k", 0, 13.98, 452, '<span id="cmp-k-in" class="P-kicker">OLHA QUE <i>INTERESSANTE</i></span>')
    + rows
    + clip("cmp-note", 12.62, 1.36, 1262, '<span id="cmp-note-in">*COM ALGUNS LIMITES</span>', 5, CZ),
    RISE % ("#cmp-k-in", 0.02)
    + rjs
    + pulse("#cmp-r0-in .cmp-name", 2.08, 1.08)
    + pulse("#cmp-r1-in .cmp-name", 6.03, 1.08)
    + '      tl.to(["#cmp-r0-in", "#cmp-r1-in"], { opacity: 0.38, scale: 0.96, duration: 0.3, ease: "power2.out" }, 11.02);\n'
    + '      tl.to("#cmp-r2-in", { scale: 1.02, borderColor: "#1fd17a", boxShadow: "0 0 70px rgba(31,209,122,0.55)", duration: 0.3, ease: "power2.out" }, 11.02);\n'
    + '      tl.fromTo("#cmp-note-in", { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "none" }, 12.64);\n')

# ---------------------------------------------------------------- ACERTOU EM CHEIO (39.76 - 42.38)
scene("target", """
    #target-board { position: absolute; left: 310px; top: 520px; width: 460px; height: 460px; }
    #target-board svg { width: 460px; height: 460px; display: block; }
    #target-arrow { position: absolute; left: 540px; top: 750px; width: 0; height: 0; }
    #target-rot { position: absolute; left: 0; top: 0; transform: rotate(-28deg); transform-origin: 0 0; }
    #target-arrow-in { position: absolute; left: -10px; top: -30px; width: 420px; height: 60px; }
    #target-arrow-in svg { width: 420px; height: 60px; display: block; }
""",
    SCRIM
    + clip("target-k", 0.58, 2.04, 452, '<span id="target-k-in" class="P-kicker">NA MINHA <i>VISÃO</i></span>')
    + '    <div id="target-board" class="clip" data-start="0" data-duration="2.62" data-track-index="1"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" fill="#ff2d3a"/><circle cx="50" cy="50" r="38" fill="#fff"/><circle cx="50" cy="50" r="28" fill="#ff2d3a"/><circle cx="50" cy="50" r="18" fill="#fff"/><circle cx="50" cy="50" r="8" fill="#ff2d3a"/></svg></div>\n'
    + '    <div id="target-arrow" class="clip" data-start="1.3" data-duration="1.32" data-track-index="2" data-layout-allow-overflow><div id="target-rot"><div id="target-arrow-in"><svg viewBox="0 0 140 20"><path d="M4 10 L18 3 L18 17 Z" fill="#ffd60a"/><rect x="16" y="8" width="104" height="4" fill="#ffd60a"/><path d="M112 10 L138 1 L132 10 L138 19 Z" fill="#fff"/></svg></div></div></div>\n'
    + clip("target-tag", 1.62, 1.0, 1040, '<span id="target-tag-in" class="P-tag" style="font-size: 120px">ACERTOU EM CHEIO</span>', 3),
    POP % ("#target-board svg", 0.0)
    + RISE % ("#target-k-in", 0.58)
    + '      tl.fromTo("#target-arrow-in", { x: 900, opacity: 1 }, { x: 0, duration: 0.24, ease: "power3.in" }, 1.36);\n'
    + '      tl.to("#target-board svg", { scale: 1.08, duration: 0.08, ease: "power2.out", yoyo: true, repeat: 3 }, 1.6);\n'
    + '      tl.to("#target-arrow-in", { rotation: 3, duration: 0.05, yoyo: true, repeat: 5, ease: "none", transformOrigin: "0% 50%" }, 1.6);\n'
    + SLAM % ("#target-tag-in", -4, -3, 1.64))

# ---------------------------------------------------------------- CORRIDA DA IA (42.38 - 46.89)
lanes = ""
ljs = ""
for i, (lg, col, keys) in enumerate([("chatgpt", "#e9edf5", [0.05, 0.42, 0.66, 0.84]), ("grok", "#9aa4b5", [0.05, 0.5, 0.62, 0.8]), ("meta", "#0a84ff", [0.05, 0.36, 0.7, 0.86])]):
    top = 560 + i * 130
    lanes += box("race-l%d" % i, 0.1 + i * 0.08, round(4.51 - 0.1 - i * 0.08, 2), 130, top, 820, 110,
                 '<div id="race-l%d-in" class="race-lane">%s<div class="race-track"><div id="race-f%d" class="race-fill" style="background:%s"></div></div></div>' % (i, chip("race-c%d" % i, lg, 100), i, col), 1 + i)
    ljs += '      tl.fromTo("#race-l%d-in", { x: -300, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, %s);\n' % (i, 0.1 + i * 0.08)
    ljs += '      tl.fromTo("#race-f%d", { scaleX: %s, transformOrigin: "0%% 50%%" }, { scaleX: %s, duration: 1.4, ease: "power1.inOut" }, 0.45);\n' % (i, keys[0], keys[1])
    ljs += '      tl.to("#race-f%d", { scaleX: %s, duration: 1.3, ease: "power1.inOut" }, 1.85);\n' % (i, keys[2])
    ljs += '      tl.to("#race-f%d", { scaleX: %s, duration: 1.3, ease: "power1.inOut" }, 3.15);\n' % (i, keys[3])
scene("race", CHIP + """
    .race-lane { position: absolute; inset: 0; }
    #race-c0, #race-c1, #race-c2 { position: absolute; left: 0; top: 5px; }
    .race-track { position: absolute; left: 130px; right: 0; top: 34px; height: 42px; border-radius: 21px; background: rgba(255,255,255,0.1); border: 3px solid rgba(255,255,255,0.35); overflow: hidden; }
    .race-fill { position: absolute; inset: 0; border-radius: 21px; }
    #race-flag { position: absolute; left: 930px; top: 540px; width: 14px; height: 400px; background: repeating-linear-gradient(180deg, #fff 0 20px, #06080d 20px 40px); border-radius: 4px; opacity: 0.8; }
""",
    SCRIM
    + clip("race-k", 0.5, 4.01, 452, '<span id="race-k-in" class="P-kicker">A CORRIDA DA <i>IA</i></span>')
    + '    <div id="race-flag" class="clip" data-start="0.3" data-duration="4.21" data-track-index="0" data-layout-allow-occlusion></div>\n'
    + lanes
    + clip("race-a", 1.94, 2.57, 990, '<span id="race-a-in" class="P-big" style="font-size: 104px">NÃO É SÓ QUEM TEM</span>', 4)
    + clip("race-b", 3.29, 1.22, 1120, '<span id="race-b-in" class="P-tag" style="font-size: 84px">O MODELO MAIS INTELIGENTE</span>', 5, CZ),
    RISE % ("#race-k-in", 0.5)
    + '      tl.fromTo("#race-flag", { opacity: 0 }, { opacity: 0.8, duration: 0.3, ease: "none" }, 0.3);\n'
    + ljs
    + RISE % ("#race-a-in", 1.94)
    + SLAM % ("#race-b-in", -3, -2, 3.31))

# ---------------------------------------------------------------- AGENTES NA MAO DE TODO MUNDO (46.89 - 51.04)
people = ""
pjs = ""
order = [7, 2, 13, 0, 16, 9, 4, 11, 15, 1, 6, 17, 3, 12, 8, 14, 5, 10]
for idx in range(18):
    r, c = divmod(idx, 6)
    people += ('<svg id="agents-p%d" class="agents-p" viewBox="0 0 24 24" style="left:%dpx;top:%dpx"><circle cx="12" cy="7.5" r="4.5" fill="currentColor"/>'
               '<path d="M3.5 22c0-5 3.8-8.5 8.5-8.5s8.5 3.5 8.5 8.5z" fill="currentColor"/></svg>') % (idx, 18 + c * 137, 6 + r * 122)
for k, idx in enumerate(order):
    t = round(2.6 + k * 0.035, 3)
    pjs += '      tl.to("#agents-p%d", { color: "#ffd60a", scale: 1.12, duration: 0.14, ease: "power2.out" }, %s);\n' % (idx, t)
scene("agents", """
    #agents-grid { position: absolute; left: 130px; top: 760px; width: 820px; height: 370px; }
    .agents-p { position: absolute; width: 100px; height: 100px; color: rgba(255,255,255,0.32); }
""",
    SCRIM
    + clip("agents-k", 0, 4.15, 452, '<span id="agents-k-in" class="P-kicker">VAI SER QUEM <i>CONSEGUIR COLOCAR</i></span>')
    + clip("agents-big", 1.68, 2.47, 540, '<span id="agents-big-in" class="P-big" style="font-size: 170px; color: #ffd60a">AGENTES DE VERDADE</span>', 1)
    + '    <div id="agents-grid" class="clip" data-start="0.2" data-duration="3.95" data-track-index="2">' + people + '</div>\n'
    + clip("agents-tag", 2.99, 1.16, 1170, '<span id="agents-tag-in" class="P-tag" style="font-size: 90px">NA MÃO DE TODO MUNDO</span>', 3, CZ),
    RISE % ("#agents-k-in", 0.02)
    + '      tl.fromTo("#agents-grid", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 0.2);\n'
    + SLAM % ("#agents-big-in", 0, 0, 1.7)
    + pjs
    + SLAM % ("#agents-tag-in", -3, -2, 3.01))

# ---------------------------------------------------------------- CUIDADO (51.04 - 55.89)
ICON_LOCK = '<svg viewBox="0 0 24 24"><rect x="4.5" y="10.5" width="15" height="11" rx="2.2" fill="#ffd60a"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3" fill="none" stroke="#ffd60a" stroke-width="2.4"/><circle cx="12" cy="15.6" r="1.7" fill="#06080d"/></svg>'
ICON_CARD = '<svg viewBox="0 0 24 24"><rect x="2" y="5" width="20" height="14" rx="2.4" fill="#ffd60a"/><rect x="2" y="8.2" width="20" height="2.6" fill="#06080d"/><rect x="5" y="14" width="6" height="2" rx="1" fill="#06080d"/></svg>'
scene("caution", """
    .caution-card { position: absolute; inset: 0; border-radius: 30px; background: rgba(8,11,18,0.92); border: 3px solid rgba(255,214,10,0.55); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; box-shadow: 0 24px 60px rgba(0,0,0,0.6); }
    .caution-card svg { width: 96px; height: 96px; }
    .caution-card b { font-family: "League Gothic", sans-serif; font-weight: 400; font-size: 76px; line-height: 1; color: #fff; letter-spacing: 0.02em; padding-top: 6px; }
""",
    SCRIM
    + clip("caution-k", 0.17, 4.68, 452, '<span id="caution-k-in" class="P-kicker">AGORA, <i>CONFIAR</i></span>')
    + box("caution-c1", 0.56, 4.29, 130, 540, 400, 240, '<div id="caution-c1-in" class="caution-card">' + ICON_LOCK + '<b>SEUS DADOS</b></div>', 1)
    + box("caution-c2", 1.33, 3.52, 550, 540, 400, 240, '<div id="caution-c2-in" class="caution-card">' + ICON_CARD + '<b>SUAS CONTAS</b></div>', 2)
    + clip("caution-q1", 2.02, 2.83, 836, '<span id="caution-q1-in" class="P-big" style="font-size: 112px">PRA UMA IA TRABALHAR</span>', 3)
    + clip("caution-q2", 2.7, 2.15, 956, '<span id="caution-q2-in" class="P-big" style="font-size: 150px; color: #ffd60a">SOZINHA?</span>', 4)
    + clip("caution-tag", 3.26, 1.59, 1140, '<span id="caution-tag-in" class="P-tag" style="font-size: 96px">OUTRA DISCUSSÃO</span>', 5, CZ),
    RISE % ("#caution-k-in", 0.17)
    + POP % ("#caution-c1-in", 0.56) + POP % ("#caution-c2-in", 1.33)
    + RISE % ("#caution-q1-in", 2.02)
    + SLAM % ("#caution-q2-in", 0, 0, 2.74)
    + '      tl.to(["#caution-c1-in", "#caution-c2-in"], { borderColor: "#ff2d3a", duration: 0.1, ease: "none" }, 3.26);\n'
    + SLAM % ("#caution-tag-in", -3, -3, 3.28)
    + SHAKE % ("#caution-tag-in", 3.6))

# ---------------------------------------------------------------- CTA (55.89 - fim)
CTA_DUR = 6.41
scene("cta", """
    #cta-bubble { position: absolute; left: 470px; top: 780px; width: 140px; height: 140px; }
    #cta-bubble svg { width: 140px; height: 140px; display: block; }
    #cta-btn { position: absolute; left: 260px; top: 960px; width: 560px; height: 140px; }
    .cta-face { position: absolute; inset: 0; border-radius: 70px; display: flex; align-items: center; justify-content: center; gap: 22px; font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 58px; letter-spacing: 0.02em; }
    #cta-follow { background: #fff; color: #06080d; box-shadow: 0 20px 60px rgba(255,255,255,0.25); }
    #cta-following { background: #1fd17a; color: #04130b; opacity: 0; box-shadow: 0 20px 60px rgba(31,209,122,0.5); }
    #cta-tap { position: absolute; left: 640px; top: 1040px; width: 110px; height: 110px; }
    #cta-tap svg { width: 110px; height: 110px; display: block; }
""",
    '    <div class="P-scrim" data-layout-allow-occlusion></div>\n'
    + clip("cta-k", 0, CTA_DUR, 250, '<span id="cta-k-in" class="P-kicker">ME CONTA <i>UMA COISA</i></span>')
    + clip("cta-q1", 1.84, CTA_DUR - 1.84, 360, '<span id="cta-q1-in" class="P-big" style="font-size: 150px">VOCÊ JÁ CONHECIA</span>', 1)
    + clip("cta-q2", 2.5, CTA_DUR - 2.5, 520, '<span id="cta-q2-in" class="P-big" style="font-size: 240px; color: #ffd60a">O MUSE?</span>', 2)
    + '    <div id="cta-bubble" class="clip" data-start="2.7" data-duration="%s" data-track-index="3"><div id="cta-bubble-in"><svg viewBox="0 0 24 24"><path d="M4 4h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H10l-5 4v-4H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z" fill="#fff"/><circle cx="8" cy="11" r="1.4" fill="#06080d"/><circle cx="12" cy="11" r="1.4" fill="#06080d"/><circle cx="16" cy="11" r="1.4" fill="#06080d"/></svg></div></div>\n' % round(CTA_DUR - 2.7, 2)
    + '    <div id="cta-btn" class="clip" data-start="2.87" data-duration="%s" data-track-index="4"><div id="cta-btn-in" style="position:absolute;inset:0"><div id="cta-follow" class="cta-face" data-layout-allow-overlap data-layout-allow-occlusion>+ SEGUIR</div><div id="cta-following" class="cta-face" data-layout-allow-overlap data-layout-allow-occlusion>SEGUINDO ✓</div></div></div>\n' % round(CTA_DUR - 2.87, 2)
    + '    <div id="cta-tap" class="clip" data-start="3.1" data-duration="1.0" data-track-index="5"><div id="cta-tap-in"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="rgba(255,255,255,0.35)" stroke="#fff" stroke-width="1.6"/></svg></div></div>\n'
    + clip("cta-more", 4.23, CTA_DUR - 4.23, 1160, '<span id="cta-more-in" class="P-big" style="font-size: 84px">VOU CONTINUAR TESTANDO</span>', 6, CZ),
    RISE % ("#cta-k-in", 0.02)
    + POP % ("#cta-q1-in", 1.84)
    + SLAM % ("#cta-q2-in", 0, 0, 2.52)
    + POP % ("#cta-bubble-in", 2.7)
    + '      tl.to("#cta-bubble-in", { y: -14, duration: 0.3, ease: "sine.inOut", yoyo: true, repeat: 7 }, 3.0);\n'
    + '      tl.fromTo("#cta-btn-in", { y: 120, opacity: 0, scale: 0.8 }, { y: 0, opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, 2.87);\n'
    + '      tl.fromTo("#cta-tap-in", { scale: 1.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.2, ease: "power2.out" }, 3.15);\n'
    + '      tl.to("#cta-btn-in", { scale: 0.9, duration: 0.09, ease: "power2.in", yoyo: true, repeat: 1 }, 3.38);\n'
    + '      tl.to("#cta-tap-in", { scale: 0.7, opacity: 0, duration: 0.25, ease: "power2.out" }, 3.5);\n'
    + '      tl.to("#cta-following", { opacity: 1, duration: 0.12, ease: "none" }, 3.47);\n'
    + RISE % ("#cta-more-in", 4.23))
print("ok")
