# First-run setup

Run this when `python <skill>/scripts/config.py status` prints `not-configured`, or when the user asks to reconfigure. It takes about 2 minutes. Translate everything into the user's language. When reconfiguring, mark the current value as "(current)" and recommend it.

Start with one sentence: what the skill does, and that you'll ask a few questions once so every future reel comes out in their style.

## Round 1: multiple choice (AskUserQuestion, 4 questions)

```json
[
 {"header": "Language", "question": "What language are your videos in (captions, narration and post copy)?", "multiSelect": false,
  "options": [
   {"label": "Português (Brasil)", "description": "pt-BR"},
   {"label": "English", "description": "en-US"},
   {"label": "Español", "description": "es"}]},
 {"header": "Look", "question": "Which default look should your reels have?", "multiSelect": false,
  "options": [
   {"label": "Bold dark (Recommended)", "description": "Near-black scrims, white League Gothic headlines, yellow highlights, red alert tags. Tech, news, business."},
   {"label": "Clean light", "description": "Cream background, white cards with soft shadows, graphite text, green accent. Health, lifestyle, education."},
   {"label": "Neon retro", "description": "Deep purple, hot pink and cyan, synthwave vibe. Games, pop culture, entertainment."},
   {"label": "My brand colors", "description": "You give me your colors and I build the palette on a dark or light base."}]},
 {"header": "Captions", "question": "Which caption style do you want by default?", "multiSelect": false,
  "options": [
   {"label": "Word by word (Recommended)", "description": "One big word at a time with a pop; keywords in the accent color. Highest retention."},
   {"label": "Short phrases", "description": "2-3 words at a time. Calmer, easier to read."},
   {"label": "Karaoke", "description": "The phrase stays on screen and the spoken word lights up."},
   {"label": "No captions", "description": "Only titles and graphics."}]},
 {"header": "Voice", "question": "For reels without your face (voiceover or topic only), who does the narration?", "multiSelect": false,
  "options": [
   {"label": "I record it myself", "description": "The skill writes the script; you send the audio."},
   {"label": "Fish Audio clone", "description": "Your cloned voice on fish.audio (needs an API key and the voice id)."},
   {"label": "ElevenLabs clone", "description": "Your cloned voice on ElevenLabs (needs an API key and the voice id)."}]}
]
```

Mapping:
- `creator.language`: pt-BR | en-US | es.
- `defaults.theme`: bold-dark | clean-light | neon-retro | brand.
- `defaults.captions.mode`: word | phrase | karaoke | none.
- `voice.provider`: none | fish | elevenlabs.

With **Clean light**, also set `defaults.captions.style` to `pill` (white pill captions read better on light footage).

## Free text: one message

Ask for these in a single message, so the user answers in one go:

1. **Name or @handle** (used in the CTA "follow @…" and in the post caption).
2. **Niche and audience** in one line (e.g. "AI for small businesses, Brazilians in the US").
3. **Projects folder.** Suggest `~/Reels` (Windows: `C:\Users\<user>\Reels`) and accept their own.
4. **How you talk** (optional): "friendly and direct", "technical but simple"…
5. **Words a reel must never start with** (optional), e.g. their filler words ("So", "Guys", "Hey").
6. If they chose **My brand colors**: the primary and accent colors (hex or a brand link) and a dark or light base.

Mapping:
- `creator.handle`, `creator.niche`, `creator.audience`, `paths.projects`, `creator.voiceStyle`, `rules.bannedOpeners` (JSON list).
- Brand colors: `defaults.palette` (`{"accent": "#..", "alert": "#.."}`) and `defaults.brandBase` (bold-dark | clean-light).

## Round 2: multiple choice (AskUserQuestion, 4 questions)

```json
[
 {"header": "Publishing", "question": "How do you want to publish the finished reels?", "multiSelect": false,
  "options": [
   {"label": "I post them myself (Recommended)", "description": "You get the MP4, the cover and the post caption ready to paste."},
   {"label": "GoHighLevel Social Planner", "description": "The skill schedules Instagram, Facebook, TikTok and YouTube Shorts in one post (needs a GHL token and location id). It always asks you the date and time first."}]},
 {"header": "Time zone", "question": "Which time zone should scheduling use?", "multiSelect": false,
  "options": [
   {"label": "America/New_York", "description": "US Eastern"},
   {"label": "America/Sao_Paulo", "description": "Brasília"},
   {"label": "Europe/Lisbon", "description": "Portugal"},
   {"label": "America/Los_Angeles", "description": "US Pacific"}]},
 {"header": "CTA", "question": "What should your reels usually ask for at the end?", "multiSelect": false,
  "options": [
   {"label": "A yes/no question (Recommended)", "description": "Drives comments: \"Do you agree?\""},
   {"label": "Comment a keyword", "description": "\"Comment GUIDE and I'll DM you the link\" (for keyword DM automations)."},
   {"label": "Follow me", "description": "\"Follow @you for more\""},
   {"label": "Link in bio", "description": "\"Link in bio\""}]},
 {"header": "Approvals", "question": "Where should the skill stop for your approval?", "multiSelect": false,
  "options": [
   {"label": "Script and narration (Recommended)", "description": "Approve the script, then listen to the narration before the edit. Avoids rework."},
   {"label": "Script only", "description": "Approve the script; everything else runs to the final video."},
   {"label": "Fully autonomous", "description": "Only the final MP4 for approval (publishing still always asks)."}]}
]
```

Mapping:
- `publish.provider`: manual | ghl.
- `publish.timezone`: any IANA name; "Other" is free text.
- `defaults.cta.type`: question | comment-keyword | follow | link-in-bio.
- `rules.approveScript` and `rules.approveNarration` (true/false).

## Secrets: never in plain text

For each provider chosen, tell the user to run this **in their own terminal** and paste the key when it waits for input:

```bash
python <skill>/scripts/secrets_store.py set fish_api_key        # Fish Audio: https://fish.audio/app/api-keys
python <skill>/scripts/secrets_store.py set elevenlabs_api_key  # ElevenLabs: profile → API keys
python <skill>/scripts/secrets_store.py set ghl_token           # GHL: Private Integration token with social-planner scopes
```

The key goes to the OS keychain (`keyring`), or to a DPAPI-encrypted file on Windows. If the user pastes a key in the chat anyway, store it the same way (pipe it on stdin), never echo it back, and suggest rotating it later because the chat now contains it.

Ids are not secrets; save them in the config:

```bash
python <skill>/scripts/config.py set voice.voiceId "<voice id>"
python <skill>/scripts/config.py set publish.ghl.locationId "<location id>"
python <skill>/scripts/config.py set publish.ghl.userId "<user id>"
```

Then confirm the voice: run `python <skill>/scripts/tts.py check`. With Fish Audio, recommend making the cloned voice **private** if it shows as public.

## Save and verify

1. Save every answer with `python <skill>/scripts/config.py set <key> <value>`; values are parsed as JSON (`true`, `0.2`, `["So","Guys"]`).
2. Run `python <skill>/scripts/config.py set setupDone true`.
3. Run `python <skill>/scripts/doctor.py` and help the user install whatever is `MISSING`: Node 18+, FFmpeg, `pip install fonttools brotli keyring tzdata`.
4. Show a short summary of the saved profile, and tell the user they can change it any time by saying "reconfigure".
