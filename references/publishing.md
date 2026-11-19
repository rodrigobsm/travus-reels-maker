# Post caption and publishing

## Post caption (`post-caption.txt`, UTF-8, next to the MP4)

- **First line:** the hook of the video.
- Then 2–4 short blocks:
  - a list with emojis if there is a comparison or steps;
  - the creator's opinion;
  - the question for the comments;
  - the CTA from the brief (`comment KEYWORD`, follow `@handle`, link in bio);
  - `rules.captionFooter`, if any.
- **At most `rules.maxHashtags` hashtags** (Instagram accepts 5). Prefer broad ones, plus `rules.fixedHashtags`.
- **Sources:** when the reel is news or research, add a short "Sources:" line with the outlets (names, or short links when the platform allows).
- **AI disclosure:** when the avatar or the voice is AI-generated, say so plainly (e.g. "Video made with an AI avatar and AI voice; the opinion is mine."). Remind the user to switch on the platform label:
  - Instagram: "AI info"
  - TikTok: "AI-generated content"
  - YouTube: "altered or synthetic content"
- **Sponsored:** put `#ad` (or the local equivalent, e.g. `#publi`) in the caption and remind the user to switch on the platform's paid-partnership label.
- Stay faithful to what is said. If a fact is in flux, write it carefully and flag it.
- Show the caption ready to paste.

## Publishing

**Never publish or schedule unless the user asks.** **Always ask the date and time** (AskUserQuestion), even when the user said "schedule it", and confirm the networks if they weren't named.

### `publish.provider: manual`

Deliver:
- `<Name>-final.mp4` (max quality, for upload);
- the phone copy;
- `cover.png`;
- `post-caption.txt`;
- a short checklist: cover, AI or partnership labels, pinned comment, keyword automation.

### `publish.provider: ghl` (GoHighLevel / LeadConnector Social Planner)

- **Setup:** secret `ghl_token` plus `publish.ghl.locationId` and `publish.ghl.userId` in the config. The token comes from a Private Integration with the social-planner scopes; connect the accounts in the Social Planner first.
- **Command:**
  ```bash
  python <skill>/scripts/publish_ghl.py --video "<folder>/<Name>-final.mp4" --cover "<folder>/cover.png" \
    --caption "<folder>/post-caption.txt" --when "YYYY-MM-DD HH:MM" --yt-title "<title up to 100 chars> #shorts" \
    [--networks instagram,facebook,tiktok,youtube] [--dry-run]
  ```
  - Run `--dry-run` first.
  - The time is in `publish.timezone`, and the script prints the current local time there.
  - It refuses a time in the past, a time before `publish.earliestHour`, and a caption with too many hashtags.
- **"Publish now"** = `--when now`. The script creates the post with `status: published` and follows each network's child post until it publishes. The response is only "Created Post": **that is success, never repeat it**.
- **Never change the time of a created post** (PUT on `scheduleDate`), and **never delete and recreate** without listing the day's posts. GHL creates one post per network, and doing either produced duplicates.
- Use the `-final.mp4` (H.264, max quality), never the phone copy. The cover goes to the post's `thumbnail` field; ask the user to check the preview in the Social Planner.
- After scheduling, report:
  - the post id
  - the networks
  - the time and time zone
  - the YouTube title

### Other schedulers

Any scheduler with an API can be added as `scripts/publish_<name>.py` and `publish.provider: <name>`. It must follow the same rules: ask the date and time, dry-run first, one create call, and verify per network.
