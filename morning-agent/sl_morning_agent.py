#!/usr/bin/env python3
"""Morning SL agent.

Every morning this fetches live SL departures for ALL routes from
Landsnoravägen 97 to Regeringsgatan 25, chains each into a realistic
itinerary, works out when you must leave home to make the 07:30 meeting
(arrive by 07:25), and emails a concise, mobile-friendly HTML card view
to nick050408@gmail.com.

You drive ~3 min to the Malla Silfverstolpes väg bus stop and park right
by it. From there three live routes are compared:

  R1 Pendeltåg : bus 607/627 → Sollentuna → pendeltåg 40/41 → Stockholm
                 City, exit Sergels torg, walk to Regeringsgatan 25.
  R2 Direct bus: bus 697 → Stockholm C (Cityterminalen), walk.
  R3 Metro     : bus 607 → Danderyds sjukhus → metro 14 → Östermalmstorg,
                 exit Birger Jarlsgatan, walk.
  R4 Drive     : drive the whole way, park at Parkaden (fallback).

Secrets (GitHub Actions repo secrets):
  GMAIL_APP_PASSWORD  – required to send the email.

SL data from open integration APIs — no API key required.
"""

from __future__ import annotations

import json
import os
import smtplib
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Stockholm")
GMAIL_ADDRESS = "nick050408@gmail.com"

# Endpoints (park here / transfer here)
MALLA_SITE = 5513          # Malla Silfverstolpes väg (bus stop, park here)
SOLLENTUNA_SITE = 9506     # Sollentuna pendeltågsstation
DANDERYD_SITE = 9201       # Danderyds sjukhus (metro)

HOME = "Landsnoravägen 97, Sollentuna"
DEST = "Regeringsgatan 25, Stockholm"

# Daily fixed target: be at Regeringsgatan 25 by 07:25 for a 07:30 meeting.
TARGET_ARRIVAL = (7, 25)
MEETING = (7, 30)

FORECAST_MINUTES = 120
MAJOR_IMPORTANCE = 5

# Leg durations in minutes (estimates; SL departure data anchors the actual
# board times and catches cancellations — these fill in the ride/walk legs).
DRIVE_PARK = 6             # home → boarded at Malla (drive + park + walk to stop)
RIDE = {
    "bus_sollentuna": 9,   # 607/627  Malla → Sollentuna station
    "bus_697": 30,         # 697      Malla → Stockholm C (express)
    "bus_danderyd": 16,    # 607      Malla → Danderyds sjukhus
    "train": 15,           # 40/41    Sollentuna → Stockholm City
    "metro": 11,           # 14       Danderyds sjukhus → Östermalmstorg
}
TRANSFER = {"sollentuna": 5, "danderyd": 4}
# Typical wait for the next departure when the live board is truncated
# (high-frequency lines only return imminent departures).
WAIT = {"train": 5, "metro": 5}
WALK = {"city": 5, "cityterminalen": 9, "ostermalm": 8}

# Alert routing keywords
STRETCH_TRAIN = ["sollentuna", "ulriksdal", "solna", "odenplan", "stockholm city",
                 "häggvik", "norrviken", "rotebro", "upplands väsby", "helenelund"]
OFFROUTE_TRAIN = ["stockholms södra", "årstaberg", "älvsjö", "huddinge", "flemingsberg",
                  "tullinge", "tumba", "rönninge", "östertälje", "södertälje",
                  "bålsta", "kungsängen", "jakobsberg", "spånga", "sundbyberg"]
STRETCH_METRO = ["mörby", "danderyd", "bergshamra", "universitetet", "tekniska",
                 "stadion", "östermalmstorg"]
OFFROUTE_METRO = ["t-centralen", "gamla stan", "slussen", "mariatorget", "zinkensdamm",
                  "hornstull", "liljeholmen", "midsommarkransen", "telefonplan",
                  "hägerstensåsen", "västertorp", "fruängen", "ropsten", "karlaplan"]
NOISE_WORDS = ["hiss", "rulltrapp", "rullstol", "permobil", "framkomlighet",
               "tryck på knappen", "flyttad hållplats", "flyttas"]
