(() => {
  const chinese = document.documentElement.lang.startsWith('zh');
  const list = document.querySelector('[data-city-tabs]');
  if (list) {
    const tabs = [...list.querySelectorAll('[data-city]')];
    const panels = [...document.querySelectorAll('[data-city-panel]')];
    list.setAttribute('role', 'tablist');
    tabs.forEach(tab => {
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', 'network-' + tab.dataset.city);
    });
    panels.forEach(panel => {
      panel.setAttribute('role', 'tabpanel');
      panel.setAttribute('aria-labelledby', 'city-' + panel.dataset.cityPanel);
      panel.tabIndex = 0;
    });
    const select = (tab, updateURL = false) => {
      tabs.forEach(t => { const active=t===tab;t.setAttribute('aria-selected',String(active));t.tabIndex=active?0:-1; });
      panels.forEach(p => { p.hidden = p.dataset.cityPanel !== tab.dataset.city; });
      if (updateURL) history.replaceState(null, '', '#network-' + tab.dataset.city);
    };
    const fromHash = () => {
      const tab=tabs.find(t=>'#network-'+t.dataset.city===location.hash);
      if(tab) select(tab);else if(!tabs.some(t=>t.getAttribute('aria-selected')==='true'))select(tabs[0]);
    };
    tabs.forEach((tab,index) => {
      tab.addEventListener('click', event => {event.preventDefault();select(tab,true);});
      tab.addEventListener('keydown', event => {
        let next;
        if(event.key==='ArrowRight')next=(index+1)%tabs.length;
        if(event.key==='ArrowLeft')next=(index+tabs.length-1)%tabs.length;
        if(event.key==='Home')next=0;
        if(event.key==='End')next=tabs.length-1;
        if(next!==undefined){event.preventDefault();tabs[next].focus();select(tabs[next],true);}
        if(event.key===' '){event.preventDefault();select(tab,true);}
      });
    });
    fromHash();window.addEventListener('hashchange',fromHash);
    // The shared language links were initially set before interactive tab changes.
    document.querySelectorAll('.language-switch a').forEach(a=>a.addEventListener('click',()=>{const u=new URL(a.href);u.hash=location.hash;a.href=u.href;}));
  }
  const filters=document.querySelector('.partner-filters');
  if(filters){
    const buttons=[...filters.querySelectorAll('button')],cards=[...document.querySelectorAll('.partner-card')];
    filters.hidden=false;
    buttons.forEach(button=>button.addEventListener('click',()=>{
      const category=button.dataset.partnerFilter;let count=0;
      cards.forEach(card=>{card.hidden=category!=='all'&&!card.dataset.partnerCategory.split(' ').includes(category);if(!card.hidden)count++;});
      buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
      document.querySelector('#partner-count').textContent=chinese?`${count} 家合作伙伴`:`${count} collaborator${count===1?'':'s'}`;
    }));
    const reveal=()=>{if(cards.some(c=>'#'+c.id===location.hash))buttons[0].click();};
    window.addEventListener('hashchange',reveal);reveal();
  }
})();
