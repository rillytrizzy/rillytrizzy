# Agent Network — Daily Operator Checklist
**Version:** 1.0
**Date:** 2026-05-30
**Ref:** ACCOUNT_PLAYBOOKS.md, CONTENT_PIPELINE.md

Run this checklist once per day. Estimated time: 45–90 minutes total.
Accounts still in RESERVED status are included for monitoring only — skip posting steps.

---

## MORNING BLOCK (15–20 min) — 8:00–9:00 AM

### Pipeline Health
- [ ] Verify `.env` contains `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`
- [ ] Confirm no failed runs in `output/` from overnight (check for empty clip folders)
- [ ] Check disk space — `output/` accumulates fast; archive or delete runs older than 7 days

### Handle / Cooldown Check
- [ ] Check YouTube Studio — is handle rename to @agent_maxxing available yet?
- [ ] Check TikTok Profile → Edit → Username — are cooldowns released for agent.afterhours and agent.trending?
- [ ] If cooldown released: rename immediately, update STATUS.md checklist

### Agent Viral — Source Scrape
- [ ] Run: `python scraper.py --platforms twitch kick --json clips_viral.json`
- [ ] Run: `python scraper.py --brand agent_viral --json clips_viral_yt.json`
- [ ] Note top 10 URLs by view count for pipeline batch

### Agent Maxxing — Source Scrape
- [ ] Run: `python scraper.py --brand agent_maxxing --json clips_maxxing.json`
- [ ] Note top 3 URLs for pipeline

---

## MID-MORNING BLOCK (20–30 min) — 9:00–10:30 AM

### Run Pipelines

**Agent Viral (run 3–5 URLs):**
```bash
python pipeline.py <url1> --brands agent_viral
python pipeline.py <url2> --brands agent_viral
python pipeline.py <url3> --brands agent_viral
```
- [ ] Review `output/<run_id>/review_queue.json` for each run
- [ ] Approve clips with `confidence >= 0.75` AND `copyright_risk: false`
- [ ] Copy approved clips to `content_calendar/agent_viral/YYYY-MM-DD/`

**Agent Maxxing (run 2–3 URLs):**
```bash
python pipeline.py <url1> --brands agent_maxxing
python pipeline.py <url2> --brands agent_maxxing
```
- [ ] Review queue — approve `confidence >= 0.80` only
- [ ] Copy approved clips to `content_calendar/agent_maxxing/YYYY-MM-DD/`

---

## POSTING BLOCK (20–30 min) — 12:00–1:00 PM

### Agent Viral — Post 1 of 3 (midday)
- [ ] Upload approved clip to TikTok
- [ ] Cross-post to Instagram Reels
- [ ] Upload to YouTube Shorts (daily pick)
- [ ] Post clip link to X

### Agent Maxxing — Post 1 of 1–2 (midday)
- [ ] Upload approved clip to TikTok
- [ ] Cross-post to Instagram Reels
- [ ] Upload to YouTube Shorts
- [ ] Post clip link to X with original 1-sentence take

---

## AFTERNOON BLOCK (10–15 min) — 2:00–3:00 PM

### Agent Afterhours — Source + Pipeline
- [ ] Run: `python scraper.py --brand agent_afterhours --json clips_afterhours.json`
- [ ] Pick top 2 URLs. Run pipeline:
  ```bash
  python pipeline.py <url1> --brands agent_afterhours
  ```
- [ ] Review queue — **check `copyright_risk` on every clip before approving**
- [ ] `copyright_risk: true` → HOLD. Do not post.
- [ ] Copy cleared clips to `content_calendar/agent_afterhours/YYYY-MM-DD/`

### Agent Viral — Post 2 of 3 (afternoon)
- [ ] Post second clip to TikTok + Instagram

---

## EVENING BLOCK (10–15 min) — 7:00–9:00 PM

### Agent Afterhours — Post
- [ ] Upload cleared clip to TikTok
- [ ] Cross-post to Instagram Reels
- [ ] Tag artist/festival account where relevant

### Agent Viral — Post 3 of 3 (evening)
- [ ] Post third clip to TikTok + Instagram + X

### Agent Maxxing — Post 2 (evening, if 2x/day)
- [ ] Post second approved clip to TikTok + X

### Engagement Check (all active accounts)
- [ ] Reply to top 3 TikTok comments on today's posts
- [ ] Like and reply to relevant @mentions on X
- [ ] Check Instagram DMs — respond to any partnership or collaboration inquiries

---

## WEEKLY ACTIONS (add to Monday and Friday)

### Every Monday
- [ ] Review last week's top performer per account (most views, most shares)
- [ ] Document winning hook format in `content_calendar/<account>/WEEK_NOTES.md`
- [ ] Queue 7 clip sources per active account for the week
- [ ] Agent Pastforward: assign episode topic for the week; begin research

### Every Friday
- [ ] Post highest-energy clip of the week to agent_viral (evening timing)
- [ ] Post festival/event clip to agent_afterhours (Friday evening — peak reach)
- [ ] Update `STATUS.md` checklist — mark completed items
- [ ] Check domain registrar — any of the 7 domains now available?

### Every Sunday
- [ ] Draft newsletter content from week's best clip (agent_maxxing)
- [ ] Draft newsletter content from week's history episode (agent_pastforward)
- [ ] Archive `output/` runs older than 7 days to `archive/` or delete
- [ ] Confirm next week's queue is populated

---

## RESERVED ACCOUNT MONITORING

These accounts are not yet posting. Monitor handle status only.

| Account | Check | Action If Issue |
|---|---|---|
| agent_pastforward | TikTok handle still `agent_pastforward`? | Log in; verify username unchanged |
| agent_viral | TikTok account created yet? | If not, create on TikTok immediately |
| agent_trending | TikTok handle still `agent.trending`? | Check cooldown status; rename when available |

---

## INCIDENT LOG

If something goes wrong, document it here:

```
Date: YYYY-MM-DD
Account: agent_maxxing
Issue: Pipeline returned 0 clips for URL
Action taken: Tried 3 alternative URLs; found 2 clips from different source
Resolution: Posted 1 clip; flagged original URL as broken
```

---

## QUICK COMMAND REFERENCE

```bash
# Run full viral scrape
python scraper.py --platforms twitch kick --json clips_viral.json

# Run brand-specific YouTube search
python scraper.py --brand agent_maxxing --json clips_maxxing.json

# Run pipeline for one URL, one brand
python pipeline.py <url> --brands agent_maxxing --clip-duration 45

# Run pipeline for custom clip length
python pipeline.py <url> --brands agent_viral --clip-duration 30

# Check what's in a review queue
python -c "import json; q=json.load(open('output/<run_id>/review_queue.json')); [print(c['clip'], c['account'], c['confidence'], 'RISK' if c.get('copyright_risk') else 'OK') for c in q['clips']]"
```
