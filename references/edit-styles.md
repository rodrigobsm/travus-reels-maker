# Edit styles (templates)

An **edit style** is a complete recipe: look, layout, captions, signature moves, transitions and rhythm. The brief picks one (`editStyle`). The individual moves live in `references/motion-library.md` and can be used in any style.

These styles were distilled from frame-by-frame analysis of well-performing AI-edited reels (2026). Each one is a coherent system: don't mix two styles in one reel, but do borrow single moves from the library.

| Style | One line | Best for | Source material |
| --- | --- | --- | --- |
| `classic` | talking head + bold word captions + title bar + b-roll cards | opinion, news, tips | talking head, hybrid |
| `editorial-canvas` | cream "infographic canvas" on top, face below, camera travels along a connected storyboard | explaining a process, numbers, a framework | talking head |
| `product-kinetic` | Apple-like kinetic type + UI mockups + 3D clay icons, background color flips | SaaS/product demo, ads, "before × after" | voiceover, topic |
| `terminal-neon` | black + one neon color, a sentence building word by word, code windows, counters | AI/dev/tech, "how I did it", growth stories | voiceover, topic |
| `cinematic-3d` | dark scene with depth: floating tilted cards, camera fly-through, depth of field, glowing world | big launches, games, pop culture, "world" stories | any (face inside a floating card) |

`auto` (default): pick by topic and material. A face on camera means `classic` or `editorial-canvas`. No face plus a product/UI means `product-kinetic`. No face plus tech or growth means `terminal-neon`. Games, launches, cities or "a world" mean `cinematic-3d`.

---

## classic

The current default of this skill (see SKILL.md and styles.md).
- **Look:** a theme palette (bold-dark / clean-light / neon-retro / brand).
- **Layout:** the face in full screen, with b-roll alternating between full and split screen.
- **Captions:** word by word or phrase (pill).
- **Signature moves:** title bar, hook chips, cards over b-roll, SLAM tags, punch-ins on jump cuts.

## editorial-canvas

- **Look:** a cream paper ground (`#F3EEE6`), near-black ink, **one warm accent** (orange `#E8622C`).
  - Two fonts: a small sans **kicker** line, plus a large **serif italic** emphasis word in the accent color, like "Renderize vídeos *até 5x mais rápido*". Use a free serif italic such as Instrument Serif or Playfair Display Italic, self-hosted.
  - Thin dark UI windows (rounded, small traffic lights) for screenshots and code.
- **Layout:** the **top ~55%** is the canvas and the **bottom ~45%** is the speaker, framed chest-up on a dark background. The caption is **one word at a time, small (40–48 px), white, sitting on the seam** between the two halves. Every 6–10 s, cut to the speaker **full screen** for 1–2 sentences (the caption moves onto the chest), then back to the split.
- **Signature move: the connected canvas.** All visuals sit on one long horizontal (or zig-zag) board, linked by thin lines and small arrows. The camera **pans** from one station to the next on each new idea (registry `pan-stations`, or one wide div moved with GSAP `x`). The kicker and italic headline above each station type in word by word as he speaks.
- **Data vocabulary:**
  - huge serif numerals ("5x", "300", "25 milhões") with a small sans label;
  - waffle grids (10×10 squares filling);
  - icon arrays of people;
  - a gauge with a needle (`mk-usage-arc`);
  - a funnel;
  - a bar race (`bar-chart-race`, adapted);
  - a step list ("passo a passo") with numbered dots;
  - stadium or object repetition ("10 estádios").
- **Transitions:** only camera pans along the canvas, plus hard cuts to the full-screen face. No flashy wipes.
- **Rhythm:** a new station every 2–4 s, and the full-screen face 15–25% of the time.

## product-kinetic

- **Look:** white `#FFFFFF` and near-black `#0A0A0A` grounds, plus **one brand color** used as a full-bleed background for emphasis beats.
  - The background **flips between white, black and brand color** on beat changes.
  - Bold grotesk headlines, top-left aligned, 2 lines, with the key word in the brand color **or** on a brand-colored highlight box.
