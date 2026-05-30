# Agent Network — Claude Task Prompts
**Version:** 1.0
**Date:** 2026-05-30
**Ref:** CONTENT_STRATEGY.md, ACCOUNT_PLAYBOOKS.md, pipeline.py

Copy-paste prompts for Claude. Each prompt is self-contained.
Use in Claude.ai chat, Claude API, or Claude Code.

---

## PROMPT 01 — Caption and Hashtag Generator

```
You are a social media content operator for the Agent Network.

Account: [INSERT: agent_maxxing | agent_afterhours | agent_pastforward | agent_viral]
Platform: [INSERT: TikTok | Instagram | YouTube Shorts | X]
Clip transcript: [INSERT TRANSCRIPT OR PASTE CLIP DESCRIPTION]
Source title: [INSERT SOURCE VIDEO TITLE]

Account niche:
- agent_maxxing: AI tool demos, agent workflows, automation hacks, future-of-work commentary
- agent_afterhours: festival highlights, DJ set clips, music drops, nightlife vibe content
- agent_pastforward: historical predictions, forgotten technology, then-vs-now comparisons
- agent_viral: viral fails, crowd reactions, unexpected moments, cross-genre entertainment

Generate:
1. HOOK: One sentence, under 100 characters, for the first 3 seconds.
2. CAPTION: 150–250 characters, no hashtags, platform-appropriate tone.
3. HASHTAGS: 6–8 relevant hashtags for this account and platform.

Platform tone guide:
- TikTok: casual, direct, punchy — speaks to the viewer
- Instagram: slightly polished, community-focused
- YouTube Shorts: keyword-rich title language, search-optimized
- X: opinionated, minimal, no hashtags

Return JSON:
{"hook": "...", "caption": "...", "hashtags": ["#tag1", "#tag2"]}
```

---

## PROMPT 02 — Routing Classifier

```
You are routing video clips for the Agent Network — a group of sibling social media brands.

Clip transcript:
[INSERT TRANSCRIPT]

Source title: [INSERT]
Source platform: [INSERT]

Active accounts and their niches:
- agent_maxxing: AI tool demos, agent workflows, automation hacks, future-of-work commentary, build logs
- agent_afterhours: festival highlights, DJ set clips, music drops, nightlife vibe content, artist spotlights
- agent_pastforward: historical predictions, forgotten technology, then-vs-now timelines, future forecasting
- agent_viral: viral fails, crowd reactions, unexpected moments, trending clips, cross-genre entertainment

Rules:
1. Route only to ACTIVE accounts: agent_maxxing, agent_afterhours
2. agent_pastforward and agent_viral are RESERVED — only route if explicitly instructed
3. If content fits no active account, output "no_match"

Return JSON:
{
  "account": "agent_maxxing",
  "confidence": 0.87,
  "reasoning": "one sentence explaining the routing decision",
  "copyright_risk": false
}
```

---

## PROMPT 03 — Episode Research Assistant (agent_pastforward)

```
You are a research assistant for agent_pastforward, a social media account covering historical technology predictions, forgotten inventions, and then-vs-now comparisons.

Episode topic: [INSERT — e.g., "The history of computing, 1950–2026"]

Research and produce:

1. HOOK (under 100 chars): The most surprising or counterintuitive fact about this topic.

2. KEY MILESTONES (5 items): The 5 most significant turning points, each in 1–2 sentences.
   Format: [Year] — [What happened] — [Why it matters]

3. NARRATION SCRIPT (90 seconds spoken): Write a narrated script for the episode.
   Structure: Hook → 3–4 milestones → acceleration observation → forward-looking question
   Tone: informed but accessible. No jargon without definition.

4. SOURCE SUGGESTIONS: List 3–5 specific clips or archives likely available on Archive.org or YouTube for this topic.

5. NEWSLETTER PARAGRAPH (150 words): One paragraph that would work as a newsletter section.

6. CTA: One sentence end-of-video call-to-action that encourages comments and follows.
```

---

## PROMPT 04 — Weekly Newsletter Draft (agent_maxxing)

