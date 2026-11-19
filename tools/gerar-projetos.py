# -*- coding: utf-8 -*-
"""
Gera as páginas de cada projeto (projetos/<slug>.html).

O cabeçalho, o logótipo, o painel de acessibilidade e o rodapé são copiados de index.html,
por isso as páginas ficam sempre iguais ao resto do site.

EDITAR: o texto de cada projeto está na lista PROJETOS, mais abaixo.
Depois de alterar este ficheiro ou o index.html, correr na pasta do site:

    python tools/gerar-projetos.py
"""
import html
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
INDEX = (RAIZ / "index.html").read_text(encoding="utf-8")
SAIDA = RAIZ / "projetos"

# ---------------------------------------------------------------------------
# Conteúdo dos projetos (pela ordem em que aparecem no site)
# Cada secção: (título, html). Listas: "<ul><li>…</li></ul>".
# ---------------------------------------------------------------------------
PROJETOS = [
    {
        "slug": 'interfaces-a-mover',
        "titulo": 'Interfaces A-MoVeR',
        "etiqueta": 'UI/UX · Investigação',
        "resumo": 'Interfaces para mobilidade elétrica — o painel de instrumentos de uma mota e a aplicação móvel que o acompanha — desenhadas para serem lidas de relance, com segurança e por todos.',
        "meta": [('Ano', '2024–25'), ('Papel', 'UI/UX Designer · Bolseiro de Investigação'), ('Contexto', 'Projeto A-MoVeR, Vila Real'), ('Ferramentas', 'Figma, Adobe Illustrator, Adobe XD')],
        # Carrossel: (imagem em assets/img/, texto alternativo, legenda). EDITAR: trocar por imagens reais.
        "galeria": [
            ('projeto-1.svg', 'Painel digital de mota com velocímetro, bateria e indicadores.', 'Painel de instrumentos'),
            ('hero.svg', 'Painel de mota ao lado de um telemóvel com a aplicação.', 'Painel e aplicação móvel'),
            ('projeto-6.svg', 'Artigo científico com gráfico e o símbolo de acessibilidade.', 'Investigação em acessibilidade'),
        ],
        # Capítulos: ("texto", título, html) · ("frase", título, texto que acende com o scroll) · ("passos", título, [passos])
        "capitulos": [
            ('texto', 'Contexto', '<p>O A-MoVeR é um projeto de investigação em mobilidade elétrica. Entre junho de 2024 e junho de 2025, como Bolseiro de Investigação, fui responsável pelo design de interfaces das soluções digitais do projeto.</p>'),
            ('frase', 'O desafio', 'Um painel de mota é lido em segundos, em andamento, ao sol, à chuva ou à noite. A informação essencial — velocidade, bateria e navegação — tem de ser percebida de relance, sem distrair o condutor, e servir pessoas com necessidades diferentes.'),
            ('passos', 'O que fiz', ['Revisão de literatura sobre interfaces para veículos e acessibilidade digital.', 'Wireframes e protótipos de baixa e alta fidelidade.', 'Hierarquia visual centrada na informação crítica: velocidade, autonomia e navegação.', 'Avaliação das propostas com utilizadores e iteração do design.']),
            ('texto', 'Acessibilidade', '<p>Contraste elevado e números de grande dimensão para leitura rápida, estados que não dependem só da cor e o estudo de como a Inteligência Artificial pode adaptar a interface a cada condutor — tema do artigo que apresentei na IntelliSys 2025.</p>'),
            ('texto', 'Resultado', '<p>Um sistema de interfaces coerente entre o painel e a aplicação móvel, e a base de investigação para a publicação científica de que sou autor principal.</p>'),
        ],
        "behance": True,
    },
    {
        "slug": 'website-a-mover',
        "titulo": 'Website A-MoVeR',
        "etiqueta": 'Web · Multimédia',
        "resumo": 'Design e desenvolvimento do website do projeto A-MoVeR — a montra pública da investigação para parceiros, investigadores e público em geral.',
        "meta": [('Ano', '2024'), ('Papel', 'Design e desenvolvimento'), ('Contexto', 'Projeto A-MoVeR'), ('Ferramentas', 'Figma, Adobe Illustrator')],
        # Carrossel: (imagem em assets/img/, texto alternativo, legenda). EDITAR: trocar por imagens reais.
        "galeria": [
            ('projeto-2.svg', 'Website num browser, com título, imagem de destaque e cartões.', 'Página inicial'),
            ('projeto-4.svg', 'Logótipo com paleta de cores e tipografia.', 'Identidade aplicada ao site'),
            ('projeto-5.svg', 'Leitor de vídeo com botão de reprodução.', 'Conteúdos multimédia'),
        ],
        # Capítulos: ("texto", título, html) · ("frase", título, texto que acende com o scroll) · ("passos", título, [passos])
        "capitulos": [
            ('texto', 'Contexto', '<p>O website é o ponto central de comunicação do A-MoVeR, ao lado das redes sociais e das newsletters que também produzi.</p>'),
            ('frase', 'O desafio', 'Explicar um projeto técnico de forma clara a públicos muito diferentes e manter o site simples de atualizar à medida que a investigação avança.'),
            ('passos', 'O que fiz', ['Arquitetura de informação e estrutura das páginas.', 'Design da interface alinhado com a identidade visual do projeto.', 'Desenvolvimento e publicação do website.', 'Produção de conteúdos multimédia para as páginas.']),
            ('texto', 'Acessibilidade', '<p>Títulos com estrutura semântica, contraste adequado, texto alternativo nas imagens e navegação por teclado, seguindo as diretrizes WCAG.</p>'),
            ('texto', 'Resultado', '<p>Um website que reúne a informação do projeto num só lugar e que liga a comunicação nas redes sociais e nas newsletters.</p>'),
        ],
        "behance": True,
    },
    {
        "slug": 'redesign-turismo-mirandela',
        "titulo": 'Redesign Turismo Mirandela',
        "etiqueta": 'UI/UX · Web',
        "resumo": 'Redesign do website institucional de turismo de Mirandela, com foco na experiência de quem planeia uma visita ao concelho.',
        "meta": [('Ano', '2023'), ('Papel', 'Estágio curricular · UI/UX'), ('Contexto', 'Câmara Municipal de Mirandela'), ('Ferramentas', 'Figma, Adobe XD, Adobe Illustrator')],
        # Carrossel: (imagem em assets/img/, texto alternativo, legenda). EDITAR: trocar por imagens reais.
        "galeria": [
            ('projeto-3.svg', 'Website de turismo em computador e telemóvel, com paisagem verde.', 'Computador e telemóvel'),
            ('projeto-2.svg', 'Website num browser, com título, imagem de destaque e cartões.', 'Estrutura das páginas'),
        ],
        # Capítulos: ("texto", título, html) · ("frase", título, texto que acende com o scroll) · ("passos", título, [passos])
        "capitulos": [
            ('texto', 'Contexto', '<p>Durante o estágio curricular na Câmara Municipal de Mirandela (maio a junho de 2023), trabalhei no website de turismo do município e na sua presença digital.</p>'),
            ('frase', 'O desafio', 'Tornar mais fácil encontrar o que ver, fazer e visitar no concelho — tanto no computador como no telemóvel.'),
            ('passos', 'O que fiz', ['Análise do website existente e dos seus problemas de usabilidade.', 'Reorganização da arquitetura de informação.', 'Protótipos para computador e telemóvel.', 'Conteúdos para a presença digital e materiais gráficos promocionais.']),
            ('texto', 'Acessibilidade', '<p>Design responsivo, hierarquia clara, contraste suficiente e áreas de toque confortáveis no telemóvel.</p>'),
            ('texto', 'Resultado', '<p>Uma proposta de redesign centrada no visitante, acompanhada de conteúdos digitais e materiais para a promoção turística do concelho.</p>'),
        ],
        "behance": True,
    },
    {
        "slug": 'identidade-visual-a-mover',
        "titulo": 'Identidade Visual A-MoVeR',
        "etiqueta": 'Branding',
        "resumo": 'Apoio à identidade visual do A-MoVeR e adaptação a todos os suportes onde o projeto comunica.',
        "meta": [('Ano', '2024'), ('Papel', 'Design gráfico e branding'), ('Contexto', 'Projeto A-MoVeR'), ('Ferramentas', 'Adobe Illustrator, Figma')],
        # Carrossel: (imagem em assets/img/, texto alternativo, legenda). EDITAR: trocar por imagens reais.
        "galeria": [
            ('projeto-4.svg', 'Logótipo com paleta de cores e tipografia.', 'Logótipo e paleta'),
            ('projeto-2.svg', 'Website num browser com a identidade aplicada.', 'Aplicação no website'),
            ('projeto-5.svg', 'Leitor de vídeo com a identidade aplicada.', 'Aplicação nos vídeos'),
        ],
        # Capítulos: ("texto", título, html) · ("frase", título, texto que acende com o scroll) · ("passos", título, [passos])
        "capitulos": [
            ('texto', 'Contexto', '<p>Um projeto de investigação comunica em muitos sítios ao mesmo tempo: website, redes sociais, newsletters, vídeos e apresentações.</p>'),
            ('frase', 'O desafio', 'Manter a identidade reconhecível e coerente em formatos, tamanhos e fundos muito diferentes.'),
            ('passos', 'O que fiz', ['Adaptação do logótipo e da paleta de cores a diferentes formatos.', 'Modelos para publicações nas redes sociais e para newsletters.', 'Aplicação da identidade no website e nos vídeos do projeto.']),
            ('texto', 'Acessibilidade', '<p>Combinações de cor com contraste suficiente para texto e versões do logótipo para fundos claros e escuros.</p>'),
            ('texto', 'Resultado', '<p>Uma comunicação consistente em todos os canais do A-MoVeR.</p>'),
        ],
        "behance": True,
    },
    {
        "slug": 'videos-promocionais',
        "titulo": 'Vídeos promocionais',
        "etiqueta": 'Vídeo · Comunicação',
        "resumo": 'Vídeos para dar a conhecer o A-MoVeR nas redes sociais — investigação explicada em poucos segundos.',
        "meta": [('Ano', '2024–25'), ('Papel', 'Produção e edição de vídeo'), ('Contexto', 'Projeto A-MoVeR · redes sociais'), ('Ferramentas', 'Edição de vídeo, Adobe Illustrator')],
        # Carrossel: (imagem em assets/img/, texto alternativo, legenda). EDITAR: trocar por imagens reais.
        "galeria": [
            ('projeto-5.svg', 'Leitor de vídeo com botão de reprodução e linha do tempo.', 'Vídeo promocional'),
            ('projeto-4.svg', 'Logótipo e paleta usados nos grafismos.', 'Grafismos com a identidade'),
        ],
        # Capítulos: ("texto", título, html) · ("frase", título, texto que acende com o scroll) · ("passos", título, [passos])
        "capitulos": [
            ('texto', 'Contexto', '<p>As redes sociais foram um dos principais canais de comunicação do A-MoVeR, e o vídeo o formato com mais alcance.</p>'),
            ('frase', 'O desafio', 'Explicar investigação em poucos segundos, num feed onde a maioria das pessoas vê os vídeos sem som.'),
            ('passos', 'O que fiz', ['Planeamento e guião de cada vídeo.', 'Captação e edição.', 'Grafismos animados com a identidade visual do projeto.', 'Adaptação a formatos horizontais, verticais e quadrados.']),
            ('texto', 'Acessibilidade', '<p>Mensagem apoiada em texto no ecrã, para ser percebida sem som, com contraste suficiente e sem flashes rápidos.</p>'),
            ('texto', 'Resultado', '<p>Uma série de vídeos que acompanhou o projeto nas redes sociais ao longo de 2024 e 2025.</p>'),
        ],
        "behance": True,
    },
    {
        "slug": 'ia-acessibilidade-digital',
        "titulo": 'IA e acessibilidade digital',
        "etiqueta": 'Investigação · Acessibilidade',
        "resumo": 'Artigo científico sobre o uso de Inteligência Artificial para personalizar interfaces de motociclos e garantir a acessibilidade digital.',
        "meta": [('Ano', '2025'), ('Papel', 'Autor principal'), ('Publicação', 'Intelligent Systems Conference (IntelliSys) 2025'), ('Autores', 'João Mendo, Joana Oliveira, Tiago Pinto, Tânia Rocha')],
        # Carrossel: (imagem em assets/img/, texto alternativo, legenda). EDITAR: trocar por imagens reais.
        "galeria": [
            ('projeto-6.svg', 'Artigo científico com gráfico e o símbolo internacional de acessibilidade.', 'O artigo'),
            ('projeto-1.svg', 'Painel digital de mota com velocímetro e indicadores.', 'Interfaces de motociclos'),
        ],
        # Capítulos: ("texto", título, html) · ("frase", título, texto que acende com o scroll) · ("passos", título, [passos])
        "capitulos": [
            ('texto', 'O artigo', '<p lang="en"><em>New Solution to Old Problems: Leveraging AI to Customize Motorcycle User Interfaces and Guarantee Digital Accessibility</em></p>'),
            ('texto', 'Contexto', '<p>O artigo nasce do trabalho de design de interfaces no projeto A-MoVeR, onde a acessibilidade foi uma preocupação desde o início.</p>'),
            ('frase', 'A pergunta', 'As interfaces dos veículos são, em geral, iguais para todos. Como pode a Inteligência Artificial ajudar a adaptá-las a cada condutor, para que ninguém fique de fora?'),
            ('texto', 'Contribuição', '<p>O artigo explora a personalização de interfaces de motociclos com Inteligência Artificial como forma de responder a necessidades de acessibilidade digital que as abordagens tradicionais não resolvem.</p>'),
        ],
        "behance": False,
    },
]

