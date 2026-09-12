#!/usr/bin/env python3
"""Daily availability update for oiasuitesmoalboal.com

Reads build/ical_feeds.json:
{
  "suite-1": ["https://www.airbnb.com/calendar/ical/....ics", "https://ical.booking.com/v1/export?t=..."],
  ...
}
Fetches every iCal feed, collects all booked/blocked nights per suite for the next 18 months
and writes site/data/availability.json, which the calendar on /availability/ reads.

A night is stored as the check-in date of that night (YYYY-MM-DD). An event from
DTSTART 2026-10-05 to DTEND 2026-10-08 blocks the nights of 5, 6 and 7 October.

Usage:  python3 build/update_availability.py            (writes the JSON)
        python3 build/update_availability.py --dry-run  (prints the result only)
"""
import json, os, re, sys, datetime, urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FEEDS = os.path.join(ROOT, "build", "ical_feeds.json")
OUT = os.path.join(ROOT, "site", "data", "availability.json")
ROOM_NAMES = {f"suite-{i}": f"Suite {i}" for i in range(1, 7)}
HORIZON_DAYS = 550

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "oiasuitesmoalboal-availability/1.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")

def parse_date(v):
    v = v.strip()
    m = re.match(r"(\d{4})(\d{2})(\d{2})", v)
    return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

def nights_from_ical(text):
    """Return set of ISO dates (nights) blocked by VEVENTs in the iCal text."""
    text = text.replace("\r\n ", "").replace("\r\n\t", "").replace("\n ", "")
    nights = set()
    for ev in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", text, re.S):
        s = re.search(r"^DTSTART[^:]*:(\d{8})", ev, re.M)
        e = re.search(r"^DTEND[^:]*:(\d{8})", ev, re.M)
        if not s:
            continue
        start = parse_date(s.group(1))
        end = parse_date(e.group(1)) if e else start + datetime.timedelta(days=1)
        if end <= start:
            end = start + datetime.timedelta(days=1)
        d = start
        while d < end:
            nights.add(d.isoformat())
            d += datetime.timedelta(days=1)
    return nights

def main():
    dry = "--dry-run" in sys.argv
    feeds = json.load(open(FEEDS)) if os.path.exists(FEEDS) else {}
    today = datetime.date.today()
    horizon = (today + datetime.timedelta(days=HORIZON_DAYS)).isoformat()
    previous = {}
    if os.path.exists(OUT):
        try:
            previous = json.load(open(OUT)).get("rooms", {})
        except Exception:
            previous = {}
    rooms, log = {}, []
    for slug, name in ROOM_NAMES.items():
        urls = feeds.get(slug, [])
        booked, ok = set(), 0
        for u in urls:
            try:
                booked |= nights_from_ical(fetch(u))
                ok += 1
            except Exception as ex:
                log.append(f"{slug}: feed failed ({u[:60]}...): {ex}")
        if urls and ok == 0 and slug in previous:
            # every feed failed: keep yesterday's data rather than showing everything as free
            booked = set(previous[slug].get("booked", []))
            log.append(f"{slug}: kept previous data")
        booked = sorted(d for d in booked if d >= today.isoformat() and d <= horizon)
        rooms[slug] = {"name": name, "booked": booked, "feeds": len(urls)}
        log.append(f"{slug}: {len(booked)} booked nights from {ok}/{len(urls)} feeds")
    data = {"updated": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ"),
            "source": "Booking.com, Airbnb, Agoda, Expedia calendars", "rooms": rooms}
    print("\n".join(log))
    if dry:
        print(json.dumps(data, indent=1)[:2000])
    else:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump(data, open(OUT, "w"), indent=1)
        print("written", OUT)

if __name__ == "__main__":
    main()
