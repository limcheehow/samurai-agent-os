---
name: client-meeting-prep
description: "Prepare structured briefings for client and prospect meetings. Research the company, key contacts, recent news, competitive context, and past interactions. Use before any sales call or meeting."
license: MIT
---

# Client Meeting Prep

Produces a structured briefing document before every client or prospect meeting. Research-heavy — use web search, Apollo.io, and the company website to build a complete picture.

## Flow

### 1. Gather Context
Ask the user (or extract from the request):
- **Company name** (required)
- **Meeting type** — intro call / demo / proposal / QBR / negotiation / other
- **Attendees** — who is joining from their side, who from our side
- **Goal** — what does success look like for this meeting
- **Past interactions** — check deals directory and activity log for history

### 2. Research
Run parallel research:
- **Company overview** — website, Crunchbase/LinkedIn, recent funding, size, industry
- **News and signals** — last 90 days: product launches, leadership changes, funding, partnerships
- **Competitive context** — who are their competitors, where do we fit
- **Key contacts** — LinkedIn profiles of attendees, roles, tenure, background
- **Apollo.io enrichment** — firmographics, tech stack, headcount

### 3. Past Deal History
Check your deals directory for:
- Previous deals with this company (any stage)
- Past proposals, quotes, pricing discussed
- Outstanding tasks or follow-ups
- Activity log mentions

### 4. Build Briefing
Output as markdown in a briefings directory:

```markdown
---
company: <name>
date: <YYYY-MM-DD>
type: <intro|demo|proposal|qbr|negotiation>
attendees_them: <names>
attendees_us: <names>
goal: <one-liner>
---

# Briefing: <Company> — <Date>

## Company Snapshot
- **Industry**: ...
- **Size**: ...
- **Funding**: ...
- **Recent news**: ...

## Attendees
| Name | Role | Tenure | Notes |
|---|---|---|---|

## Past Interactions
- ...

## Key Talking Points
1. ...
2. ...

## Risks / Landmines
- ...

## Questions to Ask
- ...

## Next Steps Target
- ...
```

## Rules
- **Source everything** — link to articles, profiles, Crunchbase
- **Be current** — prioritize news from last 90 days
- **Flag risks** — competitive relationships, budget timing, org changes
- **Keep it actionable** — the briefing should directly inform the conversation
- **Save briefings** — never lose prep work, it builds institutional knowledge