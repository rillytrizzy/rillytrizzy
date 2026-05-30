# Agent Network — Execution Checkpoint
**Last Updated:** 2026-05-30
**Purpose:** Instant resume file. Read this first after any downtime.

---

## EXECUTION_STATUS

```
DATE:        2026-05-30
PHASE:       Phase 1 (handle acquisition, human) + Phase 4 (API keys, human) — code complete
MILESTONE:   0 / 100 posts network-wide
BLOCKERS:    YouTube cooldown, TikTok cooldown, API keys not set
CODE STATUS: ALL automation tasks complete (T05–T13, T16, T17)
NEXT ACTION: 1) Add OPENAI_API_KEY + ANTHROPIC_API_KEY to .env
             2) Smoke test: python pipeline.py <test_url> --brands agent_maxxing
             3) Claim Instagram/X/Threads for agent_maxxing, agent_afterhours, agent_viral
```

---

## NETWORK ROSTER (current)

| Account | Status | TikTok | Posting |
|---|---|---|---|
| agent_maxxing | ACTIVE | agent_maxxing ✓ | Ready — needs Instagram/X/Threads |
| agent_afterhours | ACTIVE | agent.afterhours (cooldown) | Ready — needs Instagram/X/Threads |
| agent_viral | ACTIVE | agent.trending (cooldown) | Ready — needs Instagram/X/Threads |
| agent_pastforward | RESERVED | agent_pastforward ✓ | Not yet posting |
| agent_trending | **RETIRED** | n/a | Removed from all systems |
| rillytrizzy | ACTIVE (founder) | not created | After core brands |

---

## POSTING FREQUENCIES

| Account | TikTok | Instagram | YouTube Shorts | X | Weekly Total |
|---|---|---|---|---|---|
| agent_maxxing | 1–2x/day | 1x/day | 5x/week | 2x/day | ~25 |
| agent_afterhours | 1x/day | 5x/week | 3x/week | 3–4x/week | ~18 |
| agent_viral | 2–3x/day | 2x/day | 7x/week | 3x/day | ~42 |
| **TOTAL** | | | | | **~85/week** |

---

## COOLDOWN RESTRICTIONS

| Platform | Current Handle | Target Handle | Account | Unblock Action |
|---|---|---|---|---|
| YouTube | @agent_afterhours | @agent_maxxing | Agent Maxxing channel | Check YouTube Studio → Settings → Channel → Handle daily |
| TikTok | agent.afterhours | agent_afterhours | agent_afterhours | Check TikTok Profile → Edit → Username daily |
| TikTok | agent.trending | agent_viral | agent_viral | Check TikTok Profile → Edit → Username daily (repurposed from retired agent_trending) |

**Actions blocked until cooldowns clear:**
- Posting agent_afterhours with correct TikTok handle branding
- Posting agent_viral with correct TikTok handle branding
- Configuring YouTube "Agent After Hours" channel (depends on Agent Maxxing rename first)

**Actions NOT blocked by cooldowns (execute now):**
- Claim Instagram/X/Threads for agent_maxxing, agent_afterhours, agent_viral
- Add API keys to .env
- Run Codex tasks T05–T13
- Start posting content to TikTok regardless of username mismatch

---

## AUTOMATION BUILD ORDER — ALL COMPLETE ✓

```
✓ T05/T07   →  pipeline.py: niche descriptions + content pillar routing prompt
✓ T06       →  pipeline.py: sources field per account
✓ T09       →  pipeline.py: --brands CLI argument
✓ T08       →  pipeline.py: copyright_risk flag (URL pre-screen + Claude transcript analysis)
✓ T17       →  pipeline.py: --series CLI argument + series field in manifest
✓ T10/T11/T12 → scraper.py: scrape_youtube_search() + BRAND_SEARCH_QUERIES + --brand arg
✓ T13       →  scraper.py: scrape_archive_org() — Prelinger Archives (agent_pastforward)
✓ T16       →  EP01_computing_1950_2026.md: Episode 1 outline drafted
```

**Current pipeline.py state:**
- ACTIVE_ACCOUNTS = [agent_maxxing, agent_afterhours, agent_viral]
- agent_trending: RETIRED ✓ (removed from ACCOUNT_PROFILES)
- All T05–T17 code tasks: COMPLETE ✓
- Awaiting: OPENAI_API_KEY + ANTHROPIC_API_KEY in .env → then smoke test

---

## FIRST MILESTONE: 100 POSTS NETWORK-WIDE

**Definition:** 100 total published posts across agent_maxxing, agent_afterhours, and agent_viral combined.
**Allocation:** agent_maxxing 35, agent_afterhours 25, agent_viral 40.
**Purpose:** Validates pipeline, approval workflow, cross-posting, and content quality before scaling.
**At current frequency:** ~2 weeks from operations start.