BREAKING_PHRASES = ["oregelbunden trafik", "ingen trafik", "inga tåg", "stora förseningar",
                    "ersättningsbuss", "ersätts av buss", "avstängd station",
                    "totalavstängning", "stopp i trafiken", "ställs in"]


# --------------------------------------------------------------------------- #
# Data fetching
# --------------------------------------------------------------------------- #
def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "morning-sl-agent/4.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def get_departures(site_id: int, transport: str):
    url = (f"https://transport.integration.sl.se/v1/sites/{site_id}/departures?"
           + urllib.parse.urlencode({"transport": transport, "forecast": FORECAST_MINUTES}))
    deps = []
    for attempt in range(3):            # API intermittently returns an empty list
        try:
            deps = fetch_json(url).get("departures", [])
            if deps:
                break
        except Exception as exc:  # noqa: BLE001
            print(f"departures fetch retry {attempt} for {site_id}/{transport}: {exc}",
                  file=sys.stderr)
    return deps


def get_deviations(transport_mode: str, lines: list[str]):
    params = [("transport_mode", transport_mode)] + [("line", l) for l in lines]
    url = "https://deviations.integration.sl.se/v1/messages?" + urllib.parse.urlencode(params)
    return fetch_json(url)


def eff_time(dep) -> datetime | None:
    """Expected (delay-aware) time if present, else scheduled."""
    val = dep.get("expected") or dep.get("scheduled")
    return datetime.fromisoformat(val).replace(tzinfo=TZ) if val else None


def is_cancelled(dep) -> bool:
    state = (dep.get("state") or "").upper()
    jstate = ((dep.get("journey") or {}).get("state") or "").upper()
    return "CANCELLED" in state or "CANCELLED" in jstate


# --------------------------------------------------------------------------- #
# Itinerary model
# --------------------------------------------------------------------------- #
@dataclass
class Step:
    icon: str
    text: str


@dataclass
class Itin:
    leave_home: datetime
    board: datetime
    arrival: datetime
    steps: list[Step]


@dataclass
class Route:
    key: str
    name: str
    emoji: str
    walk_note: str
    itins: list[Itin] = field(default_factory=list)
    breaking: bool = False        # disruption affecting this route's modes
    alert_note: str = ""
    status_line: str = ""         # e.g. live Sollentuna train board
    status_sev: str = "green"     # green / amber / red for status_line

    def feasible(self, target: datetime):
        return [i for i in self.itins if i.arrival <= target]

    def next_after(self, now: datetime):
        upcoming = sorted((i for i in self.itins if i.board >= now - timedelta(minutes=1)),
                          key=lambda i: i.board)
        return upcoming[0] if upcoming else None

    def last_safe(self, target: datetime, now: datetime):
        ok = [i for i in self.feasible(target) if i.board >= now - timedelta(minutes=1)]
        return max(ok, key=lambda i: i.board) if ok else None


def mins(a: datetime, b: datetime) -> int:
    return round((b - a).total_seconds() / 60)


def is_delayed(dep, threshold=4) -> bool:
    sched, exp = dep.get("scheduled"), dep.get("expected")
    if not sched or not exp:
        return False
    s = datetime.fromisoformat(sched).replace(tzinfo=TZ)
    e = datetime.fromisoformat(exp).replace(tzinfo=TZ)
    return (e - s) >= timedelta(minutes=threshold)


def sollentuna_train_status(train_deps, now):
    """Live southbound (towards city) pendeltåg board at Sollentuna.

    Returns (severity, text). Severity is red if the very next train is
    cancelled or 2+ are cancelled in the window (the case that makes you
    late), amber on any single cancellation/delay, else green.
    """
    south = sorted(
        [d for d in train_deps if d.get("direction_code") == 1
         and eff_time(d) and eff_time(d) >= now - timedelta(minutes=1)],
        key=lambda d: eff_time(d))
    if not south:
        if not train_deps:              # API returned nothing — transient, not a real outage
            return "unknown", ("Sollentuna: live train status unavailable right now — "
                               "assume normal, check the SL app.")
        return "red", "Sollentuna: no southbound trains in the next 2 h."
    parts, n_canc, n_delay = [], 0, 0
    for d in south[:4]:
        sched = datetime.fromisoformat(d["scheduled"]).replace(tzinfo=TZ)
        if is_cancelled(d):
            parts.append(f"{sched:%H:%M} ❌ cancelled")
            n_canc += 1
        elif is_delayed(d):
            parts.append(f"{sched:%H:%M}→{eff_time(d):%H:%M} ⏱ late")
            n_delay += 1
        else:
            parts.append(f"{eff_time(d):%H:%M} ✅")
    if n_canc >= 2 or is_cancelled(south[0]):
        sev = "red"
    elif n_canc or n_delay:
        sev = "amber"
    else:
        sev = "green"
    return sev, "Sollentuna southbound: " + " · ".join(parts)


