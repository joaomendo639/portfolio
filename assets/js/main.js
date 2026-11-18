/* Portfólio — interações. Tudo funciona sem JS; isto só acrescenta. */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

  /* ---------- Tema claro/escuro ---------- */
  var themeBtn = document.querySelector('.theme-toggle');
  function currentTheme() {
    return root.dataset.theme || (prefersDark.matches ? 'dark' : 'light');
  }
  function syncThemeButton() {
    var next = currentTheme() === 'dark' ? 'claro' : 'escuro';
    themeBtn.setAttribute('aria-label', 'Mudar para tema ' + next);
  }
  if (themeBtn) {
    syncThemeButton();
    themeBtn.addEventListener('click', function () {
      var next = currentTheme() === 'dark' ? 'light' : 'dark';
      root.dataset.theme = next;
      try { localStorage.setItem('theme', next); } catch (e) {}
      syncThemeButton();
    });
    prefersDark.addEventListener && prefersDark.addEventListener('change', syncThemeButton);
  }

  /* ---------- Cabeçalho ao fazer scroll ---------- */
  var header = document.querySelector('.site-header');
  function onScroll() { header.classList.toggle('is-scrolled', window.scrollY > 24); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- Menu móvel ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('nav-menu');
  var toggleLabel = toggle && toggle.querySelector('.sr-only');

  function setMenu(open) {
    toggle.setAttribute('aria-expanded', String(open));
    menu.classList.toggle('is-open', open);
    document.body.classList.toggle('nav-open', open);
    if (toggleLabel) toggleLabel.textContent = open ? 'Fechar menu' : 'Abrir menu';
    if (open) { var first = menu.querySelector('a'); first && first.focus(); }
  }
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      setMenu(toggle.getAttribute('aria-expanded') !== 'true');
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        toggle.focus();
      }
    });
    // Mantém o foco dentro do menu aberto (Tab circular)
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab' || toggle.getAttribute('aria-expanded') !== 'true') return;
      var items = [toggle].concat(Array.prototype.slice.call(menu.querySelectorAll('a')));
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    window.matchMedia('(min-width: 861px)').addEventListener('change', function (m) {
      if (m.matches) setMenu(false);
    });
  }

  /* ---------- Link ativo na navegação ---------- */
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav-menu a'));
  if ('IntersectionObserver' in window && navLinks.length) {
    var sectionObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (a) {
          if (a.getAttribute('href') === '#' + entry.target.id) a.setAttribute('aria-current', 'true');
          else a.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    navLinks.forEach(function (a) {
      var s = document.querySelector(a.getAttribute('href'));
      if (s) sectionObs.observe(s);
    });
  }

  /* ---------- Animações de entrada ---------- */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion.matches) {
    var revealObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function (el, i) {
      el.style.transitionDelay = (i % 4) * 90 + 'ms';
      revealObs.observe(el);
    });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---------- Contadores ---------- */
  var counters = document.querySelectorAll('[data-count]');
  function animateCount(el) {
    var target = parseInt(el.dataset.count, 10);
    var suffix = 'suffix' in el.dataset ? el.dataset.suffix : '+';
    var start = null, duration = 1600;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  counters.forEach(function (el) { el.textContent = el.dataset.count + ('suffix' in el.dataset ? el.dataset.suffix : '+'); });
  if ('IntersectionObserver' in window && !reduceMotion.matches) {
    var countObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { animateCount(entry.target); countObs.unobserve(entry.target); }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { countObs.observe(el); });
  }

  /* ---------- Filtro de projetos ---------- */
  var chips = document.querySelectorAll('.chip[data-filter]');
  var projects = document.querySelectorAll('.project');
  var status = document.getElementById('filter-status');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var f = chip.dataset.filter, shown = 0;
      chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
      chip.closest('.section').querySelector('.projects').classList.toggle('is-filtered', f !== 'all');
      projects.forEach(function (p) {
        var match = f === 'all' || p.dataset.category.split(' ').indexOf(f) !== -1;
        p.hidden = !match;
        if (match) { shown++; p.classList.add('is-visible'); }
      });
      if (status) status.textContent = shown + (shown === 1 ? ' projeto apresentado' : ' projetos apresentados');
    });
  });

  /* ---------- Ano no rodapé ---------- */
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