**Post tracking:** Log each published post in `content_calendar/<account>/YYYY-MM-DD/` folder.
Count files in those directories to track progress.

---

## FILE MAP (all project files)

| File | Purpose | Last Updated |
|---|---|---|
| `BRAND_ARCHITECTURE.md` | Master strategy doc — LOCKED v1.1 | 2026-05-30 |
| `ACCOUNT_REGISTRY.md` | Per-account handle + platform status | 2026-05-30 |
| `STATUS.md` | Live dashboard — update weekly | 2026-05-30 |
| `CHECKPOINT.md` | This file — update after major decisions | 2026-05-30 |
| `EXECUTION_QUEUE.md` | Ordered action list, all phases | 2026-05-30 |
| `ACCOUNT_PLAYBOOKS.md` | Per-account daily/weekly SOPs | 2026-05-30 |
| `CONTENT_PIPELINE.md` | Technical pipeline reference | 2026-05-30 |
| `CONTENT_STRATEGY.md` | Content pillars, sources, monetization | 2026-05-30 |
| `DAILY_OPERATOR_CHECKLIST.md` | Daily run-of-show | 2026-05-30 |
| `CLAUDE_TASK_PROMPTS.md` | Copy-paste prompts for Claude (content) | 2026-05-30 |
| `CODEX_TASK_PROMPTS.md` | Copy-paste prompts for Codex (code) | 2026-05-30 |
| `AUTOMATION_TASKS.md` | T04–T18 with dependencies + acceptance criteria | 2026-05-30 |
| `pipeline.py` | Main automation pipeline — T05–T09, T17 complete | 2026-05-30 |
| `scraper.py` | Source discovery — Twitch, Kick, YouTube + brand search + Archive.org | 2026-05-30 |
| `content_calendar/TEMPLATE.md` | Post tracking template | 2026-05-30 |
| `content_calendar/agent_pastforward/fastest_timeline/ROADMAP.md` | 30-episode campaign roadmap | 2026-05-30 |
| `content_calendar/agent_pastforward/fastest_timeline/EPISODE_TEMPLATE.md` | Per-episode production template (blank) | 2026-05-30 |
| `content_calendar/agent_pastforward/fastest_timeline/EP01_computing_1950_2026.md` | Episode 1 full outline — Computing 1950–2026 | 2026-05-30 |

---

## DECISIONS LOCKED (do not re-litigate)

| Decision | Status |
|---|---|
| Network operates as sibling brands, not sub-brands | LOCKED |
| Underscore convention for all agent_ handles | LOCKED |
| YouTube primary = Agent Maxxing (@agent_maxxing) | LOCKED |
| agent_trending is RETIRED | LOCKED |
| agent_viral is ACTIVE (3rd active account) | LOCKED |
| No auto-posting — human approval required | LOCKED |
| First milestone = 100 posts network-wide | LOCKED |
| Automation MVP scope = agent_maxxing + agent_afterhours + agent_viral | LOCKED |

---

## RESUME INSTRUCTIONS

After any downtime, do this in order:

```
1. Read CHECKPOINT.md (this file) — 2 minutes
2. Check STATUS.md cooldowns section — have any unlocked?
3. If cooldown cleared: rename handle immediately (YouTube / TikTok)
4. Check EXECUTION_QUEUE.md — what phase is active?
5. Execute next unchecked item in current phase
6. If running Codex: open CODEX_TASK_PROMPTS.md → find next pending task
7. If running content: open DAILY_OPERATOR_CHECKLIST.md
```

---

## CHANGE LOG

| Date | Change | Impact |
|---|---|---|
| 2026-05-30 | agent_trending retired | Removed from pipeline.py ACCOUNT_PROFILES |
| 2026-05-30 | agent_viral promoted to ACTIVE | Added to ACTIVE_ACCOUNTS in pipeline.py |
| 2026-05-30 | agent.trending TikTok repurposed | Will be renamed to agent_viral after cooldown |
| 2026-05-30 | First milestone set: 100 posts | Tracked in content_calendar/ |
| 2026-05-30 | Posting frequencies locked | agent_viral 42/week, maxxing 25/week, afterhours 18/week |
| 2026-05-30 | T05–T17 all complete | pipeline.py: pillars, copyright_risk, --brands, --series; scraper.py: scrape_youtube_search, BRAND_SEARCH_QUERIES, --brand, scrape_archive_org |
| 2026-05-30 | EP01 outline drafted | content_calendar/agent_pastforward/fastest_timeline/EP01_computing_1950_2026.md |
| 2026-05-30 | ACCOUNT_REGISTRY.md updated | Source lists + scraper/pipeline commands per account; agent_trending marked RETIRED |