def first_onward(deps, not_before: datetime, dir_code=None, dests=None):
    """First non-cancelled departure at/after not_before, matching dir/dest."""
    best = None
    for d in deps:
        if is_cancelled(d):
            continue
        if dir_code is not None and d.get("direction_code") != dir_code:
            continue
        if dests and not any(s in (d.get("destination") or "") for s in dests):
            continue
        t = eff_time(d)
        if t and t >= not_before and (best is None or t < eff_time(best)):
            best = d
    return best


# --------------------------------------------------------------------------- #
# Route builders (each chains live departures into itineraries)
# --------------------------------------------------------------------------- #
def build_pendeltag(bus_deps, train_deps) -> Route:
    r = Route("pendel", "Pendeltåg via Sollentuna", "🚆",
              "exit Sergels torg → 5 min walk")
    for b in bus_deps:
        if is_cancelled(b) or b.get("direction_code") != 1:
            continue
        if (b.get("line") or {}).get("designation") not in ("607", "627"):
            continue
        tb = eff_time(b)
        if not tb:
            continue
        arr_soll = tb + timedelta(minutes=RIDE["bus_sollentuna"])
        ready = arr_soll + timedelta(minutes=TRANSFER["sollentuna"])
        train = first_onward(train_deps, ready, dir_code=1)
        if train:                       # live train within the board
            tt = eff_time(train)
            tl = (train.get("line") or {}).get("designation")
            tt_label = f"Pendeltåg {tl} {tt:%H:%M} → Stockholm City"
        else:                           # board truncated — estimate next train
            tt = ready + timedelta(minutes=WAIT["train"])
            tt_label = f"Pendeltåg ~{tt:%H:%M} (est.) → Stockholm City"
        arrival = tt + timedelta(minutes=RIDE["train"] + WALK["city"])
        line = (b.get("line") or {}).get("designation")
        r.itins.append(Itin(
            leave_home=tb - timedelta(minutes=DRIVE_PARK), board=tb, arrival=arrival,
            steps=[
                Step("🚗", f"Drive to Malla stop, park (~{DRIVE_PARK} min)"),
                Step("🚌", f"Bus {line} {tb:%H:%M} → Sollentuna st."),
                Step("🚆", tt_label),
                Step("🚶", f"Sergels torg exit → Regeringsgatan 25 (arrive {arrival:%H:%M})"),
            ]))
    return r


def build_direct_bus(bus_deps) -> Route:
    r = Route("bus697", "Direct bus 697", "🚌", "→ Stockholm C → 9 min walk")
    for b in bus_deps:
        if is_cancelled(b) or b.get("direction_code") != 1:
            continue
        if (b.get("line") or {}).get("designation") != "697":
            continue
        tb = eff_time(b)
        if not tb:
            continue
        arrival = tb + timedelta(minutes=RIDE["bus_697"] + WALK["cityterminalen"])
        r.itins.append(Itin(
            leave_home=tb - timedelta(minutes=DRIVE_PARK), board=tb, arrival=arrival,
            steps=[
                Step("🚗", f"Drive to Malla stop, park (~{DRIVE_PARK} min)"),
                Step("🚌", f"Bus 697 {tb:%H:%M} → Stockholm C (no transfer)"),
                Step("🚶", f"Cityterminalen → Regeringsgatan 25 (arrive {arrival:%H:%M})"),
            ]))
    return r


