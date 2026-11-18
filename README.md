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
