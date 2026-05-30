# Agent Network — Account Playbooks
**Version:** 1.0
**Date:** 2026-05-30
**Ref:** CONTENT_STRATEGY.md, BRAND_ARCHITECTURE.md v1.1

One SOP per account. Each section is self-contained and can be handed to an operator independently.

---

## PLAYBOOK: AGENT_MAXXING

**Niche:** AI / agents / automation / productivity / future of work
**Status:** ACTIVE
**Posting target:** TikTok 1–2x/day · Instagram 1x/day · YouTube Shorts 5x/week · X 2x/day

---

### Daily Actions

1. Run source scrape: `python scraper.py --brand agent_maxxing --json clips_maxxing.json`
2. Sort output by `view_count` desc. Pick top 3 URLs.
3. Run pipeline: `python pipeline.py <url> --brands agent_maxxing` for each URL.
4. Open `output/<run>/review_queue.json`. Approve clips where `confidence >= 0.80`.
5. For approved clips: copy to `content_calendar/agent_maxxing/YYYY-MM-DD/`.
6. Post to TikTok. Repost to Instagram Reels with caption adjusted. Share clip link on X with 1-sentence opinion take.
7. Upload to YouTube Shorts (title = hook line from manifest).
8. Check X @mentions and TikTok comments — reply to top 3 relevant comments.

### Weekly Actions

- **Monday:** Plan the week — 7 clips minimum identified and queued.
- **Wednesday:** Review engagement data — what hook format is performing? Adjust next 3 clips.
- **Friday:** Identify and engage with one AI creator account (tag, comment, share) for network growth.
- **Sunday:** Newsletter segment — pick best clip of the week, write 150-word analysis, queue for next send.

### Content Sources

| Priority | Source | Method |
|---|---|---|
| 1 | YouTube: Fireship, Matt Wolfe, AI Explained, Two Minute Papers, TheAIGrid | `scraper.py --brand agent_maxxing` (T10/T11) |
| 2 | YouTube: Andrej Karpathy, Lex Fridman AI segments, Y Combinator talks | Manual search + pipeline.py URL |
| 3 | X: @sama, @karpathy, @xlr8harder, @emollick video clips | Manual embed + caption |
| 4 | Product demos: Claude, ChatGPT, Gemini new feature launches | Manual (pipeline.py URL) |

### Approval Requirements

| Condition | Action |
|---|---|
| `confidence >= 0.80` | Auto-approve for posting |
| `0.70 <= confidence < 0.80` | Human reviews before approval |
| `confidence < 0.70` | Reject or re-route |
| `copyright_risk: true` | Hold — do not post without legal clearance |
| Source is competitor's original content | Reject — use for inspiration only, not repurpose |

### Posting Workflow

```
1. TikTok: Upload vertical clip. Paste hook as on-screen text if not burned in.
   Caption: [hook] + [body] + hashtags from manifest.
   Post immediately (TikTok rewards recency).

2. Instagram Reels: Same clip. Adjust caption:
   Replace TikTok-specific phrasing with Instagram tone.
   Same hashtags. Tag related accounts where relevant.

3. YouTube Shorts: Same clip. Title = hook line (max 100 chars).
   Description: full caption + "Subscribe for daily AI content."
   Tags: pull from hashtag list (remove # prefix).

4. X: Post clip link + 1 original sentence take on the content.
   Example: "Everyone's talking about [tool]. Here's why it actually matters."
   No hashtags on X — they suppress reach.
```

### Monetization Milestones

| Milestone | Target | Action |
|---|---|---|
| 1,000 TikTok followers | Month 1–2 | Launch newsletter waitlist — link in bio |
| 5,000 TikTok followers | Month 2–3 | Approach first SaaS affiliate partner (Notion AI, Zapier) |
| 10,000 TikTok followers | Month 3–4 | Launch paid newsletter tier ($7–10/month) |
| 25,000 TikTok followers | Month 4–6 | First paid brand deal pitch |
| 50,000 TikTok followers | Month 6–9 | Launch digital product (prompt pack or automation template) |
| 100,000 TikTok followers | Month 9–12 | Launch paid community (Discord/Circle, $20–50/month) |

### Automation Opportunities

