# SL morning agent

Every day at **06:00 (Europe/Stockholm)** the GitHub Actions workflow
[`.github/workflows/morning-agent.yml`](../.github/workflows/morning-agent.yml)
runs [`sl_morning_agent.py`](sl_morning_agent.py) and posts the result as a
GitHub issue titled *"🚆 SL morning report YYYY-MM-DD"*.

The report contains:

- **Cancelled pendeltåg departures** from Sollentuna station towards
  Stockholm City in the next two hours (plus departures delayed ≥10 min),
  from SL's open departures API (`transport.integration.sl.se`, no API key).
- **Service alerts** for pendeltåg lines 40/41 and red metro line 14, from
  SL's deviations API (`deviations.integration.sl.se`).
- **A route recommendation** for Landsnoravägen 97 → Regeringsgatan 25,
  assuming you drive to a station and park at the commuter parking:
  1. *Normal:* drive to Sollentuna station → pendeltåg to Stockholm City →
     walk to Regeringsgatan 25 (~30–35 min).
  2. *Pendeltåg disrupted:* drive to Danderyds sjukhus → red line 14 to
     Östermalmstorg → walk (~40 min).
  3. *Both disrupted:* drive all the way, park at Parkaden (Regeringsgatan 47).

## Getting the report by email at 06:00

GitHub emails you when an issue is created in this repo if you watch it:
click **Watch → All Activity** on the repo page, and make sure issue
notifications are routed to email under
[Settings → Notifications](https://github.com/settings/notifications).

## Testing

Run it manually anytime:

```bash
python3 morning-agent/sl_morning_agent.py
```

or trigger the workflow from the Actions tab (**SL morning agent → Run
workflow**) — manual runs skip the 06:00 time guard.

Note: GitHub scheduled workflows can fire a few minutes late at busy times,
and GitHub disables schedules in repos with no activity for 60 days (a
single commit re-enables them).