def build_metro(bus_deps, metro_deps) -> Route:
    r = Route("metro", "Metro via Danderyd", "🚇", "exit Birger Jarlsgatan → 8 min walk")
    for b in bus_deps:
        if is_cancelled(b) or b.get("direction_code") != 2:
            continue
        if (b.get("line") or {}).get("designation") != "607":
            continue
        if "Danderyd" not in (b.get("destination") or ""):
            continue
        tb = eff_time(b)
        if not tb:
            continue
        arr_dan = tb + timedelta(minutes=RIDE["bus_danderyd"])
        ready = arr_dan + timedelta(minutes=TRANSFER["danderyd"])
        metro = first_onward(metro_deps, ready, dir_code=2)
        if metro:                       # live metro within the board
            tm = eff_time(metro)
            tm_label = f"Metro 14 {tm:%H:%M} → Östermalmstorg"
        else:                           # board truncated (red line ~every 5 min) — estimate
            tm = ready + timedelta(minutes=WAIT["metro"])
            tm_label = f"Metro 14 ~{tm:%H:%M} (est., ~5 min freq.) → Östermalmstorg"
        arrival = tm + timedelta(minutes=RIDE["metro"] + WALK["ostermalm"])
        r.itins.append(Itin(
            leave_home=tb - timedelta(minutes=DRIVE_PARK), board=tb, arrival=arrival,
            steps=[
                Step("🚗", f"Drive to Malla stop, park (~{DRIVE_PARK} min)"),
                Step("🚌", f"Bus 607 {tb:%H:%M} → Danderyds sjukhus"),
                Step("🚇", tm_label),
                Step("🚶", f"Birger Jarlsgatan exit → Regeringsgatan 25 (arrive {arrival:%H:%M})"),
            ]))
    return r


# --------------------------------------------------------------------------- #
# Alerts (concise: only count + breaking flags per mode)
# --------------------------------------------------------------------------- #
def scan_alerts(messages, stretch, offroute):
    """Return (breaking, top_headers) — top_headers = list of relevant red headers."""
    breaking, headers = False, []
    for msg in messages:
        importance = (msg.get("priority") or {}).get("importance_level") or 0
        v = (msg.get("message_variants") or [{}])[0]
        header = v.get("header") or ""
        text = f"{header} {v.get('details') or ''}".lower()
        if any(w in text for w in NOISE_WORDS):
            continue
        on_route = any(w in text for w in stretch)
        off_only = not on_route and any(w in text for w in offroute)
        if off_only:
            continue
        if importance >= MAJOR_IMPORTANCE:
            headers.append(header)
            if any(p in text for p in BREAKING_PHRASES):
                breaking = True
    return breaking, headers


# --------------------------------------------------------------------------- #
# Navigation links
# --------------------------------------------------------------------------- #
def gmaps(origin: str, destination: str, mode: str) -> str:
    return ("https://www.google.com/maps/dir/?" + urllib.parse.urlencode({
        "api": 1, "origin": origin, "destination": destination, "travelmode": mode}))


NAV_TRANSIT = gmaps(HOME, DEST, "transit")
NAV_DRIVE_STOP = gmaps(HOME, "Malla Silfverstolpes väg, Sollentuna", "driving")
NAV_DRIVE_ALL = gmaps(HOME, DEST, "driving")


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
def buffer_str(arrival: datetime, target: datetime) -> str:
    b = mins(arrival, target)
    return f"{b} min margin" if b >= 0 else f"{-b} min LATE"


def pick_recommended(routes, target, now, deadline=True):
    """Best route by earliest arrival of its next departure.

    In deadline mode prefer non-breaking routes that still make the target;
    in live-board mode (late run) just prefer the soonest clean arrival.
    """
    scored = []
    for r in routes:
        nxt = r.next_after(now)
        if not nxt or r.breaking:
            continue
        if deadline and nxt.arrival > target:
            continue
        scored.append((nxt.arrival, len(nxt.steps), r))
    if scored:
        scored.sort(key=lambda x: (x[0], x[1]))
        return scored[0][2]
    # nothing clean — fall back to any route with an upcoming departure
    fallback = [(r.next_after(now).arrival, r) for r in routes if r.next_after(now)]
    return min(fallback, key=lambda x: x[0])[1] if fallback else None


