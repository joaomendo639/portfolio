// Teste automático de acessibilidade (axe-core) segundo a WCAG 2.x A/AA.
// Corre o site em smartphone, tablet e PC, nos temas claro e escuro,
// com o painel de acessibilidade fechado e aberto, e com cada opção ligada.
//
// Uso:  BASE_URL=http://localhost:8000/ node a11y.mjs
// (opcional) BROWSER_PATH=caminho/para/chrome-ou-edge
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';

const BASE_URL = process.env.BASE_URL || 'http://localhost:8000/';
import { readdirSync } from 'node:fs';
const PROJECT_PAGES = readdirSync(new URL('../projetos/', import.meta.url)).filter(f => f.endsWith('.html')).map(f => 'projetos/' + f);
const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];
const VIEWPORTS = [
  { name: 'smartphone', width: 390, height: 844, touch: true },
  { name: 'tablet', width: 820, height: 1180, touch: true },
  { name: 'pc', width: 1440, height: 900, touch: false },
];
const SCENARIOS = [
  { name: 'claro', storage: { theme: 'light' } },
  { name: 'escuro', storage: { theme: 'dark' } },
  { name: 'alto contraste claro', storage: { theme: 'light', a11y: { contrast: true } } },
  { name: 'alto contraste escuro', storage: { theme: 'dark', a11y: { contrast: true } } },
  { name: 'texto 200% + espaçamento + letra legível', storage: { a11y: { fs: 200, spacing: true, font: true, links: true, focus: true } } },
];

const browser = await chromium.launch(process.env.BROWSER_PATH ? { executablePath: process.env.BROWSER_PATH } : {});
let failures = 0;

for (const vp of VIEWPORTS) {
  for (const sc of SCENARIOS) {
    const ctx = await browser.newContext({
      viewport: { width: vp.width, height: vp.height }, hasTouch: vp.touch, isMobile: vp.touch,
      reducedMotion: 'reduce', // sem animações a meio durante a análise
    });
    await ctx.addInitScript((s) => {
      sessionStorage.setItem('introSeen', '1');
      localStorage.clear();
      if (s.theme) localStorage.setItem('theme', s.theme);
      if (s.a11y) localStorage.setItem('a11y', JSON.stringify(s.a11y));
    }, sc.storage);
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', (e) => errors.push(e.message));
    await page.goto(BASE_URL, { waitUntil: 'networkidle' });

    // Sem deslocamento horizontal (1.4.10 Reflow)
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);

    const states = [['painel fechado', null], ['painel aberto', async () => {
      await page.click('.a11y-open');
      await page.waitForSelector('#a11y-panel[open]');
    }]];
    for (const [state, action] of states) {
      if (action) await action();
      const res = await new AxeBuilder({ page }).withTags(TAGS).analyze();
      const label = `${vp.name} · ${sc.name} · ${state}`;
      if (res.violations.length) {
        failures += res.violations.length;
        console.log(`✗ ${label}`);
        for (const v of res.violations) {
          console.log(`   [${v.impact}] ${v.id}: ${v.help}`);
          for (const n of v.nodes.slice(0, 3)) console.log(`      ${n.target.join(' ')}`);
        }
      } else {
        console.log(`✓ ${label}`);
      }
    }
    if (overflow > 1) { failures++; console.log(`✗ ${vp.name} · ${sc.name}: deslocamento horizontal de ${overflow}px (1.4.10)`); }

    // Páginas de projeto
    for (const pg of PROJECT_PAGES) {
      await page.goto(BASE_URL + pg, { waitUntil: 'networkidle' });
      const res = await new AxeBuilder({ page }).withTags(TAGS).analyze();
      const ov = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      const label = `${vp.name} · ${sc.name} · ${pg}`;
      if (res.violations.length || ov > 1) {
        failures += res.violations.length + (ov > 1 ? 1 : 0);
        console.log(`✗ ${label}` + (ov > 1 ? ` (deslocamento horizontal ${ov}px)` : ''));
        for (const v of res.violations) console.log(`   [${v.impact}] ${v.id}: ${v.help} — ${v.nodes[0].target.join(' ')}`);
      } else console.log(`✓ ${label}`);
    }
    if (errors.length) { failures += errors.length; console.log(`✗ ${vp.name} · ${sc.name}: erros JS`, errors); }
    await ctx.close();
  }
}

await browser.close();
if (failures) {
  console.log(`\n${failures} problema(s) de acessibilidade encontrados.`);
  process.exit(1);
}
console.log('\nSem violações WCAG 2.2 A/AA detetadas automaticamente.');
