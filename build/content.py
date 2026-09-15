# Content for OIA Suites Moalboal website
BASE = "https://oiasuitesmoalboal.com"
SITE_NAME = "OIA Suites Moalboal"
PHONE = "+63 908 546 0118"
PHONE_TEL = "+639085460118"
WHATSAPP = "+49 174 210 1192"
WHATSAPP_WA = "491742101192"
EMAIL = "migue.langrich@gmail.com"
FB = "https://www.facebook.com/OiaSuitesMoalboal/"
MESSENGER = "https://m.me/OiaSuitesMoalboal"
ADDRESS = "Oltmanns Road, Tongo, Basdiot, Moalboal, Cebu 6032, Philippines"
LAT, LNG = 9.9352, 123.3793
MAPS = "https://www.google.com/maps/search/?api=1&query=Oia+Suites+Moalboal+Oltmanns+Road+Basdiot"

PLATFORMS = [
    ("Booking.com", "https://www.booking.com/hotel/ph/oia.html", "9.4 / 10", "126 reviews"),
    ("Airbnb", "https://www.airbnb.com/users/show/13295008", "4.96 / 5", "154 reviews, Superhost"),
    ("Agoda", "https://www.agoda.com/oia/hotel/all/moalboal-ph.html", "9.6 / 10", "8 reviews"),
    ("Expedia", "https://www.expedia.com/Moalboal-Hotels-Oia-Suites.h119314905.Hotel-Information", "10 / 10", "2 reviews"),
]

AIRBNB = {
    1: "https://www.airbnb.com/rooms/1458522028549389022",
    2: "https://www.airbnb.com/rooms/1460279794265386473",
    3: "https://www.airbnb.com/rooms/1461571120753301246",
    4: "https://www.airbnb.com/rooms/1462983677136911840",
    5: "https://www.airbnb.com/rooms/1534590328456183955",
}

COMMON_ROOM_FEATURES = [
    "King-size bed with hypo-allergenic bedding",
    "Private bathroom with hot and cold shower",
    "Private balcony",
    "Work desk and office chair",
    "Split-type air conditioning",
    "Smart TV with Netflix",
    "Fiber internet (250 Mbps) with Starlink backup",
    "Closet, clothes rack and luggage space",
    "Coffee and tea facilities, drinking water",
    "Daily room cleaning",
]

ROOMS = [
    dict(n=1, slug="suite-1", name="Suite 1", size=25, floor="First floor", view="Private balcony",
         bed="1 king-size bed", guests=2, airbnb=AIRBNB[1], rating="5.0 (45 reviews on Airbnb)",
         intro="Suite 1 is the most-reviewed room of the house and holds a perfect 5.0 on Airbnb. A 25 m² room on the first floor with king-size bed, en-suite bathroom, work desk and a private balcony.",
         photos=["suite-1-c", "suite-1-b", "suite-1-a", "suite-1-d", "balcony-green"]),
    dict(n=2, slug="suite-2", name="Suite 2", size=25, floor="First floor", view="Private balcony",
         bed="1 king-size bed (extra bed for 1 child on request)", guests=3, airbnb=AIRBNB[2], rating="4.97 (37 reviews on Airbnb)",
         intro="Suite 2 is a 25 m² first-floor room with a king-size bed, private bathroom, dedicated desk and a balcony with a chair for the evening. It is the room that takes an extra bed for one child. Guests rate it 4.97 on Airbnb and it is marked as a Guest Favorite.",
         photos=["suite-2-a", "suite-2-b", "suite-2-c", "suite-2-d", "balcony-chairs"]),
    dict(n=3, slug="suite-3", name="Suite 3", size=24, floor="First floor", view="Private balcony",
         bed="1 king-size bed", guests=2, airbnb=AIRBNB[3], rating="4.89 (28 reviews on Airbnb)",
         intro="Suite 3 is a 24 m² room with king-size bed, a glass-walled shower room, work desk with office chair and its own balcony. Dark curtains keep the room cool and dark for late sleepers or early calls.",
         photos=["suite-3-a", "suite-3-b", "suite-3-c", "suite-3-d", "stairs"]),
    dict(n=4, slug="suite-4", name="Suite 4", size=25, floor="First floor", view="Private balcony",
         bed="1 king-size bed", guests=2, airbnb=AIRBNB[4], rating="4.93 (28 reviews on Airbnb)",
         intro="Suite 4 is a bright 25 m² room in soft green tones with a king-size bed, private bathroom, desk and office chair, and a balcony. Rated 4.93 on Airbnb with 93 percent five-star reviews.",
         photos=["suite-4-a", "suite-4-b", "suite-4-c", "suite-4-d", "kitchen"]),
    dict(n=5, slug="suite-5", name="Suite 5", size=25, floor="First floor", view="Private balcony",
         bed="1 king-size bed", guests=2, airbnb=AIRBNB[5], rating="5.0 (16 reviews on Airbnb)",
         intro="Suite 5 is the newest room on the platforms and already holds a 5.0 rating. 25 m², king-size bed, en-suite bathroom, work desk, smart TV and a balcony with two chairs among the palm tops.",
         photos=["suite-5-a", "suite-5-b", "suite-5-c", "suite-5-d", "balcony-view"]),
]

