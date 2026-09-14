#!/usr/bin/env python3
"""Static site generator for oiasuitesmoalboal.com"""
import json, os, shutil, html, datetime
from content import *

OUT = os.path.join(os.path.dirname(__file__), "..", "site")
TODAY = datetime.date.today().isoformat()

NAV = [
    ("/", "Home"), ("/rooms/", "Rooms"), ("/availability/", "Availability"),
    ("/accommodation-for-digital-nomads/", "Digital Nomads"), ("/breakfast/", "Breakfast"), ("/services/", "Services & Tours"), ("/laundry-moalboal/", "Laundry"),
    ("/faq/", "FAQ"), ("/contact/", "Contact"),
]

def esc(s): return html.escape(s, quote=True)

def img(name, alt, cls="", w=1600, lazy=True, sizes="(max-width: 800px) 100vw, 800px"):
    return (f'<img src="/images/{name}.webp" srcset="/images/{name}-800.webp 800w, /images/{name}.webp 1600w" '
            f'sizes="{sizes}" alt="{esc(alt)}" class="{cls}" {"loading=lazy decoding=async" if lazy else "fetchpriority=high"}>')

def hotel_schema():
    return {
        "@context": "https://schema.org", "@type": ["Hotel", "LodgingBusiness"],
        "@id": BASE + "/#hotel", "name": SITE_NAME, "alternateName": ["Oia Suites", "Oia Moalboal"],
        "url": BASE + "/", "logo": BASE + "/images/logo.png", "image": [BASE + "/images/exterior-side.webp", BASE + "/images/suite-1-a.webp", BASE + "/images/living-room.webp"],
        "description": "Newly built guesthouse with five air-conditioned suites in Basdiot, Moalboal, Cebu. King-size beds, private bathrooms, balconies, work desks, 250 Mbps fiber internet with Starlink backup, shared kitchen, free parking, 2 minutes from a quiet beach.",
        "telephone": PHONE_TEL, "email": EMAIL, "priceRange": "PHP 1,500 - PHP 2,500",
        "currenciesAccepted": "PHP", "paymentAccepted": "Cash, Credit Card, Debit Card",
        "address": {"@type": "PostalAddress", "streetAddress": "Oltmanns Road, Tongo, Basdiot", "addressLocality": "Moalboal", "addressRegion": "Cebu", "postalCode": "6032", "addressCountry": "PH"},
        "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LNG},
        "hasMap": MAPS, "checkinTime": "13:00", "checkoutTime": "12:00", "numberOfRooms": 5,
        "petsAllowed": True, "smokingAllowed": False,
        "availableLanguage": ["English", "Filipino", "Cebuano", "Dutch", "German", "Spanish", "French"],
        "sameAs": [FB] + [p[1] for p in PLATFORMS],
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True} for n in [
            "Free WiFi 250 Mbps fiber", "Starlink backup internet", "Air conditioning", "Private bathroom", "Balcony", "Work desk",
            "Shared kitchen", "Free parking", "Free drinking water", "Smart TV with Netflix", "Laundry service", "Luggage storage",
            "Free pick-up from Jollibee Moalboal", "Motorbike rental", "Tour desk", "Airport shuttle", "Pets allowed", "Non-smoking rooms", "Beach access 2 minutes"]],
        "containsPlace": [{"@type": "HotelRoom", "@id": f"{BASE}/rooms/{r['slug']}/#room", "name": r["name"], "url": f"{BASE}/rooms/{r['slug']}/"} for r in ROOMS],
    }

def website_schema():
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": SITE_NAME, "publisher": {"@id": BASE + "/#hotel"}, "inLanguage": "en"}

def breadcrumb(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (u, n) in enumerate(items)]}

def layout(path, title, desc, body, schemas=(), og_image="/images/og-image.jpg", crumbs=None, h1_in_body=True):
    canonical = BASE + path
    active = lambda u: ' aria-current="page"' if (u == path or (u != "/" and path.startswith(u))) else ""
    nav = "".join(f'<li><a href="{u}"{active(u)}>{n}</a></li>' for u, n in NAV)
    all_schemas = [hotel_schema(), website_schema()] + list(schemas)
    if crumbs: all_schemas.append(breadcrumb(crumbs))
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in all_schemas)
    crumb_html = ""
    if crumbs:
        crumb_html = '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(
            (f'<li><a href="{u}">{esc(n)}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{esc(n)}</li>') for i, (u, n) in enumerate(crumbs)) + "</ol></nav>"
    platforms = "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{n}</a> <span>{r}</span></li>' for n, u, r, c in PLATFORMS)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0f3d5e">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/images/favicon-32.png" type="image/png">
<link rel="apple-touch-icon" href="/images/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/style.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/"><img src="/images/logo-192.png" width="52" height="56" alt="OIA Suites Moalboal logo"><span>OIA Suites<small>Moalboal, Cebu</small></span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span></span><span></span><span></span></button>
    <nav id="nav" class="site-nav"><ul>{nav}</ul><a class="btn btn-primary nav-cta" href="/availability/">Check availability</a></nav>
  </div>
</header>
<main id="main">
{crumb_html}
{body}
</main>
<footer class="site-footer">
  <div class="wrap grid-4">
    <div>
      <img src="/images/logo-192.png" width="96" height="104" alt="" loading="lazy">
      <p>{SITE_NAME}<br>{ADDRESS}</p>
      <p><a href="{MAPS}" rel="noopener" target="_blank">Open in Google Maps</a></p>
    </div>
    <div>
      <h2>Contact</h2>
      <ul class="plain">
        <li><a href="tel:{PHONE_TEL}">{PHONE}</a> (call or text)</li>
        <li><a href="https://wa.me/{WHATSAPP_WA}" rel="noopener" target="_blank">WhatsApp {WHATSAPP}</a></li>
        <li><a href="{MESSENGER}" rel="noopener" target="_blank">Facebook Messenger</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>Staff on site 8:00 AM - 8:00 PM, family member 8:00 PM - 8:00 AM</li>
      </ul>
    </div>
    <div>
      <h2>Also on</h2>
      <ul class="plain platforms">{platforms}</ul>
    </div>
    <div>
      <h2>Pages</h2>
      <ul class="plain">{"".join(f'<li><a href="{u}">{n}</a></li>' for u, n in NAV)}<li><a href="/rooms/suite-1/">Suite 1</a> · <a href="/rooms/suite-2/">2</a> · <a href="/rooms/suite-3/">3</a> · <a href="/rooms/suite-4/">4</a> · <a href="/rooms/suite-5/">5</a></li></ul>
    </div>
  </div>
  <div class="wrap copy"><p>© {datetime.date.today().year} {SITE_NAME}. Bookings through this website are requests and are confirmed by the team before they are final.</p></div>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>"""

def write(path, content):
    full = os.path.join(OUT, path.lstrip("/"))
    if path.endswith("/"): full = os.path.join(full, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f: f.write(content)

def review_card(r):
    return f'''<figure class="review"><blockquote><p>{esc(r["text"])}</p></blockquote><figcaption>{esc(r["name"])}, {esc(r["origin"])} · <a href="{r["url"]}" rel="noopener nofollow" target="_blank">{r["platform"]}</a></figcaption></figure>'''

def room_card(r):
    return f'''<article class="card room-card">
  <a href="/rooms/{r['slug']}/">{img(r['photos'][0], f"{r['name']} at OIA Suites Moalboal: king-size bed, desk and balcony", "card-img")}</a>
  <div class="card-body">
    <h3><a href="/rooms/{r['slug']}/">{r['name']}</a></h3>
    <p class="meta">{r['size']} m² · {esc(r['bed'])} · up to {r['guests']} guests · {esc(r['view'].lower())}</p>
    <p>{esc(r['intro'].split('. ')[0])}.</p>
    <div class="card-actions"><a class="btn btn-primary" href="/availability/?room={r['slug']}">Check availability</a><a class="btn btn-ghost" href="/rooms/{r['slug']}/">Details</a></div>
  </div>
</article>'''

# ---------------------------------------------------------------- pages
def page_home():
    rooms = "".join(room_card(r) for r in ROOMS)
    reviews = "".join(review_card(r) for r in REVIEWS[:6])
    platforms = "".join(f'<li><a href="{u}" rel="noopener" target="_blank"><strong>{r}</strong><span>{n}</span><small>{c}</small></a></li>' for n, u, r, c in PLATFORMS)
    body = f"""
