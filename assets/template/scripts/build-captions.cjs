// Builds compositions/captions.html from assets/transcript.json.
// Usage (project root):  node scripts/build-captions.cjs
//
// Reads reel.config.json:
// {
//   "duration": 55.2,                 // video length in seconds (same as the root data-duration)
//   "language": "pt",                 // transcript language (pt enables the whisper "Eisso" -> "E isso" fix)
//   "theme": "bold-dark",             // palette preset from scripts/palettes.json (+ optional "palette" overrides)
//   "keywords": ["free", "ai"],       // words highlighted in the accent color (no punctuation, any case)
//   "captions": {
//     "mode": "word",                 // word | phrase | karaoke | none
//     "style": "outline",             // outline (white text, dark stroke) | pill (text on a rounded card)
//     "position": "low",              // low (y 1436) | middle (y 1060) | top (y 560, only when there is no fixed title)
//     "uppercase": true,
//     "maxWords": 3,                  // phrase/karaoke: words per line
//     "maxChars": 22,                 // phrase/karaoke: characters per line
//     "size": null                    // max font size in px (default: word 112, phrase/karaoke 84)
//   }
// }
const fs = require("fs");
const path = require("path");
const root = path.join(__dirname, "..");
const cfgPath = path.join(root, "reel.config.json");
const cfg = fs.existsSync(cfgPath) ? JSON.parse(fs.readFileSync(cfgPath, "utf8")) : {};
const palettes = JSON.parse(fs.readFileSync(path.join(__dirname, "palettes.json"), "utf8"));
const P = Object.assign({}, palettes[cfg.theme] || palettes["bold-dark"], cfg.palette || {});
const C = Object.assign({ mode: "word", style: "outline", position: "low", uppercase: true, maxWords: 3, maxChars: 22, size: null }, cfg.captions || {});
const LANG = (cfg.language || "pt").toLowerCase();

const outFile = path.join(root, "compositions/captions.html");
const SAFE_W = 820; // 1080 - 2 x 130 side margin (Instagram full-screen zoom)
const TOP = { low: 1436, middle: 1060, top: 560 }[C.position] || 1436;
const MAX = C.size || (C.mode === "word" ? 112 : 84);

function luminance(hex) {
  const h = String(hex).replace("#", "");
  if (h.length < 6) return 1;
  return (0.2126 * parseInt(h.slice(0, 2), 16) + 0.7152 * parseInt(h.slice(2, 4), 16) + 0.0722 * parseInt(h.slice(4, 6), 16)) / 255;
}
const accentInk = luminance(P.accent) > 0.6 ? "#0a0c12" : "#ffffff";

let words = [];
if (C.mode !== "none") {
  const raw = JSON.parse(fs.readFileSync(path.join(root, "assets/transcript.json"), "utf8"));
  const src = raw.words || raw;
  for (const w of src) {
    const t = String(w.text).trim();
    if (!t || /^[♪�]+$/.test(t)) continue;
    // Whisper (pt) glues a leading "E" ("and") to the next word: "Eisso" -> "E" + "isso".
    // If a real word starting with E gets split, add it to the exception list below.
    const m = LANG.startsWith("pt") ? /^E([a-zà-ú].*)$/.exec(t) : null;
    if (m && !/^(Ela|Elas|Ele|Eles|Eu|Então|Encontrar|Empresa|Empresas|Empresário|Etapas|Existe|Esse|Essa|Esses|Essas|Este|Esta|Está|Estão|Estou|Entre|Enquanto|Em|Era|Exemplo|Exemplos|Exatamente|Entender|Entendeu|Enfim|Erro|Erros|Esperar|Espera|Escolher|Equipe|Energia|Economia|Email|Entrar|Enviar|Enviado|Evitar|Estratégia|Estudo|Efeito|Eficiente|Especial|Especialista|Essencial|Estrutura|Evento|Evolução|Experiência|Explicar|Extremamente|Engenharia|Engenheiro|Ensinar|Estados|Estoque|Emergência|Enrolação|Escola|Exigido|Esquece|Espalhou)$/i.test(t.replace(/[.,!?;:]/g, ""))) {
      const cut = Math.min(0.16, (w.end - w.start) * 0.35);
      words.push({ text: "E", start: w.start, end: w.start + cut });
      words.push({ text: m[1], start: w.start + cut, end: w.end });
    } else words.push({ text: t, start: w.start, end: w.end });
  }
}
const DUR = cfg.duration || (words.length ? +(words[words.length - 1].end + 0.35).toFixed(2) : 10);
const KEYS = new Set((cfg.keywords || []).map((k) => k.toLowerCase()));
words = words.map((w) => {
  const clean = w.text.replace(/[.,!?;:]/g, "").toLowerCase();
  let text = w.text.replace(/[.,;:]/g, "");
  if (C.uppercase) text = text.toUpperCase();
  return { text, raw: w.text, start: +w.start, end: +w.end, key: KEYS.has(clean) };
});