def route_status(r, target, now, deadline=True):
    nxt = r.next_after(now)
    if not nxt:
        return "red", "no departures"
    if r.breaking:
        return "amber", "disruption reported"
    if not deadline:
        return "green", "running"
    if nxt.arrival > target:
        ls = r.last_safe(target, now)
        return ("amber", "tight") if ls else ("red", "misses 07:25")
    return "green", "on time"


# ---- HTML ----
COLORS = {"green": "#16a34a", "amber": "#d97706", "red": "#dc2626"}
DOTS = {"green": "🟢", "amber": "🟡", "red": "🔴"}


def html_route_card(r, target, now, recommended_key, deadline=True):
    status, _ = route_status(r, target, now, deadline)
    color = COLORS[status]
    nxt = r.next_after(now)
    ls = r.last_safe(target, now) if deadline else None
    is_rec = r.key == recommended_key
    border = f"2px solid {color}" if is_rec else "1px solid #e5e7eb"
    badge = (f'<span style="background:{color};color:#fff;font-size:11px;font-weight:700;'
             f'padding:2px 8px;border-radius:10px;margin-left:6px;">RECOMMENDED</span>'
             if is_rec else "")
    # times line
    if nxt:
        margin = (f'<span style="color:#6b7280;">({buffer_str(nxt.arrival, target)})</span>'
                  if deadline else "")
        times = (f'<div style="font-size:13px;color:#374151;margin:6px 0;">'
                 f'⏰ Leave home <b style="color:{color};">{nxt.leave_home:%H:%M}</b> '
                 f'· arrive <b>{nxt.arrival:%H:%M}</b> {margin}</div>')
        upcoming = ", ".join(f"{i.board:%H:%M}" for i in
                             sorted([i for i in r.itins if i.board >= now - timedelta(minutes=1)],
                                    key=lambda i: i.board)[:4])
        safe = (f'<div style="font-size:12px;color:#6b7280;">🔒 Last safe bus '
                f'<b>{ls.board:%H:%M}</b> · next buses: {upcoming}</div>' if ls
                else f'<div style="font-size:12px;color:#6b7280;">Next buses: {upcoming}</div>')
        steps = "".join(
            f'<div style="font-size:13px;color:#374151;line-height:1.5;">{s.icon}&nbsp;{s.text}</div>'
            for s in nxt.steps)
    else:
        times = ('<div style="font-size:13px;color:#dc2626;margin:6px 0;">'
                 'No departures available right now.</div>')
        safe = steps = ""
    alert = (f'<div style="font-size:12px;color:{COLORS["amber"]};margin-top:6px;">'
             f'⚠️ {r.alert_note}</div>' if r.alert_note else "")
    if r.status_line:
        sc = COLORS[r.status_sev]
        status_box = (f'<div style="font-size:12px;color:{sc};background:{sc}14;'
                      f'border-left:3px solid {sc};padding:6px 8px;border-radius:6px;'
                      f'margin:6px 0;line-height:1.5;">🚆 {r.status_line}</div>')
    else:
        status_box = ""
    return f"""
    <div style="border:{border};border-radius:12px;padding:14px;margin:10px 0;background:#fff;">
      <div style="font-size:15px;font-weight:700;color:#111827;">
        {DOTS[status]} {r.emoji} {r.name}{badge}
      </div>
      {status_box}
      {times}
      <div style="margin:8px 0;">{steps}</div>
      {safe}
      {alert}
      <a href="{NAV_TRANSIT}" style="display:inline-block;margin-top:10px;font-size:13px;
         font-weight:600;color:#2563eb;text-decoration:none;">▶ Navigate in Google Maps</a>
    </div>"""