<section class="hero">
  {img("exterior-side", "OIA Suites Moalboal, newly built two-storey guesthouse in Basdiot, Moalboal", "hero-img", lazy=False, sizes="100vw")}
  <div class="hero-text wrap">
    <p class="eyebrow">Basdiot · Moalboal · Cebu</p>
    <h1>Five quiet suites, two minutes from the sea, built for people who stay a while</h1>
    <p class="lead">Newly built guesthouse with king-size beds, private bathrooms, balconies, 250 Mbps fiber internet with Starlink backup and a shared kitchen. Rated 9.4 on Booking.com and 4.96 on Airbnb.</p>
    <div class="hero-actions"><a class="btn btn-primary btn-lg" href="/availability/">Check availability</a><a class="btn btn-light btn-lg" href="/rooms/">See the rooms</a></div>
  </div>
</section>

<section class="wrap ratings">
  <ul class="rating-strip">{platforms}</ul>
</section>

<section class="wrap intro-grid">
  <div>
    <h2>A small guesthouse in a quiet corner of Moalboal</h2>
    <p>OIA Suites sits on Oltmanns Road in Tongo, Basdiot, a residential lane just before Turtle Bay Dive Resort. It is a two-storey house finished to European standards in 2025, with five guest suites upstairs and a large shared kitchen, dining and living area downstairs. A small beach with good snorkelling is a two-minute walk away; Panagsama Beach and the dive shops are 13 minutes on foot or five minutes by scooter.</p>
    <p>The house is run on site by a small local team from 8:00 AM to 8:00 PM, with a family member reachable through the night. Guests can book tours, motorbikes, laundry and transfers at the counter, and every arriving guest is collected free of charge from Jollibee Moalboal or the bus stop.</p>
    <ul class="checks">
      <li>Five suites of 24 to 25 m², each with king-size bed, en-suite bathroom, desk and balcony</li>
      <li>Globe fiber 250 Mbps plus Starlink Gen 3 backup, in every room</li>
      <li>Shared kitchen with ice-making fridge, espresso machine and grill</li>
      <li>Free parking, free drinking water, daily cleaning, pets welcome</li>
    </ul>
  </div>
  <div class="intro-imgs">
    {img("living-room", "Shared living room with sofas and smart TV at OIA Suites Moalboal")}
    {img("beach-boat", "Outrigger boat on the quiet beach two minutes from OIA Suites")}
  </div>
</section>

<section class="wrap">
  <div class="section-head"><h2>The five suites</h2><p>All rooms are on the first floor and share the same standard: king-size bed, private hot-and-cold shower, air conditioning, work desk, smart TV and balcony. The differences are in the colours, the outlook and the number of guests.</p></div>
  <div class="grid-3">{rooms}</div>
</section>

<section class="band">
  <div class="wrap band-grid">
    <div>
      <p class="eyebrow">Remote work</p>
      <h2>Possibly the best base for digital nomads in Cebu</h2>
      <p>Fast fiber with satellite backup, a proper desk and office chair in every suite, air conditioning, a quiet lane away from the bars and a kitchen for long stays. Guests have taken job interviews and full working days from their rooms.</p>
      <a class="btn btn-light" href="/accommodation-for-digital-nomads/">Why remote workers choose OIA Suites</a>
    </div>
    {img("workspace", "Desk with office chair and king-size bed in a suite at OIA Suites Moalboal")}
  </div>
</section>

<section class="wrap two-col">
  {img("kitchen-island", "Kitchen island at OIA Suites Moalboal where breakfast is prepared and served")}
  <div>
    <p class="eyebrow">Breakfast</p>
    <h2>Tosilog, bacsilog or an American set, cooked to order</h2>
    <p>There is no restaurant in the lane and nothing open early on Panagsama. Breakfast is cooked in the house kitchen instead: five Filipino silog sets or an American set, {BREAKFAST_PRICE} per serving with {BREAKFAST_INCLUDED}, served {BREAKFAST_HOURS} in the dining room or on the balcony. Order it at the counter the evening before. Guests leaving early for Oslob or canyoneering can have it earlier or packed to take along.</p>
    <a class="btn btn-ghost" href="/breakfast/">See the breakfast menu</a>
  </div>
</section>

<section class="wrap">
  <div class="section-head"><h2>What guests say</h2><p>Quotes from public reviews on Booking.com and Airbnb. Booking.com score 9.4 from 126 reviews; Airbnb host rating 4.96 from 154 reviews.</p></div>
  <div class="grid-3 reviews">{reviews}</div>
</section>

<section class="wrap two-col">
  <div>
    <h2>Around the house</h2>
    <ul class="distances">
      <li><strong>2 min walk</strong> small beach with snorkelling and starfish</li>
      <li><strong>13 min walk / 5 min scooter</strong> Panagsama Beach, dive shops, restaurants and the sardine run</li>
      <li><strong>10 min scooter</strong> Moalboal town, market and Ceres bus stop</li>
      <li><strong>20 min scooter</strong> White Beach (Basdaku)</li>
      <li><strong>30 min</strong> Kawasan Falls and Badian canyoneering</li>
      <li><strong>1.5 h</strong> Oslob whale sharks</li>
      <li><strong>3 h</strong> Cebu City and Mactan-Cebu International Airport</li>
    </ul>
    <p><a class="btn btn-ghost" href="/services/">Tours, transfers and scooter rental</a> <a class="btn btn-ghost" href="/laundry-moalboal/">Own laundry service</a></p>
  </div>
  <div>
    {img("beach-starfish", "Starfish in the shallow water at the beach near OIA Suites Moalboal")}
  </div>
</section>

<section class="wrap cta-box">
  <h2>Ready to book?</h2>
  <p>Pick a suite and dates in the calendar and send a request. The team confirms by e-mail or WhatsApp, usually within 24 hours. No payment until the booking is confirmed.</p>
  <a class="btn btn-primary btn-lg" href="/availability/">Open the availability calendar</a>
</section>
"""
    write("/", layout("/", "OIA Suites Moalboal | Guesthouse in Basdiot, Moalboal, Cebu",
        "Five quiet suites with king-size beds, private bathrooms, balconies, 250 Mbps fiber internet and a shared kitchen, two minutes from the beach in Moalboal, Cebu. Rated 9.4 on Booking.com.",
        body))

def page_rooms():
    rooms = "".join(room_card(r) for r in ROOMS)
    feats = "".join(f"<li>{esc(f)}</li>" for f in COMMON_ROOM_FEATURES)
    body = f"""
