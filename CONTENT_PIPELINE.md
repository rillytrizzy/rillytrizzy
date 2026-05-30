# Agent Network — Content Pipeline Reference
**Version:** 1.0
**Date:** 2026-05-30
**Ref:** pipeline.py, scraper.py, AUTOMATION_TASKS.md

Covers: end-to-end flow per brand, commands, stage ownership, error handling.

---

## PIPELINE OVERVIEW

```
SOURCE DISCOVERY       DOWNLOAD        CLIP + CAPTION       REVIEW        POST
─────────────────    ──────────────   ──────────────────   ─────────     ──────────────
scraper.py        →  pipeline.py   →  pipeline.py        →  Human    →  Platform (manual)
(clips.json)         (yt-dlp)         (ffmpeg + Whisper      review       TikTok / Reels /
                                       + Claude)             queue        Shorts / X
```

**Automated stages:** Discovery → Download → Clip → Caption → Route → Review queue write
**Manual stages:** Human review → Approval → Upload to platforms

---

## STAGE 1: SOURCE DISCOVERY

### Commands by brand

```bash
# agent_viral — uses existing Twitch/Kick scrape
python scraper.py --platforms twitch kick --json clips_viral.json

# agent_maxxing — YouTube search (requires T10/T11/T12)
python scraper.py --brand agent_maxxing --json clips_maxxing.json

# agent_afterhours — YouTube search for festival content
python scraper.py --brand agent_afterhours --json clips_afterhours.json

# agent_pastforward — Archive.org + YouTube search (requires T12/T13)
python scraper.py --brand agent_pastforward --json clips_pastforward.json

# All platforms, no brand filter (original behavior)
python scraper.py --platforms twitch kick youtube --json all_clips.json
```

### Output schema (`clips.json`)
```json
{
  "platform": "twitch|kick|youtube|archive.org",
  "game": "category or empty",
  "title": "clip title",
  "url": "https://...",
  "view_count": 12345,
  "duration_sec": 45,
  "channel": "channel name",
  "created_at": "ISO 8601",
  "account": "agent_viral"  // present when --brand is used
}
```

### Sorting output for pipeline input
```bash
# Sort by view_count, extract top N URLs for pipeline
python -c "
import json
clips = json.load(open('clips_viral.json'))
clips.sort(key=lambda x: x.get('view_count', 0), reverse=True)
for c in clips[:10]:
    print(c['url'])
" > top_urls.txt
```

---

## STAGE 2: DOWNLOAD

Handled internally by `pipeline.py` via `yt-dlp`.

Supported sources: YouTube, TikTok, Twitch, Kick, Instagram, Archive.org (direct URL).

```bash
# Single URL
python pipeline.py https://example.com/video

# Single URL, specific brand, custom clip duration
python pipeline.py <url> --brands agent_maxxing --clip-duration 45 --output output/
```

**Error:** If yt-dlp fails, check that the URL is publicly accessible. Private/age-restricted videos will fail.

---

## STAGE 3: CLIP EXTRACTION

Handled internally by `pipeline.py` via `ffmpeg`.

- Segments video into `--clip-duration` second chunks (default: 45s)
- Center-crops to 9:16 vertical (1080×1920)
- Output: `output/<run_id>/clips/clip_00.mp4`, `clip_01.mp4`, etc.

**Error handling:** If a clip file is 0 bytes, ffmpeg encountered an error — check source video resolution and codec.

---

## STAGE 4: TRANSCRIPTION

Handled internally by `pipeline.py` via OpenAI Whisper API.

Requires `OPENAI_API_KEY` in `.env`.

If `OPENAI_API_KEY` is missing: transcript will be empty — routing quality degrades significantly.

---

## STAGE 5: METADATA GENERATION + ROUTING

Handled internally by `pipeline.py` via Claude API.

Requires `ANTHROPIC_API_KEY` in `.env`.

Per clip output:
```json
{
  "account": "agent_maxxing",
  "hook": "This AI agent just replaced my entire workflow.",
  "caption": "150-250 char caption body",
  "hashtags": ["#AI", "#AgentMaxxing", "#automation"],
  "confidence": 0.87,
  "copyright_risk": false,
  "series": null
}
```

