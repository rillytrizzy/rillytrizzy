# CURRENT_STATE
**Last Updated:** 2026-05-30
**Purpose:** Single-file snapshot of verified project state. Read alongside CHECKPOINT.md.

---

## System Status

| Component | Status | Notes |
|---|---|---|
| Architecture | LOCKED | BRAND_ARCHITECTURE.md v1.1 — do not modify without formal audit |
| Content Strategy | COMPLETE | CONTENT_STRATEGY.md — pillars, sources, monetization per brand |
| Automation Stack | BUILT | pipeline.py + scraper.py — all T05–T17 tasks implemented |
| Smoke Test | BLOCKED | Awaiting OPENAI_API_KEY + ANTHROPIC_API_KEY in .env |
| Posting | MANUAL ACTIVE | Human-operated; all 3 active brands can post now |
| Mobile Ops | PARTIAL | Checklist + playbooks exist; no mobile automation layer yet |
| Telegram Bot | NOT BUILT | Not in current scope; noted as future phase |
| Codex Remote Control | NOT BUILT | Blocked pending interactive auth / safe command layer |

---

## Active Brands

| Brand | Status | TikTok | Posting Target |
|---|---|---|---|
| agent_maxxing | **ACTIVE** | `agent_maxxing` ✓ | 1–2x/day TikTok, 1x/day IG, 5x/week YT, 2x/day X |
| agent_afterhours | **ACTIVE** | `agent.afterhours` (rename → `agent_afterhours` pending cooldown) | 1x/day TikTok, 5x/week IG, 3x/week YT, 3–4x/week X |
| agent_viral | **ACTIVE** | `agent.trending` (repurposed; rename → `agent_viral` pending cooldown) | 2–3x/day TikTok, 2x/day IG, 7x/week YT, 3x/day X |
| agent_pastforward | **RESERVED** | `agent_pastforward` ✓ | Not posting — activate after active trio stable |

---

## Founder

| Brand | Status |
|---|---|
| rillytrizzy | ACTIVE (founder layer) — handles not yet secured cross-platform |

---

## Retired

| Brand | Notes |
|---|---|
| agent_trending | RETIRED. TikTok account (agent.trending) repurposed as agent_viral. No handles to claim on any platform. |

---

## Automation Stack — Verified Complete

All tasks implemented and importable. Verified with `python -c "import pipeline, scraper"`.

### pipeline.py

| Task | Feature | Status |
|---|---|---|
| T05 | ACCOUNT_PROFILES niche fields updated to content pillar language | ✓ COMPLETE |
| T06 | sources field added per account | ✓ COMPLETE |
| T07 | generate_metadata() routing prompt extended with pillars list | ✓ COMPLETE |
| T08 | copyright_risk flag — URL domain pre-screen + Claude transcript analysis | ✓ COMPLETE |
| T09 | --brands CLI arg — restricts routing to specified account subset | ✓ COMPLETE |
| T17 | --series CLI arg — tags clips with campaign series name | ✓ COMPLETE |

### scraper.py

| Task | Feature | Status |
|---|---|---|
| T10 | scrape_youtube_search(query, limit, brand) via yt-dlp ytsearch | ✓ COMPLETE |
| T11 | BRAND_SEARCH_QUERIES — 5 queries per brand (maxxing, afterhours, pastforward, viral) | ✓ COMPLETE |
| T12 | --brand CLI arg — runs brand YouTube searches; composable with --platforms | ✓ COMPLETE |
| T13 | scrape_archive_org() — Prelinger Archives public domain search | ✓ COMPLETE |

### Content

| Task | Feature | Status |
|---|---|---|
| T16 | EP01_computing_1950_2026.md — full Episode 1 production outline | ✓ COMPLETE |

---

## Human Blockers (ordered by priority)

1. **Add API keys to .env**
   ```
   OPENAI_API_KEY=<your_key>
   ANTHROPIC_API_KEY=<your_key>
   ```
   Then run smoke test: `python pipeline.py <test_url> --brands agent_maxxing`