BEHANCE = "https://www.behance.net/joomendo"


# ---------------------------------------------------------------------------
# Partes copiadas do index.html
# ---------------------------------------------------------------------------
def entre(inicio, fim, texto=INDEX, incluir_fim=True):
    i = texto.index(inicio)
    j = texto.index(fim, i) + (len(fim) if incluir_fim else 0)
    return texto[i:j]


versao = re.search(r"style\.css\?v=(\d+)", INDEX).group(1)
script_cabeca = entre("  <script>\n    document.documentElement.classList.add('js');", "  </script>\n")
# sem animação de entrada nas páginas de projeto
script_cabeca = re.sub(r"    // Animação de entrada.*?\} catch \(e\) \{\}\n", "", script_cabeca, count=1, flags=re.S)
sprite = entre('  <!-- Logótipo "jm"', "  </svg>\n")
cabecalho = entre('  <header class="site-header" id="topo">', "  </header>\n")
cabecalho = cabecalho.replace('href="#topo"', 'href="../"')
cabecalho = re.sub(r'href="#(projetos|sobre|percurso|servicos|contacto)"', r'href="../#\1"', cabecalho)
painel = entre("  <!-- Botão flutuante de acessibilidade", "</dialog>\n")
rodape = entre('  <footer class="site-footer">', "  </footer>\n")


