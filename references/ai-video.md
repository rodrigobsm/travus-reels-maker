# AI video (avatar shots, b-roll) and AI images (covers, b-roll) with the Gemini API

Use this when the creator has a Gemini API key (`python <skill>/scripts/secrets_store.py check gemini_api_key`). Without a key, skip it: the user records the talking head or brings the clip, and covers are made with HyperFrames.

## Facts to know (checked 2026-11-19)

- **Video model:** `gemini-omni-1.2-flash` (config `gemini.videoModel`), via the Interactions API.
  - 3–15 s per shot, 9:16 or 16:9, 720p native (1080p and 4K upscaled), 24 fps, MP4 with native audio.
  - About US$ 0.07/s at 720p and 0.10/s at 1080p.
  - The **Veo 3.1 API was shut down on 2026-10-22**; `predictLongRunning` calls fail.
- **Avatars:** the API has **no "saved avatar" or @handle**. An avatar made in the Gemini app (e.g. `@name`) cannot be called by name. Consistency comes from **reference images**: up to 3 per character, 2 characters per shot, sent with every request.
  - Keep 1–3 images of the avatar in `avatar.refsDir` (default `~/.travus-reels/avatar/`): a sharp frontal face, the usual framing, the outfit.
  - The best source is a frame from a video of that avatar the user already likes. `ffmpeg -ss <t> -i clip.mp4 -frames:v 1 ref1.png`, using 2–3 different moments.
  - Uploads of certain recognizable public figures are refused; the creator's own likeness is fine.
- **Voice:** the model speaks with a voice it generates from the prompt, **not** the creator's cloned voice. Two modes (config `avatar.voice`):
  - `fish` (default when a cloned voice exists): generate the avatar shot **with the dialogue in the prompt** so the lips move with the words. Then replace the audio with the cloned voice saying the same line (`tts.py`), time-stretched to the shot length (`atempo`). Tell the user that lip-sync is approximate.
  - `model`: keep the model's voice. Describe it in the prompt (gender, age, accent, energy) and use the same description in every shot so it stays consistent.
- **Paid tier required:** on the free tier, every image and video model has a quota of **0** (HTTP 429 "limit: 0 … on Free Tier"); text models still work. The user must enable billing for the API key's project in Google AI Studio. Until then, fall back to HyperFrames covers and user-supplied clips.
- **Images:** `gemini-nano-banana-2.1` (b-roll, fast, ~US$ 0.05 at 2K) and `gemini-3-pro-image` (**covers/thumbnails**, best text rendering, ~US$ 0.13).
  - Input images such as the creator's face cutout keep the person consistent. 9:16 at 2K.
  - Images carry a SynthID watermark.

## Commands

```bash
python <skill>/scripts/gemini.py check                                   # key + model ids + avatar refs
python <skill>/scripts/gemini.py video --prompt shot01.txt --out ai/shot01.mp4 --avatar --duration 8
python <skill>/scripts/gemini.py video --prompt broll03.txt --out ai/broll03.mp4 --duration 5      # no avatar
python <skill>/scripts/gemini.py image --prompt cover.txt --out cover.png --thumb --input face-cut.png
```

Each call writes `<out>.json` with the request (without image data) and the response metadata. Keep the prompt files in the project (`ai/prompts/`).

## Turning a script into avatar shots

1. Split the script into shots of **≤ 15 s of speech** (~35 words in Portuguese at a natural pace). Break at sentence ends: each shot = one idea.
2. For each shot, write the prompt with the template below. **Repeat the same character, wardrobe, setting and voice description word for word in every shot**: that is what keeps continuity.
3. Generate the hook shot first, show it, and then generate the rest. Never spend on all the shots before the user sees the first.
4. Join the shots with hard cuts or punch-ins (talking-head rules in SKILL.md §4), then the normal pipeline: transcribe → captions → scenes.

### Prompt template (avatar speaking)

```
Vertical 9:16 portrait video, medium close-up, eye-level camera, subtle handheld movement.
The man in the reference images (same face, hair, beard and black polo shirt) speaks directly to the camera,
friendly and energetic, natural hand gestures, confident smile.
Setting: Miami Ocean Drive at golden hour, palm trees, neon Art Deco buildings softly out of focus behind him.
Lighting: warm sunset key light from the left, pink and cyan neon rim light.
He says in Brazilian Portuguese, fast and natural, like talking to a friend:
"O jogo mais aguardado da última década teve seu mundo criado sem IA generativa. E isso não foi por acaso."
Audio: only his voice, clean and close to the microphone. No background music. No sound effects. No subtitles or on-screen text.
Do not change his face or clothes. No other people in frame.
```

Rules that matter:
- **Dialogue in double quotes**, with the language and the delivery: "in Brazilian Portuguese, fast and natural, like talking to a friend".
- **Audio line always present.** For the edit we want **no music and no SFX** from the model; those come from the skill. Silent b-roll: "No dialogue. No music. Ambient sound only." or "Silent." Pure visuals: "No audio".
- **No on-screen text** ("No subtitles or on-screen text"): captions and graphics come from HyperFrames.
- Camera, lens, lighting and mood in concrete words: "medium close-up", "35mm", "shallow depth of field", "golden hour", "neon rim light".
- Put negatives in the prompt as plain sentences; the API has no negative-prompt field.
- Keep the prompt under ~1,000 tokens.

### B-roll shots (no avatar)

Describe a single, concrete moment that illustrates the sentence:
```
Vertical 9:16, cinematic slow dolly-in. A developer's desk at night, two monitors with code, neon pink and cyan reflections, rain on the window.
Shallow depth of field, 35mm, moody. No people's faces. No text. No dialogue. No music. Ambient room tone only.
```
- Never generate fake "official" footage of real products, games or people (e.g. fake trailer shots). Use the official material for those.
- AI b-roll is for generic, illustrative moments.

## Covers / thumbnails (always with Gemini when the key exists)

1. Get a clean face image: the best frame of the talking head or avatar. Cut it out with `npx hyperframes remove-background frame.png -o face-cut.png`, or send the frame as-is.
2. Write `cover.txt` with the text in double quotes, the layout and the style, then run `gemini.py image --thumb --input face-cut.png [--input background.png]`.
3. Template:
```
Vertical 9:16 Instagram Reels cover, 1080x1920, bold and high-contrast.
Use the man from the input image (same face, do not alter his features), chest-up, centered, looking at the camera with a curious expression.
Background: neon Miami at night inspired by the input background image, pink and cyan glow, slight blur.
Headline at the top in huge condensed bold sans-serif, white with pink neon glow: "GTA VI SEM IA?"
Second line in a hot-pink rounded label under his chin: "POR QUE A ROCKSTAR DECIDIU ISSO?"
Keep all text and his face inside the central 4:5 area (the Instagram grid crop). Spell every word exactly as written, in Portuguese, with accents.
No logos, no watermark, no extra text.
```
4. Check the result: spelling (compare letter by letter), the face looks like the person, and the 4:5 crop (`crop=1080:1350:0:285`) keeps the title and face. Generate 2–3 variations and offer the best. If the text comes out wrong, regenerate. Last resort: generate without text and add the text with HyperFrames.
5. Save as `thumb.png`. Keep the HyperFrames cover as a fallback.

## Honesty and disclosure

- AI-generated avatar, voice or footage must be disclosed in the post caption and with the platform label (see publishing.md).
- Don't make the avatar say claims the creator didn't approve: the shot script follows the approved script.
