# Agent Network — Execution Queue
**Version:** 1.0
**Date:** 2026-05-30
**Ref:** AUTOMATION_TASKS.md, BRAND_ARCHITECTURE.md v1.1, STATUS.md

Items are ordered: unblock first → human tasks → Codex tasks → Claude tasks → operations.
Execute in sequence within each phase. Phases run sequentially.

---

## PHASE 0 — UNBLOCK (waiting on platform cooldowns)

These cannot be actioned until the platform releases the lock. Check daily.

| ID | Action | Owner | Platform | Check |
|---|---|---|---|---|
| EQ-00A | Rename handle @agent_afterhours → @agent_maxxing | Human | YouTube | YouTube Studio → Settings → Channel → Handle |
| EQ-00B | Configure empty channel → "Agent After Hours" + handle @agent_afterhours | Human | YouTube | After EQ-00A completes |
| EQ-00C | Rename username agent.afterhours → agent_afterhours | Human | TikTok | TikTok → Profile → Edit → Username |
| EQ-00D | Rename username agent.trending → agent_viral | Human | TikTok | TikTok → Profile → Edit → Username (account repurposed — agent_trending is retired) |

---

## PHASE 1 — HANDLE ACQUISITION (human actions, no cooldowns)

Execute these now — no blockers.

| ID | Action | Owner | Platform | Target Handle |
|---|---|---|---|---|
| EQ-01A | Claim handle | Human | Instagram | agent_maxxing |
| EQ-01B | Claim handle | Human | Instagram | agent_afterhours |
| EQ-01C | Claim handle | Human | Instagram | agent_pastforward |
| EQ-01D | Claim handle | Human | Instagram | agent_viral |
| EQ-02A | Claim handle | Human | X | agent_maxxing |
| EQ-02B | Claim handle | Human | X | agent_afterhours |
| EQ-02C | Claim handle | Human | X | agent_pastforward |
| EQ-02D | Claim handle | Human | X | agent_viral |
| EQ-03A | Claim handle | Human | Threads | agent_maxxing |
| EQ-03B | Claim handle | Human | Threads | agent_afterhours |
| EQ-03C | Claim handle | Human | Threads | agent_pastforward |
| EQ-03D | Claim handle | Human | Threads | agent_viral |
| EQ-04A | Claim handle | Human | TikTok | agent_viral — rename agent.trending → agent_viral after cooldown (EQ-00D) |
| EQ-04B | Claim handle | Human | YouTube | agent_pastforward channel |
| ~~EQ-agent_trending~~ | ~~RETIRED~~ | — | — | agent_trending is retired. No handle claims needed. |
| EQ-05 | Check domain availability + purchase | Human | Registrar | agentmaxxing.com / .co, agentafterhours.com, agentpastforward.com, agentviral.com, agenttrending.com, rillytrizzy.com |

---

## PHASE 2 — CODE IMPLEMENTATION (Codex)

Run these after Phase 1 is in progress. No handle dependency.

| ID | Task Ref | Action | Operator | Effort | Blocked By |
|---|---|---|---|---|---|
| EQ-10 | T05 | Update ACCOUNT_PROFILES niche fields in pipeline.py | Codex | 15 min | None |
| EQ-11 | T07 | Extend generate_metadata() routing prompt with content pillars | Codex | 20 min | EQ-10 |
| EQ-12 | T08 | Add copyright_risk flag to pipeline.py manifest output | Codex | 20 min | None |
| EQ-13 | T09 | Add --brands CLI argument to pipeline.py | Codex | 20 min | None |
| EQ-14 | T10 | Add scrape_youtube_search() to scraper.py | Codex | 30 min | None |
| EQ-15 | T11 | Add BRAND_SEARCH_QUERIES config dict to scraper.py | Codex | 15 min | EQ-14 |
| EQ-16 | T12 | Add --brand CLI argument to scraper.py | Codex | 20 min | EQ-14, EQ-15 |
| EQ-17 | T13 | Add scrape_archive_org() stub to scraper.py | Codex | 30 min | None |
| EQ-18 | T17 | Add series field to pipeline.py manifest output | Codex | 10 min | None |

---

## PHASE 3 — FILE UPDATES (Claude)

| ID | Task Ref | Action | Operator | Effort |
|---|---|---|---|---|
| EQ-20 | T01 | Add CONTENT_STRATEGY.md cross-reference to BRAND_ARCHITECTURE.md §8 | Claude | 5 min |
| EQ-21 | T02 | Add source list fields to ACCOUNT_REGISTRY.md per account | Claude | 15 min |
| EQ-22 | T03 | Update STATUS.md checklist with content pillar + source list items | Claude | 10 min |
| EQ-23 | T16 | Draft Episode 1 outline (Computing 1950–2026) in EPISODE_TEMPLATE.md | Claude | 30 min |

---

## PHASE 4 — ENV SETUP (human)

| ID | Action | File |
|---|---|---|
| EQ-30 | Add OPENAI_API_KEY to .env | .env |
| EQ-31 | Add ANTHROPIC_API_KEY to .env | .env |
| EQ-32 | Run pipeline smoke test: python pipeline.py <test_url> | terminal |

---

## PHASE 5 — OPERATIONS START

Begins when Phase 1 (handles) and Phase 4 (env) are complete.

| ID | Action | Owner | Frequency |
|---|---|---|---|
| EQ-40 | Run DAILY_OPERATOR_CHECKLIST.md | Human | Daily |
| EQ-41 | Run agent_viral pipeline (Twitch/Kick scrape → review → post) | Human + Claude | Daily |
| EQ-42 | Run agent_maxxing pipeline (YouTube search → review → post) | Human + Claude | Daily |
| EQ-43 | Run agent_afterhours pipeline (festival search → review → post) | Human | Daily |
| EQ-44 | Research and draft agent_pastforward Fastest Timeline episode | Human | Weekly |

---

## QUEUE STATUS SUMMARY

| Phase | Status | Blocker |
|---|---|---|
| 0 — Unblock | WAITING | YouTube + TikTok cooldowns |
| 1 — Handle acquisition | IN PROGRESS | Human action required |
| 2 — Code | **COMPLETE** | — |
| 3 — File updates | **COMPLETE** | — |
| 4 — Env setup | READY | Add API keys to .env |
| 5 — Operations | BLOCKED | Phases 1 + 4 must complete first |
