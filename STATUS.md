# Agent Network — Status Dashboard
**Version:** 1.2
**Last Updated:** 2026-05-30
**Architecture ref:** BRAND_ARCHITECTURE.md v1.1

---

## NETWORK ROSTER

| Account | Status | Posting | TikTok Handle | Notes |
|---|---|---|---|---|
| agent_maxxing | **ACTIVE** | Live | agent_maxxing | Underscore — correct |
| agent_afterhours | **ACTIVE** | Live | agent.afterhours | Dot — rename pending cooldown |
| agent_viral | **ACTIVE** | Live | agent.trending | Dot — rename to agent_viral pending cooldown |
| agent_pastforward | **RESERVED** | Not posting | agent_pastforward | Secured — activate after ACTIVE trio stable |
| agent_trending | **RETIRED** | — | — | Retired. TikTok account repurposed as agent_viral |
| rillytrizzy | **ACTIVE (founder)** | Not yet posting | — | Secure after core brands |

---

## POSTING FREQUENCIES

| Account | TikTok | Instagram | YouTube Shorts | X | Total/week |
|---|---|---|---|---|---|
| agent_maxxing | 1–2x/day | 1x/day | 5x/week | 2x/day | ~25 posts |
| agent_afterhours | 1x/day | 5x/week | 3x/week | 3–4x/week | ~18 posts |
| agent_viral | 2–3x/day | 2x/day | 7x/week | 3x/day | ~42 posts |
| **NETWORK TOTAL** | | | | | **~85 posts/week** |

---

## FIRST MILESTONE: 100 POSTS NETWORK-WIDE

**Target:** 100 total published posts across all active accounts and platforms.
**Estimated time to reach:** ~2 weeks at full frequency.
**Tracking:** Mark posts in `content_calendar/<account>/YYYY-MM-DD/` folders.
**Why it matters:** Forces pipeline to be tested under real conditions; validates routing, copyright, and approval workflow before scale.

| Account | Posts Needed | Progress |
|---|---|---|
| agent_maxxing | 35 | [ ] |
| agent_afterhours | 25 | [ ] |
| agent_viral | 40 | [ ] |
| **TOTAL** | **100** | **0 / 100** |

---

## PLATFORM STATUS

### TikTok

| Account | Handle | Status | Action |
|---|---|---|---|
| agent_maxxing | agent_maxxing | **SECURED** | None |
| agent_afterhours | agent.afterhours | SECURED — rename pending | Rename to agent_afterhours when cooldown clears |
| agent_viral | agent.trending | SECURED — rename pending | Rename to agent_viral when cooldown clears (repurposed from agent_trending) |
| agent_pastforward | agent_pastforward | SECURED | None — not yet posting |
| rillytrizzy | — | NOT CREATED | Create after core brands |

### YouTube

| Channel | Handle | Status | Action |
|---|---|---|---|
| Agent Maxxing | @agent_afterhours | MISMATCH | Rename to @agent_maxxing when cooldown clears |
| Agent After Hours | — | EMPTY | Configure after Agent Maxxing rename completes |
| Agent Viral | — | EXISTS | Verify handle matches @agent_viral |

### Instagram

| Handle | Status |
|---|---|
| agent_maxxing | CLAIM NEEDED |
| agent_afterhours | CLAIM NEEDED |
| agent_viral | CLAIM NEEDED |
| agent_pastforward | CLAIM NEEDED |
| rillytrizzy | CLAIM NEEDED |

### X (Twitter)

| Handle | Status | Notes |
|---|---|---|
| agent_maxxing | CLAIM NEEDED | @agentmaxxing (no underscore) taken — @agent_maxxing distinct |
| agent_afterhours | CLAIM NEEDED | — |
| agent_viral | CLAIM NEEDED | — |
| agent_pastforward | CLAIM NEEDED | — |
| rillytrizzy | CLAIM NEEDED | — |

### Threads

| Handle | Status |
|---|---|
| agent_maxxing | CLAIM NEEDED |
| agent_afterhours | CLAIM NEEDED |
| agent_viral | CLAIM NEEDED |
| agent_pastforward | CLAIM NEEDED |
| rillytrizzy | CLAIM NEEDED |

### Domains

| Domain | Status |
|---|---|
| agentmaxxing.com | VERIFY URGENTLY |
| agentmaxxing.co | For sale — purchase if .com unavailable |
| agentafterhours.com | Check and claim |
| agentpastforward.com | Check and claim |
| agentviral.com | Check and claim |
| rillytrizzy.com | Check and claim |

