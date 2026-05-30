# Agent Network — Activation Checklist
**Version:** 1.0
**Date:** 2026-05-30
**Ref:** STATUS.md, CURRENT_STATE.md, ACCOUNT_REGISTRY.md

Complete in order. Each section unlocks the next.

---

## SECTION 1 — API KEYS

Must be completed before any pipeline smoke test.

- [ ] Open `.env` in a text editor (never share or commit this file)
- [ ] Add `OPENAI_API_KEY=<your_key>` — get from platform.openai.com/api-keys
- [ ] Add `ANTHROPIC_API_KEY=<your_key>` — get from console.anthropic.com/settings/keys
- [ ] Verify keys loaded without printing values:
  ```bash
  python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OPENAI:', bool(os.getenv('OPENAI_API_KEY'))); print('ANTHROPIC:', bool(os.getenv('ANTHROPIC_API_KEY')))"
  ```
  Expected output: `OPENAI: True` / `ANTHROPIC: True`
- [ ] Confirm `.env` is in `.gitignore` — never commit key values

---

## SECTION 2 — HANDLE CLAIMS

No cooldown blocking these — can be done today.

### Instagram
- [ ] Claim `agent_maxxing` on Instagram
- [ ] Claim `agent_afterhours` on Instagram
- [ ] Claim `agent_viral` on Instagram
- [ ] Claim `agent_pastforward` on Instagram (RESERVED — claim now, post later)
- [ ] Claim `rillytrizzy` on Instagram (verify current status — was @agent_rillytrizzy)

### X (Twitter)
- [ ] Claim `agent_maxxing` on X — note: @agentmaxxing (no underscore) is taken; @agent_maxxing (underscore) is distinct and claimable
- [ ] Claim `agent_afterhours` on X
- [ ] Claim `agent_viral` on X
- [ ] Claim `agent_pastforward` on X
- [ ] Claim `rillytrizzy` on X

### Threads
- [ ] Claim `agent_maxxing` on Threads
- [ ] Claim `agent_afterhours` on Threads
- [ ] Claim `agent_viral` on Threads
- [ ] Claim `agent_pastforward` on Threads
- [ ] Claim `rillytrizzy` on Threads

### Domains
- [ ] Check `agentmaxxing.com` — if available, claim immediately (concept spreading fast)
- [ ] Check `agentmaxxing.co` — listed for sale on Spaceship; purchase as fallback
- [ ] Check and claim `agentafterhours.com`
- [ ] Check and claim `agentpastforward.com`
- [ ] Check and claim `agentviral.com`
- [ ] Check and claim `rillytrizzy.com` (after core network domains secured)

### After Claiming Each Handle
- [ ] Update STATUS.md — change `CLAIM NEEDED` to `SECURED` for each completed handle
- [ ] Update ACCOUNT_REGISTRY.md — change `Claim needed` to `SECURED` for each row

---

## SECTION 3 — COOLDOWN RENAMES

Check daily. Rename immediately when cooldown clears — do not wait.

### YouTube
- [ ] Daily: Check YouTube Studio → Settings → Channel → Handle
- [ ] When available: Rename handle `@agent_afterhours` → `@agent_maxxing` on Agent Maxxing channel
- [ ] After Agent Maxxing rename completes: Configure empty channel as "Agent After Hours" at `@agent_afterhours`
- [ ] Update STATUS.md YouTube table when each rename completes

### TikTok
- [ ] Daily: Check TikTok Profile → Edit → Username for both accounts
- [ ] When available: Rename `agent.afterhours` → `agent_afterhours`
- [ ] When available: Rename `agent.trending` → `agent_viral` (this is the repurposed account — NOT agent_trending, which is RETIRED)
- [ ] Update STATUS.md TikTok table when each rename completes

> **agent_trending is RETIRED.** The `agent.trending` TikTok account is being repurposed as `agent_viral`. Do not rename it to agent_trending under any circumstances.

---

## SECTION 4 — SMOKE TEST

Run after Section 1 (API keys) is complete. Sections 2 and 3 can be in progress.

```bash
# Step 1: Confirm environment
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OPENAI:', bool(os.getenv('OPENAI_API_KEY'))); print('ANTHROPIC:', bool(os.getenv('ANTHROPIC_API_KEY')))"

# Step 2: Run pipeline — agent_maxxing only, 30-second clips
python pipeline.py <test_youtube_url> --brands agent_maxxing --clip-duration 30

# Step 3: Inspect review queue
cat output/<run_id>/review_queue.json | python -m json.tool | head -60

# Step 4: Verify governance — no clip auto-approved (this must pass)
python -c "import json; q=json.load(open('output/<run_id>/review_queue.json')); assert all(not c['approved'] for c in q['clips']); print('PASS: no auto-approvals')"

# Step 5: Verify copyright_risk field present on all clips
python -c "import json; q=json.load(open('output/<run_id>/review_queue.json')); assert all('copyright_risk' in c for c in q['clips']); print('PASS: copyright_risk field present')"
```