def render_html(routes, rec, target, meeting, now, deadline=True):
    nxt = rec.next_after(now) if rec else None
    status, _ = route_status(rec, target, now, deadline) if rec else ("red", "")
    hero_color = COLORS[status]
    if nxt:
        sub = (f"Arrive Regeringsgatan 25 by <b>{nxt.arrival:%H:%M}</b> · "
               f"{buffer_str(nxt.arrival, meeting)} before 07:30" if deadline
               else f"Next departure · arrive Regeringsgatan 25 <b>{nxt.arrival:%H:%M}</b>")
        hero = f"""
        <div style="background:{hero_color};border-radius:14px;padding:18px;color:#fff;">
          <div style="font-size:13px;opacity:.9;">TAKE {rec.emoji} {rec.name.upper()}</div>
          <div style="font-size:30px;font-weight:800;margin:4px 0;">Leave {nxt.leave_home:%H:%M}</div>
          <div style="font-size:14px;opacity:.95;">{sub}</div>
        </div>"""
    else:
        hero = (f'<div style="background:{hero_color};border-radius:14px;padding:18px;color:#fff;">'
                f'<div style="font-size:20px;font-weight:800;">⚠️ No clean transit option — '
                f'consider driving.</div></div>')
    cards = "".join(html_route_card(r, target, now, rec.key if rec else "", deadline)
                    for r in routes)
    deadline_note = (" Target arrival 07:25 for your 07:30 meeting." if deadline
                     else " Showing next available departures (run executed after 07:25).")
    drive = f"""
    <div style="border:1px dashed #d1d5db;border-radius:12px;padding:12px;margin:10px 0;">
      <div style="font-size:14px;font-weight:600;color:#374151;">🚗 Drive all the way (fallback)</div>
      <div style="font-size:12px;color:#6b7280;margin:4px 0;">~30–45 min · park at Parkaden, Regeringsgatan 47</div>
      <a href="{NAV_DRIVE_ALL}" style="font-size:13px;font-weight:600;color:#2563eb;text-decoration:none;">▶ Drive route</a>
    </div>"""
    return f"""<!doctype html><html><body style="margin:0;background:#f3f4f6;
      font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;">
      <div style="max-width:480px;margin:0 auto;padding:16px;">
        <div style="font-size:13px;color:#6b7280;">{now:%A %d %B} · morning commute</div>
        {hero}
        <a href="{NAV_DRIVE_STOP}" style="display:inline-block;margin:10px 0;font-size:13px;
           font-weight:600;color:#2563eb;text-decoration:none;">🅿️ Drive to Malla Silfverstolpes väg stop</a>
        {cards}
        {drive}
        <div style="font-size:11px;color:#9ca3af;margin-top:14px;line-height:1.5;">
          Board times are live from SL; ride/walk legs are estimates.{deadline_note}
        </div>
      </div></body></html>"""


def render_text(routes, rec, target, now, deadline=True):
    lines = [f"SL morning commute — {now:%A %d %B %H:%M}", ""]
    nxt = rec.next_after(now) if rec else None
    if nxt:
        tail = (f"({buffer_str(nxt.arrival, target)} before 07:25)" if deadline
                else "(next departure)")
        lines += [f"TAKE: {rec.name}",
                  f"Leave home {nxt.leave_home:%H:%M} → arrive {nxt.arrival:%H:%M} {tail}", ""]
    for r in routes:
        status, note = route_status(r, target, now, deadline)
        n = r.next_after(now)
        head = f"[{status.upper()}] {r.name} — {note}"
        lines.append(head)
        if r.status_line:
            lines.append(f"  🚆 {r.status_line}")
        if n:
            lines.append(f"  leave {n.leave_home:%H:%M}, arrive {n.arrival:%H:%M}")
            for s in n.steps:
                lines.append(f"   {s.icon} {s.text}")
        lines.append("")
    lines.append(f"Navigate: {NAV_TRANSIT}")
    return "\n".join(lines)


def make_subject(rec, routes, target, now, deadline=True) -> str:
    date = f"{now:%a %d %b}"
    if not rec or not rec.next_after(now):
        return f"⚠️ SL {date} – Drive, no transit"
    status, _ = route_status(rec, target, now, deadline)
    nxt = rec.next_after(now)
    icon = "✅" if status == "green" else "⚠️"
    disrupted = [r.emoji for r in routes if r.breaking]
    tag = f" · störning {''.join(disrupted)}" if disrupted else ""
    return f"{icon} SL {date} – Leave {nxt.leave_home:%H:%M} ({rec.name}){tag}"


