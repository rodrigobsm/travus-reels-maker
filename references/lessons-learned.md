# Pitfalls already solved

Add a row whenever you solve a new one.

## Render, check and layout

| Symptom | Cause | Fix |
| --- | --- | --- |
| Render dies midway ("Streaming encoder exited... unknown encoder failure") | HDR a-roll (HLG/bt2020) makes the render try HDR | convert the a-roll to SDR bt709 with tonemap (command in SKILL.md §4) and render with `--sdr` |
| Logos or cards cut at the sides on Instagram | Instagram full-screen zoom crops ~97 px per side | 130 px side margin on everything readable |
| League Gothic / Montserrat show as a generic font | built-in fonts didn't resolve by name | woff2 in `assets/fonts` + `@font-face` in `index.html` (already in the template) |
| Two caption words at once | a minimum duration pushed a word's end past the next start | end = `min(next start, end + 0.3)`; minimum only on the last word (already in the script) |
| Captions show "EISSO", "EAGORA" (Portuguese) | whisper glues the leading "E" | `build-captions.cjs` splits it; if it splits a real word starting with E, add it to the exception list |
| `transcribe` fails with `ECONNRESET` | model download | run it again |
| `transcribe` output not in `assets/` | the JSON is written next to the input file | move it to `assets/transcript.json` |
| Whisper changes product names, sometimes a whole phrase | generic model | fix `transcript.json` using the user's script (keep `transcript.raw.json`) |
| Mixkit 1080 download is an invalid file (403) | only 720 is public | use `-720.mp4`, shown darkened behind graphics |
| `check`: `text_occluded` by the scrim, the title shade or split-flap faces | intentional overlap | `data-layout-allow-occlusion` on the background element |
| `check`: `gsap_fullscreen_overlay_starts_visible` | an animated element is born visible | `opacity: 0` in the element's CSS |
| `check`: `content_overlap` / `text_occluded` on a state swap (FOLLOW→FOLLOWING, app→home screen) | layers overlap on purpose | `data-layout-allow-overlap data-layout-allow-occlusion` on both layers |
| `check` error `gsap_non_transform_motion` (letterSpacing) | tweening `letterSpacing` reflows text | animate only `scale` / `x` / `opacity` |
| `check` warning `svg_round_cap_hidden_dash` | a round-cap stroke hidden by `dasharray 1` leaves a dot | `stroke-dasharray="1 1.2" stroke-dashoffset="1.1"` |
| `check` warning `duplicate_audio_track` | two `<audio>` overlap on the same `data-track-index` | separate whoosh / impact / pops into their own tracks (6, 7, 8/9) |
| Red text fails the contrast check on dark backgrounds | `#ff2d3a` on thin text | `alertText` (`#ff5661`) for text; `alert` only for backgrounds and tags |
| Scene text lines get a weird background or height, and content disappears (a giant white panel, misplaced pills) | `clip()` uses the class `P-row`, which becomes `<scene>-row`; a scene class named `.<scene>-row` collides with it | **never name a class `-row`** in a scene; use `-item` or `-line` |
| A card class without `font-size` rendered tiny (16 px) | a new card class had no default size | always set `font-size` on new classes (`.P-card` has 58 px) |
| `reel_scenes.py`: `ModuleNotFoundError: brotli` | reading woff2 | `python -m pip install fonttools brotli` |

## Shell, ffmpeg and files

| Symptom | Cause | Fix |
| --- | --- | --- |
| A Python heredoc in bash breaks on quotes | JS quotes inside Python | write the `.py` to a file and run it |
| ffmpeg inside `while read` eats the rest of the list (file names cut: `ople.mp4`) | ffmpeg reads stdin | `ffmpeg -nostdin ...` |
| Concat with `afade` fails on the last segment | a trailing-silence segment came out negative or too short | clamp segment ends to the duration and drop segments < 0.1 s |
| File doesn't reach the phone | 30 MB limit on remote transfer | HEVC phone copy (command in SKILL.md §3.11) |

## Editing decisions

| Symptom | Cause | Fix |
| --- | --- | --- |
| A "stumble" cut removed a word that was really said | whisper duplicated a phrase in the transcript of the raw video | before cutting a repetition, transcribe only the ±3 s window of the original; after cutting, transcribe the whole cut video again |
| Jump cuts found from word gaps barely cut anything | whisper stretches word ends into pauses | detect pauses with `silencedetect` (−32 dB, 0.38 s) and leave 0.1 s of breath |
| Voiceover folder with two files of the same block | repeated takes | transcribe everything, use one take, say which |
| Narration "sounds read" | one tone tag per segment | one descriptive tone tag per **sentence** + spoken connectors (see scriptwriting.md) |
| All reels start the same way | habit opener ("So…", "Guys…") | `rules.bannedOpeners` + vary the hook structure |

## Publishing (GHL)

| Symptom | Cause | Fix |
| --- | --- | --- |
| "Publish now" got scheduled hours later | `TZ=America/New_York date` in Git Bash returns UTC without converting | compute times only in `publish_ghl.py` (zoneinfo); "now" = `--when now` |
| Duplicated posts on Instagram and TikTok | a PUT on `scheduleDate` published the per-network posts while the parent stayed "scheduled"; then it was deleted and recreated | never PUT the time and never recreate without listing the day's posts; the real status is in the per-network posts |
| `"Schedule Date must be after current date"` | GHL refuses schedules ~2 min ahead | immediate publishing is `status: "published"` without `scheduleDate` |
| Creating with `status: published` returns only `{"message": "Created Post"}` | no `results.post` in the response | it is success; follow the per-network posts in `/posts/list` |
| The cover disappears from `media[0].thumbnail` | GHL stores it in the post's `thumbnail` | normal; a PUT with a top-level `thumbnail` returns 422, so check the preview in the Social Planner |
| `ZoneInfoNotFoundError` | Python without time-zone data (Windows) | `python -m pip install tzdata` |

## Notes

- `.hyperframes/` keeps the project history and snapshots: don't delete it.
- `check` "craft" warnings about texts that stay on screen briefly, and about split-flap transition glyphs, are expected in this style.
- When the face fills the whole frame, the caption falls on the chin. That is the best compromise: higher covers the mouth, lower goes into the app UI. Consider the `middle` position or `pill` style.
- Logo resolve with "company + product" can return the parent company's logo (e.g. xAI instead of Grok): ask for the product name alone and look at the SVG.
