# oiasuitesmoalboal.com

Static website for OIA Suites Moalboal (Basdiot, Moalboal, Cebu).

- `build/content.py` all content (rooms, reviews, FAQ, contact details)
- `build/build.py` generator, writes to `site/` (`python3 build/build.py`)
- `build/update_availability.py` daily availability update from iCal feeds in `build/ical_feeds.json`, writes `site/data/availability.json`
- `site/` deployed as-is by Cloudflare Pages (no build command, output directory `site`)
