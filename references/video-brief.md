# Per-video brief

Ask before creating each project. Translate the options into the user's language, and put the user's current default first as "My default (…)" so one click keeps it.

Don't ask what the request already answers. "Make a light reel with karaoke captions" already answers look and captions: only ask what is missing, or skip straight to round 1's last question.

## Source material: inferred, asked only if ambiguous

| The user gave | `source` |
| --- | --- |
| a video of someone talking | `talking-head` |
| MP3/WAV narration files or a "voiceover" folder | `voiceover` |
| only a subject ("make a reel about X") | `topic` |
| an opening clip + a script to narrate | `hybrid` |

If it is unclear (e.g. a video **and** a script), ask one AskUserQuestion with these four options before round 1.

## Round 1: essentials (always, one AskUserQuestion with 4 questions)

```json
[
 {"header": "Captions", "question": "Captions for this video?", "multiSelect": false,
  "options": [
   {"label": "My default (word by word)", "description": "Keep the setup choice."},
   {"label": "Word by word", "description": "One big word at a time with a pop; keywords highlighted."},
   {"label": "Short phrases", "description": "2-3 words at a time."},
   {"label": "Karaoke", "description": "Phrase on screen, spoken word lights up."}]},
 {"header": "Look", "question": "Color look for this video?", "multiSelect": false,
  "options": [
   {"label": "My default (bold dark)", "description": "Keep the setup choice."},
   {"label": "Bold dark", "description": "Dark scrims, white headlines, yellow and red accents."},
   {"label": "Clean light", "description": "Cream and white cards, graphite text, green accent."},
   {"label": "Inspired by the topic", "description": "A palette taken from the subject (e.g. neon for games, brand colors of the company mentioned)."}]},
 {"header": "Length", "question": "Target length?", "multiSelect": false,
  "options": [
   {"label": "My default (45-60 s)", "description": "Keep the setup choice."},
   {"label": "Up to 30 s", "description": "One idea, fast. Best for reach."},
   {"label": "Up to 58 s (fits a Story)", "description": "Story-safe layout too."},
   {"label": "60-90 s", "description": "More depth; needs a strong hook and pace."}]},
 {"header": "Customize", "question": "Customize pace, b-roll, music and CTA too?", "multiSelect": false,
  "options": [
   {"label": "No, use my defaults (Recommended)", "description": "Start right away."},
   {"label": "Yes: style, pace, b-roll, music", "description": "One more round of 4 questions (edit style, pace, b-roll, music)."},
   {"label": "Yes, everything", "description": "Two more rounds (adds title, caption style, CTA, narration tone)."}]}
]
```

Note: "Other" is always available for free text (e.g. "neon pink and cyan", "exactly 40 s").

## Round 2: style, pace and content (only when asked to customize)

```json
[
 {"header": "Edit style", "question": "Which edit style (references/edit-styles.md)?", "multiSelect": false,
  "options": [
   {"label": "Auto (Recommended)", "description": "Picked from the topic and the material."},
   {"label": "Classic", "description": "Face + bold captions + title bar + b-roll cards."},
   {"label": "Editorial canvas", "description": "Cream infographic canvas on top, face below, camera travels along a storyboard."},
   {"label": "Product kinetic", "description": "Apple-like type, UI mockups, 3D icons, color flips. (Other: terminal-neon, cinematic-3d)"}]},
 {"header": "Pace", "question": "Editing pace?", "multiSelect": false,
  "options": [
   {"label": "Dynamic (Recommended)", "description": "New visual every 2-4 s, aggressive jump cuts, punch-ins."},
   {"label": "Calm", "description": "New visual every 4-6 s, light jump cuts, few zooms."},
   {"label": "Frantic", "description": "Cuts every 1.5-2.5 s, more SFX. Entertainment."},
   {"label": "Keep the raw rhythm", "description": "No jump cuts, no punch-ins."}]},
 {"header": "B-roll", "question": "What footage goes over the narration?", "multiSelect": false,
  "options": [
   {"label": "Free stock (Recommended)", "description": "Mixkit/Pexels clips matched to each sentence."},
   {"label": "Official material", "description": "Trailers, press kits and sites of the companies mentioned (short commentary excerpts, credited)."},
   {"label": "Motion graphics only", "description": "Animated scenes, logos, cards, no footage."},
   {"label": "None", "description": "Only the speaker plus titles."}]},
 {"header": "Music", "question": "Background music?", "multiSelect": false,
  "options": [
   {"label": "Tech / electronic (Recommended)", "description": "Modern, light, low under the voice."},
   {"label": "Cinematic / synthwave", "description": "Epic or 80s retro (games, pop culture)."},
   {"label": "Lo-fi / corporate", "description": "Soft, for advice and education."},
   {"label": "No music", "description": "Only voice and subtle SFX."}]},
]
```

