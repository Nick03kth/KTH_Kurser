# SL morning agent

Every day at **06:00 (Europe/Stockholm)** the GitHub Actions workflow
[`.github/workflows/morning-agent.yml`](../.github/workflows/morning-agent.yml)
runs [`sl_morning_agent.py`](sl_morning_agent.py) and posts the result as a
GitHub issue titled *"🚆 SL morning report YYYY-MM-DD"*.

The report contains:

- **Cancelled departures** in the next two hours: buses 607/627 at Malla
  Silfverstolpes väg and pendeltåg from Sollentuna towards Stockholm City
  (plus departures delayed ≥10 min), with the next departure times for each
  leg. From SL's open departures API (`transport.integration.sl.se`, no key).
- **Service alerts** with full details for pendeltåg 40/41, buses 607/627
  and red metro line 14, from SL's deviations API. Alerts about other parts
  of a line (e.g. a broken lift at Gamla stan) are marked ⚪ as not
  affecting this route; accessibility-only notices never change the plan.
- **A route recommendation** for Landsnoravägen 97 → Regeringsgatan 25.
  You drive ~2 min to the **Malla Silfverstolpes väg** bus stop and park
  right by it — both plans start from that same spot:
  1. *Plan A (normal):* bus 607/627 → Sollentuna station → pendeltåg 40/41
     → Stockholm City, exit **Sergels torg**, walk ~300 m (~40 min total).
  2. *Plan B (pendeltåg disrupted):* bus 607 → Danderyds sjukhus → metro 14
     → Östermalmstorg, exit **Birger Jarlsgatan**, walk ~650 m (~45 min).
  3. *Plan C (both disrupted):* drive all the way, park at Parkaden
     (Regeringsgatan 47).

  A plan only switches on real disruption: a line-wide alert (e.g.
  "Oregelbunden trafik"), several major alerts at once, or two or more
  cancelled departures on that leg.

## Optional: live Google Maps walking times

Walking legs use fixed measured values by default. To get live walking
distance/time from the Google Maps Directions API instead, add a repo
secret named `GOOGLE_MAPS_API_KEY` (Settings → Secrets and variables →
Actions). If the key is missing or the call fails, the agent silently
falls back to the fixed values — nothing breaks.

## Getting the report by email at 06:00

No setup needed: each report issue is assigned to the repo owner and
@mentions them, which makes GitHub send the report by email automatically
("participating" notifications are emailed by default). The email goes to
the address configured under
[Settings → Notifications](https://github.com/settings/notifications).
Older report issues are closed automatically, so only today's stays open.

## Testing

Run it manually anytime:

```bash
python3 morning-agent/sl_morning_agent.py
```

or trigger the workflow from the Actions tab (**SL morning agent → Run
workflow**) — manual runs skip the 06:00 time guard.

## Scheduling reliability

GitHub delays on-the-hour cron triggers badly (04:00/05:00 UTC are the most
congested slots), so the workflow instead triggers at off-peak minutes
shortly *before* 06:00 Stockholm time and sleeps until exactly 06:00 before
posting. A backup trigger fires ~06:10 local in case the first one never
starts, and the issue step deduplicates by title so the report is sent
exactly once per day. GitHub disables schedules in repos with no activity
for 60 days (a single commit re-enables them).
