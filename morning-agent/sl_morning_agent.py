#!/usr/bin/env python3
"""Morning SL agent.

Every morning this script checks SL's open APIs and sends a report by
email to nick050408@gmail.com with cancelled departures, service alerts
and a recommended route from Landsnoravägen 97 to Regeringsgatan 25.

You drive to the Malla Silfverstolpes väg bus stop and park right next
to it. From there two plans share the same parking spot:

  Plan A (normal):   bus 607/627 → Sollentuna station,
                     pendeltåg 40/41 → Stockholm City,
                     exit "Sergels torg", walk to Regeringsgatan 25.
  Plan B (fallback): bus 607 → Danderyds sjukhus,
                     metro 14 towards Fruängen → Östermalmstorg,
                     exit "Birger Jarlsgatan", walk to Regeringsgatan 25.

Requires one repo secret: GMAIL_APP_PASSWORD
  (Google Account → Security → App passwords → create one for Mail)

SL data from open integration APIs — no API key required:
  https://transport.integration.sl.se/v1/...
  https://deviations.integration.sl.se/v1/messages
"""

from __future__ import annotations

import json
import os
import smtplib
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Stockholm")

GMAIL_ADDRESS = "nick050408@gmail.com"

MALLA_SITE = 5513
SOLLENTUNA_SITE = 9506
PENDELTAG_LINES = ["40", "41"]
BUS_LINES = ["607", "627"]
METRO_LINE = "14"
BUS_DIR_TRAIN, BUS_DIR_METRO = 1, 2

FORECAST_MINUTES = 120
HEAVY_DELAY_MINUTES = 10
MAJOR_IMPORTANCE = 5

REGERINGSGATAN_25 = (59.33170, 18.06803)
WALK_FROM_CITY = ("Stockholm City, exit Sergels torg", (59.33250, 18.06450), 300, 4)
WALK_FROM_OSTERMALM = ("Östermalmstorg, exit Birger Jarlsgatan", (59.33540, 18.07310), 650, 8)

STRETCH_TRAIN = [
    "sollentuna", "ulriksdal", "solna", "odenplan", "stockholm city",
    "häggvik", "norrviken", "rotebro", "upplands väsby", "rosersberg",
    "märsta", "arlanda", "uppsala", "helenelund",
]
OFFROUTE_TRAIN = [
    "stockholms södra", "årstaberg", "älvsjö", "huddinge", "flemingsberg",
    "tullinge", "tumba", "rönninge", "östertälje", "södertälje hamn",
    "bålsta", "kungsängen", "jakobsberg", "spånga", "sundbyberg",
]
STRETCH_METRO = [
    "mörby", "danderyd", "bergshamra", "universitetet", "tekniska högskolan",
    "stadion", "östermalmstorg", "fruängen",
]
OFFROUTE_METRO = [
    "t-centralen", "gamla stan", "slussen", "mariatorget", "zinkensdamm",
    "hornstull", "liljeholmen", "midsommarkransen", "telefonplan",
    "hägerstensåsen", "västertorp", "ropsten", "gärdet", "karlaplan",
]
NOISE_WORDS = ["hiss", "rulltrapp", "rullstol", "permobil", "framkomlighet",
               "tryck på knappen", "flyttad hållplats", "flyttas"]
BREAKING_PHRASES = ["oregelbunden trafik", "ingen trafik", "inga tåg", "stora förseningar",
                    "ersättningsbuss", "ersätts av buss", "avstängd station", "totalavstängning"]
BREAKING_MAJOR_COUNT = 3


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "morning-sl-agent/3.0"})
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


def hhmm(value: str | None) -> str:
    t = parse_time(value)
    return t.strftime("%H:%M") if t else "?"


def classify(departures, direction_code, lines=None):
    cancelled, delayed, ok = [], [], []
    for dep in departures:
        if dep.get("direction_code") != direction_code:
            continue
        if lines and (dep.get("line") or {}).get("designation") not in lines:
            continue
        state = (dep.get("state") or "").upper()
        journey_state = ((dep.get("journey") or {}).get("state") or "").upper()
        scheduled, expected = parse_time(dep.get("scheduled")), parse_time(dep.get("expected"))
        if "CANCELLED" in state or "CANCELLED" in journey_state:
            cancelled.append(dep)
        elif scheduled and expected and expected - scheduled >= timedelta(minutes=HEAVY_DELAY_MINUTES):
            delayed.append(dep)
        else:
            ok.append(dep)
    by_time = lambda d: d.get("scheduled") or ""  # noqa: E731
    return sorted(cancelled, key=by_time), sorted(delayed, key=by_time), sorted(ok, key=by_time)


def fmt_dep(dep) -> str:
    line = (dep.get("line") or {}).get("designation", "?")
    return f"{hhmm(dep.get('scheduled'))} – {line} towards {dep.get('destination', '?')}"


