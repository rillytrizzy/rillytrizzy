# Agent Network — Automation Task List
**Version:** 1.1
**Date:** 2026-05-30
**Ref:** CONTENT_STRATEGY.md, BRAND_ARCHITECTURE.md v1.1, pipeline.py, scraper.py
**Implementation prompts:** CODEX_TASK_PROMPTS.md (code tasks), CLAUDE_TASK_PROMPTS.md (content tasks)

Tasks T04–T18 below include: exact description, dependencies, estimated effort, recommended operator, acceptance criteria.

---

## BATCH 1 — FILE UPDATES

| ID | Status | Operator |
|---|---|---|
| T01 | COMPLETE | Claude |
| T02 | COMPLETE | Claude |
| T03 | COMPLETE | Claude |
| T04 | COMPLETE | Claude |

---

## BATCH 2 — PIPELINE UPDATES

### T05 — Update ACCOUNT_PROFILES Niche Fields

**File:** `pipeline.py`
**Description:** Replace the `niche` value in each entry of `ACCOUNT_PROFILES` with the exact content pillar language from `CONTENT_STRATEGY.md`. This improves LLM routing accuracy because Claude's routing decisions depend on how precisely the niche is described.
**Dependencies:** None
**Effort:** 15 minutes
**Operator:** Codex
**Prompt:** See `CODEX_TASK_PROMPTS.md` → "T05 + T07"
**Acceptance criteria:**
- `ACCOUNT_PROFILES["agent_maxxing"]["niche"]` = `"AI tool demos, agent workflows, automation hacks, future-of-work commentary, build logs"`
- `ACCOUNT_PROFILES["agent_afterhours"]["niche"]` = `"festival highlights, DJ set clips, music drops, nightlife vibe content, artist spotlights"`
- `ACCOUNT_PROFILES["agent_pastforward"]["niche"]` = `"historical predictions, forgotten technology, then-vs-now timelines, future forecasting"`
- `ACCOUNT_PROFILES["agent_viral"]["niche"]` = `"viral fails, crowd reactions, unexpected moments, trending clips, cross-genre entertainment"`
- `python -c "import pipeline; print('OK')"` passes

---

### T06 — Add Sources Field to ACCOUNT_PROFILES

**File:** `pipeline.py`
**Description:** Add a `sources` list field to each account in `ACCOUNT_PROFILES` listing preferred input source types. Used by operators to know which scraper mode to use per brand.
**Dependencies:** T05
**Effort:** 10 minutes
**Operator:** Codex
**Acceptance criteria:**
- Each account in `ACCOUNT_PROFILES` has a `"sources"` key with a list of strings
- Example: `"agent_viral": {"sources": ["twitch", "kick", "youtube_search"]}`
- `python -c "import pipeline; print(pipeline.ACCOUNT_PROFILES['agent_viral']['sources'])"` returns a list

---

### T07 — Extend Routing Prompt with Content Pillars

**File:** `pipeline.py`
**Description:** Extend `generate_metadata()` so the Claude routing prompt includes the full content pillar list per account, not just the niche string. Requires adding a `pillars` list to each `ACCOUNT_PROFILES` entry.
**Dependencies:** T05
**Effort:** 20 minutes
**Operator:** Codex
**Prompt:** See `CODEX_TASK_PROMPTS.md` → "T05 + T07"
**Acceptance criteria:**
- `ACCOUNT_PROFILES` has a `pillars` key per account
- Claude routing prompt in `generate_metadata()` includes `Pillars:` line per account
- `python -c "import pipeline; print('OK')"` passes

---

### T08 — Add Copyright Risk Flag

**File:** `pipeline.py`
**Description:** Add `copyright_risk` boolean to the pipeline output manifest. Triggered by music domain URLs (pre-check) and by Claude's analysis of the transcript. Required for `agent_afterhours` safety.
**Dependencies:** None
**Effort:** 20 minutes
**Operator:** Codex
**Prompt:** See `CODEX_TASK_PROMPTS.md` → "T08"
**Acceptance criteria:**
- Every clip in `review_queue.json` has `"copyright_risk": true` or `"copyright_risk": false`
- URLs from soundcloud.com, spotify.com, bandcamp.com produce `copyright_risk: true`
- Terminal output shows `© MUSIC RISK` for flagged clips
- No other pipeline behavior changes

