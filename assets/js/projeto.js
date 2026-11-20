/* Páginas de projeto: carrossel de imagens e índice de capítulos.
   Sem JS o carrossel continua a deslizar (scroll horizontal com snap) e o índice são links normais. */
(function () {
  'use strict';
  var root = document.documentElement;
  var sysReduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  function motionOn() { return !sysReduce.matches && !root.classList.contains('reduce-motion'); }
  function behavior() { return motionOn() ? 'smooth' : 'auto'; }

  /* ---------- Carrossel (padrão WAI-ARIA, sem passagem automática) ---------- */
  var gallery = document.querySelector('.gallery');
  if (gallery) {
    var track = gallery.querySelector('.gallery-track');
    var slides = Array.prototype.slice.call(track.querySelectorAll('.gallery-slide'));
    var prev = gallery.querySelector('.gallery-prev');
    var next = gallery.querySelector('.gallery-next');
    var now = gallery.querySelector('.gallery-now');
    var bar = gallery.querySelector('.gallery-progress span');
    var thumbs = Array.prototype.slice.call(gallery.querySelectorAll('.gallery-thumb'));
    var status = document.getElementById('gallery-status');
    var current = 0, announce = false;

    function pad(n) { return (n < 10 ? '0' : '') + n; }
    function setActive(i) {
      current = i;
      slides.forEach(function (s, k) { s.classList.toggle('is-active', k === i); });
      thumbs.forEach(function (t, k) { if (k === i) t.setAttribute('aria-current', 'true'); else t.removeAttribute('aria-current'); });
      if (now) now.textContent = pad(i + 1);
      if (bar) bar.style.setProperty('--p', ((i + 1) / slides.length).toFixed(4));
      if (prev) prev.disabled = i === 0;
      if (next) next.disabled = i === slides.length - 1;
      if (announce && status) {
        var cap = slides[i].querySelector('figcaption');
        status.textContent = 'Imagem ' + (i + 1) + ' de ' + slides.length + (cap ? ': ' + cap.textContent : '');
      }
    }
    function goTo(i, speak) {
      i = Math.max(0, Math.min(slides.length - 1, i));
      announce = !!speak;
      track.scrollTo({ left: slides[i].offsetLeft - slides[0].offsetLeft, behavior: behavior() });
      setActive(i);
    }
    // Atualiza ao deslizar (toque, trackpad, arrastar)
    var ticking = false;
    track.addEventListener('scroll', function () {
      if (ticking) return; ticking = true;
      requestAnimationFrame(function () {
        ticking = false;
        var x = track.scrollLeft, best = 0, d = Infinity;
        slides.forEach(function (s, k) { var dd = Math.abs(s.offsetLeft - slides[0].offsetLeft - x); if (dd < d) { d = dd; best = k; } });
        if (best !== current) { announce = false; setActive(best); }
      });
    }, { passive: true });

    if (prev) prev.addEventListener('click', function () { goTo(current - 1, true); });
    if (next) next.addEventListener('click', function () { goTo(current + 1, true); });
    thumbs.forEach(function (t) { t.addEventListener('click', function () { goTo(parseInt(t.dataset.go, 10), true); }); });
    gallery.addEventListener('keydown', function (e) {
      if (e.target.closest('input, textarea')) return;
      if (e.key === 'ArrowRight') { e.preventDefault(); goTo(current + 1, true); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(current - 1, true); }
      else if (e.key === 'Home') { e.preventDefault(); goTo(0, true); }
      else if (e.key === 'End') { e.preventDefault(); goTo(slides.length - 1, true); }
    });

    // Arrastar com o rato (no toque o scroll nativo já faz isto)
    var drag = null;
    track.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse' || e.button !== 0) return;
      drag = { x: e.clientX, left: track.scrollLeft, moved: false };
      track.setPointerCapture(e.pointerId);
    });
    track.addEventListener('pointermove', function (e) {
      if (!drag) return;
      var dx = e.clientX - drag.x;
      if (Math.abs(dx) > 4) { drag.moved = true; track.classList.add('is-dragging'); }
      track.scrollLeft = drag.left - dx;
    });
    function endDrag(e) {
      if (!drag) return;
      var dx = e.clientX - drag.x, moved = drag.moved;
      drag = null; track.classList.remove('is-dragging');
      if (moved) goTo(current + (dx < -60 ? 1 : dx > 60 ? -1 : 0), true);
    }
    track.addEventListener('pointerup', endDrag);
    track.addEventListener('pointercancel', endDrag);

    // Cursor "Arrastar" que segue o rato por cima das imagens
    var viewport = gallery.querySelector('.gallery-viewport');
    var cursor = gallery.querySelector('.gallery-cursor');
    if (viewport && cursor) {
      viewport.addEventListener('pointermove', function (e) {
        if (e.pointerType !== 'mouse') return;
        var r = viewport.getBoundingClientRect();
        cursor.style.setProperty('--cx', (e.clientX - r.left) + 'px');
        cursor.style.setProperty('--cy', (e.clientY - r.top) + 'px');
      });
    }
    setActive(0);
  }

  /* ---------- Copiar (cores, citação) ---------- */
  function copiar(texto, statusEl) {
    var feito = function () { if (statusEl) { statusEl.textContent = ''; setTimeout(function () { statusEl.textContent = 'Copiado: ' + texto; }, 30); } };
    if (navigator.clipboard && window.isSecureContext) { navigator.clipboard.writeText(texto).then(feito, feito); return; }
    var ta = document.createElement('textarea'); ta.value = texto; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); } catch (e) {} document.body.removeChild(ta); feito();
  }
  document.querySelectorAll('[data-copiar], [data-copiar-de]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var alvo = btn.dataset.copiarDe ? document.getElementById(btn.dataset.copiarDe) : null;
      var texto = alvo ? alvo.textContent.trim() : btn.dataset.copiar;
      var status = btn.closest('.modulo').querySelector('.copiar-status');
      copiar(texto, status);
      if (alvo) { var orig = btn.textContent; btn.textContent = 'Copiado ✓'; setTimeout(function () { btn.textContent = orig; }, 1800); }
    });
  });

  /* ---------- Design: amostra tipográfica ---------- */
  var tamanho = document.getElementById('tipo-tamanho');
  var amostra = document.getElementById('tipo-texto');
  if (tamanho && amostra) {
    var saida = document.getElementById('tipo-valor');
    tamanho.addEventListener('input', function () { amostra.style.setProperty('--tamanho', (tamanho.value / 16) + 'rem'); if (saida) saida.textContent = tamanho.value + ' px'; });
    document.querySelectorAll('.tipo-pesos button').forEach(function (b, _, todos) {
      b.addEventListener('click', function () {
        todos.forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
        amostra.style.setProperty('--peso', b.dataset.peso);
      });
    });
  }

  /* ---------- Web: simulador de dispositivos ---------- */
  var palco = document.querySelector('.disp-palco');
  if (palco) {
    var ecra = palco.querySelector('.disp-ecra');
    document.querySelectorAll('.disp-btn').forEach(function (b, _, todos) {
      b.addEventListener('click', function () {
        var d = b.dataset.disp;
        todos.forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
        palco.dataset.atual = d;
        palco.querySelectorAll('.disp-img').forEach(function (img) { img.classList.toggle('is-on', img.dataset.disp === d); });
        if (ecra) ecra.scrollTop = 0;
      });
    });
  }

  /* ---------- Fotografia: ecrã inteiro com parâmetros ---------- */
  var lb = document.querySelector('.lightbox');
  if (lb && typeof lb.showModal === 'function') {
    var fotos = Array.prototype.slice.call(document.querySelectorAll('.foto'));
    var lbImg = lb.querySelector('.lightbox-fig img'), lbLeg = lb.querySelector('.lightbox-leg');
    var lbPar = lb.querySelector('.lightbox-params'), lbStatus = lb.querySelector('.lightbox-status');
    var atual = 0, origem = null;
    var mostrar = function (i) {
      atual = (i + fotos.length) % fotos.length;
      var f = fotos[atual], img = f.querySelector('img');
      lbImg.src = img.src; lbImg.alt = img.alt;
      lbLeg.textContent = f.querySelector('.foto-leg').textContent;
      lbPar.innerHTML = ''; var lista = f.querySelector('.foto-params'); if (lista && lista.children.length) lbPar.appendChild(lista.cloneNode(true));
      if (lbStatus) lbStatus.textContent = 'Fotografia ' + (atual + 1) + ' de ' + fotos.length + ': ' + lbLeg.textContent;
    };
    fotos.forEach(function (f, i) {
      f.querySelector('.foto-abrir').addEventListener('click', function (e) { origem = e.currentTarget; mostrar(i); lb.showModal(); });
    });
    lb.querySelector('.lightbox-prev').addEventListener('click', function () { mostrar(atual - 1); });
    lb.querySelector('.lightbox-next').addEventListener('click', function () { mostrar(atual + 1); });
    lb.querySelector('.lightbox-close').addEventListener('click', function () { lb.close(); });
    lb.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); mostrar(atual + 1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); mostrar(atual - 1); }
    });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lightbox-inner')) lb.close(); });
    lb.addEventListener('close', function () { if (origem) origem.focus(); });
    if (fotos.length < 2) { lb.querySelector('.lightbox-prev').hidden = true; lb.querySelector('.lightbox-next').hidden = true; }
  }

  /* ---------- Demonstração "Experimente" (acessibilidade) ---------- */
  document.querySelectorAll('.a11y-demo').forEach(function (demo) {
    var card = demo.querySelector('.demo-card');
    demo.querySelectorAll('.demo-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var on = btn.getAttribute('aria-pressed') !== 'true';
        btn.setAttribute('aria-pressed', String(on));
        card.classList.toggle('is-' + btn.dataset.demo, on);
      });
    });
  });

  /* ---------- Capítulos: marcador acende quando o capítulo entra no ecrã ---------- */
  var chs = Array.prototype.slice.call(document.querySelectorAll('.chapter'));
  if ('IntersectionObserver' in window) {
    var inObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); inObs.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -25% 0px' });
    chs.forEach(function (c) { inObs.observe(c); });
  } else { chs.forEach(function (c) { c.classList.add('is-in'); }); }

  /* ---------- Índice de capítulos: capítulo atual, imagem do painel e linha de leitura ---------- */
  var stage = document.querySelector('.story-stage');
  var stageImgs = stage ? Array.prototype.slice.call(stage.querySelectorAll('.stage-img')) : [];
  var stageNum = stage && stage.querySelector('.stage-num');
  var stageCap = stage && stage.querySelector('.stage-cap');
  var stageNow = 0;
  function setStage(k) {
    if (!stage || k === stageNow || !stageImgs[k]) return;
    stageNow = k;
    stageImgs.forEach(function (img, i) { img.classList.toggle('is-on', i === k); });
    if (stageNum) stageNum.textContent = (k < 9 ? '0' : '') + (k + 1);
    if (stageCap) stageCap.textContent = stageImgs[k].dataset.cap;
    stage.classList.remove('is-changing'); void stage.offsetWidth; stage.classList.add('is-changing');
  }

  var index = document.querySelector('.story-index');
  var chapters = Array.prototype.slice.call(document.querySelectorAll('.chapter'));
  if (index && chapters.length) {
    var links = Array.prototype.slice.call(index.querySelectorAll('a'));
    var line = index.querySelector('.story-line span');
    var story = document.querySelector('.story-chapters');
    var raf = false;
    function update() {
      raf = false;
      var vh = window.innerHeight, active = 0;
      chapters.forEach(function (c, k) { if (c.getBoundingClientRect().top < vh * 0.45) active = k; });
      links.forEach(function (a, k) { if (k === active) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
      setStage(active);
      if (line && story) {
        var r = story.getBoundingClientRect();
        var p = (vh * 0.45 - r.top) / r.height;
        line.style.setProperty('--read', Math.max(0, Math.min(1, p)).toFixed(3));
      }
    }
    window.addEventListener('scroll', function () { if (!raf) { raf = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', update);
    update();
  }
})();
