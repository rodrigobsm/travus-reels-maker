# Script (for approval) and voice script (cloned voice)

## 1. Research

- Research the topic on the web, with fresh results for news: what it is, what changed, numbers, prices, dates, and the official sources.
- Note each fact with its source. Prefer original statements (interviews, earnings calls, official posts) and recognized outlets.
- A fact you can't confirm stays out. A fact in flux (plan, price, free preview, release date) goes in with a caveat.
- Distinguish nuances the audience could get wrong (e.g. "no generative AI in the game world" ≠ "no AI anywhere in the company").
- If the user gave a script, verify it and apply only the **minimal** factual correction, keeping their narrative and opinion. Tell them what you changed and why.

## 2. Structure (45–65 s, about 130–160 words)

Split it into numbered files, one per block.

| Block | Time | Purpose |
| --- | --- | --- |
| 01 Hook | 0–5 s | promise or tension in the first sentence; no "hi everyone" |
| 02 Reveal | 5–15 s | what it is, in plain words, with the product or company name |
| 03 Wow factor | 15–28 s | the surprising detail, shown as a concrete scene |
| 04 Proof / comparison | 28–43 s | numbers, competitors, before × after, source |
| 05 Opinion | 43–55 s | the creator's view in one strong sentence |
| 06 Close + CTA | 55–65 s | honest caveat + question to comment + follow |

For shorter targets, merge blocks: ≤ 30 s = hook, reveal, wow, CTA.

Rules:
- One idea per sentence, 6–14 words each. Write as people speak.
- A turn every 3–5 s ("but", "and here's the interesting part", "except").
- One impact word per sentence: it becomes a tag on screen and a highlighted caption word.
- The CTA asks for one specific thing: a yes/no question, or "comment X", plus "follow".
- **Never start with a word from `rules.bannedOpeners`.** Vary the opening from one reel to the next: the first word is already the hook (the fact, the number, the question or the name).

## 3. Proven hooks (pick 1, offer 2 alternatives)

- **Hidden gain:** "<Company> is giving away FOR FREE what competitors charge for."
- **Nobody talks about it:** "Almost nobody is talking about this, and they should."
- **Contrast:** "Everyone is using <X> wrong."
- **Number + consequence:** "<N> <things> that <result> in <time>."
- **Tense question:** "Would you let an AI <risky action> on its own?"
- **News + personal impact:** "<Company> just launched <X>, and it changes <everyday thing>."
- **Warning:** "Stop <common habit> now."
- **Visual proof:** "Look what this AI did in <time>."
- **Irony / reveal:** "The most anticipated <thing> of the decade was made without <expected thing>, and that wasn't by chance."

The hook must work without sound: it becomes the fixed title (up to 4 words) and the first screen.

## 4. What to show for approval (when `rules.approveScript` is on)

Show it in the chat and save `script.md` in the project folder:
- 3 hook options, with the recommended one marked;
- the text of each block with its estimated time (~2.6 words per second);
- the fixed title and the text of the main scenes;
- the sources.

**Don't generate the voice before approval.**

## 5. Voice script (`voice_script.json`)

After approval, write the approved text with tone tags. Don't change the approved words, except for spoken-style contractions the creator uses.

```json
{"speed": 1.08, "temperature": 0.85,
 "segments": [
  {"file": "01 Hook", "text": "[excited, energetic, smiling while talking to a friend] Meta is giving away [emphasis] FOR FREE something competitors charge a fortune for! [surprised, amused] And almost nobody is talking about it."},
  {"file": "05 Opinion", "text": "[warm, sincere, confident] And honestly? [passionate, determined] I think they nailed it."}
 ]}
```

**What makes it sound like talking, not reading** (validated in production):
- **One tone instruction at the start of EVERY sentence**, in English and descriptive:
  - `[excited, energetic, smiling while talking to a friend]`
  - `[surprised, amused]`
  - `[playful, rhetorical question]`
  - `[emphasis, confident]`
  - `[amused, laughing]`
  - `[warm, upbeat, reassuring friend]`

  A single tag per segment sounded read.
- **Spoken-style text:** "Look…", "Now, here's the lie:", "…relax, OK?", rhetorical questions, and exclamations on impact sentences.
- **Pacing:** `speed` 1.05–1.10 and `temperature` 0.85. `[break]` before a turn, `[long-break]` rarely; `...` also creates natural pauses.
- `[emphasis]` right before the impact word. `[chuckling]` only for humor, `[whispering]` for "the secret".
- **Vary the energy:**
  - hook: excited
  - reveal: curious or confident
  - wow: surprised
  - proof: confident
  - opinion: determined or sincere
  - caveat: calm
  - CTA: excited and friendly
- **Spell out** numbers and acronyms when the reading could go wrong ("twenty years", "GTA six", "A.I." vs "AI" depending on the language).

Tones by brief `narrationTone`:

| Tone | Tags to lean on |
| --- | --- |
| friendly | `talking to a friend`, `smiling`, `amused`, `playful` |
| journalistic | `clear, confident, serious but warm`; avoid "news anchor" |
| didactic | `calm, patient, step by step, encouraging` |
| hype | `very excited, high energy, fast` |

**Providers:**
- **Fish Audio drama-3 (recommended for expressive narration):** set `"model": "drama-3"` in the voice script. Free-text directions in [brackets] written like a brief to an actor (`[playful, leaning in like sharing a secret]`, `[small laugh]`, `[pause]`) plus scoped tags `<emphasis>`, `<stress>`, `<slow>`, `<fast>`, `<soft>`, `<whisper>`, `<forceful>` around single words. Generate the whole narration as **one take** for natural flow. It runs slow: use `speed` ~1.25 and few `[pause]`s. A misspelled model silently falls back to s2.1-pro.
- **Fish Audio (s2.1-pro):** free-form tags in [brackets].
- **ElevenLabs:** `eleven_v3` understands [audio tags]. With other models, `tts.py` strips the tags; use punctuation for emotion instead.

**Generate and check:**
```bash
python <skill>/scripts/tts.py generate voice_script.json "<project>/voiceover"
```
Transcribe the result and compare it with the script. Redo only a bad segment with `--only 03`. Keep versions in `voiceover/v1-…`, `v2-…`. If `rules.approveNarration` is on, send `narration-full.mp3` before editing.

If the user says it "sounds read": add more per-sentence tags and spoken-style connectors, and raise the energy. Don't just change the speed.
