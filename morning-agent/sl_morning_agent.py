#!/usr/bin/env python3
"""Morning SL agent.

Every morning this script checks SL's open APIs for:
  1. Cancelled (and heavily delayed) pendeltåg departures from Sollentuna
     station heading towards Stockholm City.
  2. Ongoing service disruptions on pendeltåg lines 40/41 and on the red
     metro line 14 (the park & ride fallback via Danderyds sjukhus).

It then prints a markdown report with a recommended route from
Landsnoravägen 97 (Sollentuna/Edsberg) to Regeringsgatan 25 (Stockholm),
assuming you can drive to a station/stop and park right next to it.

Uses only the Python standard library. APIs are SL's open integration
APIs (no API key required):
  https://transport.integration.sl.se/v1/...
  https://deviations.integration.sl.se/v1/messages
"""

from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Stockholm")

SOLLENTUNA_SITE = 9506        # Sollentuna pendeltågsstation
DANDERYD_SITE = 9201          # Danderyds sjukhus (red metro line, fallback)
PENDELTAG_LINES = ["40", "41"]
METRO_FALLBACK_LINE = "14"

# How far ahead to look for departures, in minutes.
FORECAST_MINUTES = 120
# A departure this many minutes behind schedule counts as heavily delayed.
HEAVY_DELAY_MINUTES = 10
# Deviation messages at or above this importance level count as major.
MAJOR_IMPORTANCE = 5


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "morning-sl-agent/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def get_departures(site_id: int, transport: str):
    url = (
        f"https://transport.integration.sl.se/v1/sites/{site_id}/departures?"
        + urllib.parse.urlencode({"transport": transport, "forecast": FORECAST_MINUTES})
    )
    return fetch_json(url).get("departures", [])


def get_deviations(transport_mode: str, lines: list[str]):
    params = [("transport_mode", transport_mode)] + [("line", l) for l in lines]
    url = "https://deviations.integration.sl.se/v1/messages?" + urllib.parse.urlencode(params)
    return fetch_json(url)


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value).replace(tzinfo=TZ)


def classify_departures(departures, towards_city_direction_code: int):
    """Split departures towards the city into cancelled / delayed / ok."""
    cancelled, delayed, ok = [], [], []
    for dep in departures:
        if dep.get("direction_code") != towards_city_direction_code:
            continue
        state = (dep.get("state") or "").upper()
        journey_state = ((dep.get("journey") or {}).get("state") or "").upper()
        scheduled = parse_time(dep.get("scheduled"))
        expected = parse_time(dep.get("expected"))
        if "CANCELLED" in state or "CANCELLED" in journey_state:
            cancelled.append(dep)
        elif scheduled and expected and expected - scheduled >= timedelta(minutes=HEAVY_DELAY_MINUTES):
            delayed.append(dep)
        else:
            ok.append(dep)
    return cancelled, delayed, ok


def deviation_lines(messages):
    out = []
    for msg in messages:
        importance = (msg.get("priority") or {}).get("importance_level") or 0
        variants = msg.get("message_variants") or [{}]
        header = variants[0].get("header") or "(no header)"
        out.append((importance, header))
    out.sort(reverse=True)
    return out


def fmt_departure(dep) -> str:
    line = (dep.get("line") or {}).get("designation", "?")
    scheduled = parse_time(dep.get("scheduled"))
    when = scheduled.strftime("%H:%M") if scheduled else "?"
    return f"{when} – line {line} towards {dep.get('destination', '?')}"