REVIEWS = [
    dict(name="Lydia", origin="United Kingdom", platform="Booking.com", url="https://www.booking.com/hotel/ph/oia.html",
         text="Amazing room with en-suite! Great WiFi connection (had an interview for a role back in the UK and the connection was very stable). Bed was comfy, staff were so lovely! Would recommend and stay again."),
    dict(name="Wei", origin="Netherlands", platform="Booking.com", url="https://www.booking.com/hotel/ph/oia.html",
         text="The house and room were sooo clean. Definitely the best accommodation we had in the Philippines and for such a cheap price. Also really loved the balcony with a beautiful view. The room was very spacious."),
    dict(name="Maria", origin="Olongapo City, Philippines", platform="Airbnb", url=AIRBNB[1],
         text="The room was clean, comfortable, smelled fresh, and had everything we needed. One thing we really appreciated was the fully equipped kitchen, especially the fridge that dispenses crushed ice. The location is peaceful and slightly away from the busy diving area, making it a relaxing place to stay."),
    dict(name="Kathleen Jane", origin="Airbnb guest", platform="Airbnb", url=AIRBNB[1],
         text="This place is fantastic! The room was clean and incredibly comfortable. If you want to escape the crowds, this is absolutely the best place to stay. They offer convenient motorcycle rentals on-site to help you get around."),
    dict(name="Williams", origin="Australia", platform="Booking.com", url="https://www.booking.com/hotel/ph/oia.html",
         text="Clean, modern and had everything needed to enjoy the stay. Also cheap bike hire and easy to book tours or transfer to the airport."),
    dict(name="Shaurya", origin="Lithuania", platform="Booking.com", url="https://www.booking.com/hotel/ph/oia.html",
         text="Modern room and common spaces with big balconies and friendly staff and facilities."),
    dict(name="Anthony", origin="Santa Rosa, California", platform="Airbnb", url="https://www.airbnb.com/users/show/13295008",
         text="The host and staff were very friendly and helpful throughout our stay. Everything you need is nearby: scooter rental, food, beaches. Laundry service available. Everything you need for a great experience here in Moalboal."),
    dict(name="Kevin", origin="Manila, Philippines", platform="Airbnb", url="https://www.airbnb.com/users/show/13295008",
         text="Nice place and nice people. I enjoyed staying there, slept really well and it was quiet. Very easy to check in. Great room!"),
    dict(name="Ying Kiu", origin="Airbnb guest", platform="Airbnb", url=AIRBNB[1],
         text="We arrived very late the first night but the staff was still around to help with check-in. Staff are all very friendly and helpful and pick-up and drop-off from the bus stop to Moalboal is available."),
    dict(name="Sander", origin="Netherlands", platform="Booking.com", url="https://www.booking.com/hotel/ph/oia.html",
         text="Super clean and tidy. Everything can be arranged: transport to the port, excursions, scooter rental and even laundry. It is nice that the place is a little outside the busy centre."),
]

