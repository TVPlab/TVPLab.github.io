// No build step or external scripts required: works on GitHub Pages.
(() => {
  // Preserve links from the previous single-page website.
  if (/\/(?:index\.html)?$/.test(location.pathname)) {
    const routes = { about:'about.html', research:'research.html', people:'people.html', pi:'antonio-vidal-puig.html', publications:'publications.html', news:'news.html', 'news-article':'news.html', contact:'contact.html', vacancies:'vacancies.html' };
    const target = routes[location.hash.slice(1)];
    if (target) { location.replace(target); return; }
  }
  const isChinese = document.documentElement.lang.startsWith('zh');
  // Keep section anchors when switching between the corresponding language pages.
  document.querySelectorAll('.language-switch a').forEach(link => {
    if (location.hash) link.href += location.hash;
  });
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#primary-navigation');
  const closeMenu = () => { nav?.classList.remove('is-open'); toggle?.setAttribute('aria-expanded','false'); };
  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  });
  document.addEventListener('keydown', e => { if(e.key === 'Escape' && toggle?.getAttribute('aria-expanded') === 'true') { closeMenu(); toggle.focus(); } });
  document.addEventListener('click', e => { if (!e.target.closest('.site-header')) closeMenu(); });
  nav?.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
  window.matchMedia('(min-width:1201px)').addEventListener('change', closeMenu);
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('[data-carousel]').forEach(carousel => {
    const track = carousel.querySelector('.carousel-track');
    const slides = [...track.children];
    const controls = carousel.querySelector('.carousel-controls');
    const prev = controls.querySelector('[data-prev]');
    const next = controls.querySelector('[data-next]');
    const count = controls.querySelector('.carousel-count');
    controls.hidden = false;
    track.setAttribute('aria-roledescription', isChinese ? '轮播' : 'carousel');
    const update = () => {
      const box = track.getBoundingClientRect();
      const visible = slides.flatMap((slide, i) => {
        const r = slide.getBoundingClientRect();
        return Math.min(r.right, box.right) - Math.max(r.left, box.left) > r.width * .6 ? [i + 1] : [];
      });
      if (visible.length) count.textContent = `${visible[0]}${visible.length > 1 ? '–' + visible.at(-1) : ''} / ${slides.length}`;
      prev.disabled = track.scrollLeft < 3;
      next.disabled = track.scrollLeft >= track.scrollWidth - track.clientWidth - 3;
    };
    const move = direction => {
      const step = slides[1].offsetLeft - slides[0].offsetLeft;
      track.scrollBy({left: direction * step, behavior: reducedMotion.matches ? 'instant' : 'smooth'});
    };
    prev.addEventListener('click', () => move(-1));
    next.addEventListener('click', () => move(1));
    track.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        e.preventDefault(); move(e.key === 'ArrowLeft' ? -1 : 1);
      }
    });
    let frame;
    track.addEventListener('scroll', () => { cancelAnimationFrame(frame); frame = requestAnimationFrame(update); }, {passive:true});
    new ResizeObserver(update).observe(track);
    update();
  });

  // Photo links still open the image when JavaScript or <dialog> is unavailable.
  const photographs = [...document.querySelectorAll('[data-gallery]')];
  if (photographs.length && typeof HTMLDialogElement !== 'undefined') {
    const dialog = document.createElement('dialog');
    dialog.className = 'lightbox';
    dialog.setAttribute('aria-labelledby', 'lightbox-title');
    const labels = isChinese
      ? ['实验室相册', '关闭相册', '上一张照片', '下一张照片']
      : ['Laboratory photo gallery', 'Close gallery', 'Previous photograph', 'Next photograph'];
    dialog.innerHTML = `<div class="lightbox-top"><p id="lightbox-title">${labels[0]}</p><button type="button" data-close aria-label="${labels[1]}" autofocus>×</button></div><figure><img alt="" /><div class="lightbox-bottom"><figcaption aria-live="polite"></figcaption><div class="carousel-buttons"><button type="button" data-prev aria-label="${labels[2]}">←</button><span class="carousel-count"></span><button type="button" data-next aria-label="${labels[3]}">→</button></div></div></figure>`;
    document.body.append(dialog);
    let selected = 0, opener;
    const show = i => {
      selected = (i + photographs.length) % photographs.length;
      const link = photographs[selected];
      const img = dialog.querySelector('img');
      img.src = link.href;
      img.alt = link.querySelector('img').alt;
      dialog.querySelector('figcaption').textContent = link.querySelector('h3').textContent;
      dialog.querySelector('.carousel-count').textContent = `${selected + 1} / ${photographs.length}`;
    };
    photographs.forEach((link, i) => link.addEventListener('click', e => {
      if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
      e.preventDefault(); opener = link; show(i); dialog.showModal();
      document.documentElement.classList.add('lightbox-open');
    }));
    dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
    dialog.querySelector('[data-prev]').addEventListener('click', () => show(selected - 1));
    dialog.querySelector('[data-next]').addEventListener('click', () => show(selected + 1));
    dialog.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        e.preventDefault(); show(selected + (e.key === 'ArrowLeft' ? -1 : 1));
      }
    });
    dialog.addEventListener('click', e => { if (e.target === dialog) {
      const r = dialog.getBoundingClientRect();
      if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close();
    }});
    dialog.addEventListener('close', () => {
      document.documentElement.classList.remove('lightbox-open');
      opener?.focus({preventScroll:true});
    });
  }
  document.querySelector('#contact-form')?.addEventListener('submit', e => {
    e.preventDefault();
    const form = e.currentTarget;
    if(!form.reportValidity()) return;
    const values = new FormData(form);
    const subject = values.get('subject') || (isChinese ? 'TVPlab咨询' : 'TVPlab enquiry');
    const body = String(values.get('message')) + (isChinese ? '\n\n姓名：' : '\n\nFrom: ') + values.get('name') + (isChinese ? '\n邮箱：' : '\nEmail: ') + values.get('email');
    const recipient = form.getAttribute('action');
    location.href = recipient + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    document.querySelector('#contact-status').textContent = isChinese ? '邮件应用将打开草稿，请在那里检查并发送。如果没有打开邮件应用，请直接发送至 ajv22@cam.ac.uk。' : 'Your email app will open a draft. Review it and send it there. If no app opens, email ajv22@cam.ac.uk directly.';
  });
})();