**B-roll layout** is not asked by default (it uses `brollLayout` from the config, `mix`). If the user mentions it ("only full screen", "more split screen"), set `brollLayout` to `full`, `split` or `mix` in `brief.json`.

## Round 3: finishing (only with "Yes, everything")

```json
[
 {"header": "Title bar", "question": "Fixed title at the top?", "multiSelect": false,
  "options": [
   {"label": "Whole video (Recommended)", "description": "Headline always visible; doubles as the cover."},
   {"label": "Only during the hook", "description": "First ~6 s, then the screen is clean."},
   {"label": "No title", "description": "Good when the speaker's head is high in the frame."}]},
 {"header": "Caption look", "question": "Caption look and position?", "multiSelect": false,
  "options": [
   {"label": "Outline, low (Recommended)", "description": "White text with a dark outline, above the app buttons."},
   {"label": "Pill, low", "description": "Text on a white rounded card; keyword on an accent pill."},
   {"label": "Outline, middle", "description": "Center of the screen; more presence."},
   {"label": "Pill, middle", "description": "Card captions in the center."}]},
 {"header": "CTA", "question": "How should the video end?", "multiSelect": false,
  "options": [
   {"label": "My default (yes/no question)", "description": "Keep the setup choice."},
   {"label": "Comment a keyword", "description": "\"Comment WORD and I'll DM you…\" (I'll ask for the word)."},
   {"label": "Follow for more", "description": "Follow @handle."},
   {"label": "Link in bio", "description": "Points to the bio."}]},
 {"header": "Tone", "question": "Narration tone (cloned voice)?", "multiSelect": false,
  "options": [
   {"label": "Friendly chat (Recommended)", "description": "Animated, like talking to a friend; never sounds read."},
   {"label": "Journalistic", "description": "Firm and clear, but not a news anchor."},
   {"label": "Didactic", "description": "Calm, step by step."},
   {"label": "Hype", "description": "High energy, for launches and entertainment."}]}
]
```

Ask the **Tone** question only for `voiceover`, `topic` or `hybrid` with TTS. For a talking head, replace it with **Deliverables**:
- MP4 + phone copy + caption (Recommended)
- + designed cover
- MP4 only

**Sponsorship** is no longer a multiple-choice question. Ask it as a follow-up only when the request or the material suggests a paid partnership (a brand, a product, "publi", "#ad"). Then set `"sponsored"` in `brief.json`.

## Follow-ups (free text, only when needed)

- **Comment-keyword CTA:** the word, and what gets sent by DM (remind the user to set up the automation).
- **Sponsored:** brand name, product, official site for the logo and product photo, and the offer or coupon.
- **Official material:** which trailers or pages to use, if the user has a preference.
- **Topic:** the angle or opinion of the creator, if not obvious.

## brief.json

Write the answers here, then run `new_project.py --brief brief.json`. Missing keys fall back to `config.defaults`.

```json
{
  "source": "hybrid",
  "editStyle": "cinematic-3d",
  "language": "pt-BR",
  "theme": "neon-retro",
  "palette": {},
  "brandBase": "bold-dark",
  "captions": {"mode": "word", "style": "outline", "position": "low", "uppercase": true},
  "titleBar": "hook",
  "duration": "45-60",
  "pace": "dynamic",
  "jumpCuts": "aggressive",
  "punchIns": true,
  "broll": "official",
  "brollLayout": "mix",
  "logos": true,
  "music": {"enabled": true, "style": "synthwave", "volume": 0.18},
  "sfx": "subtle",
  "narrationTone": "friendly",
  "cta": {"type": "question", "keyword": ""},
  "sponsored": null,
  "deliverables": ["mp4", "phone-copy", "cover", "post-caption"]
}
```

`sponsored` when yes: `{"brand": "...", "product": "...", "site": "...", "offer": "..."}`.
