# Agent Network — Automation Task List
**Version:** 1.0
**Date:** 2026-05-30
**Ref:** CONTENT_STRATEGY.md, BRAND_ARCHITECTURE.md v1.1, pipeline.py, scraper.py

These tasks are sequenced for handoff to Claude or Codex.
Each task is self-contained and references the relevant file.

---

## BATCH 1 — FILE UPDATES (no code changes)

- [ ] **T01** Add `CONTENT_STRATEGY.md` path reference to `BRAND_ARCHITECTURE.md` Section 8 (Automation Architecture) so operators know where the source lists live
- [ ] **T02** Add source list fields to each account in `ACCOUNT_REGISTRY.md` (pull from CONTENT_STRATEGY.md per-brand source lists)
- [ ] **T03** Update `STATUS.md` Phase 2 checklist to include "content pillars documented" and "source list configured" as checklist items per brand
- [ ] **T04** Create `content_calendar/` directory with a blank template file `content_calendar/TEMPLATE.md` — columns: Date | Account | Platform | Hook | Caption | Hashtags | Clip Path | Status | Approved By

---

## BATCH 2 — PIPELINE UPDATES (pipeline.py)

- [ ] **T05** In `pipeline.py` `ACCOUNT_PROFILES`, update each brand's `niche` field to match the exact pillar descriptions in `CONTENT_STRATEGY.md` (currently general — needs to be specific enough for the LLM routing classifier)

  Targets:
  ```python
  "agent_maxxing": { "niche": "AI tool demos, agent workflows, automation hacks, future-of-work commentary, build logs" }
  "agent_afterhours": { "niche": "festival highlights, DJ set clips, music drops, nightlife vibe content, artist spotlights" }
  "agent_pastforward": { "niche": "historical predictions, forgotten technology, then-vs-now comparisons, future forecasting" }
  "agent_viral": { "niche": "viral fails, crowd reactions, unexpected moments, trending clips, cross-genre entertainment" }
  ```

- [ ] **T06** In `pipeline.py` `ACCOUNT_PROFILES`, add a `sources` field to each account listing the preferred input source types (maps to scraper extensions in T10–T12)

- [ ] **T07** In `pipeline.py` `generate_metadata()`, extend the Claude routing prompt to include the content pillars per account (not just niche) so routing decisions are more accurate

- [ ] **T08** In `pipeline.py`, add a `copyright_risk` flag to the output manifest for clips flagged as containing music. Trigger: transcript contains song lyrics, or source URL is from a music-adjacent platform

- [ ] **T09** In `pipeline.py`, update `ACTIVE_ACCOUNTS` filter logic to support a `--brands` CLI argument so the pipeline can be run for a specific account subset (e.g., `python pipeline.py <url> --brands agent_maxxing agent_afterhours`)

---

## BATCH 3 — SCRAPER EXTENSIONS (scraper.py)

- [ ] **T10** Add `scrape_youtube_search(query, limit)` function to `scraper.py`:
  - Uses yt-dlp's `ytsearch{limit}:{query}` URI format to pull top results for a search query
  - Returns same dict schema as existing scraper output (`platform`, `title`, `url`, `view_count`, `duration_sec`)
  - Required for: agent_maxxing, agent_afterhours, agent_pastforward, agent_viral source discovery

- [ ] **T11** Add brand-specific search query presets to `scraper.py` as a config dict:
  ```python
  BRAND_SEARCH_QUERIES = {
      "agent_maxxing": [
          "AI agent demo 2026", "Claude automation workflow",
          "AI productivity hack", "LLM tool walkthrough",
      ],
      "agent_afterhours": [
          "EDC 2026 highlights", "festival drop reaction",
          "DJ set best moment 2026", "AriAtHome highlights",
      ],
      "agent_pastforward": [
          "old prediction came true", "retro futurism technology",
          "vintage future technology", "they predicted smartphones",
      ],
      "agent_viral": [
          "best clip of the week", "unexpected viral moment",
          "funny fail compilation 2026", "crowd reaction compilation",
      ],
  }
  ```

- [ ] **T12** Add `--brand` CLI argument to `scraper.py`:
  - Accepts one brand name (e.g., `--brand agent_maxxing`)
  - Runs `scrape_youtube_search()` with that brand's query list from `BRAND_SEARCH_QUERIES`
  - Outputs clips tagged with the target brand in the JSON/CSV output
  - Falls back to full scrape if `--brand` is not specified (preserves existing behavior)

- [ ] **T13** Add Archive.org clip discovery stub function `scrape_archive_org(query, limit)` for agent_pastforward:
  - Queries `https://archive.org/advancedsearch.php` with `mediatype:movies` and the given query
  - Returns items with direct video download URLs where available
  - Tag output with `"platform": "archive.org"` and `"account": "agent_pastforward"`
  - Copyright safe: Archive.org Prelinger collection is public domain

