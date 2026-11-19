---
name: travus-reels-maker
description: Creates and edits professional vertical reels (Instagram Reels, TikTok, YouTube Shorts, Facebook Reels) end to end with HyperFrames (HTML + GSAP rendered to video). Starts from a talking-head video, a voiceover MP3, an opening clip plus narration, or just a topic (research, hook-driven script, cloned-voice narration). Adds animated captions (word-by-word, phrase or karaoke), fixed title, hook, b-roll, official logos, motion-graphics scenes, royalty-free music and subtle sound effects, renders the MP4 plus a phone-sized copy, writes the post caption and can schedule it on social networks. Asks first-time setup questions and a short multiple-choice brief per video. Use it whenever someone wants to make, edit, caption, cut or "do the same as last time" for a reel, short, TikTok or any vertical video (raw .mp4/.mov, a folder of voiceover MP3s, or a topic), write the post caption for it, or schedule/publish it.
---

# Travus Reels Maker

Turns raw material (or just a topic) into a 1080×1920 reel that looks professionally edited, then writes the post caption and optionally schedules it. The heavy lifting is done by **HyperFrames**. This skill holds the workflow, the questions to ask, the styles, the project template and the pitfalls already solved.

Before writing any composition, load the HyperFrames skills: `hyperframes` (render contract), `hyperframes-cli` (commands) and `media-use` (logos, SFX, media). If they are not installed, run `npx hyperframes init` once and they are offered. They own the "how"; this skill owns the "what".

`<skill>` below means the folder of this file. Scripts run with `python <skill>/scripts/<name>.py`.

## 0. Talk in the user's language

Ask every question and write every message in the language the user writes in, or in `creator.language` from the config. The option texts in `references/*.md` are written in English: translate them when you ask.

**Asking multiple-choice questions.** The question sets in `references/setup.md` and `references/video-brief.md` are written as AskUserQuestion payloads (Claude Code).
- If your agent has an equivalent multiple-choice tool, use it with the same questions and options.
- If not, ask them in **one plain message as a numbered list**. Put the options under each question as letters (a, b, c, d), with the recommended one marked, and tell the user they can answer compactly ("1a 2c 3b 4a") or in their own words.
- Never split one round into several messages.

## 1. First run: setup

Run `python <skill>/scripts/config.py status`.

- `not-configured`: run the setup in **`references/setup.md`**. That is two rounds of multiple-choice questions plus one short free-text message. Store the answers with `config.py set`, have the user store the API keys with `secrets_store.py`, then run `python <skill>/scripts/doctor.py` and fix what is missing.
- `configured`: read `python <skill>/scripts/config.py show` and go on.

**Personal rules.** If `~/.travus-reels/creator.md` exists (or `$TRAVUS_REELS_HOME/creator.md`), read it before every reel and follow it. It holds the creator's own preferences and extra steps (e.g. logging each post in their content history). When it conflicts with this file, it wins, except for the safety rules in §9. The setup can create it from `references/creator.example.md`. Never copy it into a public repo.

If the user says "setup", "reconfigure" or "change my defaults", run the setup again with the current values as the recommended options.

## 2. Each video: the brief

Before creating a project, ask the per-video questions in **`references/video-brief.md`**:

1. **Round 1: essentials.** Captions, look, length, and whether to customize more. Every option list starts with "My default (…)".
2. **Rounds 2 and 3: advanced.** Ask these only if the user chose to customize more. They cover pace and cuts, b-roll, music, CTA, title bar, caption style and position, sponsorship and narration tone.

Skip any question the request already answers (e.g. "light theme, phrase captions"). Infer the **source material** from what was given (see the table below) and ask about it only if it is ambiguous.

Write the answers to `brief.json`, then create the project:

```bash
python <skill>/scripts/new_project.py --name "<Short-Topic-Name>" --brief brief.json
```

This creates `<projects>/<Name>/` with `reels-project/` (HyperFrames + template, already themed), `broll-originals/`, `music-candidates/`, `voiceover/` and the merged `brief.json`. If the user already has a folder with the material, pass `--root` to its parent and use the same name.

| Source | What the user gives | Pipeline |
| --- | --- | --- |
| `talking-head` | raw vertical video of someone speaking | §3 + §4 (a-roll, jump cuts, punch-ins) |
| `voiceover` | MP3 files (`01 Hook.mp3`, `02 …`) and/or a script | §3 + §5 (motion graphics over b-roll) |
| `topic` | only a subject | §6 (research → script → voice) and then §5 |
| `hybrid` | an opening clip (talking head or AI avatar) + a script for narration | §7 |

## 3. Common pipeline (all sources)

1. **Look at the material.** Run `ffprobe` (duration, resolution, fps, `color_transfer`). Extract 3–4 frames to see where the face, eyes and chin are: the title and chips must never cover the face.
2. **Transcribe.** Run `npx hyperframes transcribe <file> --engine whisper --model large-v3 --language <xx>`. The JSON is written **next to the input file**: move it to `assets/transcript.json`. If you get `ECONNRESET`, run it again.
   - Read the whole transcript: it is the script.
   - Fix brand and product names in the JSON before building captions, and keep the original as `transcript.raw.json`. Whisper mangles names, so use the user's script as the reference.