FAQ = [
    ("Booking and payment", [
        ("How do I book a room at OIA Suites Moalboal?",
         "Use the <a href='/availability/'>availability calendar</a> to pick a suite and dates and send a booking request. The team confirms by e-mail or WhatsApp, usually within 24 hours. Rooms can also be booked on Booking.com, Airbnb, Agoda and Expedia."),
        ("Is my booking request a confirmed reservation?",
         "No. A request through this website is a reservation request. It becomes a confirmed booking only after OIA Suites has approved it and sent a confirmation. Until then, no payment is due."),
        ("What do the rooms cost?",
         "Rates start from roughly PHP 1,500 per night (about USD 26 or EUR 24) for two people including taxes, depending on the suite, season and platform. Long-stay rates for remote workers are quoted on request."),
        ("Which payment methods are accepted?",
         "Cash (Philippine peso) and credit or debit card. Bookings via Booking.com, Airbnb, Agoda or Expedia are paid through that platform."),
        ("What is the cancellation policy?",
         "The conditions for a direct booking are stated in the confirmation message before any payment is made. Platform bookings follow the policy shown on that platform at the time of booking."),
    ]),
    ("Check-in and house rules", [
        ("What are the check-in and check-out times?",
         "Check-in is from 1:00 PM, check-out until 12:00 noon. Late arrivals until 11:00 PM are fine when announced in advance; a family member is reachable from 8:00 PM to 8:00 AM. Luggage can be stored before check-in and after check-out."),
        ("Is there someone on site?",
         "Yes. Staff are on site daily from 8:00 AM to 8:00 PM, and a family member is available from 8:00 PM to 8:00 AM. There are exterior security cameras and a 24-hour security presence."),
        ("Are children welcome?",
         "Yes. Children of all ages are welcome. Children from 3 years pay the adult rate. A baby cot is available on request at no charge. Suite 2 can take an extra bed for one child."),
        ("Are pets allowed?",
         "Yes, pets are allowed on request. Food and water bowls are available."),
        ("Is smoking allowed?",
         "OIA Suites is a non-smoking house. Smoking is possible outside in the designated area."),
        ("Are there quiet hours?",
         "Yes, from 10:00 PM to 8:00 AM."),
    ]),
    ("Rooms and facilities", [
        ("What is in each room?",
         "Every suite has a king-size bed, private bathroom with hot and cold shower, split-type air conditioning, a work desk with office chair, closet, smart TV with Netflix, coffee and tea facilities and a private balcony. Rooms measure 24 to 25 m²."),
        ("How fast is the internet?",
         "Globe fiber internet with 250 Mbps download, plus a Starlink Gen 3 dish as automatic backup. Guests report stable video calls and job interviews. Every room and the common areas are covered."),
        ("Is there a kitchen?",
         "Yes. The ground floor has a fully equipped shared kitchen with cooking hob, microwave, refrigerator with ice maker, espresso machine and drip coffee maker, cooking utensils and a dining table. Use is free of charge. A grill is available outside."),
        ("Is breakfast available?",
         "Yes, on order. Filipino sets (tosilog, hotsilog, longsilog, bacsilog, cornsilog) or an American set for PHP 250 per serving, each with coffee, juice and fruit. Order at the counter the night before or send a message. There is no restaurant on site; several restaurants are a few minutes away by scooter. The full menu is on the <a href=\'/breakfast/\'>breakfast page</a>."),
        ("Is breakfast included in the room rate?",
         "No. Breakfast is ordered and paid separately, PHP 250 per serving, and settled at check-out together with the room. This applies to direct bookings and to bookings made through Booking.com, Airbnb, Agoda or Expedia."),
        ("What time is breakfast served?",
         "Between 6:00 AM and 10:00 AM, every day, in the suite or at the table downstairs. Guests leaving earlier for Oslob or canyoneering can ask for a packed breakfast instead."),
        ("Is drinking water provided?",
         "Yes. Water dispensers on both floors give free drinking water around the clock. The refrigerator has a built-in ice maker."),
        ("Is there parking?",
         "Yes, free private parking on the premises for cars and motorbikes."),
        ("Is there a swimming pool?",
         "A swimming pool is being built next to the house from 14 September 2026. Construction takes place on working days from 8:00 to 11:00 AM and 2:00 to 5:00 PM, with a quiet break in between and no work in the evening or at weekends. Guests who are sensitive to daytime noise can ask the team for the quietest suite."),
        ("Is laundry service available?",
         "Yes. OIA Suites runs its own laundry, Laundry Lounge Cebu in Moalboal town. Laundry is collected at the house and returned the next day, washed, dried and folded, for PHP 190 per load of up to 9 kg. See the <a href=\"/laundry-moalboal/\">laundry page</a>."),
    ]),
    ("Location and getting around", [
        ("Where exactly is OIA Suites?",
         "On Oltmanns Road in Tongo, Basdiot, Moalboal, Cebu, just before Turtle Bay Dive Resort. It is a quiet residential area about 13 minutes on foot (5 minutes by scooter) from Panagsama Beach and the dive shops, and 10 minutes from Moalboal town and the market."),
        ("Is there a beach nearby?",
         "Yes. A small, quiet beach with rocky shore and good snorkelling is a 2-minute walk from the house. Panagsama Beach is 13 minutes on foot, White Beach 20 minutes by scooter."),
        ("How do I get to OIA Suites from Cebu City or the airport?",
         "From Mactan-Cebu International Airport take a taxi or Grab to the Cebu South Bus Terminal, then a Ceres bus to Moalboal (about 3 hours). Get off at Moalboal town or Jollibee Moalboal and the team collects guests free of charge. Private airport transfers can also be arranged, and a Cebu to Moalboal van or car can be booked through the team."),
        ("Is there free pick-up?",
         "Yes. Free pick-up from Jollibee Moalboal or the Moalboal bus stop at check-in. Send a message with the arrival time."),
        ("Can I rent a scooter?",
         "Yes, on site. Yamaha Mio PHP 300 per day, Honda Click PHP 400 per day, Honda ADV160 PHP 600 per day. A valid driving licence is required."),
        ("Can the team arrange tours?",
         "Yes. Sardine run and turtle snorkelling, Kawasan and Badian canyoneering, whale shark watching in Oslob, waterfall tours, Osmeña Peak trekking and private car transfers to Oslob or Liloan port. See <a href='/services/'>services and tours</a> for prices."),
    ]),
    ("Working remotely", [
        ("Is OIA Suites suitable for digital nomads?",
         "Yes. It is one of the few guesthouses in Moalboal built around remote work: 250 Mbps fiber with Starlink backup, a desk and office chair in every room, air conditioning, quiet surroundings and a shared living room and kitchen for longer stays. Read more on the <a href='/accommodation-for-digital-nomads/'>digital nomad page</a>."),
        ("Are there weekly or monthly rates?",
         "Long-stay rates are quoted individually. Send a request through the calendar and mention the intended length of stay."),
    ]),
]

# Own laundry business
LAUNDRY_NAME = "Laundry Lounge Cebu"
LAUNDRY_URL = "https://laundryloungecebu.ph/"
LAUNDRY_PHONE = "(032) 421-9766"
LAUNDRY_PHONE_TEL = "+63324219766"