---

### T09 — Add --brands CLI Argument to pipeline.py

**File:** `pipeline.py`
**Description:** Add `--brands` argument to restrict routing to a specified account subset. Enables per-brand pipeline runs without routing errors.
**Dependencies:** None
**Effort:** 20 minutes
**Operator:** Codex
**Prompt:** See `CODEX_TASK_PROMPTS.md` → "T09"
**Acceptance criteria:**
- `python pipeline.py <url> --brands agent_maxxing` routes only to `agent_maxxing`
- `python pipeline.py <url>` (no `--brands`) routes to `ACTIVE_ACCOUNTS` as before
- Unknown brand names print warning and are ignored
- `python pipeline.py --help` shows `--brands` in usage

---

## BATCH 3 — SCRAPER EXTENSIONS

### T10 — Add scrape_youtube_search() Function

**File:** `scraper.py`
**Description:** Add a `scrape_youtube_search(query, limit, brand)` function using yt-dlp's `ytsearch{N}:` URI format to discover clips via YouTube search. Returns the same dict schema as existing scraper functions.
**Dependencies:** None (yt-dlp already installed)
**Effort:** 30 minutes
**Operator:** Codex
**Prompt:** See `CODEX_TASK_PROMPTS.md` → "T10 + T11 + T12"
**Acceptance criteria:**
- `from scraper import scrape_youtube_search` succeeds
- `scrape_youtube_search("AI agent demo", limit=3)` returns a list of dicts
- Each dict contains: `platform`, `title`, `url`, `view_count`, `duration_sec`, `channel`
- Returns empty list (not exception) on network failure

---

### T11 — Add BRAND_SEARCH_QUERIES Config

**File:** `scraper.py`
**Description:** Add `BRAND_SEARCH_QUERIES` dict mapping each brand to its preferred YouTube search queries. Drives the `--brand` scraper argument.
**Dependencies:** T10
**Effort:** 15 minutes
**Operator:** Codex
**Prompt:** See `CODEX_TASK_PROMPTS.md` → "T10 + T11 + T12"
**Acceptance criteria:**
- `from scraper import BRAND_SEARCH_QUERIES` succeeds
- `BRAND_SEARCH_QUERIES["agent_maxxing"]` returns a list of 5 query strings
- Keys: `agent_maxxing`, `agent_afterhours`, `agent_pastforward`, `agent_viral`, `agent_trending`

---

### T12 — Add --brand CLI Argument to scraper.py

**File:** `scraper.py`
**Description:** Add `--brand` argument to `scraper.py` that runs `scrape_youtube_search()` for all queries in `BRAND_SEARCH_QUERIES[brand]`. Output clips tagged with target brand.
**Dependencies:** T10, T11
**Effort:** 20 minutes
**Operator:** Codex
**Prompt:** See `CODEX_TASK_PROMPTS.md` → "T10 + T11 + T12"
**Acceptance criteria:**
- `python scraper.py --brand agent_maxxing` runs YouTube searches and outputs clips
- All output clips contain `"account": "agent_maxxing"`
- `python scraper.py` (no `--brand`) behavior unchanged
- `python scraper.py --help` shows `--brand` in usage

---

### T13 — Add scrape_archive_org() Function

**File:** `scraper.py`
**Description:** Add public-domain video discovery via Archive.org Advanced Search API. Targets Prelinger Archives (historical footage, fully public domain). For `agent_pastforward` only.
**Dependencies:** None
**Effort:** 30 minutes
**Operator:** Codex
**Prompt:** See `CODEX_TASK_PROMPTS.md` → "T13"
**Acceptance criteria:**
- `from scraper import scrape_archive_org` succeeds
- `scrape_archive_org("futurism film", limit=3)` returns a list (may be empty on network error)
- All returned items have `"license": "public_domain"` and `"account": "agent_pastforward"`
- URL format: `https://archive.org/download/<id>/<id>.mp4`
- Does not throw exception on network failure

