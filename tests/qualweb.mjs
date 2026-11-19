// Avaliação com o QualWeb — o mesmo motor do AccessMonitor (acessibilidade.gov.pt).
// Falha se houver qualquer erro nas regras ACT, nas técnicas WCAG ou nas boas práticas,
// em particular contraste mínimo (AA, QW-ACT-R37) e melhorado (AAA, QW-ACT-R76).
//
// Uso: BASE_URL=http://localhost:8000/ node qualweb.mjs
// (opcional) BROWSER_PATH=caminho/para/chrome-ou-edge
import { readdirSync } from 'node:fs';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { QualWeb } = require('@qualweb/core');

const BASE_URL = process.env.BASE_URL || 'http://localhost:8000/';
const PAGES = ['', ...readdirSync(new URL('../projetos/', import.meta.url)).filter(f => f.endsWith('.html')).map(f => 'projetos/' + f)];

let executablePath = process.env.BROWSER_PATH;
if (!executablePath) {
  const { chromium } = await import('playwright');
  executablePath = chromium.executablePath();
}

const qw = new QualWeb({});
await qw.start({ maxConcurrency: 1, timeout: 180000 }, { executablePath, headless: true, args: ['--no-sandbox'] });
const reports = await qw.evaluate({ urls: PAGES.map(p => BASE_URL + p), viewport: { mobile: false, landscape: true, resolution: { width: 1366, height: 768 } } });
await qw.stop();

let failures = 0;
for (const [url, rep] of Object.entries(reports)) {
  const out = [];
  for (const mod of ['act-rules', 'wcag-techniques', 'best-practices']) {
    const m = rep.modules[mod]; if (!m) continue;
    for (const [code, a] of Object.entries(m.assertions)) {
      if (a.metadata.outcome !== 'failed') continue;
      failures += a.metadata.failed;
      out.push(`   [${code}] ${a.name} — ${a.metadata.failed} erro(s)`);
      for (const r of a.results.filter(r => r.verdict === 'failed').slice(0, 5))
        for (const el of (r.elements || []).slice(0, 1)) out.push(`      ${(el.htmlCode || '').replace(/\s+/g, ' ').slice(0, 110)}`);
    }
  }
  console.log((out.length ? '✗ ' : '✓ ') + url.replace(BASE_URL, '/') + (out.length ? '\n' + out.join('\n') : ''));
}
if (failures) { console.log(`\n${failures} erro(s) QualWeb/AccessMonitor.`); process.exit(1); }
console.log('\nQualWeb (AccessMonitor): sem erros.');
process.exit(0);
