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
| CV | não publicado (contém dados pessoais); versão sem morada/telefone/data de nascimento pode ir para `assets/cv.pdf` |
| Formulário | em `#contacto`, substitui `COLOCAR_ACCESS_KEY` pela chave do [Web3Forms](https://web3forms.com) |
| Redes | secção `#contacto` |

Cada projeto tem `data-category` (`uiux`, `web`, `multimedia`, `investigacao`; vários separados por espaço) usado pelos filtros.

## Acessibilidade

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