def alert_rows(messages, stretch, offroute, label):
    rows, major_count, breaking = [], 0, False
    for msg in messages:
        importance = (msg.get("priority") or {}).get("importance_level") or 0
        variant = (msg.get("message_variants") or [{}])[0]
        header = variant.get("header") or "(no header)"
        details = (variant.get("details") or "").strip().replace("\n", " ")
        text = f"{header} {details}".lower()
        noise = any(w in text for w in NOISE_WORDS)
        on_route = any(w in text for w in stretch)
        off_route_only = not on_route and any(w in text for w in offroute)
        major = importance >= MAJOR_IMPORTANCE and not noise and not off_route_only
        if major:
            major_count += 1
            if any(p in text for p in BREAKING_PHRASES):
                breaking = True
        if major:
            icon, note = "🔴", ""
        elif off_route_only:
            icon, note = "⚪", " *(other part of the line — does not affect this route)*"
        else:
            icon, note = "ℹ️", ""
        row = f"- {icon} **{label}:** {header}"
        if details:
            row += f" — {details[:220]}{'…' if len(details) > 220 else ''}"
        rows.append(row + note)
    return rows, breaking or major_count >= BREAKING_MAJOR_COUNT


def google_walk(origin: tuple[float, float], dest: tuple[float, float]):
    key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not key:
        return None
    try:
        url = "https://maps.googleapis.com/maps/api/directions/json?" + urllib.parse.urlencode({
            "origin": f"{origin[0]},{origin[1]}",
            "destination": f"{dest[0]},{dest[1]}",
            "mode": "walking",
            "key": key,
        })
        data = fetch_json(url)
        leg = data["routes"][0]["legs"][0]
        return leg["distance"]["value"], round(leg["duration"]["value"] / 60)
    except Exception:  # noqa: BLE001
        return None


def walk_text(leg) -> str:
    name, origin, fb_metres, fb_minutes = leg
    live = google_walk(origin, REGERINGSGATAN_25)
    if live:
        return f"walk **{live[0]} m (~{live[1]} min)** *(live via Google Maps)*"
    return f"walk **~{fb_metres} m (~{fb_minutes} min)**"


def next_times(deps, limit=3) -> str:
    return ", ".join(hhmm(d.get("scheduled")) for d in deps[:limit]) or "none in the next 2 h"


