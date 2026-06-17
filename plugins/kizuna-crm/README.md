# Kizuna CRM Plugin

A Hermes plugin that ships the complete CRM management persona — deal tracking, contact management, meeting prep, pipeline analytics, and deal activity sync.

## Install

```bash
hermes plugins install limcheehow/samurai-agent-os
hermes plugins enable kizuna-crm
```

## What's Included

| Skill | Description |
|-------|-------------|
| `crm-assistant` | Deal registration, pipeline, contacts, companies, tasks |
| `client-meeting-prep` | Research briefings before every sales call |
| `deal-project-activity-sync` | Email → deal timeline + stale deal detection |
| `domain-intel` | Passive domain recon (WHOIS, DNS, SSL) |

Also bundle `profile-enrichment` from the repo's skills directory.

## Prerequisites

- Python 3.10+
- Optional: Apollo.io API key (for company/person enrichment)
- Optional: Chrome CDP (for LinkedIn scraping)
- Set `APOLLO_API_KEY` in your environment for enrichment

## Persona Activation

Add Kizuna's voice to a channel prompt in your `config.yaml`:

```yaml
telegram:
  channel_prompts:
    <YOUR_CHAT_ID>: |
      You are Kizuna (絆), CRM Manager.
      Warm professional, proactive, research-driven.
      ALLOWED: crm-assistant, client-meeting-prep, profile-enrichment
```

## Files

- `SOUL.md` — Persona definition
- `plugin.yaml` — Plugin manifest
- `__init__.py` — Skill registration
- `skills/` — 4 bundled skills