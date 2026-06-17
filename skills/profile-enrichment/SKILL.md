---
name: profile-enrichment
description: "Enrich people and company profiles from emails, meetings, calendar events, and contact lists using web research, LinkedIn, and Apollo.io. Use when processing new contacts or refreshing stale profiles."
license: MIT
compatibility: "Works with any filesystem-based knowledge store. Requires: curl, Python 3, optional Jina AI Reader script, optional Chrome CDP for LinkedIn. Web search backends: DuckDuckGo (free, no key), Exa (API key), Firecrawl (API key)."
metadata:
  agentskills:
    author: Chee How Lim
    tags: [enrichment, people, companies, contacts, linkedin, apollo, research]
    categories: [contact-management, research, data-enrichment]
  hermes:
    tags: [enrichment, people, companies, contacts, linkedin, apollo, research]
---

# Profile Enrichment — Universal Enrichment Pipeline

Enrich contact profiles from any source — emails, meetings, calendar events, business cards, conference contacts, or social media exports. For each person/company discovered, research via web search and structured APIs, then write enriched profile files.

**For batch enrichment (10+ contacts):** Use parallel subagents to research 3-5 contacts each, then consolidate results.

## When to Use

- After processing email threads — enrich new external contacts
- After syncing meeting transcripts — enrich attendees
- After importing event contacts (conference lists, business cards)
- After exporting social media connections (Facebook, LinkedIn)
- For refreshing stale profiles that need updated data

## Enrichment Workflow

For each person or company discovered in the interaction:

### Step 1: Check if profile exists

Search your knowledge store for an existing profile file. Naming convention: `{firstname-lastname}.md` with path prefix `persons/` or `people/`.

If the file exists:
- Read it to see what info is already recorded (LinkedIn, role, company, etc.)
- Skip to Step 3 (add timeline entry for the new interaction)

### Step 2: Create / update person file

**Phase 1 — Web search (general intel, ~30s)**

Run a web search to get the big picture before diving into LinkedIn:

```bash
web_search "First Last Company role"
web_extract "company-website.com/about"
```

Target fields:
- **Company** — name, website, industry (confirm or discover)
- **Cross-reference** — if email says one company, web search may reveal they moved
- **Role / title** — confirm or flag discrepancies vs email signature
- **News / recent context** — recent hires, promotions, conference talks
- **Background** — education, publications, previous roles

Write findings and flag discrepancies.

**Phase 2 — LinkedIn for depth (~30-60s)**

After web search, fill career history, education, and mutual connections from LinkedIn.

**Option A: Direct profile URL lookup (fast)**

Try the direct LinkedIn URL pattern `linkedin.com/in/{firstnamelastname}` (lowercase, no spaces/hyphens):

```bash
cd /path/to/skill && python3 scripts/linkedin-profile.py "First Last"
```

The script (in `scripts/linkedin-profile.py`) tries the direct URL, falls back to search if 404.

**Option B: Browser via CDP (Chrome remote debugging)**

If Chrome is running with `--remote-debugging-port`, use Playwright or raw CDP WebSocket to navigate LinkedIn in your real logged-in session:

```python
from playwright.async_api import async_playwright

CDP_URL = "http://172.31.176.1:9222"  # Or: http://$(ip route | awk '/default/ {print $3}'):9222

async with async_playwright() as p:
    browser = await p.chromium.connect_over_cdp(CDP_URL)
    context = browser.contexts[0]
    page = await context.new_page()
    await page.goto("https://www.linkedin.com/in/username/", wait_until="domcontentloaded")
    page_text = await page.evaluate("document.body.innerText")
    print(page_text)
    await browser.close()
```

**⚠️ Chrome 148+ CDP note:** Use `window.location.href` via `Runtime.evaluate` instead of `Page.navigate` to avoid WebSocket disconnection on navigation.

**Option C: Web search fallback (when CDP unavailable)**

