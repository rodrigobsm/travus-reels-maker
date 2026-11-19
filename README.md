# Travus Reels Maker

*[Leia em português](README.pt-BR.md)*

A **Claude Code skill** that turns a talking-head video, a voiceover, an AI-avatar opening or just a topic into a finished, professionally edited **vertical reel** (Instagram Reels, TikTok, YouTube Shorts, Facebook Reels), and can schedule it for you.

It is built on [HyperFrames](https://hyperframes.heygen.com) (HTML + GSAP rendered to video), so every caption, title and motion graphic is real animation, not an ffmpeg overlay.

## What it does

- **4 starting points:**
  - raw talking head (jump cuts + punch-ins);
  - voiceover MP3s (motion graphics over b-roll);
  - a **topic**: research → hook-driven script → narration in **your cloned voice** (Fish Audio or ElevenLabs);
  - **hybrid**: an opening clip (e.g. an AI avatar) followed by narration.
- **Animated captions:** word by word, short phrases or karaoke, with an outline or pill style and keyword highlights, placed inside the platform safe zones.
- **3 looks + your brand:** bold-dark, clean-light, neon-retro, or your colors on a dark or light base.
- **Fixed title and hook**, official logos, b-roll synced to each sentence, ready-made scene patterns (company cards, comparisons, checklists, sponsored product hero, CTA).
- **Sound:** royalty-free background music (picked by measuring how much it competes with the voice), ducking, subtle SFX, and loudness at −14 LUFS.
- **Deliverables:** max-quality MP4, a < 30 MB phone copy, a cover, and a post caption (hashtag limit, sources, AI and #ad disclosure).
- **Optional publishing:** one-shot scheduling to Instagram, Facebook, TikTok and YouTube Shorts through the GoHighLevel Social Planner. It always asks you the date and time first.
- **Honest by design:** it verifies claims with sources, never invents numbers or quotes, and credits third-party material.

## How it talks to you

**First run: setup** (~2 minutes, once). Multiple-choice questions for language, default look, caption style and voice provider, then publishing, time zone, default CTA and where to stop for approval. Plus one short message with your @handle, niche, projects folder and the words your reels must never start with. API keys are stored in your OS keychain, never in plain text.

**Every video: a short brief.**

| Round | When | Questions |
| --- | --- | --- |
| 1 | always | captions · look · length · customize more? |
| 2 | if you want | pace and jump cuts · b-roll source · music style · CTA |
| 3 | if you want everything | title bar · caption look and position · sponsored? · narration tone (or deliverables) |

Every question has a "my default" option, and anything your request already says is skipped.

## Install

**Requirements:**
- Node.js 18+
- FFmpeg on your PATH
- Python 3.9+, plus `python -m pip install fonttools brotli keyring tzdata`
- an AI agent that can **run commands on your computer** (see the compatibility table below)

### Option 1: Claude Code plugin (recommended)

Inside Claude Code:

```
/plugin marketplace add rodrigobsm/travus-reels-maker
/plugin install travus-reels-maker@travus
```

Or from a terminal:

```bash
claude plugin marketplace add rodrigobsm/travus-reels-maker
claude plugin install travus-reels-maker@travus
```

### Option 2: Manual (Claude Code skill folder)

```bash
git clone https://github.com/rodrigobsm/travus-reels-maker ~/.claude/skills/travus-reels-maker
```

On Windows, the folder is `%USERPROFILE%\.claude\skills\travus-reels-maker`. This works in the Claude Code CLI, the IDE extensions and the Code tab of the Claude desktop app.

### Option 3: Other agents (untested)

`SKILL.md` follows the open Agent Skills format, so agents that load skills may run it. Clone the repo into your agent's skills folder and check its docs for the exact location. Examples: OpenAI Codex CLI, Cursor, GitHub Copilot.

Differences outside Claude Code:
- The multiple-choice questions arrive as a numbered list (answer like `1a 2c 3b`).
- You may need to install the HyperFrames skills yourself.

### After installing

Run `python <skill folder>/scripts/doctor.py`. In Claude Code, the HyperFrames skills (`hyperframes`, `hyperframes-cli`, `media-use`) are offered by `npx hyperframes init` the first time.

### Compatibility

| Tool | Status |
| --- | --- |
| Claude Code (CLI, IDE, desktop Code tab) | ✅ built and tested here |
| Codex CLI, Cursor, Copilot and other local agents with skills | ⚠️ should work, untested |
| ChatGPT, Gemini or Claude **in the browser** | ❌ no: they can't run FFmpeg, Node or the renderer on your machine |

## Use

Just ask Claude Code:

- "Edit the reel in `~/Videos/raw.mov`"
- "Make a 45-second reel about the new iPhone, light theme"
- "Here are my voiceover files in `./voiceover`, make the reel"
- "Use `opening.mp4` as the opening and narrate this script with my voice"
- "Write the post caption" / "Schedule it on my 4 networks"

## Optional providers

| Provider | For | Secret | Config |
| --- | --- | --- | --- |
| Fish Audio | cloned-voice narration (s2.1-pro, free-form emotion tags) | `fish_api_key` | `voice.voiceId` |
| ElevenLabs | cloned-voice narration (eleven_v3 audio tags) | `elevenlabs_api_key` | `voice.voiceId` |
| GoHighLevel Social Planner | scheduling IG, FB, TikTok, YouTube Shorts | `ghl_token` | `publish.ghl.locationId`, `publish.ghl.userId` |

Store secrets in your own terminal: `python scripts/secrets_store.py set fish_api_key`, then paste the key. To add another TTS or scheduler, add a provider to `scripts/tts.py` or a `scripts/publish_<name>.py`.

## Repository layout

```
.claude-plugin/              plugin.json + marketplace.json (Claude Code plugin install)
SKILL.md                     the workflow the agent follows
references/
  setup.md                   first-run questions + config mapping
  video-brief.md             per-video questions + brief.json
  styles.md                  themes, captions, typography, scenes, b-roll
  audio.md                   voice normalization, music selection, ducking, SFX
  scriptwriting.md           research, proven hooks, voice-script tags
  publishing.md              post caption, AI/#ad disclosure, GHL scheduling
  creator.example.md         template for your private ~/.travus-reels/creator.md (personal rules)
  lessons-learned.md         pitfalls already solved (render, layout, whisper, GHL)
  examples/                  real scene scripts and index files (talking head, voiceover, light sponsored)
scripts/
  config.py  secrets_store.py  doctor.py  new_project.py  tts.py  publish_ghl.py
assets/template/             HyperFrames project template (index, title, hook, captions builder,
                             scene library, palettes, OFL fonts)
```

Your config lives in `~/.travus-reels/config.json` (override with `TRAVUS_REELS_HOME`). Nothing personal is stored in the repo.

## Credits and licenses

- Code and docs: [MIT](LICENSE).
- Fonts (League Gothic, Montserrat, JetBrains Mono): SIL Open Font License 1.1, see `assets/template/assets/fonts/OFL.txt`.
- [HyperFrames](https://hyperframes.heygen.com) is a separate project with its own license.
- Stock media is downloaded per project from its source (e.g. Mixkit) under that source's license. None is redistributed here.
- You are responsible for the rights to any third-party material you put in your videos.