def build_report() -> str:
    now = datetime.now(TZ)
    lines: list[str] = [f"# 🚆 SL morning report – {now.strftime('%A %d %B %Y, %H:%M')}", ""]

    # --- Pendeltåg from Sollentuna ---
    train_error = None
    cancelled = delayed = ok = []
    try:
        departures = get_departures(SOLLENTUNA_SITE, "TRAIN")
        # direction_code 1 = southbound (towards Stockholm City/Södertälje)
        cancelled, delayed, ok = classify_departures(departures, towards_city_direction_code=1)
    except Exception as exc:  # noqa: BLE001 - report API failure in the report itself
        train_error = str(exc)

    lines.append("## Cancelled trains (Sollentuna → Stockholm City, next 2 h)")
    if train_error:
        lines.append(f"⚠️ Could not reach the SL departures API: `{train_error}`")
    elif cancelled:
        lines += [f"- ❌ {fmt_departure(d)} — **CANCELLED**" for d in cancelled]
    else:
        lines.append("✅ No cancelled pendeltåg departures from Sollentuna towards the city.")
    if delayed:
        lines.append("")
        lines.append(f"Heavily delayed (≥{HEAVY_DELAY_MINUTES} min):")
        for d in delayed:
            expected = parse_time(d.get("expected"))
            lines.append(f"- ⏱️ {fmt_departure(d)} — now expected {expected.strftime('%H:%M') if expected else '?'}")
    if ok and not train_error:
        lines.append("")
        lines.append("Next trains running as planned: " + ", ".join(
            parse_time(d.get("scheduled")).strftime("%H:%M") for d in ok[:4] if d.get("scheduled")))
    lines.append("")

    # --- Deviation messages ---
    train_major = False
    lines.append("## Service alerts")
    try:
        train_msgs = deviation_lines(get_deviations("TRAIN", PENDELTAG_LINES))
        metro_msgs = deviation_lines(get_deviations("METRO", [METRO_FALLBACK_LINE]))
        train_major = any(imp >= MAJOR_IMPORTANCE for imp, _ in train_msgs)
        metro_major = any(imp >= MAJOR_IMPORTANCE for imp, _ in metro_msgs)
        if not train_msgs and not metro_msgs:
            lines.append("✅ No active alerts on pendeltåg 40/41 or metro line 14.")
        for imp, header in train_msgs:
            lines.append(f"- {'🔴' if imp >= MAJOR_IMPORTANCE else 'ℹ️'} Pendeltåg: {header}")
        for imp, header in metro_msgs:
            lines.append(f"- {'🔴' if imp >= MAJOR_IMPORTANCE else 'ℹ️'} Metro 14: {header}")
    except Exception as exc:  # noqa: BLE001
        metro_major = False
        lines.append(f"⚠️ Could not reach the SL deviations API: `{exc}`")
    lines.append("")

    # --- Recommendation ---
    pendeltag_disrupted = bool(cancelled) or train_major or bool(train_error)
    lines.append("## Recommended route: Landsnoravägen 97 → Regeringsgatan 25")
    if not pendeltag_disrupted:
        lines += [
            "**Take the pendeltåg (normal plan):**",
            "1. 🚗 Drive to **Sollentuna station** (~7 min) and park at the commuter "
            "parking (infartsparkering) right by the station entrance.",
            "2. 🚆 Pendeltåg **41/40 southbound (towards Södertälje/Tumba)** "
            "to **Stockholm City** (~16 min, 6 trains/h in rush hour).",
            "3. 🚶 Exit towards **Sergels torg**, walk ~5 min to Regeringsgatan 25.",
            "",
            "Estimated door-to-door: **~30–35 min**.",
        ]
    elif not metro_major:
        lines += [
            "**Pendeltåg is disrupted — take the metro fallback:**",
            "1. 🚗 Drive to **Danderyds sjukhus** (~12 min via Edsbergsvägen/E18) and "
            "park at the commuter parking next to the bus terminal/metro entrance.",
            "2. 🚇 Red line **14 towards Fruängen** to **Östermalmstorg** (~12 min).",
            "3. 🚶 Walk ~7 min via Birger Jarlsgatan to Regeringsgatan 25.",
            "",
            "Estimated door-to-door: **~40 min**.",
        ]
    else:
        lines += [
            "**Both pendeltåg and metro are disrupted — drive all the way:**",
            "1. 🚗 Drive E18/Sveavägen into the city (~30–45 min in rush hour).",
            "2. 🅿️ Park at **Parkaden, Regeringsgatan 47** — 200 m from Regeringsgatan 25.",
        ]
    return "\n".join(lines)


def main() -> int:
    # DST guard: the workflow triggers at both 04:00 and 05:00 UTC so that one
    # of them is 06:00 in Stockholm year-round. The wrong one exits here.
    if "--guard-0600" in sys.argv and datetime.now(TZ).hour != 6:
        print("Not 06:00 in Stockholm — skipping this trigger.", file=sys.stderr)
        return 78
    print(build_report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