**Routing rules:**
- RESERVED accounts can only receive content if `--brands` explicitly forces it
- Clips below `CONFIDENCE_THRESHOLD` (0.70) are flagged `needs_review: true`
- `copyright_risk: true` is flagged when transcript contains song lyrics or source is music-adjacent

---

## STAGE 6: REVIEW QUEUE

Output file: `output/<run_id>/review_queue.json`

Human operator opens file. Per-clip approval:
```json
{
  "clip": "clips/clip_00.mp4",
  "account": "agent_maxxing",
  "approved": false,   // <-- change to true after review
  "needs_review": false,
  "copyright_risk": false,
  "confidence": 0.87
}
```

**Set `"approved": true` for clips cleared for posting. Do not remove the `false` entries.**

After approval: copy approved clip + caption to `content_calendar/<account>/YYYY-MM-DD/`.

---

## STAGE 7: POSTING (MANUAL)

No auto-posting. Human operator uploads approved clips to each platform.

### agent_viral (TikTok)
1. Open TikTok app / creator portal
2. Upload `clip_XX.mp4`
3. Paste `hook` as on-screen text (if not burned in)
4. Paste `caption` + `hashtags` into caption field
5. Post immediately

### agent_maxxing (TikTok + Reels + Shorts + X)
1. TikTok: post as above
2. Instagram Reels: upload same clip; adjust caption tone; tag relevant accounts
3. YouTube Shorts: upload; set title = hook; description = caption
4. X: post clip URL + 1 original sentence (no hashtags)

### agent_afterhours (TikTok + Reels + Shorts)
1. Check `copyright_risk` one final time before uploading
2. Post as above. Tag artist/festival accounts in caption.
3. Skip YouTube Shorts if not one of the 3 weekly curated picks.

### agent_pastforward (TikTok + Reels + Shorts + X)
1. Confirm narration voiceover is burned into clip before posting
2. TikTok: post with history-category hashtags
3. Instagram: longer caption with one additional fact
4. YouTube: pin comment linking to newsletter
5. X: thread format (clip + 3 bullet facts)

---

## PIPELINE PER-BRAND CONFIGURATION

| Brand | Clip Duration | Confidence Threshold | Copyright Check | Requires Narration | Batch OK |
|---|---|---|---|---|---|
| agent_viral | 30s | 0.75 | Standard | No | Yes |
| agent_maxxing | 45s | 0.80 | Standard | No | Yes |
| agent_afterhours | 45s | 0.75 | **Strict** | No | No — human reviews each |
| agent_pastforward | 60–90s | 0.70 | Strict | **Yes** | No — manual production step |

---

## BATCH PIPELINE SCRIPT

For agent_viral (high volume):
```bash
# Read top 10 URLs from clips file and run pipeline for each
python -c "
import json, subprocess
clips = json.load(open('clips_viral.json'))
clips.sort(key=lambda x: x.get('view_count', 0), reverse=True)
for c in clips[:10]:
    subprocess.run(['python', 'pipeline.py', c['url'], '--brands', 'agent_viral'])
"
```

---

## ERROR REFERENCE

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError` | Missing dependency | `pip install -r requirements.txt` |
| `yt-dlp download failed` | URL unavailable or private | Try next URL from clips.json |
| `ffmpeg clip_XX.mp4 is 0 bytes` | ffmpeg codec error | Check source video; try different URL |
| `OpenAI API error` | Missing/invalid OPENAI_API_KEY | Add key to .env; transcription skipped |
| `Claude returned non-JSON` | Claude API response malformed | Re-run pipeline on same URL; usually transient |
| `confidence < 0.70 on all clips` | Source video is off-niche | Source video doesn't fit any account niche; reject |
| `copyright_risk: true` | Music detected in transcript | Human review required; do not auto-approve |

---

## FILE LOCATIONS

| File | Path | Purpose |
|---|---|---|
| Source discovery output | `clips_<brand>.json` | Input to pipeline |
| Pipeline run output | `output/<run_id>/` | Clips + review queue |
| Review queue | `output/<run_id>/review_queue.json` | Human approval interface |
| Approved content | `content_calendar/<account>/YYYY-MM-DD/` | Ready to post |
| Content calendar template | `content_calendar/TEMPLATE.md` | Tracking sheet |
| Account profiles | `pipeline.py: ACCOUNT_PROFILES` | Routing config |
| Brand search queries | `scraper.py: BRAND_SEARCH_QUERIES` | Source discovery config |