<section class="wrap page-head"><h1>Rooms at OIA Suites Moalboal</h1><p class="lead">Five suites on the first floor of a newly built house. Each is 24 to 25 m² with a king-size bed, private bathroom with hot and cold shower, split-type air conditioning, work desk with office chair, smart TV with Netflix and a private balcony. Rates from roughly PHP 1,500 per night for two people.</p></section>
<section class="wrap"><div class="grid-3">{rooms}</div></section>
<section class="wrap two-col">
  <div><h2>In every suite</h2><ul class="checks">{feats}</ul></div>
  <div><h2>Shared by all guests</h2><ul class="checks"><li>Fully equipped kitchen with hob, microwave, espresso machine, drip coffee maker and utensils</li><li>Refrigerator with built-in ice maker</li><li>Dining area and living room with Smart UHD TV</li><li>Water dispensers on both floors</li><li>Outdoor grill</li><li>Free private parking</li><li>Luggage storage</li><li>Laundry service, motorbike rental and tour desk</li></ul></div>
</section>
<section class="wrap"><h2>Photos of the house</h2><div class="gallery">
{img("kitchen", "Shared kitchen with granite counters and pendant lights")}{img("living-room-2", "Living room with sofas, dining table and staircase")}{img("stairs", "Hallway on the first floor with the suite doors")}{img("kitchen-island", "Kitchen island with bar stools")}{img("balcony-chairs", "Balcony with two chairs among the palms")}{img("grill", "Outdoor grill for guests")}{img("exterior-front", "Front of the house with glass sliding doors and balconies")}{img("beach-shore", "Shoreline of the small beach two minutes from the house")}
</div></section>
<section class="wrap cta-box"><h2>Check dates for a suite</h2><p>The calendar shows live availability for all five rooms, refreshed every 30 minutes from the booking platforms.</p><a class="btn btn-primary btn-lg" href="/availability/">Open the calendar</a></section>
"""
    write("/rooms/", layout("/rooms/", "Rooms | Five suites with king-size bed, balcony and desk | OIA Suites Moalboal",
        "Five 24-25 m² suites with king-size bed, private hot-and-cold shower, air conditioning, work desk, smart TV and balcony. Shared kitchen, free parking. From about PHP 1,500 per night.",
        body, crumbs=[("/", "Home"), ("/rooms/", "Rooms")]))

def page_room(r):
    others = "".join(f'<li><a href="/rooms/{o["slug"]}/">{o["name"]}</a></li>' for o in ROOMS if o["n"] != r["n"])
    feats = "".join(f"<li>{esc(f)}</li>" for f in COMMON_ROOM_FEATURES)
    gallery = "".join(img(p, f"{r['name']} at OIA Suites Moalboal, photo {i+1}", lazy=(i > 0)) for i, p in enumerate(r["photos"]))
    ext = ""
    if r["airbnb"]:
        ext = f'<p class="meta">Also listed on <a href="{r["airbnb"]}" rel="noopener nofollow" target="_blank">Airbnb</a> ({esc(r["rating"])}) and <a href="https://www.booking.com/hotel/ph/oia.html" rel="noopener nofollow" target="_blank">Booking.com</a>.</p>'
    else:
        ext = '<p class="meta">Also listed on <a href="https://www.booking.com/hotel/ph/oia.html" rel="noopener nofollow" target="_blank">Booking.com</a>.</p>'
    schema = {"@context": "https://schema.org", "@type": "HotelRoom", "@id": f"{BASE}/rooms/{r['slug']}/#room", "name": f"{r['name']} - {SITE_NAME}",
              "url": f"{BASE}/rooms/{r['slug']}/", "description": r["intro"], "image": [f"{BASE}/images/{p}.webp" for p in r["photos"]],
              "floorSize": {"@type": "QuantitativeValue", "value": r["size"], "unitCode": "MTK"},
              "bed": {"@type": "BedDetails", "typeOfBed": "King", "numberOfBeds": 1},
              "occupancy": {"@type": "QuantitativeValue", "minValue": 1, "maxValue": r["guests"]},
              "containedInPlace": {"@id": BASE + "/#hotel"},
              "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": f, "value": True} for f in COMMON_ROOM_FEATURES],
              "potentialAction": {"@type": "ReserveAction", "target": f"{BASE}/availability/?room={r['slug']}", "name": "Check availability and request a booking"}}
    body = f"""
<section class="wrap page-head">
  <h1>{r['name']} at OIA Suites Moalboal</h1>
  <p class="meta">{r['size']} m² · {esc(r['bed'])} · up to {r['guests']} guests · {esc(r['floor'].lower())} · {esc(r['view'].lower())}</p>
  <p class="lead">{esc(r['intro'])}</p>
  <div class="hero-actions"><a class="btn btn-primary btn-lg" href="/availability/?room={r['slug']}">Check availability for {r['name']}</a></div>
  {ext}
</section>
<section class="wrap"><div class="gallery gallery-4">{gallery}</div></section>
<section class="wrap two-col">
  <div><h2>What is in {r['name']}</h2><ul class="checks">{feats}</ul></div>
  <div><h2>Good to know</h2><ul class="checks"><li>Check-in from 1:00 PM, check-out until 12:00 noon</li><li>Free pick-up from Jollibee Moalboal or the bus stop on arrival</li><li>Shared kitchen, living room and grill on the ground floor, free to use</li><li>Free private parking</li><li>Children welcome; baby cot on request</li><li>Pets allowed on request</li><li>Non-smoking room; quiet hours 10:00 PM to 8:00 AM</li><li>From 14 September 2026 a swimming pool is being built next to the house on weekday mornings and afternoons</li></ul></div>
</section>
<section class="wrap"><h2>Other suites</h2><ul class="inline-list">{others}</ul></section>
"""
    write(f"/rooms/{r['slug']}/", layout(f"/rooms/{r['slug']}/", f"{r['name']} | {r['size']} m², king bed, balcony | OIA Suites Moalboal",
        f"{r['name']} at OIA Suites Moalboal: {r['size']} m², {r['bed']}, private bathroom, air conditioning, desk, smart TV and balcony. Check live availability and send a booking request.",
        body, schemas=[schema], og_image=f"/images/{r['photos'][0]}.webp",
        crumbs=[("/", "Home"), ("/rooms/", "Rooms"), (f"/rooms/{r['slug']}/", r["name"])]))

def page_availability():
    room_opts = "".join(f'<option value="{r["slug"]}">{r["name"]} ({r["size"]} m², up to {r["guests"]} guests)</option>' for r in ROOMS)
    body = f"""
<section class="wrap page-head"><h1>Availability and booking requests</h1>
<p class="lead">The calendar below shows which of the five suites are free on which nights. It is refreshed every 30 minutes from the booking calendars of the platforms the house is listed on. Choose a suite, click a check-in and a check-out date, and send the request. <strong>A request is not yet a confirmed booking</strong>: the team checks it and confirms by e-mail or WhatsApp, usually within 24 hours. No payment is due until then.</p>
<p class="meta" id="avail-updated">Loading availability…</p></section>