**Acceptance criteria:**
- [ ] Pipeline runs without exception
- [ ] At least 1 clip generated in review queue
- [ ] All clips have `approved: false` (governance check)
- [ ] All clips have `copyright_risk` field
- [ ] Clip routed to `agent_maxxing` (not another account)
- [ ] Hook and caption present and non-empty

**After smoke test passes:**
- [ ] Run agent_afterhours smoke test: `python pipeline.py <test_url> --brands agent_afterhours`
- [ ] Verify `copyright_risk` flagging works — use a music URL; expect `copyright_risk: true`
- [ ] Run agent_viral smoke test: `python pipeline.py <test_url> --brands agent_viral`
- [ ] Mark smoke test COMPLETE in STATUS.md Phase 3 checklist

---

## SECTION 5 — FIRST CONTENT BATCH

Begin after smoke test passes. Use scraper to find source material, pipeline to process, human to approve.

### Setup
- [ ] Create today's date folders:
  ```bash
  mkdir -p content_calendar/agent_maxxing/2026-05-30
  mkdir -p content_calendar/agent_afterhours/2026-05-30
  mkdir -p content_calendar/agent_viral/2026-05-30
  ```

### agent_viral (highest volume — 3 clips/day target)
- [ ] Run: `python scraper.py --platforms twitch kick --json clips_viral.json`
- [ ] Run: `python scraper.py --brand agent_viral --json clips_viral_yt.json`
- [ ] Select top 5 URLs by view count
- [ ] Run pipeline on each: `python pipeline.py <url> --brands agent_viral`
- [ ] Review each queue — approve clips with `confidence >= 0.75` AND `copyright_risk: false`
- [ ] Copy 3 approved clips to `content_calendar/agent_viral/2026-05-30/`
- [ ] Post: TikTok (1), Instagram Reels (1), YouTube Shorts (1), X (1) — one clip at a time

### agent_maxxing (1–2 clips/day target)
- [ ] Run: `python scraper.py --brand agent_maxxing --json clips_maxxing.json`
- [ ] Select top 3 URLs
- [ ] Run pipeline: `python pipeline.py <url> --brands agent_maxxing`
- [ ] Review queue — approve clips with `confidence >= 0.80` only
- [ ] Copy 1–2 approved clips to `content_calendar/agent_maxxing/2026-05-30/`
- [ ] Post: TikTok, Instagram Reels, YouTube Shorts, X

### agent_afterhours (1 clip/day target — highest copyright risk)
- [ ] Run: `python scraper.py --brand agent_afterhours --json clips_afterhours.json`
- [ ] Select top 2 URLs
- [ ] Run pipeline: `python pipeline.py <url> --brands agent_afterhours`
- [ ] Review queue — check `copyright_risk` on EVERY clip before approving
  - `copyright_risk: true` → HOLD. Do not post under any circumstances.
  - `copyright_risk: false` AND `confidence >= 0.75` → approve
- [ ] Copy 1 cleared clip to `content_calendar/agent_afterhours/2026-05-30/`
- [ ] Post evening: TikTok, Instagram Reels — tag artist/festival account where relevant

---

## SECTION 6 — FIRST 100 POSTS MILESTONE

**Definition:** 100 total published posts across agent_maxxing, agent_afterhours, and agent_viral combined.

| Account | Allocation | Progress |
|---|---|---|
| agent_maxxing | 35 posts | [ ] |
| agent_afterhours | 25 posts | [ ] |
| agent_viral | 40 posts | [ ] |
| **TOTAL** | **100** | **0 / 100** |

**Estimated time:** ~2 weeks at full frequency (~85 posts/week network-wide).

### Tracking Method
Each published post = one file in `content_calendar/<account>/YYYY-MM-DD/`. Count files to track progress:
```bash
find content_calendar/agent_maxxing -type f -not -name "*.md" | wc -l
find content_calendar/agent_afterhours -type f -not -name "*.md" | wc -l
find content_calendar/agent_viral -type f -not -name "*.md" | wc -l
```

### Milestone Completion Criteria
- [ ] 35 posts published from agent_maxxing
- [ ] 25 posts published from agent_afterhours
- [ ] 40 posts published from agent_viral
- [ ] Pipeline approval workflow validated under real posting conditions
- [ ] Copyright workflow validated — no flagged clips posted
- [ ] Cross-posting workflow validated across TikTok, Instagram, YouTube Shorts, X

### After Milestone Is Reached
- [ ] Activate agent_pastforward — begin posting from `content_calendar/agent_pastforward/fastest_timeline/`
- [ ] Evaluate pipeline performance — refine confidence thresholds if routing accuracy is low
- [ ] Begin newsletter content queue from best clips (agent_maxxing + agent_pastforward)

---

**CURRENT STATUS:** Awaiting Section 1 (API Keys) to unblock Section 4 (Smoke Test).
**Sections 2 & 3** (Handle Claims + Cooldown Renames) have no dependencies — begin immediately.
