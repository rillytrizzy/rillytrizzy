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
- Keys: `agent_maxxing`, `agent_afterhours`, `agent_pastforward`, `agent_viral` (agent_trending is RETIRED — no entry)

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

