# Audio: voice, music, sound effects

## Voice normalization (two-pass loudnorm, target −14 LUFS, TP −1.5)

```bash
# join (voiceover files): list.txt has lines like  file 'C:/.../01 Hook.mp3'
ffmpeg -f concat -safe 0 -i list.txt -ar 48000 -ac 1 -c:a pcm_s16le assets/audio/raw.wav
# pass 1: measure
ffmpeg -i assets/audio/raw.wav -af "highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json" -f null - 2> loud.txt
# pass 2: apply with the measured_* values from the JSON block in loud.txt
ffmpeg -i assets/audio/raw.wav -af "highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=..:measured_TP=..:measured_LRA=..:measured_thresh=..:offset=..:linear=true" -ar 48000 -ac 2 assets/audio/voz.wav
```

Read the loudnorm JSON with Python by finding the `{...}` block that contains `"input_i"`. A `tail | json.load` breaks.

**Two different voices** (hybrid: avatar clip + cloned voice):
- normalize both the same way;
- add `acompressor=threshold=-20dB:ratio=3:attack=5:release=80` to both;
- keep the seam gap at ≤ 0.15 s.

If one sounds brighter, a gentle `equalizer=f=6000:t=q:w=1:g=-2` on that one usually matches them.

## Music (on by default unless the brief says no)

The source is **Mixkit** ("Mixkit Stock Music Free License": free, no credit required, allowed on Instagram, TikTok and YouTube). No source can promise zero automated claims, but Mixkit is one of the safest.

1. **List tracks:** `https://mixkit.co/free-stock-music/tag/<tag>/` or `https://mixkit.co/free-stock-music/<genre>/`.
   - The id is in `data-audio-player-item-id-value` and the title in the nearest `h2.item-grid-card__title`.
   - The MP3 is `https://assets.mixkit.co/music/<id>/<id>.mp3`.
   - Styles → where to look:
     - tech: `technology`, `electronic`
     - corporate: `corporate`
     - lo-fi: `lofi`, `chill`
     - cinematic: `cinematic`, `epic`
     - synthwave / 80s: `retro`, `synthwave`, `80s`
     - upbeat: `upbeat`, `pop`

     The tags change, so if a page is empty, search the site.
2. **Download 4–7 candidates** into `music-candidates/` and measure each one:
   - BPM, with onset autocorrelation in numpy;
   - loudness every 5 s (`ebur128`): no long intro and no drops in the stretch you'll use;
   - **energy in the voice band (300–3000 Hz):** lower is better, because it competes less with speech. A track at 31% beat one at 79%.
3. **Prepare** `assets/music/musica.wav`:
   - cut it to the video length;
   - `equalizer=f=2200:t=q:w=1.2:g=-3`;
   - fade-in 0.15 s and fade-out 1.4 s at the end;
   - two-pass loudnorm to −14 LUFS.
4. **Ducking:**
   - **Simple:** `data-volume="0.2"` puts the music ~14 dB under the voice.
   - **Better:** pre-duck it against the voice:
     ```bash
     ffmpeg -i assets/music/musica.wav -i assets/audio/voz.wav -filter_complex "[0][1]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[m]" -map "[m]" assets/music/musica-duck.wav
     ```
     Then use it at `data-volume` 0.3–0.35, so the music breathes in the pauses.
5. **In the index:**
   ```html
   <audio id="musica" class="clip" src="assets/music/musica.wav" data-timeline-role="music" data-start="0" data-duration="<dur>" data-track-index="10" data-volume="0.2">
   ```
   The final mix lands near −14.5 LUFS. Tell the user **not to add another app music on top**.
6. Keep the other candidates in the folder and offer to swap the track or the volume.

## Sound effects

Use the HyperFrames built-ins: `npx hyperframes media-use resolve --type sfx --intent "<...>" --local-only --project .` and copy them to `assets/sfx/`.

| File | Intent for resolve | Use | Volume (subtle / punchy) |
| --- | --- | --- | --- |
| `whoosh.mp3` | "short fast swoosh" (0.6 s) | scene change, starting 0.12–0.16 s before the cut | 0.24 / 0.36 |
| `pop.mp3` | "pop click" | chips, tags, checks, buttons | 0.3 / 0.42, duration 0.3 |
| `impact.mp3` | "impact hit" | only on the 4–5 main beats: hook word, product name, the reveal, the final question | 0.1 / 0.2 |

- The "cinematic whoosh" (5.5 s) is too long for reels.
- Every `<audio>` needs an `id`.
- Use separate tracks (whoosh 6, impact 7, pops alternating 8/9/11). `check` flags `duplicate_audio_track` when two sounds overlap on one track.
- With `sfx: none`, skip them.