- **Scrape-to-pipeline:** Already supported. Requires T10/T11/T12 to be complete.
- **Caption variants:** Claude generates 3 caption variants per clip — operator picks one.
- **X auto-thread:** Claude drafts 3-tweet thread expanding on the clip content — operator reviews + posts.
- **Newsletter draft:** Claude generates newsletter segment from weekly top clip — operator edits.
- **Routing enforcement:** pipeline.py `--brands agent_maxxing` ensures no cross-contamination.

---

## PLAYBOOK: AGENT_AFTERHOURS

**Niche:** EDM / festivals / dance / nightlife / music culture
**Status:** ACTIVE
**Posting target:** TikTok 1x/day · Instagram 5x/week · YouTube Shorts 3x/week · X 3–4x/week

---

### Daily Actions

1. Run source scrape: `python scraper.py --brand agent_afterhours --json clips_afterhours.json`
2. Pick top 2 URLs by view count.
3. Run pipeline: `python pipeline.py <url> --brands agent_afterhours`
4. Open review queue. **Check `copyright_risk` field on EVERY clip before approving.**
5. For `copyright_risk: false` clips only: approve and copy to `content_calendar/agent_afterhours/YYYY-MM-DD/`.
6. For `copyright_risk: true` clips: hold. Determine if clip qualifies as commentary/reaction (fair use) before posting.
7. Post approved clips to TikTok. Cross-post to Instagram Reels. Upload to YouTube Shorts 3x/week (curate — not every clip).

### Weekly Actions

- **Monday:** Identify which festivals/events are happening this week. Prioritize live-event clips.
- **Wednesday:** Engage with 2–3 artist accounts (tag, comment). Artist reshares = highest reach multiplier.
- **Friday:** "Weekend drop" post — highest-energy clip of the week, timed for Friday evening.
- **Sunday:** Review TikTok sounds used in top clips — note which tracks are trending for next week's content.

### Content Sources

| Priority | Source | Method |
|---|---|---|
| 1 | YouTube: EDC Las Vegas, AriAtHome, Tomorrowland, Ultra Music Festival (official channels) | `scraper.py --brand agent_afterhours` |
| 2 | YouTube: DJ Mag, festival highlight playlists | Manual search + pipeline.py URL |
| 3 | TikTok trending festival sounds | Manual — download + pipeline.py |
| 4 | Artist official YouTube (with commentary framing) | Manual — must qualify as fair use |

### Approval Requirements

| Condition | Action |
|---|---|
| `copyright_risk: false` AND `confidence >= 0.75` | Approve |
| `copyright_risk: true` | HOLD — mandatory human review. Do not post without clearance. |
| Clip contains full song (not a drop/moment) | Reject — too high copyright exposure |
| Clip is from official festival channel | Lower risk — still review, but faster approval |
| Artist account reshared the original | Lowest risk for that specific clip |

⚠ **This account has the highest copyright exposure in the network. When in doubt, do not post.**

### Posting Workflow

```
1. TikTok: Upload vertical clip.
   Caption: "🎪 [event/artist] [hook]" + hashtags.
   Use trending sound if clip allows (check TikTok sound library first).
   Post Friday evening or Saturday for maximum reach.

2. Instagram Reels: Same clip. Adjust caption to be less TikTok-native.
   Tag the official artist/festival account — reshare potential is high.
   Use Instagram music sticker if available.

3. YouTube Shorts: Curate — only best 3 clips per week.
   Title: "[Artist/Event] — [Hook moment]"
   Description: "Best moments from [event]. Subscribe for festival highlights."

4. X: Post during or just after the event for real-time reach.
   Tag artist + festival official accounts.
   Short caption — let the clip speak.
```

### Monetization Milestones

| Milestone | Target | Action |
|---|---|---|
| 5,000 TikTok followers | Month 2–3 | Approach festival ticket affiliate programs (Insomniac, Live Nation) |
| 10,000 TikTok followers | Month 3–4 | Pitch artist manager for first paid promo |
| 25,000 TikTok followers | Month 5–6 | Launch merchandise (festival-aesthetic apparel, drop model) |
| 50,000 TikTok followers | Month 6–9 | Secure first event promotion deal |
| 100,000 TikTok followers | Month 9–12 | Approach streaming platforms (Spotify, Apple Music) for playlist placement deals |

### Automation Opportunities