def esc(t):
    return html.escape(t, quote=True)


def ident(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower().translate(str.maketrans("áàâãéêíóôõúç", "aaaaeeiooouc"))).strip("-")


def capitulo(n, tipo, titulo, conteudo):
    cid = "c-" + ident(titulo)
    if tipo == "frase":
        corpo = f'<p class="chapter-statement" data-scrub>{esc(conteudo)}</p>'
    elif tipo == "passos":
        itens = "\n".join(
            f'            <li class="step spot reveal"><span class="step-n" aria-hidden="true">{k:02d}</span><p>{esc(t)}</p></li>'
            for k, t in enumerate(conteudo, 1))
        corpo = f'<ol class="steps">\n{itens}\n          </ol>'
    else:
        corpo = f'<div class="chapter-text reveal">{conteudo}</div>'
    return f"""        <section class="chapter chapter-{tipo}" id="{cid}" aria-labelledby="{cid}-t">
          <p class="chapter-num" aria-hidden="true">{n:02d}</p>
          <h2 class="chapter-title reveal" id="{cid}-t">{esc(titulo)}</h2>
          {corpo}
        </section>"""


def galeria(p):
    g = p["galeria"]
    total = len(g)
    slides = "\n".join(
        f"""          <div class="gallery-slide" role="group" aria-roledescription="diapositivo" aria-label="{k} de {total}: {esc(leg)}">
            <figure><img src="../assets/img/{img}" width="800" height="1000" alt="{esc(alt)}"{' loading="lazy"' if k > 1 else ''}><figcaption>{esc(leg)}</figcaption></figure>
          </div>""" for k, (img, alt, leg) in enumerate(g, 1))
    thumbs = "\n".join(
        f'            <button type="button" class="gallery-thumb" data-go="{k - 1}" aria-label="Mostrar imagem {k}: {esc(leg)}"'
        + (' aria-current="true"' if k == 1 else '')
        + f'><img src="../assets/img/{img}" alt="" width="80" height="100" loading="lazy"></button>'
        for k, (img, alt, leg) in enumerate(g, 1))
    return f"""      <section class="gallery container" aria-roledescription="carrossel" aria-label="Imagens do projeto">
        <div class="gallery-viewport">
          <div class="gallery-track" id="gallery-track" tabindex="0" role="group" aria-label="Imagens: deslize ou use as setas do teclado">
{slides}
          </div>
          <span class="gallery-cursor" aria-hidden="true">Arrastar</span>
        </div>
        <div class="gallery-bar">
          <button type="button" class="gallery-btn gallery-prev" aria-controls="gallery-track" aria-label="Imagem anterior"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button>
          <p class="gallery-count"><span class="gallery-now">01</span> <span aria-hidden="true">/</span><span class="sr-only">de</span> {total:02d}</p>
          <span class="gallery-progress" aria-hidden="true"><span style="--p:{1 / total:.4f}"></span></span>
          <div class="gallery-thumbs">
{thumbs}
          </div>
          <button type="button" class="gallery-btn gallery-next" aria-controls="gallery-track" aria-label="Imagem seguinte"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button>
          <p class="sr-only" aria-live="polite" id="gallery-status"></p>
        </div>
      </section>"""


