# Agent Network — Account Registry
**Version:** 1.1
**Date:** 2026-05-30
**Architecture ref:** BRAND_ARCHITECTURE.md v1.1

---

## ACTIVE ACCOUNTS

### agent_maxxing
| Field | Value |
|---|---|
| Handle | agent_maxxing |
| Purpose | AI, agents, automation, productivity, future-of-work content |
| Status | **ACTIVE** |
| Priority | Tier 1 |
| TikTok | **SECURED** — underscore handle correct |
| YouTube | Channel "Agent Maxxing" exists — handle currently @agent_afterhours (cooldown pending rename to @agent_maxxing) |
| Instagram | Claim needed |
| X | Claim needed — note: @agentmaxxing (no underscore) is taken by unrelated account |
| Threads | Claim needed |
| Notes | Namespace conflicts on similar handles: @agentmaxx TikTok (54.6K followers), @agentmaxxing X (no underscore). Underscore handle @agent_maxxing is distinct and claimable. |
| **Content Sources** | YouTube: Fireship, Matt Wolfe, AI Explained, Two Minute Papers, TheAIGrid, Andrej Karpathy, Lex Fridman (AI segments), Y Combinator |
| **Scraper Command** | `python scraper.py --brand agent_maxxing --json clips_maxxing.json` |
| **Pipeline Command** | `python pipeline.py <url> --brands agent_maxxing` |

---

### agent_afterhours
| Field | Value |
|---|---|
| Handle | agent_afterhours |
| Purpose | EDM, festivals, dance, nightlife, music culture |
| Status | **ACTIVE** |
| Priority | Tier 1 |
| TikTok | **SECURED** — current username: agent.afterhours (dot). Rename to agent_afterhours queued pending cooldown |
| YouTube | Empty channel exists — to be configured as "Agent After Hours" once @agent_afterhours handle is freed from primary channel |
| Instagram | Claim needed |
| X | Claim needed |
| Threads | Claim needed |
| Notes | TikTok dot-to-underscore rename is a cooldown issue only — account is secured. YouTube channel configuration depends on primary channel handle rename completing first. |
| **Content Sources** | YouTube: EDC Las Vegas, AriAtHome, Tomorrowland, Ultra Music Festival, Coachella, DJ Mag |
| **Copyright Note** | ⚠ HIGHEST copyright risk in network. All clips require human review before posting. |
| **Scraper Command** | `python scraper.py --brand agent_afterhours --json clips_afterhours.json` |
| **Pipeline Command** | `python pipeline.py <url> --brands agent_afterhours` |

---

### rillytrizzy
| Field | Value |
|---|---|
| Handle | rillytrizzy |
| Purpose | Founder identity, music releases, creator journey, personal brand |
| Status | **ACTIVE** |
| Priority | Medium — secure after core Agent network handles |
| TikTok | Claim needed |
| YouTube | — |
| Instagram | Claim needed (was @agent_rillytrizzy — verify current status) |
| X | Claim needed |
| Threads | Claim needed |
| Music Platforms | Claim on Spotify for Artists, SoundCloud, Apple Music for Artists |
| Notes | Not a network account — founder layer only. Secure after agent_maxxing, agent_afterhours, agent_pastforward, and agent_viral handles are all claimed. (agent_trending is RETIRED — no handles to claim.) |

---

## RESERVED ACCOUNTS

### agent_pastforward
| Field | Value |
|---|---|
| Handle | agent_pastforward |
| Purpose | History, forgotten technology, old predictions, future forecasting |
| Status | **RESERVED** |
| Priority | Tier 1 — claim everywhere now; do NOT publish until agent_maxxing + agent_afterhours are producing consistently |
| TikTok | **SECURED** |
| YouTube | Claim needed |
| Instagram | Claim needed |
| X | Claim needed |
| Threads | Claim needed |
| Notes | Highest long-term content equity among reserved accounts. TikTok handle secured. Complete cross-platform coverage while the window is open. |
| **Content Sources** | Archive.org Prelinger Archives (public domain), Wikimedia Commons (CC-licensed), NASA public domain, US Government NARA footage |
| **YouTube Search** | "old prediction came true", "retro futurism", "vintage future technology", "forgotten technology documentary" |
| **Scraper Command** | `python scraper.py --brand agent_pastforward --json clips_pastforward.json` |
| **Pipeline Command** | `python pipeline.py <url> --brands agent_pastforward --series fastest_timeline` |

