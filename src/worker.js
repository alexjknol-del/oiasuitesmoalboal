/**
 * oiasuitesmoalboal.com Worker
 * - Serves the static site from ./site (ASSETS binding)
 * - /data/availability.json is generated live from the iCal feeds of the
 *   booking platforms when the secret ICAL_FEEDS is set:
 *     {"suite-1":["https://...ics", ...], "suite-2":[...], ...}
 *   Extra secrets ICAL_FEEDS_BOOKING and ICAL_FEEDS_EXTRA use the same format and are merged.
 *   Result is cached for 30 minutes. Without any secret the static file is served.
 */
const CANONICAL_HOST = "oiasuitesmoalboal.com";
const ROOMS = ["suite-1", "suite-2", "suite-3", "suite-4", "suite-5"];
const CACHE_SECONDS = 1800;
const HORIZON_DAYS = 550;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    // Canonical host: redirect www and workers.dev to the main domain once the zone is active
    if (url.hostname !== CANONICAL_HOST && (url.hostname === "www." + CANONICAL_HOST || url.hostname.endsWith(".workers.dev"))) {
      url.hostname = CANONICAL_HOST;
      return Response.redirect(url.toString(), 301);
    }
    // Suite 6 was removed from the site (no such room on the platforms)
    if (/^\/rooms\/suite-6\/?$/.test(url.pathname)) {
      url.pathname = "/rooms/";
      return Response.redirect(url.toString(), 301);
    }
    // Alias without hyphen
    if (/^\/accommodation-for-digitalnomads\/?$/.test(url.pathname)) {
      url.pathname = "/accommodation-for-digital-nomads/";
      return Response.redirect(url.toString(), 301);
    }
    if (url.pathname === "/data/availability.json" && (env.ICAL_FEEDS || env.ICAL_FEEDS_BOOKING)) {
      const cache = caches.default;
      const key = new Request(url.origin + "/data/availability.json", { method: "GET" });
      let res = await cache.match(key);
      if (!res) {
        res = await buildAvailability(env, url.origin);
        ctx.waitUntil(cache.put(key, res.clone()));
      }
      return res;
    }
    return env.ASSETS.fetch(request);
  },
};

async function buildAvailability(env, origin) {
  // Feeds come from one or more secrets (ICAL_FEEDS = Airbnb, ICAL_FEEDS_BOOKING = Booking.com, ...); merged per room
  const feeds = {};
  for (const name of ["ICAL_FEEDS", "ICAL_FEEDS_BOOKING", "ICAL_FEEDS_EXTRA"]) {
    if (!env[name]) continue;
    try {
      const part = JSON.parse(env[name]);
      for (const slug of ROOMS) feeds[slug] = (feeds[slug] || []).concat(part[slug] || []);
    } catch (e) { /* invalid JSON in secret, ignore */ }
  }
  const today = isoDate(new Date());
  const horizon = isoDate(new Date(Date.now() + HORIZON_DAYS * 864e5));
  const results = {};
  await Promise.all(ROOMS.map(async (slug, i) => {
    const urls = feeds[slug] || [];
    const booked = new Set();
    let ok = 0;
    await Promise.all(urls.map(async (u) => {
      try {
        const r = await fetch(u, { headers: { "User-Agent": "oiasuitesmoalboal-availability/1.0" }, cf: { cacheTtl: 600 } });
        if (!r.ok) return;
        for (const d of nightsFromIcal(await r.text())) booked.add(d);
        ok++;
      } catch (e) { /* feed failed, ignore */ }
    }));
    results[slug] = {
      name: "Suite " + (i + 1),
      booked: [...booked].filter((d) => d >= today && d <= horizon).sort(),
      feeds: urls.length, feedsOk: ok,
    };
  }));
  const rooms = {};
  for (const slug of ROOMS) rooms[slug] = results[slug];
  const body = JSON.stringify({ updated: new Date().toISOString().slice(0, 16) + "Z", source: "Booking.com, Airbnb, Agoda, Expedia calendars", rooms }, null, 1);
  return new Response(body, { headers: { "content-type": "application/json; charset=utf-8", "cache-control": "public, max-age=" + CACHE_SECONDS, "access-control-allow-origin": origin } });
}

function isoDate(d) { return d.toISOString().slice(0, 10); }

function parseDate(s) { return new Date(Date.UTC(+s.slice(0, 4), +s.slice(4, 6) - 1, +s.slice(6, 8))); }

/** Every night blocked by a VEVENT, as YYYY-MM-DD of the night's check-in date. */
function nightsFromIcal(text) {
  text = text.replace(/\r?\n[ \t]/g, "");
  const out = [];
  const re = /BEGIN:VEVENT([\s\S]*?)END:VEVENT/g;
  let m;
  while ((m = re.exec(text))) {
    const ev = m[1];
    const s = /^DTSTART[^:]*:(\d{8})/m.exec(ev);
    if (!s) continue;
    const e = /^DTEND[^:]*:(\d{8})/m.exec(ev);
    let start = parseDate(s[1]);
    let end = e ? parseDate(e[1]) : new Date(start.getTime() + 864e5);
    if (end <= start) end = new Date(start.getTime() + 864e5);
    for (let d = start; d < end; d = new Date(d.getTime() + 864e5)) out.push(isoDate(d));
  }
  return out;
}
