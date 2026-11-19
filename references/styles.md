# Styles: themes, captions, typography, scenes, b-roll

## Themes (palettes)

All theme presets are defined in `assets/template/scripts/palettes.json`, the single source used by `reel_scenes.py`, `build-captions.cjs` and `new_project.py`. A brief can override any key with `palette`.

| Key | bold-dark | clean-light | neon-retro | Use |
| --- | --- | --- | --- | --- |
| ground | `#06080d` | `#F7F3EA` | `#0b0420` | page / empty background |
| ink | `#ffffff` | `#15211B` | `#ffffff` | main text |
| accent | `#ffd60a` | `#1F9D63` | `#2de2e6` | keywords, highlights (one accent only) |
| alert | `#ff2d3a` | `#D2442C` | `#ff2e88` | tags, "problem" items (backgrounds) |
| alertText | `#ff5661` | `#D2442C` | `#ff5aa5` | alert color for thin text (contrast) |
| cool | `#5b7cff` | `#2F6FDB` | `#8b5cf6` | secondary info |
| ok | `#1fd17a` | `#1F9D63` | `#f9c80e` | free / correct / check |
| card | dark glass | `#ffffff` | purple glass | cards, kickers, pill captions |
| scrim | near-black | cream | deep purple | tint over b-roll behind scenes |

- **bold-dark:** tech, news, business. Strong contrast, League Gothic headlines, slanted red tags that SLAM in.
- **clean-light:** health, wellness, lifestyle, education.
  - White cards with soft shadows and pill captions.
  - Nothing dark: brighten dark b-roll (`eq=brightness=0.06:saturation=1.1`) or put it inside a white card.
  - No fixed title when the speaker's head sits high in the frame: use a hook title only during the first ~7 s, then put the graphics in the lower third (y 1150–1320).
- **neon-retro:** games, pop culture, 80s/synthwave.
  - Glow with `text-shadow: 0 0 40px <accent>`.
  - Gradient sunsets (pink → purple) behind cards.
- **brand:** the creator's colors on top of `brandBase`. Keep one accent for keywords. Check contrast: the accent on white must stay above 3:1 for big text.

In scene CSS, use `C["ink"]`, `C["accent"]`… from `reel_scenes` (Python), or `var(--ink)`, `var(--accent)`… inside compositions, so the same scene works on any theme.

## Captions (`reel.config.json` → `captions`)

| mode | What it shows | Best for |
| --- | --- | --- |
| `word` | one word at a time, a big pop, keywords in the accent with a bigger pop | retention, fast talkers, bold-dark |
| `phrase` | 2–3 words (`maxWords`, `maxChars`), split on punctuation and pauses > 0.35 s | calmer content, light theme, long words |
| `karaoke` | the phrase stays and the spoken word lights up in the accent | music-like rhythm, tutorials |
| `none` | no captions (the track is removed from the index) | aesthetic / visual-only reels |

| style | Look |
| --- | --- |
| `outline` | white Montserrat 900, dark outline 0.125 em, shadow; the keyword in the accent |
| `pill` | text on a rounded `card` pill; the keyword only changes to the accent color, with no inner bubble (word mode: the whole pill turns accent) |

- Position: `low` (y 1436, default), `middle` (y 1060), `top` (y 560, only without a fixed title).
  - With `middle`, scenes must keep the y 960–1160 band free: move cards to y 430–900, or to the lower third (y 1200–1320).
  - With `top`, keep y 480–640 free.
- The max size is 112 px for words and 84 px for phrases; text auto-shrinks to fit 820 px.
- Keywords: one impact word per sentence, the same ones that become tags on screen.

## Typography

The fonts are bundled in `assets/fonts` (SIL OFL) and declared with `@font-face`, because built-in names didn't resolve reliably.

| Font | Use |
| --- | --- |
| **League Gothic** | titles, impact words, tags (uppercase) |
| **Montserrat 900/700** | captions, cards, body |
| **JetBrains Mono 700** | kickers ("INCIDENT 01/04"), labels, terminal |

## Fixed title and hook

- **Title:** up to 4 words that promise the content, with a number if there is one ("4 BIG MISTAKES", "GTA VI WITHOUT AI?"). It sits in a shade gradient at y 186–390, plus a tag that changes when the topic turns.
- **Hook:** frame 0 already shows the title plus a logo or a strong phrase, with no fade from black. Logo chips slide in from the left with an alert badge, or the first scene starts right away.

## Typical scenes (see `references/examples/`)

- Company card: kicker pill + big logo + name in League Gothic + slanted alert tag that SLAMs in on the impact word.
- Sites going from ONLINE to "503 · DOWN"; an airport split-flap board (`npx hyperframes add split-flap-board`).
- Logo chips linked by a line; a filling bar or gauge; a pulsing "AI" chip.
- A terminal typing a list; A vs B contrast in two colors; a checklist with animated checks.
- Comparison in 3 cards with a price and the winner highlighted; a race with bars and logos.
- A phone closing an app + a "WORKING…" panel; a grid of people lighting up.
- **Source screenshot (credibility):** a real screenshot of the study or news page inside a white card with a fake browser bar showing the real URL.
  - Keep the site's logo/header in the crop (e.g. NIH + PubMed Central) and stack it over the title/citation crop (`ffmpeg ... vstack`).
  - Animate a highlighter (`scaleX` 0→1) over the title on the word that names the source.
  - Capture with headless Chrome at 2× (see lessons-learned). Never edit the page text; screenshots must be real.
- **Sponsored product hero:** cream/radial background, product cutout floating, benefit pills, brand logo, a discreet `#ad` pill for the whole product section.
- **CTA:** question + speech bubble + FOLLOW → FOLLOWING button; or the keyword in quotes with an arrow to the comments.

Search the registry first (`npx hyperframes catalog`) for anything new (charts, maps, counters, transitions) and adapt it to 1080×1920 inside the margins.

**Over the face** (talking head without b-roll): only small elements at the left or top. Never a card over the face.

## Motion

- **Punch-ins** (talking head): a hard zoom cut 1.0 → 1.10–1.22 on emphasis and on every jump cut, then a slow drift.
- **B-roll:** a slow push-in 1.02 → 1.12/1.14.
- **Pattern interrupt** (a "but here's the thing" moment): a quick flash or whip (white 2-frame flash or `x` shake), an SFX impact, a hard zoom, and a color flip of the caption.
- **Freeze-frame callback:** extract the frame (`ffmpeg -ss <t> -frames:v 1`), show it with a slow push-in, a thin accent frame and a tag.

## B-roll

| Source | How |
| --- | --- |
| **Mixkit** (free license, no credit required) | `https://mixkit.co/free-stock-video/<theme>/`. The ids are in `assets.mixkit.co/videos/<id>/<id>-360.mp4`; download `-720.mp4` (1080 returns 403). |
| **Pexels / Pixabay** (free licenses) | Use the official site or API and keep the URL of each clip in `broll-originals/SOURCES.md`. |
| **Official material** (trailers, press kits) | Official channel or site only. Use short excerpts in a commentary context, credit the source in the post caption, and never fan-made or AI footage presented as official. |

Workflow:
1. Make a contact sheet with one frame per candidate before choosing.
2. Cut each clip to the scene length with `-g 15`, cropped to 9:16 (`crop=ih*9/16:ih,scale=720:1280`).
3. On dark themes, show it darkened behind graphics (the `SCRIM`), never as the sharp main image. On the light theme, brighten it or frame it in a card.
