# Motion library

Single moves that you can drop into any reel where they fit the line being said. Each row names the technique, when to use it, and **how to build it**: a HyperFrames registry item, a `reel_scenes.py` helper, or a CSS/GSAP recipe.

**Using registry items:**
1. Install with `npx hyperframes add <name>` inside the project. **Components** land in `compositions/components/<name>.html`. Read the header comment first: markup, variables (tone, speed, spacing) and the mount pattern.
2. Components have no fixed size, so they work in 1080×1920. **Blocks** marked 1920×1080 are landscape scenes: adapt the layout before use, or take only the motion idea.
3. Keep everything readable inside x 130–950 (see the safe zones in SKILL.md).

`(C)` = registry component · `(B)` = registry block · `helper` = our code · `recipe` = do it by hand with GSAP/CSS.

## Numbers and data

| Move | Use when he says… | Build |
| --- | --- | --- |
| Odometer / rolling digits | views, money, followers ("500 mil views") | `number-wheel` (C) |
| Count-up stat | any metric that should land with weight | `count-up` (C); `mk-progress-stat` (B, adapt) |
| Analytics card (line growing + counter) | growth, "passou de 1 milhão" | `mk-line-graph` (B, adapt) + `count-up`; dark glass card |
| Bar race | comparing tools or speeds ("5x mais rápido") | `bar-chart-race` (B, adapt); or 3–4 bars with `scaleX` from 0, ending on labels |
| Gauge with needle / arc | rates, percentages, "taxa de conversão" | `mk-usage-arc` (C), `conic-progress-ring` (C) |
| Waffle grid 10×10 | "100 reels", "1 em cada 10" | recipe: 100 squares, stagger `opacity` in reading order, highlight N in the accent |
| Icon array | people, customers, "100 mil seguidores" | recipe: SVG person icons in a grid, stagger in |
| Funnel | views → leads → sales | recipe: 3–4 trapezoids (SVG) drawing down, a dot dropping through |
| Big serif numeral | the one number of the reel | recipe: serif italic 260–360 px + small sans label; `focus-blur-resolve` (C) |
| Calendar grid filling | "30 dias", consistency | recipe: 7×5 cells checking in |
| Credit meter dropping | "sem crédito", "custo zero" | recipe: bar `scaleX` 1→0 with the counter going to 0 |

## UI mockups (show, don't tell)

| Move | Use when… | Build |
| --- | --- | --- |
| Claude/ChatGPT chat typing | showing a prompt and an answer | `claude-exchange` (B, **vertical**), `chatgpt-exchange`, `typed-prompt` (C), `streaming-text` |
| Chat thread / WhatsApp | customer messages, support | `chat-thread` (C), `chat-message`, `typing-indicator` (C), `message-thread-reveal` |
| Phone mockup, tilted | apps, mobile flows | `vfx-iphone-device` (B, real 3D), `multi-device-splay` (C), CSS `perspective` + `rotateY(-14deg)` |
| Push through a phone screen | entering the app | `parallax-device-dive` (C) |
| Cursor that clicks / types | demos, "é só clicar" | `agent-cursor` (C), `cursor-zoom-follow` (C), `cursor-drag-drop` (C, kanban) |
| Code / terminal typing | "escrito em código", dev | `code-typing` (B), `terminal-simulator` (C), `code-highlight`, `code-diff` |
| Notifications stacking | alerts, sales, "chegou mensagem" | `notification-stack` (C), `native-notification-pop`, `notification-pileup` |
| Instagram profile / follow | CTA follow, profile growth | `instagram-follow` (B, **vertical**) |
| Comment box + auto-reply DM | "comenta PALAVRA" CTA | `yt-comment-card` (B, adapt) or recipe: input types the keyword → "Publicado ✓" → DM bubble slides in |
| Kanban / pipeline scroll | sales stages, process | recipe: columns of cards, a wide row moving with `x`; `cursor-drag-drop` (C) |
| Form + radio + click | settings, choosing an option | recipe + `agent-cursor` (C) |
| Receipt printing | prices, quotes, "orçamento" | recipe: paper card sliding down out of a slot (`clipPath` + `y`), lines typing |
| Source screenshot card | a study, a headline, a site | see styles.md (real screenshot + browser bar + highlighter) |