def build_report() -> tuple[str, bool, bool, bool]:
    """Return (report_text, train_breaking, metro_breaking, bus_breaking)."""
    now = datetime.now(TZ)
    out: list[str] = [f"# 🚆 SL morning report – {now.strftime('%A %d %B %Y, %H:%M')}", ""]
    api_failed = False

    try:
        bus_deps = get_departures(MALLA_SITE, "BUS")
        train_deps = get_departures(SOLLENTUNA_SITE, "TRAIN")
    except Exception as exc:  # noqa: BLE001
        out += [f"⚠️ Could not reach the SL departures API: `{exc}`", ""]
        bus_deps, train_deps, api_failed = [], [], True

    bus_a_cancelled, bus_a_delayed, bus_a_ok = classify(bus_deps, BUS_DIR_TRAIN, BUS_LINES)
    bus_b_cancelled, _, bus_b_ok = classify(
        [d for d in bus_deps if d.get("destination") == "Danderyds sjukhus"], BUS_DIR_METRO)
    train_cancelled, train_delayed, train_ok = classify(train_deps, 1, None)

    out.append("## Cancelled departures (next 2 h)")
    cancelled_rows = (
        [f"- ❌ Bus {fmt_dep(d)} (from Malla Silfverstolpes väg) — **CANCELLED**"
         for d in bus_a_cancelled + bus_b_cancelled]
        + [f"- ❌ Train {fmt_dep(d)} (from Sollentuna) — **CANCELLED**" for d in train_cancelled]
    )
    out += cancelled_rows or ["✅ No cancelled buses at Malla Silfverstolpes väg and no "
                              "cancelled pendeltåg from Sollentuna towards the city."]
    for d in bus_a_delayed + train_delayed:
        out.append(f"- ⏱️ {fmt_dep(d)} — delayed, now expected {hhmm(d.get('expected'))}")
    if not api_failed:
        out += [
            "",
            f"Next buses to Sollentuna station (607/627): **{next_times(bus_a_ok)}**",
            f"Next buses to Danderyds sjukhus (607): **{next_times(bus_b_ok)}**",
            f"Next trains Sollentuna → Stockholm City: **{next_times(train_ok, 4)}**",
        ]
    out.append("")

    out.append("## Service alerts")
    train_breaking = metro_breaking = bus_breaking = False
    try:
        train_rows, train_breaking = alert_rows(
            get_deviations("TRAIN", PENDELTAG_LINES), STRETCH_TRAIN, OFFROUTE_TRAIN, "Pendeltåg 40/41")
        metro_rows, metro_breaking = alert_rows(
            get_deviations("METRO", [METRO_LINE]), STRETCH_METRO, OFFROUTE_METRO, "Metro 14")
        bus_rows, bus_breaking = alert_rows(
            get_deviations("BUS", BUS_LINES), ["silfverstolpe", "sollentuna", "danderyd", "edsberg"],
            [], "Bus 607/627")
        rows = train_rows + bus_rows + metro_rows
        out += rows or ["✅ No active alerts on pendeltåg 40/41, buses 607/627 or metro 14."]
    except Exception as exc:  # noqa: BLE001
        out.append(f"⚠️ Could not reach the SL deviations API: `{exc}`")
    out.append("")

    plan_a_broken = (len(train_cancelled) >= 2 or train_breaking
                     or bus_breaking or len(bus_a_cancelled) >= 2)
    plan_b_broken = metro_breaking or len(bus_b_cancelled) >= 2

    out.append("## Recommended route: Landsnoravägen 97 → Regeringsgatan 25")
    if not plan_a_broken:
        out += [
            "**Plan A — pendeltåg (normal plan):**",
            "1. 🚗 Drive to the **Malla Silfverstolpes väg** bus stop (~2 min) and park right by it.",
            f"2. 🚌 Bus **607 or 627 towards Sollentuna station** (~10 min) — next: {next_times(bus_a_ok)}.",
            "3. 🚆 Pendeltåg **40/41 southbound (towards Södertälje/Tumba)** to "
            "**Stockholm City** (~16 min, 6 trains/h in rush hour).",
            "4. 🚶 Best exit: **uppgång Sergels torg** (follow the Sergels torg signs — it is the "
            f"exit closest to Regeringsgatan). Then {walk_text(WALK_FROM_CITY)} east via "
            "Hamngatan, right onto Regeringsgatan to no. 25.",
            "",
            "Estimated door-to-door: **~40 min**.",
        ]
    elif not plan_b_broken:
        out += [
            "**Plan B — pendeltåg is disrupted, take the metro instead (same parking spot):**",
            "1. 🚗 Drive to the **Malla Silfverstolpes väg** bus stop (~2 min) and park right by it.",
            f"2. 🚌 Bus **607 towards Danderyds sjukhus** (~15 min) — next: {next_times(bus_b_ok)}.",
            "3. 🚇 Metro red line **14 towards Fruängen** to **Östermalmstorg** (~12 min).",
            "4. 🚶 Best exit: **uppgång Birger Jarlsgatan** (front of the train from Danderyd, "
            f"towards Stureplan). Then {walk_text(WALK_FROM_OSTERMALM)} via Birger Jarlsgatan "
            "and Mäster Samuelsgatan, right onto Regeringsgatan to no. 25.",
            "",
            "Estimated door-to-door: **~45 min**.",
        ]
    else:
        out += [
            "**Plan C — both pendeltåg and metro are disrupted, drive all the way:**",
            "1. 🚗 Drive E18/Sveavägen into the city (~30–45 min in rush hour).",
            "2. 🅿️ Park at **Parkaden, Regeringsgatan 47** — 200 m from Regeringsgatan 25.",
        ]
    return "\n".join(out), train_breaking, metro_breaking, bus_breaking


def make_subject(report: str, train_breaking: bool, metro_breaking: bool,
                 bus_breaking: bool, now: datetime) -> str:
    date_str = now.strftime("%a %d %b")
    problems = []
    if train_breaking or "❌ Train" in report:
        problems.append("pendeltåg")
    if bus_breaking or "❌ Bus" in report:
        problems.append("buss 607/627")
    if metro_breaking:
        problems.append("metro 14")
    if problems:
        return f"⚠️ SL {date_str} – Störning: {', '.join(problems)}"
    return f"✅ SL {date_str} – Allt verkar ok"


def send_email(subject: str, body: str) -> None:
    """Send the report directly to nick050408@gmail.com via Gmail SMTP."""
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not password:
        print("No GMAIL_APP_PASSWORD set — skipping email.", file=sys.stderr)
        return
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = GMAIL_ADDRESS
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_ADDRESS, password.strip())
            smtp.sendmail(GMAIL_ADDRESS, [GMAIL_ADDRESS], msg.as_string())
        print(f"Email sent: {subject}", file=sys.stderr)
    except Exception as exc:  # noqa: BLE001
        print(f"Email failed: {exc}", file=sys.stderr)
        raise


def main() -> int:
    report, train_breaking, metro_breaking, bus_breaking = build_report()
    print(report)
    now = datetime.now(TZ)
    subject = make_subject(report, train_breaking, metro_breaking, bus_breaking, now)
    send_email(subject, report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
