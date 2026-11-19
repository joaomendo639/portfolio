# Portfólio — João Mendo

Site estático (HTML, CSS e JS, sem build) publicado em **https://joaomendo639.github.io/portfolio/**.

## Editar conteúdo

Tudo o que precisa de ser personalizado está marcado com `EDITAR` em `index.html`:

| O quê | Onde |
|---|---|
| Nome / marca | cabeçalho e rodapé |
| Números | secção `stats` (atributo `data-count`) |
| Projetos | `assets/img/projeto-*.svg` → troca por imagens tuas (4:5, `.webp`/`.jpg`, ~1600 px) e atualiza `alt`, título, local e ano |
| Fotografia | `assets/img/retrato.svg` |
| Biografia e ferramentas | secção `#sobre` |
| Serviços | grelha `.bento` em `#servicos` |
| CV | não publicado (contém dados pessoais); versão sem morada/telefone/data de nascimento pode ir para `assets/cv.pdf` |
| Formulário | em `#contacto`, substitui `COLOCAR_ACCESS_KEY` pela chave do [Web3Forms](https://web3forms.com) |
| Redes | secção `#contacto` |

Cada projeto tem `data-category` (`uiux`, `web`, `multimedia`, `investigacao`; vários separados por espaço) usado pelos filtros.

## Acessibilidade (WCAG 2.2 AA)

### Painel de acessibilidade
Botão flutuante "Acessibilidade" no canto inferior direito (todos os tamanhos de ecrã; só ícone abaixo de 700 px). Abre um `<dialog>` com:
tema (sistema/claro/escuro), tamanho do texto (100–200 %, 1.4.4), alto contraste (1.4.6), reduzir movimento (2.2.2/2.3.3),
espaçamento de texto (1.4.12), letra legível (Atkinson Hyperlegible), sublinhar links (1.4.1), foco reforçado (2.4.13), cursor grande
e "Repor predefinições". As escolhas ficam em `localStorage` (`a11y`, `theme`, `motion`) e são aplicadas antes da pintura.

### Acompanhar a WCAG
- `wcag-version.txt` — versão que o site segue.
- `.github/workflows/acessibilidade.yml` — axe-core (WCAG 2.0/2.1/2.2 A e AA) em cada push e todas as segundas-feiras:
  smartphone, tablet e PC × claro, escuro, alto contraste e texto 200 %, com o painel fechado e aberto.
- `.github/workflows/wcag-versao.yml` — no dia 1 de cada mês compara com https://www.w3.org/TR/WCAG/ e abre uma *issue* se houver nova versão.
- Correr os testes localmente: `cd tests && npm install && npx playwright install chromium && BASE_URL=http://localhost:8000/ npm test`

### Outras medidas

- Botão **Reduzir movimento** no cabeçalho (2.2.2 / 2.3.3), guardado entre visitas; respeita também `prefers-reduced-motion`
- Painel lateral (cápsula de vidro com ícones) só aparece com margem livre (≥ 1440 px) — não tapa conteúdo (1.4.10); etiquetas fecham com `Esc` (1.4.13); cada ícone tem `aria-label`
- `scroll-padding-top` evita que o cabeçalho fixo tape o foco (2.4.11)
- Bordas dos campos com contraste ≥ 3:1 (1.4.11); alvos ≥ 24×24 px (2.5.8)
- Testado: axe-core (0 violações, claro/escuro, 390 e 1600 px), reflow a 320 px, espaçamento de texto 1.4.12, navegação por Tab

- HTML semântico, `lang="pt-PT"`, link "Saltar para o conteúdo"
- Navegação total por teclado, foco visível, menu móvel com `Esc` e foco contido
- Contraste WCAG AA nos dois temas (claro/escuro, segue o sistema e pode ser trocado)
- Respeita `prefers-reduced-motion` e o modo de alto contraste do Windows
- Conteúdo visível mesmo sem JavaScript
- Texto alternativo em todas as imagens

## Pré-visualizar localmente

```bash
npx serve .
```

## Publicar

```bash
git add -A && git commit -m "Atualiza conteúdo" && git push
```

O GitHub Pages atualiza em ~1 minuto.