<section class="wrap avail">
  <div class="cal-controls">
    <button class="btn btn-ghost" id="prev-month" aria-label="Previous month">‹</button>
    <h2 id="cal-title" aria-live="polite">Month</h2>
    <button class="btn btn-ghost" id="next-month" aria-label="Next month">›</button>
  </div>
  <p class="legend"><span class="lg free"></span> available <span class="lg booked"></span> booked or blocked <span class="lg sel"></span> selected <span class="lg past"></span> past</p>
  <div class="overview-wrap"><table class="overview" id="overview" aria-label="Availability of all suites for the month"><caption class="sr-only">Availability per suite per night</caption></table></div>
  <p class="meta">Tip: click a suite name in the table to open its calendar, then click the arrival date and the departure date.</p>

  <div class="room-cal" id="room-cal">
    <div class="room-cal-head"><label for="room-select">Suite</label><select id="room-select">{room_opts}</select></div>
    <div class="month-grid" id="month-grid" role="grid" aria-label="Calendar for the selected suite"></div>
    <p class="meta" id="selection-text">Select an arrival date and a departure date in the calendar.</p>
  </div>
</section>

<section class="wrap form-wrap" id="request">
  <h2>Send a booking request</h2>
  <form id="request-form" action="https://formsubmit.co/{EMAIL}" method="POST" novalidate>
    <input type="hidden" name="_subject" value="Booking request via oiasuitesmoalboal.com">
    <input type="hidden" name="_template" value="table">
    <input type="hidden" name="_next" id="next-url" value="{BASE}/request-sent/">
    <input type="text" name="_honey" class="sr-only" tabindex="-1" autocomplete="off">
    <div class="grid-2">
      <label>Suite<select name="Suite" id="f-room" required>{room_opts}</select></label>
      <label>Guests<select name="Guests" id="f-guests"><option>1</option><option selected>2</option><option>3</option></select></label>
      <label>Check-in<input type="date" name="Check-in" id="f-checkin" required></label>
      <label>Check-out<input type="date" name="Check-out" id="f-checkout" required></label>
      <label>Full name<input type="text" name="Name" required autocomplete="name"></label>
      <label>E-mail<input type="email" name="_replyto" required autocomplete="email"></label>
      <label>WhatsApp or phone (optional)<input type="tel" name="Phone" autocomplete="tel"></label>
      <label>Arrival time and transport (optional)<input type="text" name="Arrival" placeholder="e.g. Ceres bus, arriving around 4 PM"></label>
    </div>
    <label>Message (optional)<textarea name="Message" rows="4" placeholder="Purpose of stay, remote work, extra bed for a child, tours, anything else"></textarea></label>
    <p class="meta">By sending this request the details above go to the OIA Suites team by e-mail. The team replies with a confirmation or alternative dates. Nothing is charged at this stage.</p>
    <button class="btn btn-primary btn-lg" type="submit">Send booking request</button>
    <p class="form-error" id="form-error" hidden></p>
  </form>
  <p class="alt-contact">Prefer to ask first? <a href="https://wa.me/{WHATSAPP_WA}" rel="noopener" target="_blank">WhatsApp</a>, <a href="{MESSENGER}" rel="noopener" target="_blank">Messenger</a> or <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
</section>
<script src="/assets/calendar.js" defer></script>
"""
    write("/availability/", layout("/availability/", "Availability calendar and booking request | OIA Suites Moalboal",
        "Live availability for all five suites at OIA Suites Moalboal, refreshed every 30 minutes from the booking platform calendars. Send a booking request; the team confirms within 24 hours.",
        body, crumbs=[("/", "Home"), ("/availability/", "Availability")]))

def page_nomads():
    path = "/accommodation-for-digital-nomads/"
    proof = "".join(review_card(r) for r in [REVIEWS[0], REVIEWS[3], REVIEWS[2], REVIEWS[7]])
    schema = {"@context": "https://schema.org", "@type": "WebPage", "@id": BASE + path + "#webpage", "url": BASE + path,
              "name": "Accommodation for digital nomads in Moalboal, Cebu", "about": {"@id": BASE + "/#hotel"}, "isPartOf": {"@id": BASE + "/#website"},
              "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".lead", ".facts"]}}
    body = f"""
<section class="wrap page-head">
  <p class="eyebrow">Remote work in Moalboal</p>
  <h1>Accommodation for digital nomads in Moalboal, Cebu</h1>
  <p class="lead">OIA Suites was built with remote workers in mind, and the reviews back that up: stable 250 Mbps fiber with Starlink backup, a real desk and office chair in every suite, air conditioning that keeps a laptop room cool, a quiet lane, and a full kitchen for weeks rather than nights. For anyone working online from Cebu, and arguably from anywhere in the Philippines, it is hard to find a better set-up at this price.</p>
  <div class="hero-actions"><a class="btn btn-primary btn-lg" href="/availability/">Check availability</a><a class="btn btn-ghost btn-lg" href="#proof">Read what remote workers say</a></div>
</section>

<section class="wrap two-col">
  {img("workspace-2", "Work desk with office chair next to the bed in a suite at OIA Suites Moalboal")}
  <div>
    <h2>Why Moalboal is a good place to work from</h2>
    <p>Moalboal is a small coastal town on the south-west side of Cebu island, about three hours from Cebu City. It is known for the sardine run at Panagsama Beach, turtles a few metres from shore, Kawasan Falls and canyoneering in nearby Badian, and whale sharks in Oslob down the coast. Living costs are low, the pace is slow and the time zone (UTC+8) lines up with Australian mornings and European afternoons. What Moalboal has lacked is accommodation where the internet actually holds up. That is the gap OIA Suites fills.</p>
  </div>
</section>

<section class="wrap facts">
  <h2>The facts</h2>
  <div class="grid-3 fact-cards">
    <div class="fact"><h3>250 Mbps fiber + Starlink</h3><p>Globe fiber internet with 250 Mbps download, with a Starlink Gen 3 V4 dish as backup. Both are mounted on the property and cover every suite and the common areas. Guests rate the WiFi 9.2 on Booking.com.</p></div>
    <div class="fact"><h3>A desk in every room</h3><p>Each suite has a work desk with an office chair, power sockets by the bed, and a large smart TV that doubles as a second screen. Blackout curtains and split-type air conditioning keep the room cool and dark for calls at odd hours.</p></div>
    <div class="fact"><h3>Quiet by design</h3><p>The house is in a residential lane in Tongo, Basdiot, 13 minutes on foot from the bars of Panagsama. Quiet hours from 10 PM to 8 AM, five rooms in total, and a team on site during the day.</p></div>
    <div class="fact"><h3>Kitchen for long stays</h3><p>A full shared kitchen with hob, microwave, espresso machine, ice-making fridge and utensils. Free drinking water on both floors. A grill outside. Groceries are 10 minutes away at Moalboal market and Gaisano Grand.</p></div>
    <div class="fact"><h3>Everything arranged at the counter</h3><p>Scooter rental from PHP 300 per day, laundry collected and returned the next day, tours and transfers booked on the spot, free pick-up on arrival. Less admin, more work done.</p></div>
    <div class="fact"><h3>Rated by the people who stayed</h3><p>Booking.com 9.4 from 126 reviews. Airbnb host rating 4.96 from 154 reviews, Superhost. Agoda 9.6. Cleanliness scores 9.7 to 10 across platforms.</p></div>
  </div>
</section>