# --------------------------------------------------------------------------- #
# Email
# --------------------------------------------------------------------------- #
def send_email(subject: str, text_body: str, html_body: str) -> None:
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not password:
        print("No GMAIL_APP_PASSWORD set — skipping email.", file=sys.stderr)
        return
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = GMAIL_ADDRESS
    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_ADDRESS, password.strip())
        smtp.sendmail(GMAIL_ADDRESS, [GMAIL_ADDRESS], msg.as_string())
    print(f"Email sent: {subject}", file=sys.stderr)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def build_everything():
    now = datetime.now(TZ)
    target = now.replace(hour=TARGET_ARRIVAL[0], minute=TARGET_ARRIVAL[1], second=0, microsecond=0)
    meeting = now.replace(hour=MEETING[0], minute=MEETING[1], second=0, microsecond=0)

    bus_deps = get_departures(MALLA_SITE, "BUS")
    train_deps = get_departures(SOLLENTUNA_SITE, "TRAIN")
    metro_deps = get_departures(DANDERYD_SITE, "METRO")

    routes = [
        build_pendeltag(bus_deps, train_deps),
        build_direct_bus(bus_deps),
        build_metro(bus_deps, metro_deps),
    ]

    # Attach disruption flags per route
    try:
        tb, th = scan_alerts(get_deviations("TRAIN", ["40", "41"]), STRETCH_TRAIN, OFFROUTE_TRAIN)
        mb, mh = scan_alerts(get_deviations("METRO", ["14"]), STRETCH_METRO, OFFROUTE_METRO)
        bb, bh = scan_alerts(get_deviations("BUS", ["607", "627", "697"]),
                             ["silfverstolpe", "sollentuna", "danderyd", "edsberg"], [])
        for r in routes:
            if r.key == "pendel" and (tb or bb):
                r.breaking = tb or bb
                r.alert_note = (th + bh)[0] if (th + bh) else "disruption reported"
            if r.key == "bus697" and bb:
                r.breaking = True
                r.alert_note = bh[0] if bh else "bus disruption reported"
            if r.key == "metro" and (mb or bb):
                r.breaking = mb or bb
                r.alert_note = (mh + bh)[0] if (mh + bh) else "disruption reported"
    except Exception as exc:  # noqa: BLE001
        print(f"Alert fetch failed: {exc}", file=sys.stderr)

    # Live Sollentuna pendeltåg board — the late/cancelled trains that would
    # actually make you miss the 07:30 meeting. Shown prominently on the
    # pendeltåg card; a cancelled next train escalates that route to red.
    t_sev, t_text = sollentuna_train_status(train_deps, now)
    for r in routes:
        if r.key == "pendel":
            r.status_line = t_text
            r.status_sev = t_sev if t_sev in COLORS else "amber"  # 'unknown' → amber tint
            if t_sev == "red":          # genuine cancellation/outage only
                r.breaking = True
                if not r.alert_note:
                    r.alert_note = "Cancelled trains at Sollentuna — check before leaving."

    deadline = now <= target  # full leave-by mode only if the job runs before 07:25
    rec = pick_recommended(routes, target, now, deadline)
    # Concise: hide alternative routes with no departures (e.g. bus 697 only
    # runs nights), but always keep the recommended one.
    visible = [r for r in routes if r.next_after(now) or (rec and r.key == rec.key)]
    subject = make_subject(rec, visible, target, now, deadline)
    html = render_html(visible, rec, target, meeting, now, deadline)
    text = render_text(visible, rec, target, now, deadline)
    return subject, text, html


def main() -> int:
    subject, text, html = build_everything()
    # A `schedule` run is the delayed safety-net path; mark it so a late
    # email is obviously the backup, not the on-time 06:00 send.
    if os.environ.get("RUN_MODE") == "fallback":
        subject = "⏰ [delayed backup] " + subject
        text = ("NOTE: This is the delayed backup — the on-time 06:00 trigger "
                "did not run today. Times below are live as of now.\n\n") + text
    print(text)
    send_email(subject, text, html)
    # Write HTML for the workflow to archive/preview.
    with open("report.html", "w", encoding="utf-8") as fh:
        fh.write(html)
    return 0


if __name__ == "__main__":
    sys.exit(main())