- **Festival calendar sync:** Scrape Insomniac/RA event calendar to know what to look for each week.
- **Copyright pre-screen:** Add audio fingerprinting check (AudD API) before human review to auto-flag music clips.
- **Artist tag extraction:** Claude extracts artist names from transcript/title → auto-tag in caption.
- **Event-triggered scrape:** When a major festival is running (e.g., EDC), trigger a targeted scrape for live clips.

---

## PLAYBOOK: AGENT_VIRAL

**Niche:** Viral clips / broad entertainment / reaction content
**Status:** ACTIVE
**TikTok handle:** agent.trending (temporary — rename to agent_viral pending cooldown)
**Posting target:** TikTok 2–3x/day · Instagram 2x/day · YouTube Shorts daily · X 3x/day

---

### Daily Actions (at activation)

1. Run full scrape: `python scraper.py --platforms twitch kick --json clips_viral.json`
2. Also run: `python scraper.py --brand agent_viral --json clips_viral_yt.json` (YouTube search)
3. Merge and sort by `view_count` desc. Take top 15 URLs.
4. Run pipeline for each: `python pipeline.py <url> --brands agent_viral` (can be batched)
5. Review queue — approve clips with `confidence >= 0.75`. Reject anything routed elsewhere by classifier.
6. Target 3 approvals per day minimum. Copy to `content_calendar/agent_viral/YYYY-MM-DD/`.
7. Post to TikTok 3x spread across day (morning 8am, afternoon 2pm, evening 8pm).
8. Cross-post to Instagram and YouTube Shorts. Post clip link to X with minimal text.

### Weekly Actions

- **Monday:** Identify trending formats from last week — which style got most reshares?
- **Wednesday:** Check what's trending on TikTok Discover — align 2 clips to format.
- **Friday:** Top-volume post day — schedule highest-energy clip for Friday evening.
- **Sunday:** Compile weekly top performer — document hook format for future use.

### Content Sources

| Priority | Source | Method |
|---|---|---|
| 1 | Twitch top game clips (LAST_WEEK) | `scraper.py --platforms twitch` |
| 2 | Kick top clips (LAST_WEEK) | `scraper.py --platforms kick` |
| 3 | YouTube search: "unexpected viral moment", "best clip week" | `scraper.py --brand agent_viral` (T12) |
| 4 | YouTube: Sports highlights, public freak-out moments | Manual + pipeline.py URL |

### Approval Requirements

| Condition | Action |
|---|---|
| `confidence >= 0.75` AND `copyright_risk: false` | Approve |
| `confidence >= 0.75` AND `copyright_risk: true` | Human review — check for music |
| Clip is from a recognizable sports broadcast | Reject — high copyright risk |
| Clip contains NSFW content | Reject immediately |
| Clip is a duplicate of already-posted content | Reject — check content_calendar log |

### Posting Workflow

```
1. TikTok (3x/day): Spread posts across morning/afternoon/evening.
   Keep captions short — 1 hook line + 3–5 hashtags.
   Let the clip carry the content; caption is a vehicle, not the story.

2. Instagram Reels (2x/day): Morning + evening.
   Slightly longer caption than TikTok — add 1 sentence of context.

3. YouTube Shorts (daily): 1 clip per day. Best performer of the day.
   Title = hook line. Description = one-line expansion.

4. X (3x/day): Match TikTok schedule. Post clip link.
   Minimal caption — ideally a question or short reaction.
```

### Monetization Milestones

| Milestone | Target | Action |
|---|---|---|
| 10,000 TikTok followers | Month 2–3 | Enable TikTok Creator Fund |
| 25,000 TikTok followers | Month 3–4 | First consumer brand deal (gaming peripherals, food, streaming) |
| 50,000 TikTok followers | Month 5–6 | Launch meme-adjacent merchandise |
| 100,000 TikTok followers | Month 6–9 | Premium ad rates; approach brand deal agencies |
| 500,000 TikTok followers | Month 12+ | Clip licensing / content syndication deals |

### Automation Opportunities

- **Full-auto pipeline:** agent_viral has the highest automation potential. Once T05–T12 are complete, the scrape-to-queue cycle can run with minimal human input.
- **Duplicate detection:** Add content hash check to pipeline to prevent re-processing already-used clips.
- **Batch pipeline run:** Script to run pipeline.py on all URLs from clips_viral.json in sequence.
- **Posting scheduler:** Buffer or Later integration — agent_viral volume justifies scheduling tool cost.

---

## PLAYBOOK: AGENT_PASTFORWARD