<section class="wrap two-col">
  <div>
    <h2>A working week at OIA Suites</h2>
    <p>Mornings start with breakfast in the room or the dining area (Filipino or American set for PHP 250, ordered the night before) and a swim or snorkel at the small beach two minutes down the lane. Work happens at the desk in the suite or at the big table downstairs. Afternoons are for calls with Europe; evenings are for a scooter ride to Panagsama for dinner, or the grill at the house. Weekends are Kawasan Falls, the sardine run, Osmeña Peak or a day at White Beach.</p>
    <h2>Long stays</h2>
    <p>Rooms can be booked per night on the platforms, but for stays of a week or longer it is better to send a request through this website with the intended dates. The team quotes a long-stay rate directly. Daily cleaning is included and laundry can be arranged at the counter.</p>
  </div>
  <div class="intro-imgs">{img("starlink", "Starlink dish mounted above the house as backup internet")}{img("kitchen-2", "Shared kitchen at OIA Suites with coffee machine and hob")}</div>
</section>

<section class="wrap" id="proof">
  <div class="section-head"><h2>What remote workers and long-stay guests say</h2><p>Quotes from public reviews on Booking.com and Airbnb.</p></div>
  <div class="grid-2 reviews">{proof}</div>
</section>

<section class="wrap">
  <h2>Practical notes for working from Moalboal</h2>
  <ul class="checks">
    <li>Power: the local grid is generally reliable, but short interruptions happen in the Visayas. The team knows the quietest room and best times for important calls; a laptop with a charged battery bridges most outages.</li>
    <li>Mobile data: Globe and Smart both have 4G/LTE coverage in Basdiot. A local SIM or eSIM is a sensible second backup.</li>
    <li>Working spots: the desk in the suite and the big table downstairs are the usual places to work; cafés along Panagsama offer a change of scene.</li>
    <li>Visa: most nationalities get 30 days on arrival in the Philippines, extendable at the Bureau of Immigration in Cebu City. Check the current rules for the relevant passport before travelling.</li>
    <li>Construction: from 14 September 2026 a swimming pool is being built next to the house on weekdays from 8 to 11 AM and 2 to 5 PM. Guests who need silence in those hours should mention it in the request.</li>
  </ul>
</section>

<section class="wrap cta-box"><h2>Book a suite for the coming weeks</h2><p>Pick dates in the calendar and mention remote work and the intended length of stay in the message. The team replies with a long-stay quote.</p><a class="btn btn-primary btn-lg" href="/availability/">Check availability</a></section>
"""
    write(path, layout(path, "Accommodation for digital nomads in Moalboal, Cebu | OIA Suites",
        "250 Mbps fiber with Starlink backup, desk and office chair in every suite, air conditioning, quiet lane, shared kitchen. Why OIA Suites in Moalboal is a strong base for remote workers in Cebu and the Philippines.",
        body, schemas=[schema], og_image="/images/workspace.webp", crumbs=[("/", "Home"), (path, "Digital nomads")]))

def page_services():
    path = "/services/"
    offers = [
        ("Breakfast", "PHP 250 per serving", "Filipino set (tosilog, hotsilog, longsilog, bacsilog or cornsilog with garlic rice and eggs) or American set (bacon, whole-wheat bread, omelette, marmalade, butter), all served with coffee, juice and fruit. Tortang talong and chicken tinola by pre-order. Available 6:00 to 10:00 AM; order the night before at the counter or by message."),
        ("Motorbike rental", "PHP 300 to 600 per day", "Yamaha Mio PHP 300, Honda Click PHP 400, Honda ADV160 PHP 600 per day, rented at the house. A valid driving licence is required."),
        ("Car transfers", "PHP 150 to 2,500", "Panagsama Beach PHP 150, Moalboal bus stop PHP 150, White Beach PHP 250, Oslob or Liloan port PHP 2,500. Private car with driver, up to 4 passengers. Pick-up from Jollibee Moalboal at check-in is free."),
        ("Sardine run and turtle snorkelling", "PHP 500 per person", "1 to 1.5 hours in the water at Panagsama with a guide, goggles and life jacket, entrance fee, pick-up and drop-off included."),
        ("Badian canyoneering to Kawasan Falls", "PHP 2,100 per person", "4 to 5 hours of jumping, swimming and trekking through the canyon to Kawasan Falls. Includes pick-up and drop-off, registration fee, gear, guide and lunch."),
        ("Chasing waterfalls", "PHP 2,500 per person", "Three waterfalls of choice from Cambais, Hidden, Inambakan, Dao, Kanlaob and Tumalog Falls. Includes transport, entrance fees and guide."),
        ("Whale shark watching in Oslob", "PHP 1,800 to 3,500 per person", "Joiner van PHP 1,800 (pick-up 3:20 AM), private car PHP 2,000 (pick-up 5:00 AM), by scuba PHP 3,500. Includes pick-up and drop-off, entrance fee, boat, gear and guide."),
        ("Oslob private tour", "PHP 4,000 per person", "Whale sharks, Tumalog Falls and Sumilon Island in one day. Includes transport, guides and entrance fees. Private car only (without guide and fees) PHP 3,000 for up to 4 passengers."),
        ("Osmeña Peak and Casino Peak trekking", "PHP 1,800 per person", "About 5 hours in total to the highest point of Cebu and the neighbouring Casino Peak. Includes transport, entrance fees and guide. Private car only PHP 2,500 for up to 4 passengers."),
        ("Laundry", "PHP 190 per load", "Collected at the house and returned the next day, washed, dried and folded, through Laundry Lounge Cebu, the own laundry of OIA Suites in Moalboal town. Up to 9 kg per load."),
    ]
    cards = "".join(f'<div class="fact"><h3>{esc(n)}</h3><p class="price">{esc(p)}</p><p>{esc(d)}</p></div>' for n, p, d in offers)
    schema = {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "Services and tours at OIA Suites Moalboal", "url": BASE + path,
              "itemListElement": [{"@type": "Offer", "name": n, "description": d, "price": p.replace("PHP ", "").split(" ")[0].replace(",", ""), "priceCurrency": "PHP", "seller": {"@id": BASE + "/#hotel"}} for n, p, d in offers if p.startswith("PHP")]}
    body = f"""
<section class="wrap page-head"><h1>Services, tours and transfers</h1><p class="lead">Everything below is arranged at the counter or by message. Prices are in Philippine peso and were last checked in September 2026; entrance fees are included where stated. Tour prices may change with fuel costs and local fees, so the team confirms the current price when booking.</p></section>
<section class="wrap"><div class="grid-3 fact-cards">{cards}</div></section>
<section class="wrap two-col">
  <div><h2>Getting to OIA Suites</h2>
  <p><strong>From Mactan-Cebu International Airport or Cebu City:</strong> taxi or Grab to Cebu South Bus Terminal, then a Ceres bus towards Bato via Barili; get off in Moalboal town (about 3 hours, roughly PHP 200 to 250). From the bus stop or Jollibee Moalboal the team collects guests free of charge. A private van or car from the airport can be arranged in advance.</p>
  <p><strong>From Oslob, Dumaguete or the south:</strong> Ceres bus to Moalboal via Bato, or a private car from Liloan port (PHP 2,500).</p>
  <p><strong>Address:</strong> {ADDRESS}, just before Turtle Bay Dive Resort. <a href="{MAPS}" rel="noopener" target="_blank">Open in Google Maps</a>.</p></div>
  {img("exterior-day", "OIA Suites seen from the lane, with the turquoise stairwell and balconies")}