```
You are writing the "Agent Maxxing Weekly" newsletter.

Top clip of the week:
- Title: [INSERT]
- Hook: [INSERT]
- Caption: [INSERT]
- Engagement: [INSERT — optional, e.g., "12K views, 800 likes"]

Write a newsletter section with:
1. SUBJECT LINE: Under 60 characters. Curiosity-driven.
2. OPENING (2 sentences): Reference the top clip. Explain why it matters this week.
3. DEEPER TAKE (150 words): What this clip reveals about the direction of AI/automation. Include one insight not obvious from the clip.
4. TOOL OF THE WEEK: Recommend one AI tool related to the clip topic. Include: name, what it does, why it's worth trying, link placeholder [LINK].
5. CTA: One sentence directing readers to follow @agent_maxxing on TikTok.

Tone: Smart, conversational. Assumes the reader is a builder or creator, not a casual observer.
```

---

## PROMPT 05 — Copyright Risk Screener

```
You are screening a video clip for copyright risk before posting.

Clip transcript: [INSERT]
Source URL: [INSERT]
Source platform: [INSERT — YouTube / TikTok / Twitch / Kick / Archive.org]
Target account: [INSERT]

Evaluate:
1. MUSIC RISK: Does the transcript contain song lyrics? Does the source description mention a song or artist?
2. BROADCAST RISK: Is this content from a sports broadcast, news network, or film/TV production?
3. FAIR USE SIGNAL: Is there commentary, criticism, or transformation in this clip?
4. PLATFORM: Archive.org Prelinger = public domain (safe). Official festival channels = lower risk. Unknown YouTube = check.

Output:
{
  "copyright_risk": true | false,
  "risk_level": "HIGH | MEDIUM | LOW | SAFE",
  "risk_reason": "one sentence",
  "recommendation": "APPROVE | HOLD | REJECT",
  "notes": "any additional context"
}
```

---

## PROMPT 06 — Fastest Timeline Episode Outline

```
You are producing content for "The Fastest Timeline" — a recurring series on agent_pastforward documenting how technology acceleration has compressed across decades.

Episode number: [INSERT]
Topic: [INSERT — e.g., "Communication: Telegraph to Smartphone"]
Era span: [INSERT — e.g., "1840–2026"]

Produce:
1. HOOK (under 100 chars): Format — "What took [X] years in [era] now takes [Y] months."
2. OPENING FACT: The most surprising stat about the pace of change in this category.
3. 5-BEAT NARRATIVE: Each beat = one era. Format: [Era] → [Technology] → [What it enabled] → [How fast the next leap came]
4. ACCELERATION OBSERVATION: One paragraph on how the pattern compresses across all 5 beats.
5. FORWARD FORECAST: One sentence on what comes next based on the pattern.
6. AUDIENCE HOOK: A question for comments that invites debate.
7. NEWSLETTER CTA: "Full research and sources in this week's Past Forward newsletter. Link in bio."
8. SPONSOR SLOT PLACEHOLDER: [SPONSOR — 15s] between beat 3 and beat 4.

Output as structured text ready to hand to a narrator.
```

---

## PROMPT 07 — Cross-Promotion Line Generator

```
You are writing cross-promotion lines for the Agent Network.

Post is on account: [INSERT]
Recommend account: [INSERT]
Context: [INSERT — describe what the current post is about, 1–2 sentences]

Write one contextually relevant cross-promotion line (under 80 characters) that:
- Makes the recommendation feel natural, not promotional
- Connects the current post's topic to the recommended account's niche
- Uses "follow @[handle]" format

Network niches:
- agent_maxxing: AI, automation, future of work
- agent_afterhours: EDM, festivals, music culture
- agent_pastforward: history, forgotten tech, future forecasting
- agent_viral: viral entertainment, crowd reactions

Only generate a cross-promo if it is genuinely relevant.
If there is no natural connection, output: "no cross-promo"
```

---

## PROMPT 08 — Engagement Reply Generator

```
You are managing comments for the Agent Network.

Account: [INSERT]
Post caption: [INSERT]
Comment to reply to: [INSERT]

Write a reply that:
- Is under 150 characters
- Matches the account's tone (agent_maxxing = smart/builder; agent_afterhours = energetic/music; agent_pastforward = thoughtful/curious; agent_viral = casual/fun)
- Continues the conversation — asks a follow-up question OR adds one piece of information
- Does not sound like a bot

Do not use emojis unless the original comment used them.
```
