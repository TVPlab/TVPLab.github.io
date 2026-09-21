(() => {
  const root = document.querySelector('.news-archive');
  if (!root) return;
  const zh = document.documentElement.lang.startsWith('zh');
  const cards = [...root.querySelectorAll('.archive-story')];
  const list = root.querySelector('#news-stories');
  const search = root.querySelector('#news-search');
  const year = root.querySelector('#news-year');
  const sort = root.querySelector('#news-sort');
  const result = root.querySelector('#news-results');
  const more = root.querySelector('#news-more');
  const chips = [...root.querySelectorAll('[data-topic-filter]')];
  const normalize = s => s.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const searchable = new Map(cards.map(c => [c, normalize(c.textContent + " " + c.id)]));
  let topic = 'all', limit = 12;
  const params = new URLSearchParams(location.search);
  if (chips.some(c => c.dataset.topicFilter === params.get('topic'))) topic = params.get('topic');
  if ([...year.options].some(o => o.value === params.get('year'))) year.value = params.get('year');
  if (params.get('sort') === 'oldest') sort.value = 'oldest';
  search.value = params.get('q') || '';
  function render(save = true) {
    const query = normalize(search.value.trim());
    const ordered = [...cards].sort((a,b) => (sort.value === 'oldest' ? 1 : -1) * a.dataset.date.localeCompare(b.dataset.date));
    const matches = ordered.filter(c => (topic === 'all' || c.dataset.topic === topic) && (year.value === 'all' || c.dataset.year === year.value) && (!query || searchable.get(c).includes(query)));
    const visible = new Set(matches.slice(0, limit));
    ordered.forEach(c => {c.hidden = !visible.has(c); list.append(c);});
    chips.forEach(c => c.setAttribute('aria-pressed', String(c.dataset.topicFilter === topic)));
    result.textContent = zh ? `显示 ${visible.size} / ${matches.length} 篇动态` : `Showing ${visible.size} of ${matches.length} stories`;
    more.hidden = visible.size >= matches.length;
    root.querySelector('#news-empty').hidden = matches.length !== 0;
    if (save) {
      const p = new URLSearchParams();
      if (topic !== 'all') p.set('topic', topic);
      if (year.value !== 'all') p.set('year', year.value);
      if (sort.value !== 'newest') p.set('sort', sort.value);
      if (search.value.trim()) p.set('q', search.value.trim());
      history.replaceState(null, '', location.pathname + (p.size ? '?' + p : '') + location.hash);
    }
    document.querySelectorAll('[data-language]').forEach(a => {
      const url = new URL(a.href, location.href); url.search = location.search; url.hash = location.hash; a.href = url.href;
    });
  }
  function change() {limit = 12; render();}
  search.addEventListener('input', change);
  year.addEventListener('change', change); sort.addEventListener('change', change);
  chips.forEach(b => b.addEventListener('click', () => {topic = b.dataset.topicFilter; change();}));
  root.querySelector('#news-reset').addEventListener('click', () => {topic = 'all'; search.value = ''; year.value = 'all'; sort.value = 'newest'; change();});
  more.addEventListener('click', () => {
    const old = new Set(cards.filter(c => !c.hidden)); limit += 12; render();
    const next = [...list.children].find(c => !c.hidden && !old.has(c));
    next?.querySelector('summary')?.focus({preventScroll: true});
  });
  function revealHash() {
    let id; try {id = decodeURIComponent(location.hash.slice(1));} catch {return;}
    const target = cards.find(c => c.id === id);
    if (!target) return;
    topic = 'all'; search.value = ''; year.value = 'all'; limit = cards.length;
    render(); target.querySelector('details').open = true;
    requestAnimationFrame(() => target.scrollIntoView({block:'start',behavior:'instant'}));
  }
  window.addEventListener('hashchange', revealHash);
  root.querySelector('.news-tools').hidden = false;
  render(false); revealHash();
  // Dated announcements never retain an "upcoming" claim after the event.
  const event = document.querySelector('[data-event-date]');
  if (event && new Date().toLocaleDateString('en-CA',{timeZone:'Europe/Madrid'}) > event.dataset.eventDate) {
    event.querySelector('.eyebrow').textContent = zh ? '活动回顾' : 'From the event calendar';
    event.querySelector('.calendar-download').hidden = true;
  }
})();