</section>
<section class="wrap"><h2>Own laundry</h2><p>OIA Suites runs its own laundry in Moalboal town, Laundry Lounge Cebu. Linen and towels are washed there, and guests can hand in laundry at the counter. Details, rates and photos on the <a href="/laundry-moalboal/">laundry page</a>.</p></section>
<section class="wrap cta-box"><h2>Book tours together with the room</h2><p>Mention the tours of interest in the booking request and the team prepares them for arrival.</p><a class="btn btn-primary btn-lg" href="/availability/">Check availability</a></section>
"""
    write(path, layout(path, "Services and tours: breakfast, scooter rental, transfers, Kawasan, Oslob | OIA Suites Moalboal",
        "Breakfast for PHP 250, scooters from PHP 300 per day, sardine run snorkelling PHP 500, Badian canyoneering PHP 2,100, Oslob whale sharks from PHP 1,800, transfers and laundry at OIA Suites Moalboal.",
        body, schemas=[schema], og_image="/images/exterior-day.webp", crumbs=[("/", "Home"), (path, "Services & Tours")]))

def page_laundry():
    path = "/laundry-moalboal/"
    schema = {"@context": "https://schema.org", "@type": "WebPage", "@id": BASE + path + "#webpage", "url": BASE + path,
              "name": "Laundry service in Moalboal for guests of OIA Suites", "about": {"@id": BASE + "/#hotel"}, "isPartOf": {"@id": BASE + "/#website"},
              "mentions": {"@type": "LocalBusiness", "@id": LAUNDRY_URL + "#business", "name": LAUNDRY_NAME, "url": LAUNDRY_URL, "telephone": LAUNDRY_PHONE,
                           "address": {"@type": "PostalAddress", "streetAddress": "Calumpang Road, Lot 502, Poblacion West", "addressLocality": "Moalboal", "addressRegion": "Cebu", "postalCode": "6032", "addressCountry": "PH"},
                           "openingHours": "Mo-Su 08:00-20:00", "parentOrganization": {"@id": BASE + "/#hotel"}}}
    offer = {"@context": "https://schema.org", "@type": "Offer", "name": "Laundry for guests: wash, dry and fold", "url": BASE + path, "price": "190", "priceCurrency": "PHP",
             "description": "Wash, dry and fold per load of up to 9 kg, collected at OIA Suites and returned the next day.", "seller": {"@id": BASE + "/#hotel"}}
    body = f"""
<section class="wrap page-head">
  <p class="eyebrow">Own laundry, clean linen</p>
  <h1>Laundry in Moalboal: OIA Suites runs its own laundry</h1>
  <p class="lead">OIA Suites Moalboal is one of the few places to stay in Moalboal with its own laundry business. Every sheet, pillowcase and towel in the five suites is washed at <a href="{LAUNDRY_URL}" rel="noopener" target="_blank">{LAUNDRY_NAME}</a>, the sister business in Moalboal town. Guests can hand in their own laundry at the counter and get it back washed, dried and folded the next day.</p>
  <div class="hero-actions"><a class="btn btn-primary btn-lg" href="/availability/">Check availability</a><a class="btn btn-ghost btn-lg" href="#guests">Laundry for guests</a></div>
</section>

<section class="wrap two-col">
  {img("laundry-machines", "Row of stacked commercial washers and dryers at Laundry Lounge Cebu in Moalboal")}
  <div>
    <h2>Why an own laundry matters for a guesthouse</h2>
    <p>Most small hotels in Moalboal send their linen to a third party or wash it in a household machine. OIA Suites controls the whole cycle itself. Bed linen and towels go through commercial machines imported from Germany, with German detergents, built for hotel volumes rather than a family wash. It shows: cleanliness scores at OIA Suites sit between 9.7 and 10 on Booking.com, Airbnb and Agoda.</p>
    <p>It also means fresh linen is never the bottleneck. On changeover days the laundry runs the same day, so a suite can be turned around without cutting corners, and extra towels or a mid-stay change of sheets are a matter of asking.</p>
  </div>
</section>

<section class="wrap facts">
  <h2>The facts</h2>
  <div class="grid-3 fact-cards">
    <div class="fact"><h3>Commercial machines</h3><p>Stacked washer and dryer units imported from Germany, with imported detergents. One load takes up to 9 kilos.</p></div>
    <div class="fact"><h3>Open every day</h3><p>{LAUNDRY_NAME} is open Monday to Sunday from 8:00 AM to 8:00 PM at Calumpang Road, Poblacion West, Moalboal.</p></div>
    <div class="fact"><h3>Same-day turnaround</h3><p>Wash, dry and fold usually takes about two hours at the shop. Laundry handed in at OIA Suites is back the next day.</p></div>
    <div class="fact"><h3>Fixed price per load</h3><p>Wash, dry and fold PHP 190 per load of up to 9 kg. Wash and dry only PHP 180. Self-service at the shop PHP 65 per machine.</p></div>
    <div class="fact"><h3>Collected at the house</h3><p>No need to find a laundromat or carry a bag of clothes on a scooter. Hand the laundry to the team at the counter and it comes back folded.</p></div>
    <div class="fact"><h3>Trusted by the town</h3><p>{LAUNDRY_NAME} serves households, resorts and partner hotels in Moalboal and picks up in Badian, Alegria and Malabuyoc as well.</p></div>
  </div>
</section>

<section class="wrap two-col" id="guests">
  <div>
    <h2>Laundry for guests</h2>
    <p>Hand in a bag of laundry at the counter before noon and it is back the next day, washed, dried and folded. The rate is the shop rate of PHP 190 per load of up to 9 kilos, paid at check-out or directly at collection. Delicate items and anything that should not go in the dryer can be marked; the team passes it on.</p>
    <p>For longer stays this adds up. Digital nomads and travellers staying a week or more can travel with a small backpack and have laundry done once or twice a week for less than the price of a meal on Panagsama. Divers get salty wetsuit shirts and towels back dry the next morning.</p>
    <h2>Doing it yourself</h2>
    <p>Anyone who prefers self-service can bring laundry to the shop in Moalboal town, use a machine for PHP 65 and wait with free WiFi and a drink. The shop also does printing and copying, which is handy for boarding passes and permits.</p>
  </div>
  <div class="intro-imgs">{img("laundry-folding", "Staff folding and sorting clean laundry at Laundry Lounge Cebu")}{img("laundry-sorting", "Freshly washed clothes being folded on the counter at the laundry shop in Moalboal")}</div>
</section>

<section class="wrap">
  <h2>Contact the laundry directly</h2>
  <p>{LAUNDRY_NAME}, Calumpang Road, Lot 502, Poblacion West, Moalboal, Cebu 6032. Phone <a href="tel:{LAUNDRY_PHONE_TEL}">{LAUNDRY_PHONE}</a>. Website <a href="{LAUNDRY_URL}" rel="noopener" target="_blank">laundryloungecebu.ph</a>, rates at <a href="{LAUNDRY_URL}rates/" rel="noopener" target="_blank">laundryloungecebu.ph/rates/</a>. Guests of OIA Suites do not need to contact the shop: the team at the house handles it.</p>
</section>

