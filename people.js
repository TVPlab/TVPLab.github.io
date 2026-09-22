(() => {
  const filters = document.querySelector('.team-filters');
  if (!filters) return;
  const buttons = [...filters.querySelectorAll('button')];
  const cards = [...document.querySelectorAll('.team-card')];
  const grid = document.getElementById('team-grid');
  const alumni = document.getElementById('alumni-directory');
  const count = document.getElementById('team-count');
  const guide = document.querySelector('.team-guide > p:first-child');
  const chinese = document.documentElement.lang.startsWith('zh');
  filters.hidden = false;
  function select(category, updateUrl = false) {
    const isAlumni = category === 'alumni';
    grid.hidden = isAlumni;
    alumni.hidden = !isAlumni;
    let visible = 0;
    cards.forEach(card => {
      card.hidden = isAlumni || (category !== 'all' && card.dataset.teamCategory !== category);
      if (!card.hidden) visible++;
      else card.open = false;
    });
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item.dataset.teamFilter === category)));
    if (isAlumni) visible = alumni.querySelectorAll('.alumni-card').length;
    count.textContent = chinese ? `${visible} 位${isAlumni ? '往届' : '团队'}成员` : `${visible} ${isAlumni ? 'alumni' : 'team member' + (visible === 1 ? '' : 's')}`;
    guide.textContent = isAlumni ? (chinese ? '曾在 TVPlab 工作与学习的伙伴。' : 'People who have been part of TVPlab.') : (chinese ? '了解团队的研究方向与专业背景。' : 'Explore our research interests and backgrounds.');
    if (updateUrl) history.pushState(null, '', category === 'all' ? location.pathname + location.search : '#role-' + category);
    document.querySelectorAll('.language-switch a').forEach(link => {
      const url = new URL(link.href);
      url.hash = location.hash;
      link.href = url.href;
    });
  }
  buttons.forEach(button => button.addEventListener('click', () => select(button.dataset.teamFilter, true)));
  function showLinkedMember() {
    const role = buttons.find(b => '#role-' + b.dataset.teamFilter === location.hash);
    if (role) { select(role.dataset.teamFilter); filters.scrollIntoView({block:'start'}); return; }
    const former = [...alumni.querySelectorAll('.alumni-card')].find(item => '#' + item.id === location.hash);
    if (former) { select('alumni'); former.scrollIntoView({block:'start'}); return; }
    const card = cards.find(item => '#' + item.id === location.hash);
    select('all');
    if (card) { card.open = true; card.scrollIntoView({block:'start'}); }
  }
  showLinkedMember();
  window.addEventListener('hashchange', showLinkedMember);
  window.addEventListener('popstate', showLinkedMember);
})();
