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

  /* ---------- Formulário de contacto (Web3Forms) ---------- */
  var form = document.getElementById('contact-form');
  if (form && window.fetch) {
    var statusEl = document.getElementById('form-status');
    var submitBtn = form.querySelector('button[type="submit"]');
    var messages = {
      name: { valueMissing: 'Indique o seu nome.' },
      email: { valueMissing: 'Indique o seu email.', typeMismatch: 'Indique um email válido, por exemplo nome@dominio.pt.' },
      message: { valueMissing: 'Escreva a sua mensagem.', tooShort: 'A mensagem deve ter pelo menos 10 caracteres.' }
    };
    var fields = form.querySelectorAll('input[required], textarea[required]');
    function validateField(field) {
      var err = document.getElementById(field.id + '-err');
      var v = field.validity, m = messages[field.name] || {}, text = '';
      if (v.valueMissing) text = m.valueMissing;
      else if (v.typeMismatch) text = m.typeMismatch;
      else if (v.tooShort) text = m.tooShort;
      field.setAttribute('aria-invalid', text ? 'true' : 'false');
      if (err) err.textContent = text || '';
      return !text;
    }
    fields.forEach(function (f) {
      f.addEventListener('blur', function () { if (f.value) validateField(f); });
      f.addEventListener('input', function () { if (f.getAttribute('aria-invalid') === 'true') validateField(f); });
    });
    function setStatus(text, ok) {
      statusEl.textContent = text;
      statusEl.className = 'form-status ' + (ok ? 'is-ok' : 'is-error');
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var firstInvalid = null;
      fields.forEach(function (f) { if (!validateField(f) && !firstInvalid) firstInvalid = f; });
      if (firstInvalid) { firstInvalid.focus(); setStatus('Corrija os campos assinalados.', false); return; }
      if (form.elements.access_key.value.indexOf('COLOCAR') === 0) {
        setStatus('O formulário ainda não está ativo. Contacte-me pelo LinkedIn, por favor.', false);
        return;
      }
      var data = {};
      new FormData(form).forEach(function (v, k) { if (k !== 'redirect') data[k] = v; });
      submitBtn.disabled = true;
      setStatus('A enviar…', true);
      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(data)
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (res.success) {
            form.reset();
            fields.forEach(function (f) { f.removeAttribute('aria-invalid'); });
            setStatus('Obrigado! A mensagem foi enviada. Respondo em breve.', true);
          } else {
            setStatus('Não foi possível enviar. Tente novamente ou contacte-me pelo LinkedIn.', false);
          }
        })
        .catch(function () { setStatus('Sem ligação. Verifique a internet e tente novamente.', false); })
        .then(function () { submitBtn.disabled = false; });
    });
  }

  /* =========================================================
     Interatividade — só com movimento permitido
     ========================================================= */
  var motionOK = !reduceMotion.matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* Título dividido em palavras (o texto continua igual para leitores de ecrã) */
  document.querySelectorAll('[data-split]').forEach(function (el) {
    if (!motionOK) return;
    var i = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (child) {
        if (child.nodeType === 3) {
          var frag = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            var w = document.createElement('span'); w.className = 'split-word';
            var inner = document.createElement('span'); inner.textContent = part; inner.style.setProperty('--i', i++);
            w.appendChild(inner); frag.appendChild(w);
          });
          child.parentNode.replaceChild(frag, child);
        } else if (child.nodeType === 1) { walk(child); }
      });
    })(el);
    requestAnimationFrame(function () { requestAnimationFrame(function () { el.classList.add('is-split'); }); });
  });

  /* Indicador lateral + barra de progresso + parallax do hero */
  var railLinks = Array.prototype.slice.call(document.querySelectorAll('.rail a'));
  var railFill = document.querySelector('.rail-fill');
  var progress = document.querySelector('.scroll-progress span');
  var heroArt = document.querySelector('[data-parallax] img');
  var heroCard = document.querySelector('.hero-card');
  var numeral = document.querySelector('.hero-numeral');
  var railTargets = railLinks.map(function (a) { return document.querySelector(a.getAttribute('href')); });
  var ticking = false;

  function onFrame() {
    ticking = false;
    var y = window.scrollY, vh = window.innerHeight;
    var max = document.documentElement.scrollHeight - vh;
    var p = max > 0 ? Math.min(Math.max(y / max, 0), 1) : 0;
    if (progress) progress.style.transform = 'scaleX(' + p + ')';
    if (railFill) railFill.style.transform = 'scaleY(' + p + ')';

    // secção ativa = a que atravessa o meio do ecrã
    var mid = y + vh * 0.45, active = 0;
    railTargets.forEach(function (t, i) { if (t && t.offsetTop <= mid) active = i; });
    railLinks.forEach(function (a, i) {
      if (i === active) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
    });

    if (motionOK && y < vh * 1.2) {
      if (heroArt) heroArt.style.transform = 'translate3d(0,' + (y * 0.08) + 'px,0) scale(' + (1 + y * 0.00012) + ')';
      if (heroCard) heroCard.style.transform = 'translate3d(0,' + (y * -0.12) + 'px,0)';
      if (numeral) numeral.style.transform = 'translate3d(0,' + (y * 0.35) + 'px,0)';
    }
  }
  function requestFrame() { if (!ticking) { ticking = true; requestAnimationFrame(onFrame); } }
  window.addEventListener('scroll', requestFrame, { passive: true });
  window.addEventListener('resize', requestFrame);
  onFrame();

  if (motionOK && finePointer) {
    /* Brilho a seguir o cursor */
    var glow = document.querySelector('.cursor-glow');
    var gx = 0, gy = 0, tx = 0, ty = 0, glowRunning = false;
    function glowLoop() {
      gx += (tx - gx) * 0.12; gy += (ty - gy) * 0.12;
      glow.style.transform = 'translate3d(' + gx + 'px,' + gy + 'px,0)';
      if (Math.abs(tx - gx) > 0.5 || Math.abs(ty - gy) > 0.5) requestAnimationFrame(glowLoop); else glowRunning = false;
    }
    if (glow) {
      window.addEventListener('pointermove', function (e) {
        tx = e.clientX; ty = e.clientY;
        if (!document.documentElement.classList.contains('has-pointer')) {
          gx = tx; gy = ty; document.documentElement.classList.add('has-pointer');
        }
        if (!glowRunning) { glowRunning = true; requestAnimationFrame(glowLoop); }
      }, { passive: true });
      document.addEventListener('pointerleave', function () { document.documentElement.classList.remove('has-pointer'); });
    }

    /* Cartões com inclinação 3D e reflexo */
    document.querySelectorAll('.tilt').forEach(function (card) {
      var art = card.querySelector('article');
      var glare = document.createElement('span'); glare.className = 'tilt-glare'; glare.setAttribute('aria-hidden', 'true');
      art.appendChild(glare);
      card.addEventListener('pointermove', function (e) {
        var r = art.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
        card.classList.add('is-tilting');
        art.style.transform = 'perspective(900px) rotateX(' + ((0.5 - py) * 8) + 'deg) rotateY(' + ((px - 0.5) * 10) + 'deg) translateZ(0)';
        art.style.setProperty('--gx', px * 100 + '%'); art.style.setProperty('--gy', py * 100 + '%');
      });
      card.addEventListener('pointerleave', function () { card.classList.remove('is-tilting'); art.style.transform = ''; });
    });

    /* Botões "magnéticos" */
    document.querySelectorAll('.magnetic').forEach(function (btn) {
      btn.addEventListener('pointermove', function (e) {
        var r = btn.getBoundingClientRect();
        var dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
        btn.style.transform = 'translate(' + dx * 0.25 + 'px,' + dy * 0.35 + 'px)';
      });
      btn.addEventListener('pointerleave', function () { btn.style.transform = ''; });
    });
  }

  /* ---------- Ano no rodapé ---------- */
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