<section class="wrap cta-box"><h2>Stay where the linen is always fresh</h2><p>Pick dates in the calendar and mention any laundry needs in the message.</p><a class="btn btn-primary btn-lg" href="/availability/">Check availability</a></section>
"""
    write(path, layout(path, "Laundry in Moalboal: own laundry service for guests | OIA Suites Moalboal",
        "OIA Suites Moalboal runs its own laundry, Laundry Lounge Cebu. Fresh linen washed in commercial German machines, and guest laundry washed, dried and folded for PHP 190 per load, back the next day.",
        body, schemas=[schema, offer], og_image="/images/laundry-machines.webp", crumbs=[("/", "Home"), (path, "Laundry")]))

def page_breakfast():
    path = "/breakfast/"
    sets = "".join(f'<div class="fact"><h3>{esc(n)}</h3><p>{esc(d)}</p></div>' for n, d in BREAKFAST_MENU)
    pre = "".join(f'<div class="fact"><h3>{esc(n)}</h3><p>{esc(d)}</p></div>' for n, d in BREAKFAST_PREORDER)
    menu = {"@context": "https://schema.org", "@type": "Menu", "@id": BASE + path + "#menu", "url": BASE + path,
            "name": "Breakfast menu at OIA Suites Moalboal", "inLanguage": "en",
            "hasMenuSection": [
                {"@type": "MenuSection", "name": "Breakfast sets", "description": f"Served {BREAKFAST_HOURS}, with {BREAKFAST_INCLUDED}.",
                 "hasMenuItem": [{"@type": "MenuItem", "name": n, "description": d,
                                  "offers": {"@type": "Offer", "price": BREAKFAST_PRICE.replace("PHP ", ""), "priceCurrency": "PHP"}} for n, d in BREAKFAST_MENU]},
                {"@type": "MenuSection", "name": "On pre-order", "description": "Ordered a day in advance.",
                 "hasMenuItem": [{"@type": "MenuItem", "name": n, "description": d,
                                  "offers": {"@type": "Offer", "price": BREAKFAST_PRICE.replace("PHP ", ""), "priceCurrency": "PHP"}} for n, d in BREAKFAST_PREORDER]},
            ]}
    offer = {"@context": "https://schema.org", "@type": "Offer", "name": "Breakfast at OIA Suites Moalboal", "url": BASE + path,
             "price": BREAKFAST_PRICE.replace("PHP ", ""), "priceCurrency": "PHP", "seller": {"@id": BASE + "/#hotel"},
             "description": f"Filipino or American breakfast, {BREAKFAST_PRICE} per serving, served {BREAKFAST_HOURS} with {BREAKFAST_INCLUDED}. Ordered the evening before."}
    body = f"""
<section class="wrap page-head">
  <p class="eyebrow">Ordered the night before</p>
  <h1>Breakfast at OIA Suites Moalboal</h1>
  <p class="lead">Breakfast is cooked to order in the house kitchen: five Filipino silog sets or an American set, {BREAKFAST_PRICE} per serving, served {BREAKFAST_HOURS} with {BREAKFAST_INCLUDED}. Order at the counter the evening before or send a message, and say whether it should be in the dining room or on the balcony.</p>
  <div class="hero-actions"><a class="btn btn-primary btn-lg" href="/availability/">Check availability</a><a class="btn btn-ghost btn-lg" href="#menu">See the menu</a></div>
</section>

<section class="wrap two-col">
  {img("kitchen", "The kitchen at OIA Suites Moalboal where breakfast is cooked to order")}
  <div>
    <h2>Why order it in the house</h2>
    <p>There is no restaurant on site and nothing open for breakfast in the lane. The nearest places to eat are on Panagsama Beach, five minutes away by scooter, and most of them start serving later than guests who dive, snorkel or take a call with Europe want to eat. Breakfast at the house closes that gap: it is ready when it is asked for, at a price no restaurant in Moalboal matches for a full plate with coffee.</p>
    <p>Guests on an early tour, the Oslob van leaves around 3:20 AM and canyoneering not much later, can ask for breakfast before 6:00 AM or have it packed to take along. Mention it when ordering.</p>
  </div>
</section>

<section class="wrap facts" id="menu">
  <div class="section-head"><h2>The menu</h2><p>Every set is {BREAKFAST_PRICE} per person and comes with {BREAKFAST_INCLUDED}. The Filipino sets are silog dishes: a protein with <em>sinangag</em> (garlic rice) and <em>itlog</em> (fried egg).</p></div>
  <div class="grid-3 fact-cards">{sets}</div>
</section>

<section class="wrap facts">
  <div class="section-head"><h2>On pre-order</h2><p>Ordered a day ahead rather than the evening before, because they are cooked from scratch.</p></div>
  <div class="grid-2 fact-cards">{pre}</div>
</section>

<section class="wrap two-col">
  <div>
    <h2>How to order</h2>
    <ul class="checks">
      <li>Tell the team at the counter the evening before, or send a message on <a href="https://wa.me/{WHATSAPP_WA}" rel="noopener" target="_blank">WhatsApp</a> or <a href="{MESSENGER}" rel="noopener" target="_blank">Messenger</a>.</li>
      <li>Say which set, for how many people, and at what time.</li>
      <li>Say where: the dining table downstairs or the balcony of the suite.</li>
      <li>Tortang talong and chicken tinola need a day's notice.</li>
      <li>Leaving before 6:00 AM for a tour? Ask for it earlier or packed to take along.</li>
      <li>Paid at check-out together with the room, or per serving at the counter.</li>
    </ul>
    <h2>Or make it yourself</h2>
    <p>The shared kitchen on the ground floor is free to use and has a hob, microwave, a refrigerator with built-in ice maker, an espresso machine and a drip coffee maker. Coffee, tea and drinking water are free for all guests, around the clock. Groceries come from the market or Gaisano Grand in Moalboal town, 10 minutes away by scooter.</p>
  </div>
  <div class="intro-imgs">{img("living-room-2", "Dining table on the ground floor where breakfast is served at OIA Suites Moalboal")}{img("balcony-chairs", "Balcony with two chairs where breakfast can be served in the suite")}</div>
</section>

<section class="wrap cta-box"><h2>Book a suite and add breakfast on arrival</h2><p>Pick dates in the calendar. Breakfast does not have to be arranged in advance; ordering it on the first evening is enough.</p><a class="btn btn-primary btn-lg" href="/availability/">Check availability</a></section>
"""
    write(path, layout(path, f"Breakfast: Filipino and American sets, {BREAKFAST_PRICE} | OIA Suites Moalboal",
        f"Breakfast at OIA Suites Moalboal: tosilog, bacsilog, longsilog, hotsilog, cornsilog or an American set, {BREAKFAST_PRICE} per serving with {BREAKFAST_INCLUDED}, served {BREAKFAST_HOURS} in the dining room or on the balcony.",
        body, schemas=[menu, offer], og_image="/images/kitchen.webp", crumbs=[("/", "Home"), (path, "Breakfast")]))

def page_faq():
    path = "/faq/"
    sections = ""
    qa_schema = []
    for cat, items in FAQ:
        sections += f'<section class="wrap faq-cat"><h2>{esc(cat)}</h2>'
        for q, a in items:
            sections += f'<details class="faq"><summary><h3>{esc(q)}</h3></summary><div class="faq-a"><p>{a}</p></div></details>'
            import re
            qa_schema.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}})
        sections += "</section>"
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "@id": BASE + path + "#faq", "url": BASE + path, "mainEntity": qa_schema}
    body = f"""