---

## CURRENT BLOCKERS

| Blocker | Platform | Waiting On |
|---|---|---|
| @agent_maxxing handle not applied | YouTube | Cooldown expiration |
| Agent After Hours channel not configured | YouTube | @agent_maxxing rename must complete first |
| agent.afterhours → agent_afterhours | TikTok | Cooldown expiration |
| agent.trending → agent_viral | TikTok | Cooldown expiration (repurposed account) |
| Instagram/X/Threads handles unclaimed | Instagram, X, Threads | Human action — no cooldown |
| API keys not configured | .env | Human action — add to .env |

---

## AUTOMATION BUILD ORDER

Execute Codex tasks in this sequence. Each depends on the previous.

| Order | Task | File | Prompt Location | Status |
|---|---|---|---|---|
| 1 | T05 / T07 — Niche + pillar routing update | pipeline.py | CODEX_TASK_PROMPTS.md | PENDING |
| 2 | T09 — --brands CLI argument | pipeline.py | CODEX_TASK_PROMPTS.md | PENDING |
| 3 | T10 / T11 / T12 — YouTube search + --brand arg | scraper.py | CODEX_TASK_PROMPTS.md | PENDING |
| 4 | T08 — Copyright risk flag | pipeline.py | CODEX_TASK_PROMPTS.md | PENDING |
| 5 | T17 — --series CLI argument | pipeline.py | CODEX_TASK_PROMPTS.md | PENDING |
| 6 | T13 — Archive.org scraper stub | scraper.py | CODEX_TASK_PROMPTS.md | PENDING |

---

## EXECUTION PHASE TRACKER

### Phase 1 — Handle Acquisition
- [ ] YouTube cooldown → @agent_maxxing handle applied to Agent Maxxing channel
- [ ] YouTube → empty channel configured as "Agent After Hours" at @agent_afterhours
- [ ] TikTok cooldown → agent.afterhours renamed to agent_afterhours
- [ ] TikTok cooldown → agent.trending renamed to agent_viral
- [ ] agent_maxxing claimed on Instagram, X, Threads
- [ ] agent_afterhours claimed on Instagram, X, Threads
- [ ] agent_viral claimed on Instagram, X, Threads
- [ ] agent_pastforward claimed on Instagram, YouTube, X, Threads

### Phase 2 — Profile Optimization
- [ ] rillytrizzy claimed on TikTok, X, Threads, music platforms
- [ ] All bios written and applied (all active accounts)
- [ ] All profile images applied
- [ ] All banners applied
- [ ] Cross-platform links in all bios

### Phase 3 — Automation + Content
- [ ] .env: OPENAI_API_KEY and ANTHROPIC_API_KEY added
- [ ] Codex tasks T05–T13 implemented (see Automation Build Order above)
- [ ] pipeline.py tested end-to-end
- [ ] First 100 posts published network-wide ← FIRST MILESTONE
- [ ] agent_pastforward activated (after ACTIVE trio stable)

---

## AUTOMATION STATUS

| Component | Status |
|---|---|
| pipeline.py | Built — awaiting API keys + Codex tasks T05–T13 |
| scraper.py | Operational — Twitch, Kick, YouTube |
| ACCOUNT_PROFILES | agent_maxxing ACTIVE, agent_afterhours ACTIVE, agent_viral ACTIVE, agent_pastforward RESERVED |
| agent_trending | RETIRED — removed from ACCOUNT_PROFILES |
| OPENAI_API_KEY | Not configured |
| ANTHROPIC_API_KEY | Not configured |
| Review queue | Built-in — no auto-posting |

---

## NAMESPACE CONFLICTS

| Conflicting Handle | Platform | Risk |
|---|---|---|
| @agentmaxxing | X | Low — no underscore, distinct handle |
| @agentmaxx | TikTok | Low — different spelling |
| agentmaxing.com | Domain | Low — one-x spelling, unrelated business |

---

**CURRENT PHASE:** Phase 1 — Handle Acquisition + Automation Build (parallel)
**ACTIVE ACCOUNTS:** agent_maxxing, agent_afterhours, agent_viral
**RETIRED:** agent_trending
**FIRST MILESTONE:** 100 posts network-wide
**BEST NEXT ACTION:** Claim Instagram/X/Threads handles for agent_maxxing, agent_afterhours, agent_viral (no cooldown — execute now)