---

## BATCH 4 — CROSS-POSTING WORKFLOW (no code — steps only)

These are manual workflow steps until a scheduling tool is integrated.

### agent_maxxing cross-posting workflow
1. Run: `python scraper.py --brand agent_maxxing --json clips_maxxing.json`
2. Run: `python pipeline.py <top_url_from_clips_maxxing.json> --brands agent_maxxing`
3. Open `output/<run>/review_queue.json` — approve clips with `confidence >= 0.80`
4. Export approved clips to `content_calendar/agent_maxxing/` folder
5. Upload to TikTok manually → cross-post to Instagram Reels → post to YouTube Shorts → share clip link on X with original text take

### agent_afterhours cross-posting workflow
1. Run: `python scraper.py --brand agent_afterhours --json clips_afterhours.json`
2. Run: `python pipeline.py <top_url> --brands agent_afterhours`
3. Open review queue — **mandatory human review for all music clips** (copyright flag T08)
4. Only approve clips with music licensing cleared or clips with no recognizable tracks
5. Export approved clips to `content_calendar/agent_afterhours/`
6. Upload to TikTok → cross-post to Instagram Reels → YouTube Shorts

### agent_pastforward cross-posting workflow
1. Manual research session (30–60 min): identify source clip from Archive.org or YouTube
2. Run: `python pipeline.py <archive_url> --brands agent_pastforward`
3. Review queue: approve clips that have clear historical context in transcript
4. Add narrated voiceover in post-processing (not yet automated — manual step)
5. Export to `content_calendar/agent_pastforward/`
6. Post to TikTok → Instagram Reels → YouTube Shorts

### agent_viral cross-posting workflow (highest volume)
1. Run: `python scraper.py --platforms twitch kick --json clips_viral.json`
2. Sort by `view_count` descending — take top 10 URLs
3. Run: `python pipeline.py <url> --brands agent_viral` for each URL (batch)
4. Review queue: approve clips scoring `confidence >= 0.75` — flag music clips
5. Export approved clips to `content_calendar/agent_viral/`
6. Post to TikTok (3x/day) → Instagram → YouTube Shorts → X

---

## BATCH 5 — CAMPAIGN IMPLEMENTATION (agent_pastforward "The Fastest Timeline")

- [ ] **T14** Create `content_calendar/agent_pastforward/fastest_timeline/` directory
- [ ] **T15** Create episode research template `fastest_timeline/EPISODE_TEMPLATE.md`:
  - Fields: Topic | Era start | Era end | Key milestones (3–5) | Source clips | Hook line | Narration script | Sponsor slot | Newsletter CTA
- [ ] **T16** Research and draft Episode 1 content outline (Computing: 1950–2026) using the template
- [ ] **T17** In `pipeline.py`, add a `series` field to the output manifest so campaign clips can be tagged (e.g., `"series": "fastest_timeline"`)
- [ ] **T18** Draft 5 episode topics and hook lines for the first campaign cycle:
  1. Computing (1950–2026) — "What took 20 years now takes 20 months."
  2. Communication (Telegraph–Smartphone) — "Every era thought they'd hit the ceiling."
  3. AI (1956–2026) — "60 years of research compressed into 3."
  4. Medicine (Penicillin–CRISPR) — "The pace of healing keeps accelerating."
  5. Space (1961–2026) — "We went from 'can we leave Earth' to 'can we stay on Mars'."

---

## BATCH 6 — VERIFICATION STEPS

After implementing Batches 2–4, run these checks:

- [ ] `python pipeline.py <test_url> --brands agent_maxxing` — verify routing to agent_maxxing only
- [ ] `python pipeline.py <test_url> --brands agent_afterhours` — verify copyright flag triggers on music clips
- [ ] `python scraper.py --brand agent_pastforward` — verify YouTube search returns relevant history clips
- [ ] `python scraper.py --brand agent_viral --platforms twitch kick` — verify existing scrape works with new brand tag
- [ ] Open review queue — verify `approved: false` on all clips before any manual approval
- [ ] Confirm no clip is routed to a RESERVED account unless explicitly forced via `--brands`

---

## TASK PRIORITY ORDER

| Priority | Task(s) | Reason |
|---|---|---|
| 1 | T05, T07 | Routing accuracy depends on better niche descriptions — everything downstream is more accurate |
| 2 | T09, T10, T11, T12 | Brand-specific scraping unlocks the full per-brand pipeline |
| 3 | T08 | Copyright flag protects agent_afterhours from DMCA risk |
| 4 | T04 | Content calendar structure needed before volume posting begins |
| 5 | T13 | agent_pastforward Archive.org integration — lower urgency, account is RESERVED |
| 6 | T14–T18 | Campaign content — blocked until agent_pastforward is ACTIVE |