<section class="wrap page-head"><h1>Frequently asked questions</h1><p class="lead">Answers to the questions guests ask most before and during a stay at OIA Suites Moalboal. Anything missing? Send a message on <a href="https://wa.me/{WHATSAPP_WA}" rel="noopener" target="_blank">WhatsApp</a> or <a href="{MESSENGER}" rel="noopener" target="_blank">Messenger</a>.</p></section>
{sections}
<section class="wrap cta-box"><h2>Ready to book?</h2><a class="btn btn-primary btn-lg" href="/availability/">Check availability</a></section>
"""
    write(path, layout(path, "FAQ: booking, check-in, internet, breakfast, location | OIA Suites Moalboal",
        "Answers about booking requests, prices, check-in times, internet speed, breakfast, pets, parking, the beach, getting to Moalboal from Cebu, scooter rental and working remotely at OIA Suites.",
        body, schemas=[schema], crumbs=[("/", "Home"), (path, "FAQ")]))

def page_contact():
    path = "/contact/"
    schema = {"@context": "https://schema.org", "@type": "ContactPage", "url": BASE + path, "about": {"@id": BASE + "/#hotel"}}
    body = f"""
<section class="wrap page-head"><h1>Contact OIA Suites Moalboal</h1><p class="lead">The quickest replies come through WhatsApp and Facebook Messenger. Booking requests go through the <a href="/availability/">availability calendar</a>.</p></section>
<section class="wrap grid-3 contact-cards">
  <a class="fact" href="https://wa.me/{WHATSAPP_WA}" rel="noopener" target="_blank"><h2>WhatsApp</h2><p class="price">{WHATSAPP}</p><p>Messages, calls, booking questions. Answered from the Netherlands and the Philippines, so usually within the hour during daytime in either time zone.</p></a>
  <a class="fact" href="{MESSENGER}" rel="noopener" target="_blank"><h2>Facebook Messenger</h2><p class="price">m.me/OiaSuitesMoalboal</p><p>Chat with the OIA Suites page. The page also posts news, photos and offers: <span class="u">facebook.com/OiaSuitesMoalboal</span></p></a>
  <a class="fact" href="tel:{PHONE_TEL}"><h2>Phone (Philippines)</h2><p class="price">{PHONE}</p><p>Call or text the team on site, daily from 8:00 AM to 8:00 PM Philippine time.</p></a>
  <a class="fact" href="mailto:{EMAIL}"><h2>E-mail</h2><p class="price">{EMAIL}</p><p>For booking requests, invoices and longer questions. Requests sent through the website arrive here as well.</p></a>
  <a class="fact" href="{MAPS}" rel="noopener" target="_blank"><h2>Address</h2><p class="price">Oltmanns Road, Tongo, Basdiot</p><p>Moalboal, Cebu 6032, Philippines. Just before Turtle Bay Dive Resort. Free parking on site. Open in Google Maps.</p></a>
  <div class="fact"><h2>Opening hours</h2><p class="price">Staff 8:00 AM to 8:00 PM</p><p>A family member is reachable from 8:00 PM to 8:00 AM for late arrivals and emergencies. Check-in from 1:00 PM, check-out until noon.</p></div>
</section>
<section class="wrap"><h2>Find OIA Suites on the map</h2><div class="map"><iframe title="Map of OIA Suites Moalboal" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.openstreetmap.org/export/embed.html?bbox=123.3693%2C9.9272%2C123.3893%2C9.9432&amp;layer=mapnik&amp;marker={LAT}%2C{LNG}"></iframe></div><p class="meta"><a href="https://www.openstreetmap.org/?mlat={LAT}&amp;mlon={LNG}#map=16/{LAT}/{LNG}" rel="noopener" target="_blank">Larger map on OpenStreetMap</a> · <a href="{MAPS}" rel="noopener" target="_blank">Google Maps</a></p></section>
<section class="wrap"><h2>Also bookable on</h2><ul class="inline-list">{"".join(f'<li><a href="{u}" rel="noopener" target="_blank">{n} ({r})</a></li>' for n, u, r, c in PLATFORMS)}</ul></section>
"""
    write(path, layout(path, "Contact | WhatsApp, Messenger, phone and address | OIA Suites Moalboal",
        f"Contact OIA Suites Moalboal via WhatsApp {WHATSAPP}, Facebook Messenger, phone {PHONE} or e-mail. Address: Oltmanns Road, Tongo, Basdiot, Moalboal, Cebu.",
        body, schemas=[schema], crumbs=[("/", "Home"), (path, "Contact")]))

def page_sent():
    path = "/request-sent/"
    body = f"""
<section class="wrap page-head"><h1>Request received</h1><p class="lead">Thank you. The booking request has been sent to the OIA Suites team. It is not yet a confirmed booking: the team checks the dates and replies by e-mail, usually within 24 hours, with a confirmation or alternative dates. Nothing is charged until the booking is confirmed.</p>
<p>In a hurry? Send a message on <a href="https://wa.me/{WHATSAPP_WA}" rel="noopener" target="_blank">WhatsApp {WHATSAPP}</a> or <a href="{MESSENGER}" rel="noopener" target="_blank">Facebook Messenger</a>.</p>
<p><a class="btn btn-ghost" href="/">Back to the homepage</a></p></section>
"""
    html_ = layout(path, "Booking request received | OIA Suites Moalboal", "The booking request has been sent to OIA Suites Moalboal and is confirmed by the team, usually within 24 hours.", body)
    html_ = html_.replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"')
    write(path, html_)

def page_404():
    body = """<section class="wrap page-head"><h1>Page not found</h1><p class="lead">That page does not exist on oiasuitesmoalboal.com. Useful places to go: <a href="/rooms/">the rooms</a>, <a href="/availability/">the availability calendar</a> or <a href="/faq/">the FAQ</a>.</p></section>"""
    html_ = layout("/404.html", "Page not found | OIA Suites Moalboal", "Page not found.", body).replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"')
    write("/404.html", html_)

def sitemap():
    urls = ["/", "/rooms/", "/availability/", "/accommodation-for-digital-nomads/", "/breakfast/", "/services/", "/laundry-moalboal/", "/faq/", "/contact/"] + [f"/rooms/{r['slug']}/" for r in ROOMS]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    write("/sitemap.xml", xml)
    write("/robots.txt", f"User-agent: *\nAllow: /\nDisallow: /request-sent/\n\nSitemap: {BASE}/sitemap.xml\n")
    write("/_headers", "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n/images/*\n  Cache-Control: public, max-age=31536000, immutable\n/assets/*\n  Cache-Control: public, max-age=86400\n/data/*\n  Cache-Control: no-cache\n")

def availability_seed():
    p = os.path.join(OUT, "data", "availability.json")
    if os.path.exists(p): return
    os.makedirs(os.path.dirname(p), exist_ok=True)
    data = {"updated": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ"), "source": "Booking.com, Airbnb, Agoda, Expedia calendars",
            "rooms": {r["slug"]: {"name": r["name"], "booked": []} for r in ROOMS}}
    json.dump(data, open(p, "w"), indent=1)

def main():
    for d in ["rooms", "availability", "accommodation-for-digital-nomads", "breakfast", "services", "laundry-moalboal", "faq", "contact", "request-sent"]:
        shutil.rmtree(os.path.join(OUT, d), ignore_errors=True)
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    for a in ["style.css", "site.js", "calendar.js"]:
        shutil.copy(os.path.join(os.path.dirname(__file__), "assets", a), os.path.join(OUT, "assets", a))
    page_home(); page_rooms()
    for r in ROOMS: page_room(r)
    page_availability(); page_nomads(); page_breakfast(); page_services(); page_laundry(); page_faq(); page_contact(); page_sent(); page_404(); sitemap(); availability_seed()
    print("built", TODAY)

if __name__ == "__main__":
    main()
