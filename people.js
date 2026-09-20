(() => {
  const filters = document.querySelector('.team-filters');
  if (!filters) return;
  const buttons = [...filters.querySelectorAll('button')];
  const cards = [...document.querySelectorAll('.team-card')];
  const count = document.getElementById('team-count');
  const chinese = document.documentElement.lang.startsWith('zh');
  filters.hidden = false;
  buttons.forEach(button => button.addEventListener('click', () => {
    const category = button.dataset.teamFilter;
    let visible = 0;
    cards.forEach(card => {
      card.hidden = category !== 'all' && card.dataset.teamCategory !== category;
      if (!card.hidden) visible++;
      else card.open = false;
    });
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    count.textContent = chinese ? `${visible} 位团队成员` : `${visible} team member${visible === 1 ? '' : 's'}`;
  }));
  // A direct member link opens the profile, including after changing language.
  function showLinkedMember() {
    const card = cards.find(item => '#' + item.id === location.hash);
    if (card) {
      buttons[0].click();
      card.open = true;
      card.scrollIntoView({block: 'start'});
    }
  }
  showLinkedMember();
  window.addEventListener('hashchange', showLinkedMember);
})();