---

## BATCH 4 — CROSS-POSTING WORKFLOW

See `CONTENT_PIPELINE.md` for per-brand posting workflows (Stage 7).
See `ACCOUNT_PLAYBOOKS.md` for per-account daily actions.

---

## BATCH 5 — CAMPAIGN IMPLEMENTATION

### T14 — Create Fastest Timeline Directory

**Status:** COMPLETE — `content_calendar/agent_pastforward/fastest_timeline/` exists

---

### T15 — Create Episode Research Template

**Status:** COMPLETE — `content_calendar/agent_pastforward/fastest_timeline/EPISODE_TEMPLATE.md` exists

---

### T16 — Draft Episode 1 Outline

**File:** `content_calendar/agent_pastforward/fastest_timeline/EPISODE_TEMPLATE.md`
**Description:** Fill out the EPISODE_TEMPLATE.md for Episode 1 (Computing: 1950–2026) with hook, milestones, source clips, narration script, and newsletter CTA.
**Dependencies:** ROADMAP.md (complete)
**Effort:** 45 minutes research + 30 minutes scripting
**Operator:** Claude (use CLAUDE_TASK_PROMPTS.md → Prompt 06) or Human
**Acceptance criteria:**
- EPISODE_TEMPLATE.md for Ep01 is fully filled
- Hook line matches ROADMAP.md: "What took 20 years in 1950 now takes 20 months."
- 5 milestones identified with source clip references
- Narration script is 90 seconds at normal spoken pace
- Sponsor slot placeholder is marked

---

### T17 — Add Series Field to pipeline.py Manifest

**File:** `pipeline.py`
**Description:** Add `--series` CLI argument and `series` field to each clip in `review_queue.json`. Enables campaign tracking for Fastest Timeline episodes.
**Dependencies:** T09
**Effort:** 10 minutes
**Operator:** Codex
**Prompt:** See `CODEX_TASK_PROMPTS.md` → "T17"
**Acceptance criteria:**
- `python pipeline.py <url> --series fastest_timeline` produces clips with `"series": "fastest_timeline"`
- Without `--series`, clips have `"series": null`
- `python pipeline.py --help` shows `--series`

---

### T18 — Draft Episode Topics 1–5

**Status:** COMPLETE — See `ROADMAP.md` episodes 01–05

---

## BATCH 6 — VERIFICATION

Run after Batches 2–3 are complete:

```bash
python pipeline.py <test_url> --brands agent_maxxing
# → verify: all clips route to agent_maxxing; review_queue.json has copyright_risk field

python pipeline.py <test_url> --brands agent_afterhours
# → verify: copyright_risk: true triggers for music URLs

python scraper.py --brand agent_pastforward --json test_pastforward.json
# → verify: results contain YouTube clips relevant to history/futurism

python scraper.py --brand agent_viral --platforms twitch kick --json test_viral.json
# → verify: results contain "account": "agent_viral" field

python -c "import json; q=json.load(open('output/<run_id>/review_queue.json')); assert all(not c['approved'] for c in q['clips']), 'ERROR: auto-approved clip found'"
# → verify: no clip is auto-approved
```

---

## TASK PRIORITY ORDER (updated)

| Priority | ID | Task | Operator | Status |
|---|---|---|---|---|
| 1 | T05, T07 | Update routing niche + pillars | Claude | **COMPLETE** |
| 2 | T09 | Add --brands to pipeline.py | Claude | **COMPLETE** |
| 3 | T10, T11, T12 | YouTube search scraper + --brand | Claude | **COMPLETE** |
| 4 | T08 | Copyright risk flag | Claude | **COMPLETE** |
| 5 | T17 | Add --series to pipeline.py | Claude | **COMPLETE** |
| 6 | T13 | Archive.org scraper stub | Claude | **COMPLETE** |
| 7 | T16 | Draft Episode 1 outline | Claude | **COMPLETE** |
| 8 | T06 | Add sources field to ACCOUNT_PROFILES | Claude | **COMPLETE** |


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
