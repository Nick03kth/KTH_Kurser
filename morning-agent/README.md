# SL morning agent

Every morning the GitHub Actions workflow
[`.github/workflows/morning-agent.yml`](../.github/workflows/morning-agent.yml)
runs [`sl_morning_agent.py`](sl_morning_agent.py), which **emails a concise,
mobile-friendly HTML card view** to nick050408@gmail.com and archives the
text version as a GitHub issue.

The agent fetches **live SL departures for every route** from
Landsnoravägen 97 → Regeringsgatan 25, chains each into a realistic
itinerary, and works out when you must **leave home** to be at
Regeringsgatan 25 by **07:25** (for the daily 07:30 meeting):

- **R1 Pendeltåg** — drive to the **Malla Silfverstolpes väg** stop & park,
  bus 607/627 → Sollentuna, pendeltåg 40/41 → Stockholm City, exit Sergels
  torg, walk to Regeringsgatan 25.
- **R2 Direct bus 697** — bus 697 → Stockholm C (no transfer), walk.
- **R3 Metro** — bus 607 → Danderyds sjukhus, metro 14 → Östermalmstorg,
  exit Birger Jarlsgatan, walk.
- **R4 Drive** — drive the whole way, park at Parkaden (fallback).

Each route shows a status dot (🟢/🟡/🔴), **leave-home / arrive / margin**,
the **last safe departure** that still makes 07:25, the next departures, and
a **tap-to-navigate Google Maps** link. The single best route is highlighted
at the top with a big "Leave HH:MM" hero. Board times are live (so
cancellations show up); ride/walk legs are estimates.

If GitHub runs the job late (after 07:25) the email switches to a plain
"next departures" live-board view instead of showing everything as missed.

## Email delivery

The script sends the report directly via Gmail SMTP, so it lands in your
inbox regardless of GitHub notification settings. Requires one repo secret
`GMAIL_APP_PASSWORD` (Google Account → Security → App passwords → Mail).
Without it the report still prints and is archived as a GitHub issue, but
no email is sent. The subject line shows the verdict at a glance, e.g.
`✅ SL Mon 22 Jun – Leave 06:48 (Pendeltåg via Sollentuna)`.

## Testing

Run it manually anytime (prints the text version; writes `report.html`):

```bash
python3 morning-agent/sl_morning_agent.py
```

or trigger the workflow from the Actions tab (**SL morning agent → Run
workflow**). Manual runs always send.

## Scheduling reliability

GitHub spreads scheduled runs and can delay them by minutes to hours on
free accounts, so the workflow fires several cron triggers across the
05:00–08:00 window and a workflow-level dedup check (by issue title) makes
the first successful run of the day the only one that sends. GitHub disables
schedules in repos with no activity for 60 days (a single commit re-enables
them).
