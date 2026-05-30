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

All automation tasks complete. Implementation verified in pipeline.py and scraper.py.

| Order | Task | File | Status |
|---|---|---|---|
| 1 | T05 / T07 — Niche + pillar routing update | pipeline.py | **COMPLETE** |
| 2 | T06 — sources field per account | pipeline.py | **COMPLETE** |
| 3 | T09 — --brands CLI argument | pipeline.py | **COMPLETE** |
| 4 | T08 — copyright_risk flag | pipeline.py | **COMPLETE** |
| 5 | T17 — --series CLI argument + manifest field | pipeline.py | **COMPLETE** |
| 6 | T10 / T11 / T12 — YouTube search + --brand arg | scraper.py | **COMPLETE** |
| 7 | T13 — Archive.org scraper stub | scraper.py | **COMPLETE** |
| 8 | T16 — Episode 1 outline (Computing 1950–2026) | EP01_computing_1950_2026.md | **COMPLETE** |

**Next step:** Add API keys to `.env` → run smoke test `python pipeline.py <url> --brands agent_maxxing`

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
- [x] T05 — ACCOUNT_PROFILES niche fields updated to content pillar language
- [x] T06 — sources field added to each ACCOUNT_PROFILES entry
- [x] T07 — generate_metadata() routing prompt extended with pillars
- [x] T08 — copyright_risk flag added to pipeline manifest
- [x] T09 — --brands CLI argument added to pipeline.py
- [x] T10 — scrape_youtube_search() added to scraper.py
- [x] T11 — BRAND_SEARCH_QUERIES config dict added to scraper.py
- [x] T12 — --brand CLI argument added to scraper.py
- [x] T13 — scrape_archive_org() stub added to scraper.py (agent_pastforward)
- [x] T17 — --series CLI argument and series field added to pipeline.py
- [x] T16 — Episode 1 outline drafted (EP01_computing_1950_2026.md)
- [ ] pipeline.py smoke tested end-to-end with API keys
- [ ] First 100 posts published network-wide ← FIRST MILESTONE
- [ ] agent_pastforward activated (after ACTIVE trio stable)
- [ ] Content pillars applied to all active account bios
- [ ] Source list scraper runs validated per account

---

## AUTOMATION STATUS

| Component | Status |
|---|---|
| pipeline.py | UPDATED — T05–T09, T17 complete. Awaiting API keys for live test. |
| scraper.py | UPDATED — T10–T13 complete. YouTube search + Archive.org + --brand arg added. |
| ACCOUNT_PROFILES | agent_maxxing ACTIVE, agent_afterhours ACTIVE, agent_viral ACTIVE, agent_pastforward RESERVED |
| Niche + Pillars | UPDATED — all accounts have precise niche strings and content pillars |
| copyright_risk flag | IMPLEMENTED — URL pre-check + Claude transcript analysis |
| --brands arg | IMPLEMENTED — restricts pipeline routing to specified brands |
| --series arg | IMPLEMENTED — tags clips with campaign series name |
| --brand arg (scraper) | IMPLEMENTED — runs BRAND_SEARCH_QUERIES for specified brand |
| scrape_archive_org() | IMPLEMENTED — Prelinger Archives public domain search |
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

**CURRENT PHASE:** Phase 1 — Handle Acquisition (human) | Automation Build: COMPLETE
**ACTIVE ACCOUNTS:** agent_maxxing, agent_afterhours, agent_viral
**RETIRED:** agent_trending
**FIRST MILESTONE:** 100 posts network-wide
**BEST NEXT ACTION:** Add OPENAI_API_KEY + ANTHROPIC_API_KEY to .env → run smoke test → claim Instagram/X/Threads handles (no cooldown)