3. **Plan the beats** on the transcript timings:
   - hook (0 to ~6 s);
   - one scene per topic or company mentioned;
   - clean face shots between blocks (talking head only);
   - a list or checklist if there is advice;
   - the CTA at the end.

   Bring new visual information every 2–4 s (`calm` pace: 4–6 s; `frantic`: 1.5–2.5 s). B-roll and scenes enter and leave on sentence cuts.
4. **Media.**
   - **Logos:** `npx hyperframes media-use resolve --type logo --intent "<company>" --project .`, or `--from <url>`. Check that you got the product's logo and not the parent company's, and never redraw a logo.
   - **B-roll:** see `references/styles.md` → "B-roll" (stock sources, official material, licensing).
   - **Music and SFX:** see `references/audio.md`.
5. **Captions.** Put `duration` and `keywords` (the impact words, one per sentence) into `reel.config.json` and run `node scripts/build-captions.cjs`. The modes and styles come from the brief. In Portuguese, check the "isolated E" count the script reports.
6. **Title and hook.**
   - Edit `compositions/title.html`: up to 4 words that promise the content, with a number if there is one, plus a tag that changes when the topic turns.
   - Edit `compositions/hook.html`: logo chips, or replace it with a scene.
   - With `titleBar: hook`, set `__TITLE_DUR__` to the hook length. With `none`, the title was already removed from the index.
7. **Scenes.** Write `scripts/build-scenes.py` with `from reel_scenes import *` and run it (needs `pip install fonttools brotli`).
   - Use the palette through `C["ink"]`, `C["accent"]`… so the scenes follow the theme.
   - Read an example first: `references/examples/build-scenes-talking-head.py`, `build-scenes-voiceover.py` or `build-scenes-light-sponsored.py`.
   - Register every scene, b-roll and audio in `index.html`, as in `references/examples/index-*.html`.
8. **Check and look.** Run `npx hyperframes check --json` until there are no errors. Then run `npx hyperframes snapshot --at <middle of each scene> --no-end -o snaps` and read the contact sheets. Look for:
   - anything outside the 130 px side margins;
   - text on the face, or text touching other text;
   - two captions at once;
   - a scene without a background.
9. **Preview** (optional): `npx hyperframes preview` opens the Studio so the user can tweak things.
10. **Render.** Run `npx hyperframes render --quality delivery --sdr --output "../<Name>-final.mp4"`.
    - Confirm the duration with `ffprobe`.
    - Measure loudness with `ffmpeg -i <mp4> -af ebur128 -f null -`; the target is about −14 LUFS.
    - Extract a few frames from the MP4 to check.
11. **Phone copy** (if `phone-copy` is in the deliverables; sized for the 30 MB limit of most phone transfer and DM flows):
    ```bash
    ffmpeg -y -i <Name>-final.mp4 -c:v libx265 -preset medium -b:v 3200k -maxrate 4500k -bufsize 9000k -tag:v hvc1 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart <Name>-final-phone.mp4
    ```
    For long videos, use `-b:v` = (MB limit × 8 ÷ duration) − 160 kbps, with a margin. Explain that both files are the same video.
12. **Cover:** frame 0 already has the title. If the brief asks for a designed cover, make `cover.png` (1080×1920) with HyperFrames. Keep the main text inside the center 1080×1350 so it survives the 4:5 grid crop.
13. **Post caption → publishing:** see `references/publishing.md`. **Always ask the date and time before scheduling.**

## 4. Talking head specifics

- **SDR a-roll.** iPhone video is often HDR (HEVC HLG/bt2020) and breaks the render. Convert it to `assets/bruto.mp4`; the original is never modified:
  ```bash
  ffmpeg -i ../raw.mov -vf "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p" -c:v libx264 -crf 15 -g 30 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 192k assets/bruto.mp4
  ```
  If the source is already SDR, just re-encode it with `-g 30`.
- **Jump cuts** (brief `jumpCuts`):
  - Detect pauses with `silencedetect`: `-af silencedetect=n=-32dB:d=0.38` for `aggressive`, `d=0.7` for `light`. Cut them, leaving 0.1 s of breath, and normalize the voice to −14 LUFS (two-pass loudnorm, see `references/audio.md`).
  - Before cutting a repetition or a stumble, re-transcribe only that ±3 s window of the original. Whisper sometimes duplicates phrases that were never said twice.
  - After cutting, transcribe the cut video again so the caption timings are exact.
- **Punch-ins** (brief `punchIns`): a hard zoom cut (1.0 → 1.10–1.22) on emphasis sentences and on every jump cut, a slow drift inside each segment, and back to 1.0 on the next sentence. Use the `cuts` list in `index.html`.
- **Over the face** (no b-roll): only small elements on the left side or at the top. Never put a card over the face.

## 5. Voiceover-only specifics (no face)