```bash
web_search "First Last Company linkedin"
web_search "First Last Company role title"
```

**Phase 3 — Apollo.io Enrichment (~15s, structured data)**

Use Apollo.io to fill structured data gaps (industry, revenue, employee count, phone, verified email):

**Company enrichment:**
```bash
curl -s "https://api.apollo.io/api/v1/organizations/search" \
  -H "X-Api-Key: $APOLLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q_organization_name": "Company Name", "per_page": 1}'
```

**Person enrichment (by name + domain):**
```bash
curl -s "https://api.apollo.io/api/v1/people/match" \
  -H "X-Api-Key: $APOLLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "company.com", "first_name": "First", "last_name": "Last"}'
```

**Email pattern detection:** When enriching multiple contacts from the same company, find the email pattern first from Apollo results, then apply it to contacts Apollo didn't have:
- Look up 1-2 known contacts
- Identify the pattern from verified results (e.g. `first_last@`, `first.last@`)
- Apply the most common pattern to remaining unmatched contacts

**⚠️ Apollo API key:** Set in environment as `APOLLO_API_KEY`. Key goes in `X-Api-Key` header, NOT request body. The `people/search` endpoint may be inaccessible even on paid plans — use `people/match` instead.

### Step 3: Create person profile file

Create `{path}/persons/{firstname-lastname}.md` with frontmatter:

```yaml
---
tags: [person, contact]
email: person@example.com
company: Company Name
role: Job Title
linkedin: https://linkedin.com/in/username
first_seen: YYYY-MM-DD
source: email|calendar|meeting
---
```

Include all known info: full name, email, company, role, LinkedIn URL, company website, phone if available, relationship type, first interaction context.

### Step 4: Add timeline entry

Append to the person file:

```markdown
## Timeline
- YYYY-MM-DD | [Interaction context]. [Source: Gmail / Calendar / Meeting]
```

### Step 5: Enrich company file

Also create `{path}/companies/{company-slug}.md`:

```yaml
---
tags: [company]
website: https://example.com
email_domain: @example.com
industry: 
first_seen: YYYY-MM-DD
source: email|calendar|meeting
---
```

Include web-researched data: LinkedIn company page, founder/key people, industry, financial metrics, subsidiaries, recent news.

For senior execs at a company, add a Company Profile section to the person file:

```markdown
## Company Profile
- **Company:** Full Name (Ticker)
- **Industry:** 
- **Revenue:** RM XM (X% YoY)
- **Subsidiaries:** ...
```

### Step 6: Skip rules (do NOT enrich)

- **Internal staff** — same-organization emails (your own domain)
- **System emails** — noreply, notifications, no-reply senders
- **Your own profile** — yourself in events
- **Newsletters** — unless clearly business-relevant
- **Recurring calendar events** — already enriched, just add timeline entry
- **All-day events** — "Home", "Office", "Out of office", "Birthday"

## Content Extraction — Fallback Chain

| Priority | Method | Speed | When to Use |
|----------|--------|-------|-------------|
| 1st | `web_extract` (ddgs by default) | ~5s | Fastest, works on most sites |
| 2nd | Jina AI Reader (`jina-extract.sh`) | ~5s | When web_extract errors; free, no auth |
| 3rd | Browser navigate + snapshot | ~15s | When Jina fails (JS-heavy sites) |
| 4th | Browser navigate + vision | ~15s | When SPA page (snapshot truncates) |
| 5th | Skip extraction, note in file | — | When browser also blocked (CAPTCHA) |

**When web_extract fails:**
- Common errors: `AUTH_ERROR`, `Unauthorized`, `timeout`, `402 Payment Required`, `out of credits`
- **Firecrawl credit exhaustion** — if using Firecrawl and you get "out of credits", switch to ddgs (DuckDuckGo): `hermes config set web.backend ddgs` and restart the gateway. ddgs is free with no API key or credit limits.
- Fallback: Jina AI Reader (free, no auth) — `~/.hermes/scripts/jina-extract.sh "<url>"`
- If also blocked: navigate directly with browser
- If browser also fails: skip, note "Web research unavailable — pending manual review"

