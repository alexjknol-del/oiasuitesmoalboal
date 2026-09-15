/* Iris - house assistant for OIA Suites Moalboal.
   Searches the FAQ that is already on the site. No external service, no model,
   no storage: if nothing matches well enough it hands the guest to WhatsApp. */
(function () {
  var root = document.getElementById('iris');
  if (!root) return;

  var WA = 'https://wa.me/491742101192';
  var STOP = ' a an and are as at be by can do does for from get has have how i in is it me my of on or our the there to we what when where which who why you your '.split(' ');
  var SYN = {
    breakfast: ['eat', 'food', 'meal', 'morning', 'coffee', 'tosilog', 'silog', 'egg', 'eggs', 'rice', 'bacon'],
    checkin: ['arrive', 'arrival', 'late', 'early', 'checkout', 'time', 'times'],
    wifi: ['internet', 'wi-fi', 'starlink', 'speed', 'connection', 'work', 'nomad', 'nomads'],
    laundry: ['wash', 'washing', 'clothes', 'dry', 'cleaning'],
    scooter: ['motorbike', 'bike', 'motorcycle', 'rent', 'rental', 'transport'],
    airport: ['cebu', 'taxi', 'transfer', 'pickup', 'pick-up', 'bus', 'van', 'terminal', 'travel', 'getting'],
    pool: ['swim', 'swimming', 'construction'],
    payment: ['pay', 'cash', 'card', 'gcash', 'deposit', 'price', 'cost', 'rate', 'rates'],
    beach: ['sardine', 'sardines', 'dive', 'diving', 'snorkel', 'sea', 'turtle', 'panagsama'],
    kitchen: ['cook', 'cooking', 'fridge', 'grill', 'espresso'],
    pets: ['dog', 'dogs', 'cat', 'cats', 'animal'],
    children: ['kid', 'kids', 'child', 'baby', 'family', 'bed'],
    water: ['drinking', 'drink', 'tap', 'bottle', 'refill'],
    cancel: ['cancellation', 'refund', 'change', 'move']
  };

  var CHIPS = ['Breakfast', 'Check-in times', 'Getting here', 'Wifi speed', 'Laundry', 'Scooter rental', 'Payment', 'Swimming pool'];

  var log = document.getElementById('iris-log');
  var panel = document.getElementById('iris-panel');
  var launch = root.querySelector('.iris-launch');
  var close = root.querySelector('.iris-close');
  var form = root.querySelector('.iris-form');
  var input = document.getElementById('iris-q');
  var faq = null, loading = false, greeted = false;

  root.hidden = false;

  function words(s) {
    return (s || '').toLowerCase().replace(/<[^>]*>/g, ' ').replace(/[^a-z0-9 ]/g, ' ').split(/\s+/)
      .filter(function (w) { return w.length > 2 && STOP.indexOf(w) === -1; })
      .map(function (w) { return w.length > 3 && w.slice(-1) === 's' && w.slice(-2) !== 'ss' ? w.slice(0, -1) : w; });
  }

  function expand(ws) {
    var out = ws.slice();
    ws.forEach(function (w) {
      Object.keys(SYN).forEach(function (key) {
        if (w === key || SYN[key].indexOf(w) > -1) { out.push(key); out = out.concat(SYN[key]); }
      });
    });
    return out;
  }

  function score(query, item) {
    var q = expand(words(query));
    var inQ = words(item.q), inA = words(item.a);
    var hit = 0, seen = {};
    q.forEach(function (w) {
      if (seen[w]) return;
      seen[w] = 1;
      if (inQ.indexOf(w) > -1) hit += 3;
      else if (inA.indexOf(w) > -1) hit += 1;
    });
    return hit;
  }

  function bubble(who, html) {
    var d = document.createElement('div');
    d.className = 'iris-msg iris-' + who;
    d.innerHTML = html;
    log.appendChild(d);
    log.scrollTop = log.scrollHeight;
    return d;
  }

  function chips(list) {
    if (!list.length) return;
    var d = document.createElement('div');
    d.className = 'iris-chips';
    list.forEach(function (t) {
      var b = document.createElement('button');
      b.type = 'button';
      b.textContent = t;
      b.addEventListener('click', function () { ask(t); });
      d.appendChild(b);
    });
    log.appendChild(d);
    log.scrollTop = log.scrollHeight;
  }

  function fallback() {
    bubble('bot', 'That one is not in my notes. The team answers within the hour during the day: ' +
      '<a href="' + WA + '" target="_blank" rel="noopener">WhatsApp</a> or the ' +
      '<a href="/contact/">contact page</a>.');
  }

  function answer(q) {
    var ranked = faq.map(function (item) { return { item: item, s: score(q, item) }; })
      .sort(function (a, b) { return b.s - a.s; });
    if (!ranked.length || ranked[0].s < 3) { fallback(); return; }
    bubble('bot', '<strong>' + ranked[0].item.q + '</strong><br>' + ranked[0].item.a);
    var more = ranked.slice(1, 4).filter(function (r) { return r.s >= 3; })
      .map(function (r) { return r.item.q; });
    if (more.length) chips(more);
  }

  function ask(q) {
    bubble('me', q.replace(/</g, '&lt;'));
    if (faq) { answer(q); return; }
    load(function (ok) { ok ? answer(q) : fallback(); });
  }

  function load(cb) {
    if (loading) return;
    loading = true;
    fetch('/data/faq.json').then(function (r) { return r.json(); })
      .then(function (d) { faq = d; loading = false; cb(true); })
      .catch(function () { loading = false; cb(false); });
  }

  function open() {
    panel.hidden = false;
    launch.setAttribute('aria-expanded', 'true');
    root.classList.add('is-open');
    if (!greeted) {
      greeted = true;
      bubble('bot', 'Kalimera. I am Iris, named after the Greek messenger. Ask me anything about the house and I will look it up.');
      chips(CHIPS);
      load(function () {});
    }
    input.focus();
  }

  function shut() {
    panel.hidden = true;
    launch.setAttribute('aria-expanded', 'false');
    root.classList.remove('is-open');
    launch.focus();
  }

  launch.addEventListener('click', function () { panel.hidden ? open() : shut(); });
  close.addEventListener('click', shut);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) shut(); });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = input.value.trim();
    if (!v) return;
    input.value = '';
    ask(v);
  });
})();
