---
name: deal-project-activity-sync
description: "Bridge email activity into deal/project pages. Matches senders to contacts, adds timeline entries to linked deals, detects stale/at-risk deals, and creates follow-up tasks."
license: MIT
---

# Deal/Project Activity Sync

After email ingestion, bridge inbox activity into deal and project pages so they reflect real communication — not just manual CRM data entry.

## What It Does

For each new email discovered:

1. **Extract sender** from the email's `from` field
2. **Match to contact** in your contacts directory by email
3. **Find linked deals/projects** that reference this contact
4. **Add timeline entry** to each deal page: `- YYYY-MM-DD | Email from <sender>: <subject>`
5. **Risk detection** per deal/project:
   - Yellow — Stalled: no activity > 7 days
   - Red — Cold: Qualified deal with no activity > 14 days
   - Yellow — On Hold: deal stuck with no decision
   - Red — Overdue: target date passed
   - Gray — No target date: project missing completion target
6. **Task creation** for high-risk items: adds `- [ ] <reason> — <suggestion>` to `## Tasks`
7. **Notify owner** (optional) — DM or notify deal/project owner about risks

## Usage

```bash
# Dry run — preview what would change
python3 sync-deal-activity.py --dry-run

# Live run — update deal/project pages
python3 sync-deal-activity.py

# Live run + notify owners
python3 sync-deal-activity.py --notify
```

## Cron Job Example

```
hermes cron create \
  --name "deal-project-activity-sync" \
  --schedule "35 8-19 * * 1-5" \
  --script sync-deal-activity.py \
  --no-agent \
  --deliver local
```

## Owner → Notification Mapping

Configure your team's notification IDs (Slack, Telegram, etc.) in your script:

```
OWNER_NOTIFY = {
    "Alice": "U01ABCDEF",
    "Bob": "U02GHIJKL",
}
```

Add new owners as your team grows.

## Risk Thresholds

| Threshold | Value | Effect |
|-----------|-------|--------|
| `STALL_DAYS` | 7 | Deal with no activity > 7d → risk + task |
| `COLD_DAYS` | 14 | Qualified deal with no activity > 14d → risk + task |
| `OVERDUE_DAYS` | 7 | Project past target date → risk + note |

Adjust in the script header.

## Dependencies

- Python stdlib only (no pip packages)
- Uses agent's messaging tools for notifications
- Reads from email data directory, writes to deals/projects directories

## Pitfalls

- **Weekend emails may have 0 matches** — automated emails (newsletters, notifications) don't have contact profiles. This is normal.
- **Contact must match** — the email `from` address must match a contact profile's `email` field exactly (case-insensitive).
- **Deal/project linking** — the deal page must reference the contact. If the deal was created before contacts were set up, the link may be missing.
- **Timeline dedup** — entries already present in the timeline are skipped (no duplicates).