def pagina(i, p):
    ant = PROJETOS[i - 1]
    seg = PROJETOS[(i + 1) % len(PROJETOS)]
    meta = "\n".join(f'          <div class="case-chip glass reveal"><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in p["meta"])
    caps = p["capitulos"]
    indice = "\n".join(
        f'            <li><a href="#c-{ident(t)}"><span class="story-n" aria-hidden="true">{n:02d}</span> {esc(t)}</a></li>'
        for n, (tipo, t, c) in enumerate(caps, 1))
    capitulos = "\n".join(capitulo(n, *c) for n, c in enumerate(caps, 1))
    behance = ""
    if p["behance"]:
        behance = (f'\n        <p class="case-ext reveal"><a class="btn btn-ghost" href="{BEHANCE}" target="_blank" rel="noopener">'
                   'Ver mais imagens no Behance <span aria-hidden="true">↗</span><span class="sr-only"> (abre num novo separador)</span></a></p>')
    titulo = f'{p["titulo"]} — João Mendo'
    return f"""<!doctype html>
<html lang="pt-PT">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(titulo)}</title>
  <meta name="description" content="{esc(p["resumo"])}">
  <meta name="author" content="João Mendo">
  <meta name="theme-color" content="#121110" media="(prefers-color-scheme: dark)">
  <meta name="theme-color" content="#f5f1eb" media="(prefers-color-scheme: light)">
  <meta name="color-scheme" content="dark light">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{esc(titulo)}">
  <meta property="og:description" content="{esc(p["resumo"])}">
  <meta property="og:url" content="https://joaomendo639.github.io/portfolio/projetos/{p["slug"]}.html">
  <meta property="og:locale" content="pt_PT">
  <!-- Página gerada por tools/gerar-projetos.py — editar o texto lá, não aqui -->

  <link rel="icon" href="../assets/img/favicon.svg?v={versao}" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Manrope:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/style.css?v={versao}">

{script_cabeca}</head>
<body class="page-case">
{sprite}
  <a class="skip-link" href="#conteudo">Saltar para o conteúdo</a>
  <div class="scroll-progress" aria-hidden="true"><span></span></div>
  <div class="cursor-glow" aria-hidden="true"></div>

{cabecalho}
  <main id="conteudo" tabindex="-1">
    <article class="case">
      <header class="case-hero container">
        <div class="hero-glow" aria-hidden="true"></div>
        <nav aria-label="Caminho">
          <a class="case-back" href="../#projetos"><span aria-hidden="true">←</span> Todos os projetos</a>
        </nav>
        <p class="eyebrow">{esc(p["etiqueta"])}</p>
        <h1 class="case-title" data-split>{esc(p["titulo"])}</h1>
        <p class="case-lead reveal">{esc(p["resumo"])}</p>
        <dl class="case-chips">
{meta}
        </dl>
      </header>

{galeria(p)}

      <div class="case-story container">
        <nav class="story-index" aria-label="Capítulos deste projeto">
          <ol>
{indice}
          </ol>
          <span class="story-line" aria-hidden="true"><span></span></span>
        </nav>
        <div class="story-chapters">
{capitulos}{behance}
        </div>
      </div>

      <nav class="case-next container" aria-label="Outros projetos">
        <a class="next-card spot" href="{seg["slug"]}.html">
          <span class="next-text">
            <span class="next-label">Próximo projeto <span aria-hidden="true">→</span></span>
            <span class="next-title">{esc(seg["titulo"])}</span>
            <span class="next-tag">{esc(seg["etiqueta"])}</span>
          </span>
          <img class="next-img" src="../assets/img/{seg["galeria"][0][0]}" alt="" width="800" height="1000" loading="lazy">
        </a>
        <a class="prev-link" href="{ant["slug"]}.html"><span aria-hidden="true">←</span> Anterior: {esc(ant["titulo"])}</a>
      </nav>

      <section class="case-cta container" aria-labelledby="cta-title">
        <h2 id="cta-title" class="case-cta-title">Tem um projeto <em>em mente?</em></h2>
        <a class="btn btn-primary magnetic" href="../#contacto">Falar comigo <span aria-hidden="true">→</span></a>
      </section>
    </article>
  </main>

{rodape}
{painel}
  <script src="../assets/js/main.js?v={versao}" defer></script>
  <script src="../assets/js/projeto.js?v={versao}" defer></script>
</body>
</html>
"""


SAIDA.mkdir(exist_ok=True)
for i, p in enumerate(PROJETOS):
    (SAIDA / f'{p["slug"]}.html').write_text(pagina(i, p), encoding="utf-8", newline="\n")
    print("gerado:", f'projetos/{p["slug"]}.html')
