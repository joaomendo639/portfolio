// Deteta sobreposições de texto/controlos e deslocamento horizontal em 6 larguras de ecrã,
// com o texto a 100–200 % e as opções de espaçamento e letra legível do painel.
// Uso: BASE_URL=http://localhost:8000/ node sobreposicao.mjs
import { chromium } from 'playwright';
const BASE_URL = process.env.BASE_URL || 'http://localhost:8000/';
const VPS = [['320', 320, 640, true], ['390', 390, 844, true], ['820', 820, 1180, true], ['1024', 1024, 768, false], ['1440', 1440, 900, false], ['1920', 1920, 1080, false]];
const CASES = [];
for (const fs of [100, 125, 150, 175, 200]) CASES.push({ fs });
CASES.push({ fs: 200, spacing: true }, { fs: 200, font: true, spacing: true }, { fs: 100, spacing: true });
const only = process.argv[2];
  const b = await chromium.launch(process.env.BROWSER_PATH ? { executablePath: process.env.BROWSER_PATH } : {});
  let total = 0;
  for (const [n, w, h, t] of VPS) {
    if (only && only !== n) continue;
    for (const cs of CASES) {
      const c = await b.newContext({ viewport: { width: w, height: h }, hasTouch: t, isMobile: t, reducedMotion: 'reduce' });
      await c.addInitScript((a) => { sessionStorage.setItem('introSeen', '1'); localStorage.setItem('a11y', JSON.stringify(a)); }, cs);
      const p = await c.newPage();
      await p.goto(BASE_URL + '?' + Date.now()); await p.waitForTimeout(900);
      const res = await p.evaluate(() => {
        const sy = scrollY;
        const skip = el => el.closest('[aria-hidden="true"], dialog, .intro, .sr-only, .hp, .site-header, .a11y-fab, .rail, .skip-link, script, style');
        const vis = el => { for (let e = el; e && e !== document.body; e = e.parentElement) { const s = getComputedStyle(e); if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0) return false; } return true; };
        const boxes = [];
        const label = el => (el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/)[0] : '') + ':"' + el.textContent.trim().replace(/\s+/g, ' ').slice(0, 22) + '"');
        // linhas de texto
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        while ((node = walker.nextNode())) {
          if (!node.textContent.trim()) continue;
          const el = node.parentElement; if (!el || skip(el) || !vis(el)) continue;
          const r = document.createRange(); r.selectNodeContents(node);
          for (const q of r.getClientRects()) if (q.width > 2 && q.height > 2) boxes.push({ el, k: label(el), x1: q.left, y1: q.top + sy, x2: q.right, y2: q.bottom + sy, text: true });
        }
        // controlos
        for (const el of document.querySelectorAll('a.btn, button, input:not([type=hidden]):not(.hp), textarea, .chip, .icon-btn, .project img, .hero-art img, .about-photo img')) {
          if (skip(el) || !vis(el)) continue;
          const q = (el.tagName === 'IMG' && el.closest('article, figure') ? el.closest('article, figure') : el).getBoundingClientRect(); if (q.width < 2) continue;
          boxes.push({ el, k: label(el), x1: q.left, y1: q.top + sy, x2: q.right, y2: q.bottom + sy, ctl: true });
        }
        const out = [];
        const related = (a, b) => a.contains(b) || b.contains(a);
        // texto pode ficar sobre a SUA imagem de fundo (cartões / destaque) — permitido
        const overlayOk = (a, b) => { const img = a.ctl && a.el.tagName === 'IMG' ? a : b.ctl && b.el.tagName === 'IMG' ? b : null; if (!img) return false; const other = img === a ? b : a; const card = img.el.closest('article, figure'); return card && card.contains(other.el); };
        // ordenadas por y: cada caixa só é comparada com as que começam antes de ela acabar
        boxes.sort((p, q) => p.y1 - q.y1);
        for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length && boxes[j].y1 < boxes[i].y2; j++) {
          const a = boxes[i], b = boxes[j];
          if (a.el === b.el || related(a.el, b.el)) continue;
          const ox = Math.min(a.x2, b.x2) - Math.max(a.x1, b.x1), oy = Math.min(a.y2, b.y2) - Math.max(a.y1, b.y1);
          if (ox > 3 && oy > 3 && !overlayOk(a, b)) out.push(a.k + ' × ' + b.k + ` @y${a.y1 | 0}`);
        }
        // fixos: cabeçalho por dentro
        const hb = [...document.querySelectorAll('.site-header .brand, .site-header .nav-menu a, .site-header button, .site-header .header-cta')].filter(e => vis(e) && e.getBoundingClientRect().width > 0 && !(e.closest('.nav-menu') && getComputedStyle(e.closest('.nav-menu')).position === 'fixed'));
        for (let i = 0; i < hb.length; i++) for (let j = i + 1; j < hb.length; j++) {
          const a = hb[i].getBoundingClientRect(), b = hb[j].getBoundingClientRect();
          if (Math.min(a.right, b.right) - Math.max(a.left, b.left) > 2 && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 2) out.push('HEADER ' + label(hb[i]) + ' × ' + label(hb[j]));
        }
        const hdr = document.querySelector('.site-header').getBoundingClientRect();
        if (hdr.right > innerWidth + 1) out.push('HEADER mais largo que o ecrã');
        if (document.documentElement.scrollWidth > innerWidth + 1) out.push('scroll horizontal ' + (document.documentElement.scrollWidth - innerWidth));
        return [...new Set(out)];
      });
      const tag = `${n} ${JSON.stringify(cs)}`;
      if (res.length) { total += res.length; console.log('✗ ' + tag + '\n   ' + res.slice(0, 8).join('\n   ') + (res.length > 8 ? `\n   … +${res.length - 8}` : '')); }
      else console.log('✓ ' + tag);
      await c.close();
    }
  }
  await b.close();
  console.log(total ? `\n${total} sobreposição(ões) encontradas.` : '\nSem sobreposições.');
  if (total) process.exit(1);