**Niche:** History / forgotten technology / old predictions / future forecasting
**Status:** RESERVED (activate after agent_maxxing + agent_afterhours are stable)
**Posting target (at activation):** TikTok 5x/week · Instagram 4x/week · YouTube Shorts 3x/week · X 3x/week

---

### Daily Actions (at activation)

1. Research session (30–60 min): identify one source clip or story from Archive.org or YouTube.
2. Run pipeline if video source: `python pipeline.py <url> --brands agent_pastforward`
3. Write or record narration script (use EPISODE_TEMPLATE.md as guide).
4. Review pipeline output — approve if historical context is clear in transcript.
5. Add narration voiceover in post-processing (Descript, CapCut, or similar).
6. Export final clip to `content_calendar/agent_pastforward/YYYY-MM-DD/`.
7. Post to TikTok. Cross-post to Instagram Reels. Alternate YouTube Shorts days.

### Weekly Actions

- **Monday:** Select episode topic for the week. Assign to research queue.
- **Tuesday:** Research + scripting day. Draft narration, find clips, fill EPISODE_TEMPLATE.md.
- **Wednesday:** Production day. Record voiceover, assemble clip, burn captions.
- **Thursday/Friday:** Publish + cross-post. Engage with history/tech accounts.
- **Saturday:** Plan next week. Review episode template for following Monday.
- **Sunday:** Newsletter draft — pull from week's best content.

### Content Sources

| Priority | Source | Method |
|---|---|---|
| 1 | Archive.org Prelinger Archives (public domain) | `scraper.py --brand agent_pastforward` (T13 stub) + manual |
| 2 | YouTube: "old prediction came true", "retro futurism" | `scraper.py --brand agent_pastforward` (T12) |
| 3 | Wikimedia Commons video (CC-licensed) | Manual search + pipeline.py URL |
| 4 | NASA public domain footage | Manual — archive.org/details/nasa |
| 5 | US Government public domain (NARA, FDA, USGS archives) | Manual |

### Approval Requirements

| Condition | Action |
|---|---|
| Source is Archive.org Prelinger / US Government / NASA | Approve — public domain |
| Source is YouTube fair use (commentary + transformation) | Human review — confirm commentary is added |
| Source is CC-licensed Wikimedia | Approve — check license type (BY, SA, ND) |
| Source is commercial broadcast footage | Reject — too high copyright exposure |
| `copyright_risk: true` | Reject unless narration clearly transforms it |
| Narration voiceover is not yet recorded | Do not post — narration is required for this account |

### Posting Workflow

```
1. TikTok: Post 5x/week. Evergreen content — timing matters less than quality.
   Caption: "[hook from template]" + 3–5 hashtags (#history #retro #tech #futuretech).
   Encourage comments: "Which prediction surprised you most?"

2. Instagram Reels: 4x/week. Same clip, slightly longer caption.
   Add one additional fact not in the video — rewards followers who read.

3. YouTube Shorts: 3x/week. Best 3 clips only.
   Title: format-first ("What [era] thought [year] would look like")
   Pin comment: link to newsletter.

4. X: 3x/week. Thread format — short clip + 3 bullet facts.
   Encourages retweet for the information density.
```

### Monetization Milestones

| Milestone | Target | Action |
|---|---|---|
| 5,000 TikTok followers | Month 2–3 | Launch newsletter ("The Past Forward") — link in bio |
| 10,000 TikTok followers | Month 3–4 | Approach first education sponsor (Brilliant.org, MasterClass) |
| 25,000 TikTok followers | Month 5–6 | Launch paid newsletter tier ($5–7/month) |
| 50,000 TikTok followers | Month 6–9 | Pitch "The Fastest Timeline" as a long-form YouTube series |
| 100,000 TikTok followers | Month 9–12 | Book proposal or podcast pitch; speaking invitations |

### Automation Opportunities

- **Archive.org scraper (T13):** Once built, automates source discovery from public domain archives.
- **Research assistant:** Claude can research episode topics and draft narration scripts from a topic prompt.
- **Narration generation:** ElevenLabs or similar for synthetic voiceover — reduces production time from 60 min to 10 min.
- **Caption burn automation:** ffmpeg caption overlay is already in pipeline.py — narration script feeds directly into caption file.
- **Series tagging (T17):** pipeline.py `series` field allows "Fastest Timeline" clips to be tracked separately from standalone posts.
