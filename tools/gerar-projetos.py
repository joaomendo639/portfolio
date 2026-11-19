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
        "slug": "interfaces-a-mover",
        "titulo": "Interfaces A-MoVeR",
        "etiqueta": "UI/UX · Investigação",
        "imagem": "projeto-1.svg",
        "alt": "Ilustração de um painel digital de mota com velocímetro e indicadores.",
        "resumo": "Interfaces para mobilidade elétrica — o painel de instrumentos de uma mota e a aplicação móvel que o acompanha — desenhadas para serem lidas de relance, com segurança e por todos.",
        "meta": [("Ano", "2024–25"), ("Papel", "UI/UX Designer · Bolseiro de Investigação"), ("Contexto", "Projeto A-MoVeR, Vila Real"), ("Ferramentas", "Figma, Adobe Illustrator, Adobe XD")],
        "seccoes": [
            ("Contexto", "<p>O A-MoVeR é um projeto de investigação em mobilidade elétrica. Entre junho de 2024 e junho de 2025, como Bolseiro de Investigação, fui responsável pelo design de interfaces das soluções digitais do projeto.</p>"),
            ("O desafio", "<p>Um painel de mota é lido em segundos, em andamento, ao sol, à chuva ou à noite. A informação essencial — velocidade, bateria e navegação — tem de ser percebida de relance, sem distrair o condutor, e servir pessoas com necessidades diferentes.</p>"),
            ("O que fiz", "<ul><li>Revisão de literatura sobre interfaces para veículos e acessibilidade digital.</li><li>Wireframes e protótipos de baixa e alta fidelidade.</li><li>Hierarquia visual centrada na informação crítica: velocidade, autonomia e navegação.</li><li>Avaliação das propostas com utilizadores e iteração do design.</li></ul>"),
            ("Acessibilidade", "<p>Contraste elevado e números de grande dimensão para leitura rápida, estados que não dependem só da cor e o estudo de como a Inteligência Artificial pode adaptar a interface a cada condutor — tema do artigo que apresentei na IntelliSys 2025.</p>"),
            ("Resultado", "<p>Um sistema de interfaces coerente entre o painel e a aplicação móvel, e a base de investigação para a publicação científica de que sou autor principal.</p>"),
        ],
        "behance": True,
    },
    {
        "slug": "website-a-mover",
        "titulo": "Website A-MoVeR",
        "etiqueta": "Web · Multimédia",
        "imagem": "projeto-2.svg",
        "alt": "Ilustração de um website num browser, com título, imagem de destaque e cartões.",
        "resumo": "Design e desenvolvimento do website do projeto A-MoVeR — a montra pública da investigação para parceiros, investigadores e público em geral.",
        "meta": [("Ano", "2024"), ("Papel", "Design e desenvolvimento"), ("Contexto", "Projeto A-MoVeR"), ("Ferramentas", "Figma, Adobe Illustrator")],
        "seccoes": [
            ("Contexto", "<p>O website é o ponto central de comunicação do A-MoVeR, ao lado das redes sociais e das newsletters que também produzi.</p>"),
            ("O desafio", "<p>Explicar um projeto técnico de forma clara a públicos muito diferentes e manter o site simples de atualizar à medida que a investigação avança.</p>"),
            ("O que fiz", "<ul><li>Arquitetura de informação e estrutura das páginas.</li><li>Design da interface alinhado com a identidade visual do projeto.</li><li>Desenvolvimento e publicação do website.</li><li>Produção de conteúdos multimédia para as páginas.</li></ul>"),
            ("Acessibilidade", "<p>Títulos com estrutura semântica, contraste adequado, texto alternativo nas imagens e navegação por teclado, seguindo as diretrizes WCAG.</p>"),
            ("Resultado", "<p>Um website que reúne a informação do projeto num só lugar e que liga a comunicação nas redes sociais e nas newsletters.</p>"),
        ],
        "behance": True,
    },
    {
        "slug": "redesign-turismo-mirandela",
        "titulo": "Redesign Turismo Mirandela",
        "etiqueta": "UI/UX · Web",
        "imagem": "projeto-3.svg",
        "alt": "Ilustração de um website de turismo em computador e telemóvel, com paisagem verde.",
        "resumo": "Redesign do website institucional de turismo de Mirandela, com foco na experiência de quem planeia uma visita ao concelho.",
        "meta": [("Ano", "2023"), ("Papel", "Estágio curricular · UI/UX"), ("Contexto", "Câmara Municipal de Mirandela"), ("Ferramentas", "Figma, Adobe XD, Adobe Illustrator")],
        "seccoes": [
            ("Contexto", "<p>Durante o estágio curricular na Câmara Municipal de Mirandela (maio a junho de 2023), trabalhei no website de turismo do município e na sua presença digital.</p>"),
            ("O desafio", "<p>Tornar mais fácil encontrar o que ver, fazer e visitar no concelho — tanto no computador como no telemóvel.</p>"),
            ("O que fiz", "<ul><li>Análise do website existente e dos seus problemas de usabilidade.</li><li>Reorganização da arquitetura de informação.</li><li>Protótipos para computador e telemóvel.</li><li>Conteúdos para a presença digital e materiais gráficos promocionais.</li></ul>"),
            ("Acessibilidade", "<p>Design responsivo, hierarquia clara, contraste suficiente e áreas de toque confortáveis no telemóvel.</p>"),
            ("Resultado", "<p>Uma proposta de redesign centrada no visitante, acompanhada de conteúdos digitais e materiais para a promoção turística do concelho.</p>"),
        ],
        "behance": True,
    },
    {
        "slug": "identidade-visual-a-mover",
        "titulo": "Identidade Visual A-MoVeR",
        "etiqueta": "Branding",
        "imagem": "projeto-4.svg",
        "alt": "Ilustração de um logótipo com paleta de cores e tipografia.",
        "resumo": "Apoio à identidade visual do A-MoVeR e adaptação a todos os suportes onde o projeto comunica.",
        "meta": [("Ano", "2024"), ("Papel", "Design gráfico e branding"), ("Contexto", "Projeto A-MoVeR"), ("Ferramentas", "Adobe Illustrator, Figma")],
        "seccoes": [
            ("Contexto", "<p>Um projeto de investigação comunica em muitos sítios ao mesmo tempo: website, redes sociais, newsletters, vídeos e apresentações.</p>"),
            ("O desafio", "<p>Manter a identidade reconhecível e coerente em formatos, tamanhos e fundos muito diferentes.</p>"),
            ("O que fiz", "<ul><li>Adaptação do logótipo e da paleta de cores a diferentes formatos.</li><li>Modelos para publicações nas redes sociais e para newsletters.</li><li>Aplicação da identidade no website e nos vídeos do projeto.</li></ul>"),
            ("Acessibilidade", "<p>Combinações de cor com contraste suficiente para texto e versões do logótipo para fundos claros e escuros.</p>"),
            ("Resultado", "<p>Uma comunicação consistente em todos os canais do A-MoVeR.</p>"),
        ],
        "behance": True,
    },
    {
        "slug": "videos-promocionais",
        "titulo": "Vídeos promocionais",
        "etiqueta": "Vídeo · Comunicação",
        "imagem": "projeto-5.svg",
        "alt": "Ilustração de um leitor de vídeo com botão de reprodução e linha do tempo.",
        "resumo": "Vídeos para dar a conhecer o A-MoVeR nas redes sociais — investigação explicada em poucos segundos.",
        "meta": [("Ano", "2024–25"), ("Papel", "Produção e edição de vídeo"), ("Contexto", "Projeto A-MoVeR · redes sociais"), ("Ferramentas", "Edição de vídeo, Adobe Illustrator")],
        "seccoes": [
            ("Contexto", "<p>As redes sociais foram um dos principais canais de comunicação do A-MoVeR, e o vídeo o formato com mais alcance.</p>"),
            ("O desafio", "<p>Explicar investigação em poucos segundos, num feed onde a maioria das pessoas vê os vídeos sem som.</p>"),
            ("O que fiz", "<ul><li>Planeamento e guião de cada vídeo.</li><li>Captação e edição.</li><li>Grafismos animados com a identidade visual do projeto.</li><li>Adaptação a formatos horizontais, verticais e quadrados.</li></ul>"),
            ("Acessibilidade", "<p>Mensagem apoiada em texto no ecrã, para ser percebida sem som, com contraste suficiente e sem flashes rápidos.</p>"),
            ("Resultado", "<p>Uma série de vídeos que acompanhou o projeto nas redes sociais ao longo de 2024 e 2025.</p>"),
        ],
        "behance": True,
    },
    {
        "slug": "ia-acessibilidade-digital",
        "titulo": "IA e acessibilidade digital",
        "etiqueta": "Investigação · Acessibilidade",
        "imagem": "projeto-6.svg",
        "alt": "Ilustração de um artigo científico com gráfico e o símbolo internacional de acessibilidade.",
        "resumo": "Artigo científico sobre o uso de Inteligência Artificial para personalizar interfaces de motociclos e garantir a acessibilidade digital.",
        "meta": [("Ano", "2025"), ("Papel", "Autor principal"), ("Publicação", "Intelligent Systems Conference (IntelliSys) 2025"), ("Autores", "João Mendo, Joana Oliveira, Tiago Pinto, Tânia Rocha")],
        "seccoes": [
            ("O artigo", '<p lang="en"><em>New Solution to Old Problems: Leveraging AI to Customize Motorcycle User Interfaces and Guarantee Digital Accessibility</em></p>'),
            ("Contexto", "<p>O artigo nasce do trabalho de design de interfaces no projeto A-MoVeR, onde a acessibilidade foi uma preocupação desde o início.</p>"),
            ("A pergunta", "<p>As interfaces dos veículos são, em geral, iguais para todos. Como pode a Inteligência Artificial ajudar a adaptá-las a cada condutor, para que ninguém fique de fora?</p>"),
            ("Contribuição", "<p>O artigo explora a personalização de interfaces de motociclos com Inteligência Artificial como forma de responder a necessidades de acessibilidade digital que as abordagens tradicionais não resolvem.</p>"),
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


def pagina(i, p):
    ant = PROJETOS[i - 1]
    seg = PROJETOS[(i + 1) % len(PROJETOS)]
    meta = "\n".join(f'            <div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in p["meta"])
    seccoes = "\n".join(
        f'''        <section class="case-section reveal" aria-labelledby="s{n}">
          <h2 id="s{n}" class="case-h">{esc(t)}</h2>
          <div class="case-text">{c}</div>
        </section>''' for n, (t, c) in enumerate(p["seccoes"], 1))
    behance = (f'''
        <p class="case-ext"><a class="btn btn-ghost" href="{BEHANCE}" target="_blank" rel="noopener">Ver mais imagens no Behance <span aria-hidden="true">↗</span><span class="sr-only"> (abre num novo separador)</span></a></p>''' if p["behance"] else "")
    titulo = f'{p["titulo"]} — João Mendo'
    return f'''<!doctype html>
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

{cabecalho}
  <main id="conteudo" tabindex="-1">
    <article class="case">
      <header class="case-hero container">
        <nav aria-label="Caminho">
          <a class="case-back" href="../#projetos"><span aria-hidden="true">←</span> Todos os projetos</a>
        </nav>
        <p class="eyebrow">{esc(p["etiqueta"])}</p>
        <h1 class="case-title">{esc(p["titulo"])}</h1>
        <p class="case-lead">{esc(p["resumo"])}</p>
        <dl class="case-meta">
{meta}
        </dl>
      </header>

      <figure class="case-cover container">
        <img src="../assets/img/{p["imagem"]}" width="800" height="1000" alt="{esc(p["alt"])}">
      </figure>

      <div class="case-body container">
{seccoes}{behance}
      </div>

      <nav class="case-nav container" aria-label="Outros projetos">
        <a class="case-nav-link" href="{ant["slug"]}.html"><span class="case-nav-label"><span aria-hidden="true">←</span> Projeto anterior</span><span class="case-nav-title">{esc(ant["titulo"])}</span></a>
        <a class="case-nav-link case-nav-next" href="{seg["slug"]}.html"><span class="case-nav-label">Projeto seguinte <span aria-hidden="true">→</span></span><span class="case-nav-title">{esc(seg["titulo"])}</span></a>
      </nav>

      <section class="case-cta container" aria-labelledby="cta-title">
        <h2 id="cta-title" class="case-cta-title">Tem um projeto <em>em mente?</em></h2>
        <a class="btn btn-primary" href="../#contacto">Falar comigo <span aria-hidden="true">→</span></a>
      </section>
    </article>
  </main>

{rodape}
{painel}
  <script src="../assets/js/main.js?v={versao}" defer></script>
</body>
</html>
'''


SAIDA.mkdir(exist_ok=True)
for i, p in enumerate(PROJETOS):
    (SAIDA / f'{p["slug"]}.html').write_text(pagina(i, p), encoding="utf-8", newline="\n")
    print("gerado:", f'projetos/{p["slug"]}.html')