// Group words into on-screen units.
let groups = [];
if (C.mode === "word") {
  groups = words.map((w) => ({ words: [w] }));
} else if (C.mode !== "none") {
  let cur = [];
  const flush = () => { if (cur.length) groups.push({ words: cur }); cur = []; };
  words.forEach((w, i) => {
    const prev = cur[cur.length - 1];
    const chars = cur.reduce((n, x) => n + x.text.length + 1, 0) + w.text.length;
    if (prev && (cur.length >= C.maxWords || chars > C.maxChars || w.start - prev.end > 0.35 || /[.!?;:,]$/.test(prev.raw))) flush();
    cur.push(w);
  });
  flush();
}
// Timing: a unit leaves when the next one enters (never two on screen); +0.3 s tail max.
groups.forEach((g, i) => {
  const next = groups[i + 1];
  g.start = +g.words[0].start.toFixed(3);
  const last = g.words[g.words.length - 1];
  let end = next ? Math.min(next.words[0].start, last.end + 0.3) : Math.min(DUR - 0.05, last.end + 0.3);
  if (end - g.start < 0.1) end = g.start + 0.1;
  g.end = +end.toFixed(3);
  g.key = g.words.some((w) => w.key);
  g.words = g.words.map((w) => ({ t: w.text, s: +w.start.toFixed(3), k: w.key }));
});

const pill = C.style === "pill";
const css = `
    #root { position: absolute; inset: 0; }
    #cap-stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
    .cap-line {
      position: absolute; left: 0; top: ${TOP}px; width: 1080px; text-align: center; line-height: 1;
      white-space: nowrap; opacity: 0; visibility: hidden;
    }
    .cap-in {
      display: inline-block; font-family: var(--font-body); font-weight: 900; letter-spacing: -0.01em;
      ${pill
        ? `color: ${P.cardInk}; background: ${P.card}; border-radius: 999px; padding: 0.2em 0.55em 0.16em; box-shadow: 0 14px 40px rgba(${P.shadow},0.28);`
        : `color: #ffffff; -webkit-text-stroke: 0.125em #05070b; paint-order: stroke fill; text-shadow: 0 10px 26px rgba(0,0,0,0.75);`}
    }
    .cap-w { display: inline-block; }
    ${pill
      ? `.cap-key .cap-in { background: ${P.accent}; color: ${accentInk}; }
    .cap-in .cap-w.k { background: ${P.accent}; color: ${accentInk}; border-radius: 0.3em; padding: 0 0.18em; }`
      : `.cap-w.k { color: ${P.accent}; }`}
`;

const html = `<template>
  <style>${css}  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
    <div id="cap-stage" class="clip" data-start="0" data-duration="${DUR}" data-track-index="0" data-layout-allow-overlap data-layout-allow-caption-zone></div>
  </div>
  <script>
    (function () {
      // Generated by scripts/build-captions.cjs from assets/transcript.json (mode: ${C.mode}, style: ${C.style}).
      var GROUPS = ${JSON.stringify(groups)};
      var MODE = "${C.mode}", MAX = ${MAX}, SAFE_W = ${SAFE_W}, PILL = ${pill};
      var ON = "${pill ? P.alert : P.accent}", BASE = "${pill ? P.cardInk : "#ffffff"}"; // karaoke: active word / spoken-or-waiting words
      var stage = document.getElementById("cap-stage");
      var tl = gsap.timeline({ paused: true });
      var cv = document.createElement("canvas").getContext("2d");
      function fit(text) {
        var size = MAX;
        while (size > 44) {
          cv.font = "900 " + size + "px Montserrat";
          if (cv.measureText(text).width * (PILL ? 1.12 : 1.0) <= SAFE_W) break;
          size -= 2;
        }
        return size;
      }
      GROUPS.forEach(function (g, i) {
        var line = document.createElement("div");
        line.className = "cap-line" + (g.key && MODE === "word" ? " cap-key" : "");
        line.id = "cap-g" + i;
        var inner = document.createElement("span");
        inner.className = "cap-in";
        var spans = g.words.map(function (w, j) {
          var s = document.createElement("span");
          s.className = "cap-w" + (w.k && MODE !== "karaoke" ? " k" : "");
          s.id = "cap-g" + i + "-w" + j;
          s.textContent = w.t;
          if (j) inner.appendChild(document.createTextNode(" "));
          inner.appendChild(s);
          return s;
        });
        line.appendChild(inner);
        inner.style.fontSize = fit(g.words.map(function (w) { return w.t; }).join(" ")) + "px";
        stage.appendChild(line);
        gsap.set(line, { yPercent: -50 });
        tl.set(line, { visibility: "visible", opacity: 1 }, g.start);
        var big = MODE === "word" && g.key;
        tl.fromTo(inner, { scale: big ? 0.62 : 0.82 }, { scale: 1, duration: big ? 0.2 : 0.14, ease: big ? "back.out(3)" : "power3.out", immediateRender: false }, g.start);
        if (MODE === "karaoke") {
          g.words.forEach(function (w, j) {
            var nextStart = j < g.words.length - 1 ? g.words[j + 1].s : g.end;
            tl.set(spans[j], { color: ON }, w.s);
            tl.fromTo(spans[j], { scale: 1.12 }, { scale: 1, duration: 0.18, ease: "power2.out", immediateRender: false }, w.s);
            if (j < g.words.length - 1) tl.set(spans[j], { color: BASE }, nextStart - 0.004);
          });
        }
        tl.set(line, { opacity: 0, visibility: "hidden" }, g.end - 0.004);
      });
      window.__timelines["captions"] = tl;
    })();
  </script>
</template>
`;
fs.writeFileSync(outFile, html);
console.log(`captions: mode=${C.mode} style=${C.style} position=${C.position} | ${groups.length} units, ${words.filter((w) => w.key).length} keywords, duration ${DUR}`);
if (LANG.startsWith("pt")) console.log("isolated E:", words.filter((w) => /^E$/i.test(w.text)).length, "(check the transcript if a cut looks wrong)");