- **Layout:** faceless. The headline sits top-left, inside the safe area (x ≥ 130, y ≥ 260), and the visual is centered below it.
- **Signature moves:**
  - **UI mockups as actors:** phone mockups (3D-tilted), chat bubbles, kanban boards scrolling sideways, inbox lists, forms with a **cursor that clicks** (`agent-cursor`, `cursor-zoom-follow`), toggles and radio buttons.
  - **3D clay icons** (spreadsheet, chat bubble, notebook, bell, calendar, funnel, clipboard) in the brand color. Generate them or use a consistent icon set; never mix styles.
  - **Chaos → order:** line-art doodles of phones, notes and spreadsheets multiply on black (the problem), then one clean board appears (the solution).
  - **Manual × product comparison:** two columns, "no manual" vs "no <produto>", with the same timer running on both sides, messy handwritten notes on the left and clean UI on the right. A red **stamp** marks the old way ("DESATUALIZADA").
  - Big **counters** for money and metrics (`count-up`, `number-wheel`).
  - Typewriter text inside UI fields, and a **marker highlight** sweeping over key phrases inside forms.
  - **Hanging sign** "Aberto / Fechado" swinging (`pendulum-swing`).
  - **Logo end card:** the logo plus a circular arc stroke drawing around it, a CTA button, and the cursor clicking it.
- **Transitions:**
  - whip pan with motion blur (`whip-pan-cut`);
  - circle **iris** (`iris-reveal`);
  - a **diagonal black slash** wipe;
  - hard **color-flip** cuts;
  - a blurred push for list changes.

  Use 2–3 kinds per reel, each with a meaning (iris = "imagine", slash = "the rest").
- **Rhythm:** a new headline every 1.5–3 s, and the UI always moving (scroll, type, click).

## terminal-neon

- **Look:** pure black, **one neon accent** (green `#22E07A`, or cyan or amber) and white text.
  - A persistent **line-art footer** (skyline or landmarks) at 10–15% opacity at the bottom, plus a small handle watermark.
  - Subtle radial glow behind the focal element.
- **Layout:** faceless. The text sits in the vertical center and the visual sits just above it.
- **Signature moves:**
  - **The sentence is the caption:** the spoken sentence builds word by word in the center (`per-word-rise`), and the key word turns neon. Previous lines dim to 40% and slide up.
  - **Code/editor windows** that type (`code-typing`, `terminal-simulator`).
  - A **strike-through** that corrects a phrase (`strikethrough-replace`): "~~os reels devem ser ruins~~ não".
  - **Credit or usage meter** bars dropping to zero.
  - **Analytics card** where views count up (`count-up`), going "634.107 → 1 milhão+".
  - **Wall of thumbnails** (100 reels).
  - A **radial burst** of lines from the logo (`sun-burst` or SVG lines).
  - Optional **monitor mockup:** the whole piece played on a real monitor filmed on a desk (screen replacement) for "made 100% with AI" credibility.
- **Ending:** a **comment box** that types the keyword, then the auto-reply DM appearing below ("Aqui estão todos os detalhes").
- **Transitions:** element-level only (fade, blur-in, scale). The black ground never changes.

## cinematic-3d

- **Look:** a night scene with real depth. Choose the world from the topic:
  - a **glowing city/map** (pink or cyan lights, aerial stock graded to the palette);
  - a **tabletop** (an object on a table under a spotlight, e.g. a film reel labeled SKILL.md);
  - a **workshop** with a 3D mascot;
  - a **perspective grid floor**.

  Add depth of field and a vignette.
- **Layout:** **floating cards** in perspective (`tilt-card`, CSS `perspective` + `rotateY/rotateX`). The talking head itself plays **inside a floating rounded card** tilted 8–15°. UI screens (profile, search, tool) float in the world. Captions are small, centered low, with the key word in the accent color.
- **Signature moves:**
  - camera **fly-through and dolly** (`camera-dolly-zoom`, a GSAP scale/translate on a 3D stage);
  - **rack focus** between layers (`rack-focus`);
  - **counters on objects** (a countdown "faltam 12 dias" on a tower);
  - curved **arrows** circling between cards;
  - a map that fills with thumbnails;
  - a glowing world map;
  - receipts printing out;
  - a magnifier passing over a film strip.
- **3D:** use registry blocks tagged `3d`/`webgl` (e.g. `extruded-logo`, `vfx-iphone-device`, carousels) or a pre-rendered asset. Keep one hero 3D element per reel, and check render time.
- **Transitions:** camera moves through the world (no cuts), plus rack focus and push-in through a card into the next scene (`parallax-device-dive`).

---

## Rules for every style

- Safe zones, honesty and audio rules from SKILL.md still apply.
- One style per reel; borrow single moves freely from the library.
- Before building, write the **beat list** with the chosen move for each beat (e.g. `00.0 hook: counter 0→500.000 | 03.2 canvas pan → station 2 | ...`) and show it in the report.
- Prefer a **registry component** (`npx hyperframes add <name>`, then read the header comment of `compositions/components/<name>.html`) over hand-building. Adapt 1920×1080 blocks to 1080×1920 before use.
