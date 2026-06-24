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

## Reliable 06:00 delivery (one-time setup, ~3 min)

**Why this is needed:** GitHub Actions `schedule` triggers are unreliable —
on this repo every scheduled run has fired **39 minutes to 6 hours late**,
and never before 06:00. GitHub deprioritises cron on free/low-traffic
repos and this will not improve. So 06:00-sharp delivery must come from an
**external minute-accurate trigger** that *dispatches* the workflow via the
GitHub API (dispatch events start within seconds, unlike `schedule`).

Set up a free [cron-job.org](https://cron-job.org) job:

1. **Create a GitHub token** at
   https://github.com/settings/personal-access-tokens/new
   - Fine-grained token, **Resource owner:** Nick03kth, **Repository
     access:** Only select repositories → `KTH_Kurser`.
   - **Permissions → Contents: Read and write** (this is what the
     `repository_dispatch` API needs). Leave the rest default.
   - Generate and copy the token (`github_pat_…`).
2. **Create the cron job** at https://console.cron-job.org → *Create cronjob*:
   - **URL:** `https://api.github.com/repos/Nick03kth/KTH_Kurser/dispatches`
   - **Schedule:** every weekday (Mon–Fri) at **06:00**, timezone
     **Europe/Stockholm**.
   - **Request method:** `POST`
   - **Headers:**
     - `Accept: application/vnd.github+json`
     - `Authorization: Bearer github_pat_…` (your token)
     - `X-GitHub-Api-Version: 2022-11-28`
   - **Body:** `{"event_type":"morning-run"}`
   - Save. (Optional: enable failure notifications so you know if it ever
     can't reach GitHub.)

That's it — at 06:00 every weekday cron-job.org pokes GitHub, the workflow
starts within seconds, and the email arrives ~06:00. The script sends
immediately; no time guard.

**Safety net:** the workflow also keeps a few weekday `schedule` crons as a
backup. If the external trigger ever fails, a backup run still sends the
report later that morning, with the subject prefixed `⏰ [delayed backup]`
so you can tell it apart. Dedup guarantees you never get two emails, and
the job only runs Mon–Fri. To get *only* the on-time send and never a late
backup, delete the `schedule:` block from the workflow.

GitHub disables `schedule` triggers in repos with no commits for 60 days,
but the external `repository_dispatch` path is unaffected.