---

### agent_viral
| Field | Value |
|---|---|
| Handle | agent_viral |
| Purpose | Viral clips, broad entertainment, reaction content |
| Status | **ACTIVE** |
| Priority | Tier 1 |
| TikTok | **SECURED** — current username: agent.trending (dot). Rename to agent_viral queued pending cooldown |
| YouTube | YouTube channel exists (created alongside Agent Maxxing) |
| Instagram | Claim needed |
| X | Claim needed |
| Threads | Claim needed |
| Notes | TikTok account secured as agent.trending (repurposed from retired agent_trending). Underscore rename to agent_viral queued. |
| **Content Sources** | Twitch top game clips (LAST_WEEK), Kick trending clips, YouTube: "unexpected viral moment", "best clip week" |
| **Scraper Command** | `python scraper.py --platforms twitch kick --json clips_viral.json` |
| **Pipeline Command** | `python pipeline.py <url> --brands agent_viral` |

---

### ~~agent_trending~~ — RETIRED

| Field | Value |
|---|---|
| Handle | agent_trending |
| Status | **RETIRED** — do not create new handles; do not route content here |
| TikTok | Repurposed — account.trending account is now agent_viral (rename to agent_viral pending cooldown) |
| All other platforms | Do not claim — niche absorbed into agent_viral |
| Notes | agent_trending was retired in favour of agent_viral. The TikTok account (agent.trending) has been repurposed and will be renamed to agent_viral once the cooldown clears. No handles to claim on any other platform. |

---

## DOMAIN REGISTRY

| Domain | Status | Action |
|---|---|---|
| agentmaxxing.com | VERIFY URGENTLY — concept spreading fast | Check registrar; if taken, acquire agentmaxxing.co (listed for sale) |
| agentmaxxing.co | For sale on Spaceship | Purchase as fallback if .com unavailable |
| agentafterhours.com | Unknown — no conflicts found | Check and claim |
| agentpastforward.com | Unknown — no conflicts found | Check and claim |
| agentviral.com | Unknown | Check and claim |
| agenttrending.com | Unknown | Check and claim |
| rillytrizzy.com | Unknown — no conflicts found | Check and claim after core network domains secured |

---

## NAMESPACE CONFLICTS LOG

| Conflicting Handle | Platform | Risk Level | Notes |
|---|---|---|---|
| @agentmaxxing | X | Low | No underscore — distinct handle; @agent_maxxing (underscore) remains claimable |
| @agentmaxx | TikTok | Low | Different handle entirely (no underscore, no 'ing') — 54.6K followers |
| agentmaxing.com | Domain | Low | Business service, one-x spelling — different enough |
| @viralagents | Instagram | None | Different handle entirely |
| @weare.afterhours | Instagram | None | Different handle entirely |

**Assessment:** No direct conflicts on the exact underscore handles. The underscore convention creates a clean namespace separation from all known conflicts.

---

## REGISTRY STATUS

### Secured
- [x] agent_maxxing — TikTok
- [x] agent_afterhours — TikTok (as agent.afterhours — rename pending)
- [x] agent_pastforward — TikTok
- [x] agent_viral — TikTok (as agent.trending — repurposed; rename to agent_viral pending cooldown)
- [x] Agent Maxxing — YouTube channel exists
- [x] Agent Viral — YouTube channel exists
- [x] Agent After Hours — YouTube empty channel exists (pending configuration)

### Pending Cooldowns
- [ ] YouTube: rename handle @agent_afterhours → @agent_maxxing
- [ ] YouTube: configure empty channel as "Agent After Hours" at @agent_afterhours
- [ ] TikTok: rename agent.afterhours → agent_afterhours
- [ ] TikTok: rename agent.trending → agent_viral (repurposed from retired agent_trending)

### Pending Claim
- [ ] agent_maxxing — Instagram, X, Threads
- [ ] agent_afterhours — Instagram, X, Threads
- [ ] agent_pastforward — Instagram, YouTube, X, Threads
- [ ] agent_viral — Instagram, X, Threads (TikTok secured as agent.trending — rename pending)
- [ ] rillytrizzy — TikTok, Instagram, X, Threads, music platforms
- [ ] Domains: agentmaxxing.com/.co, agentafterhours.com, agentpastforward.com, agentviral.com, rillytrizzy.com
- ~~agent_trending — RETIRED. No handles to claim.~~