## Text and captions

| Move | Use when… | Build |
| --- | --- | --- |
| Sentence building word by word (caption = graphic) | faceless reels | `per-word-rise` (C); previous line dims and moves up |
| Kicker + serif italic emphasis | editorial style | `caption-editorial-emphasis` (C) |
| Highlight box behind a word | the key word of a headline | `inline-highlight` (C), `marker-highlight` (C) |
| Strike-through correction | myth vs truth, "não" | `strikethrough-replace` (C) |
| Word swap in a fixed sentence | lists ("para clínicas / agências / lojas") | `kinetic-type-swap` (C) |
| Typewriter in a field | prompts, search, forms | `typed-prompt` (C), `notes-typing` |
| Handwritten notes / thought bubble | the manual, messy way | `hw-title`, `hw-write-title`, `hw-text-cloud`, `marker-checklist-card` (C) |
| Stamp | "APROVADO", "DESATUALIZADA", "FAKE" | recipe: rotated bordered label, `scale 1.6→1` with `expo.out` + a short shake |
| Focus pull on a statement | big claims | `focus-blur-resolve` (C) |

## Transitions (give each one a meaning)

| Move | Meaning | Build |
| --- | --- | --- |
| Whip pan with motion blur | "next", speed | `whip-pan-cut` (C), `whip-pan` (B shader) |
| Circle iris | "imagine", zoom into an idea | `iris-reveal` (C), `sdf-iris` (B) |
| Diagonal slash wipe | "o resto", a turn | recipe: black skewed panel sweeping across (`x` with `skewX(-20deg)`), the new scene underneath |
| Directional push | list, step to step | `directional-wipe` (C) |
| Color-flip hard cut | beat change, emphasis | recipe: change the ground color on the beat, with no tween |
| Camera pan along a canvas | process, storyboard | `pan-stations` (C) |
| Pixel / grid dissolve | swapping images in cards | `grid-pixelate-wipe` (C) |
| Scribble cover | playful reset | `hw-scribble-transition` (B) |
| Before × after divider | comparison | `before-after-wipe` (C), `comparison-split` (C) |
| Split-screen b-roll | illustrate while the face keeps talking | see styles.md "Split screen" |

## Camera, depth and 3D

| Move | Use when… | Build |
| --- | --- | --- |
| Floating tilted cards | cinematic-3d, UI in space | `tilt-card` (C), `split-tilt-cards` (C), CSS `perspective` |
| Face inside a floating card | cinematic-3d with a talking head | recipe: the a-roll in a rounded card, `rotateY(10deg)`, a slow drift |
| Dolly / fly-through | a world, a city | `camera-dolly-zoom` (B), recipe: a 3D stage `scale` + `translateZ` |
| Rack focus | from one layer to another | `rack-focus` (B) |
| 3D logo / letters | launches | `extruded-logo` (B), `logo-sting` (C), `logo-outro` (B) |
| Maps | places, reach | `world-map`, `us-map` (B, adapt); glowing aerial stock graded to the palette |
| Carousel / orbit of cards | many examples | `carousel-orbit-*`, `cuboid-carousel` (registry) |

## Backgrounds and texture

| Move | Build |
| --- | --- |
| Line-art footer (skyline, landmarks) | recipe: SVG strokes at 12% opacity, fixed at the bottom |
| Perspective grid floor | recipe: CSS repeating-linear-gradient on a plane with `rotateX(70deg)`; `dynamic-grid` (C) |
| Glow / bokeh | radial gradients; `starfield` (B) for dark skies |
| Film grain | `grain-overlay` (C), at low opacity |
| Rays | `sun-burst` (B shader), `godrays` |

## Endings and CTA

| Move | Build |
| --- | --- |
| "Comenta PALAVRA" + auto DM | comment box recipe above |
| Follow card | `instagram-follow` (B, vertical) |
| Logo + arc + button + cursor click | `logo-outro` (B, adapt) + `agent-cursor` (C) |
| Question with a speech bubble | the classic CTA scene (examples/build-scenes-voiceover.py) |