- **Look for duplicate takes.** Transcribe all the files and compare them. Use one take per block (the most fluent or the most recent) and say which one you kept.
- **Join and normalize** with the concat demuxer and two-pass loudnorm (see `references/audio.md`) into `assets/audio/voz.wav`. In `index.html`, replace the a-roll block with the `<audio id="voz">` line. The root duration is the voice length plus ~0.5 s of breath at the CTA.
- **Continuous b-roll:** one clip per scene, switching on sentence cuts, with no gaps. Every scene starts with `SCRIM`.
  - Crop the b-roll to 9:16 already: `crop=ih*9/16:ih,scale=720:1280`, with `-g 15`.
  - Use `-nostdin` inside `while read` loops.
- Frame 0 must already show the title + logo or a strong phrase, with no fade from black.

## 6. From a topic (script and voice)

Follow **`references/scriptwriting.md`**:

1. Research the topic and verify every fact with a source.
2. Write the script with a proven hook and save `script.md`.
3. If `rules.approveScript` is on, **show it and stop for approval**.
4. Write `voice_script.json` with tone tags, then generate the voiceover:
   ```bash
   python <skill>/scripts/tts.py generate voice_script.json "<project>/voiceover"
   ```
5. Transcribe it and compare it with the script. Redo only a bad segment with `--only 03`.
6. If `rules.approveNarration` is on, join the segments into `narration-full.mp3` and **send it for listening before editing**. Keep each version in `voiceover/v1-…`, `v2-…`.
7. Continue with §5.

If `voice.provider` is `none`, deliver the script and ask the user to record it.

## 7. Hybrid: opening clip + narration

Used when the user brings an opening clip (a talking head or an AI avatar, e.g. from Veo or HeyGen) that speaks the hook, and the rest is narrated.

1. **Opening clip:**
   - keep its video and audio;
   - only trim the silences (silencedetect) and normalize it;
   - never replace its voice with TTS;
   - start directly on the hook, with no intro or bumper;
   - captions follow the brief.
2. **Narration:** generate the rest with `tts.py` (§6), **without repeating the hook** that is already in the clip.
3. **Match the two voices:**
   - two-pass loudnorm of both to −14 LUFS;
   - the same `highpass=f=70`;
   - a gentle `acompressor` on both;
   - no gap longer than 0.15 s at the seam.

   Listen to the seam in a 6 s excerpt rendered with ffmpeg and say in the report how it sounds.
4. **Callbacks:** if the script refers back to the opening ("this video you just watched…"), go back to the clip footage. A freeze frame with a slow push-in and a highlight tag works well.
5. **AI disclosure:** when the avatar or the voice is AI-generated, say so in the post caption and remind the user to switch on the platform's AI label (Instagram "AI info", TikTok "AI-generated content", YouTube "altered or synthetic content").

## 8. Safe zones (1080×1920)

| Zone | Value | Why |
| --- | --- | --- |
| Sides | **130 px each side** (content at x 130–950, 820 px wide) | In full screen, Instagram zooms on tall phones and crops ~97 px per side. |
| Top | nothing above y≈186 | Instagram/TikTok top bar (and the Story progress bar) |
| Title | y≈186–390 | above the speaker's head |
| Scene graphics | y≈430–1300 | |
| Captions | center at y=1436 (`low`), 1060 (`middle`) or 560 (`top`) | above the description and buttons; keep a ±100 px band free of scene text around the chosen position |

This applies to everything readable. Backgrounds, scrims and b-roll may bleed to the edges. `reel_scenes.py` measures centered texts with the real font and shrinks anything wider than 820 px. Elements you place by hand are your responsibility: use `left: 130px; width: 820px` as the maximum box. For a reel that must also fit a Story, keep it ≤ 58 s and keep text away from the top progress bar and the bottom reply bar.

## 9. Honesty, rights and safety

- **On-screen text repeats what is said.** Never invent numbers, dates, quotes or headlines, and never "improve" a claim. When research was requested, verify claims on the web and list the sources in the final report. If something said seems wrong or outdated, keep it faithful and flag it, or propose the minimal correction before recording.
- **Third-party material** (trailers, news footage, screenshots): use official or licensed sources, short excerpts in a commentary context, and credit the source. Never present fan-made or AI-generated footage as official.
- **Secrets:** never ask for an API key in plain text when the user can store it with `secrets_store.py` in their own terminal, and never print or log it.
- **Never publish or schedule** without an explicit request and without the date and time confirmed in this conversation.

## 10. Final report

Tell the user:
- where the MP4 and the phone copy are;
- what was checked (frames, loudness, `check`) and what was not (watching the whole video with sound);
- the caveats: 720p b-roll, HDR → SDR conversion, discarded takes, unverified claims, the cover to confirm;
- 3–5 short suggestions: cover, pinned comment, music volume, a keyword-automation reminder for comment CTAs.

Known technical pitfalls and their fixes are in `references/lessons-learned.md`. Add a row there whenever you solve a new one.

## 11. Other creators

To edit for someone other than the configured creator, read `~/.travus-reels/clients/<name>.md`. If it doesn't exist, study their profile (bio, covers, 2 recent reels: caption style, colors, CTA) and write that file, including a palette for `brief.json` → `palette`. Their videos use their style, not the default one.
