// Native details retain usable navigation without JavaScript.
(() => {
  document.documentElement.classList.add('nav-js');
  const groups = [...document.querySelectorAll('.nav-group')];
  const menu = document.querySelector('.menu-toggle');
  const desktop = matchMedia('(min-width:1201px)');
  const close = except => groups.forEach(g => { if (g !== except) g.open = false; });
  groups.forEach(group => {
    let hoverOpened=false;
    group.querySelector('summary').addEventListener('click', event => {
      if(hoverOpened && group.open){event.preventDefault();hoverOpened=false;}
    });
    group.addEventListener('toggle', () => { if (group.open) close(group); });
    group.addEventListener('pointerenter', event => {
      if (desktop.matches && event.pointerType === 'mouse') { close(group); if(!group.open){hoverOpened=true;group.open=true;} }
    });
    group.addEventListener('pointerleave', event => {
      if (desktop.matches && event.pointerType === 'mouse' && !group.contains(document.activeElement)) group.open = false;
    });
    group.addEventListener('focusout', () => requestAnimationFrame(() => {
      if (!group.contains(document.activeElement) && !group.matches(':hover')) group.open = false;
    }));
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.nav-group') || event.target.closest('.nav-panel a')) close();
  });
  // Capture Escape before the mobile menu handler, closing one level at a time.
  document.addEventListener('keydown', event => {
    const open = groups.find(g => g.open);
    if (event.key === 'Escape' && open) {
      event.preventDefault();event.stopImmediatePropagation();close();open.querySelector('summary').focus();
    }
  }, true);
  menu?.addEventListener('click', close.bind(null, null));
  desktop.addEventListener('change', () => close());
})();