2. **Claim Instagram / X / Threads handles** — no cooldown blocking this
   - agent_maxxing on Instagram, X, Threads
   - agent_afterhours on Instagram, X, Threads
   - agent_viral on Instagram, X, Threads

3. **YouTube cooldown** — check YouTube Studio daily
   - Rename @agent_afterhours → @agent_maxxing
   - After rename: configure empty channel as "Agent After Hours" at @agent_afterhours

4. **TikTok cooldowns** — check TikTok Profile → Edit → Username daily
   - agent.afterhours → agent_afterhours
   - agent.trending → agent_viral (NOT agent_trending — that account is retired)

---

## Next Technical Action

After API keys are added, run the smoke test in this order:

```bash
# Step 1: Verify env
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OPENAI:', bool(os.getenv('OPENAI_API_KEY'))); print('ANTHROPIC:', bool(os.getenv('ANTHROPIC_API_KEY')))"

# Step 2: Smoke test pipeline (agent_maxxing only)
python pipeline.py <test_youtube_url> --brands agent_maxxing --clip-duration 30

# Step 3: Inspect output
cat output/<run_id>/review_queue.json | python -m json.tool | head -60

# Step 4: Verify governance — no clip auto-approved
python -c "import json; q=json.load(open('output/<run_id>/review_queue.json')); assert all(not c['approved'] for c in q['clips']); print('PASS: no auto-approvals')"
```

---

## Next Content Action

Post manually while automation smoke test is being completed:

| Brand | Daily Target | Source |
|---|---|---|
| agent_viral | 3 clips/day | Twitch / Kick highlights — use `python scraper.py --platforms twitch kick` |
| agent_maxxing | 1 AI/automation post/day | YouTube: Fireship, Matt Wolfe, AI Explained — use `python scraper.py --brand agent_maxxing` |
| agent_afterhours | 1 EDM/festival post/day | YouTube: EDC, AriAtHome — use `python scraper.py --brand agent_afterhours` |
| agent_pastforward | 1 timeline/history post/day | Archive.org + YouTube — use `python scraper.py --brand agent_pastforward` |

Note: Scraper output gives URLs. Run `python pipeline.py <url> --brands <account>` to process. Review queue must be human-approved before posting.

---

## File Map

| File | Purpose | State |
|---|---|---|
| BRAND_ARCHITECTURE.md | Master strategy — LOCKED v1.1 | LOCKED |
| ACCOUNT_REGISTRY.md | Per-account handle + platform status + source commands | CURRENT |
| STATUS.md | Live dashboard | CURRENT |
| CHECKPOINT.md | Instant-resume file | CURRENT |
| CURRENT_STATE.md | This file — verified project snapshot | CURRENT |
| EXECUTION_QUEUE.md | Ordered action list — Phase 2+3 COMPLETE | CURRENT |
| ACCOUNT_PLAYBOOKS.md | Per-account daily/weekly SOPs | CURRENT |
| CONTENT_PIPELINE.md | Technical pipeline reference | CURRENT |
| CONTENT_STRATEGY.md | Content pillars, sources, monetization | CURRENT |
| DAILY_OPERATOR_CHECKLIST.md | Daily run-of-show with CLI commands | CURRENT |
| AUTOMATION_TASKS.md | T04–T18 task list — all complete | CURRENT |
| CLAUDE_TASK_PROMPTS.md | Copy-paste prompts for Claude content tasks | CURRENT |
| CODEX_TASK_PROMPTS.md | Implementation prompt reference (tasks now complete) | HISTORICAL |
| pipeline.py | Automation pipeline — all tasks implemented | CURRENT |
| scraper.py | Source discovery — all tasks implemented | CURRENT |
| seed_data.py | Test/demo seed dataset for offline pipeline testing | UTILITY |
| EP01_computing_1950_2026.md | Episode 1 full production outline | CURRENT |
| EPISODE_TEMPLATE.md | Blank template for future episodes | TEMPLATE |
| ROADMAP.md | 30-episode Fastest Timeline campaign roadmap | CURRENT |