## Company Website Research Tips

- Many sites (especially SPA-built) use hash-based navigation where direct subpage URLs return 404 but menu clicks work
- Try the menu/sidebar navigation first — often more reliable than guessing URL paths
- Homepages frequently contain financial highlights, subsidiary info, and news in one scrollable page
- Public companies: check investor relations or annual report sections for financial data
- Malysian/SE Asian companies: Bursa Malaysia, SGX, or exchange websites for public company data
- **Paywalled sources (EMIS, D&B Hoovers, i3investor, SimplyWallSt)** — detect quickly and move on. If extracted content is mostly login prompts/pricing, switch to free alternatives.

## Batch/Event Contact Enrichment

When contacts come from a trade show, conference, or networking event:

1. **Business card scanning** — if arriving as a photo, use vision_analyze to extract name, title, company, phone, email
2. **Create a leads tracker** file:
   ```markdown
   # {Event Name} Leads Tracker
   | # | Company | Contact | Profile Saved | Notes |
   |---|---------|---------|---------------|-------|
   | 1 | Company | Name (Role) | companies/{slug}.md | Key context |
   ```
3. **Tag all profiles** with source + event name in frontmatter:
   ```yaml
   source: event
   tag: {event-name}
   lead_owner: Your Name
   ```
4. **Create individual files** per contact/company — never a single consolidated file

## Personal Contact Enrichment (Facebook / Social Exports)

For personal contacts from social media exports:
- Use a separate output directory (e.g., `friends-and-family/` not `persons/`)
- Lighter touch: web-search-only enrichment (no LinkedIn required)
- Lighter profile template with basic contact info and relationship context

## Apollo.io Endpoint Reference

| Endpoint | Status | Returns |
|----------|--------|---------|
| `organizations/search` | ✅ Full data | industry, employees, revenue, phone, LinkedIn, keywords |
| `organizations/enrich` | ✅ Works by domain | Same enriched data |
| `people/match` | ✅ Works by name + domain | Person profile, title, email, LinkedIn, org data |
| `people/search` | ❌ Often blocked | Use `people/match` instead |

**Key: Set in env var, passed in `X-Api-Key` header (not request body).**

## Common Pitfalls

- **Never save contacts as a single file** — each person gets their own file, each company gets their own file. A single "contacts.md" is the wrong format.
- **Don't overwrite existing files** — append timeline entries, don't replace
- **Don't spend too long per person** — 2-3 minutes per person is sufficient
- **Web-first order** — search for company/role/news context first (~30s), then LinkedIn for depth (~30s)
- **Don't enrich the same person twice in a day** — check the existing file first
- **Apollo key goes in env var, never hardcode in scripts** — `APOLLO_API_KEY="$APOLLO_API_KEY" python3 script.py`
- **Apollo `people/match` using domain is preferred** over `organization_name` for disambiguation
- **Apollo also returns company data** — the `people/match` response includes a full `organization` object, often saving a separate API call
- **Apollo "verified" may use a different domain** — always inspect the actual email string returned, not just the status flag
- **Search engine blocks** — Google blocks after ~2 automated searches. When CDP is unavailable, navigate directly to company sites instead.
- **Chrome CDP must be running** — if Chrome isn't launched with `--remote-debugging-port`, CDP connection fails. Check with `curl http://GW:9222/json/version` first.
- **LinkedIn SPA timeout** — use `wait_until="domcontentloaded"` not `networkidle` (LinkedIn never finishes networkidle)
- **SPA sites** — many use single-page-app architecture. Menu clicks work but direct URLs 404. Try navigation first.
- **Paywalled data** — detect login prompts quickly and move on (i3investor, SimplyWallSt, etc.)
- **Unknown contacts** — when you can't find contact data, ask the user directly rather than searching endlessly
