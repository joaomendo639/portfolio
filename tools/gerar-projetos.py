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
            ('projetos/interfaces-a-mover/perfil.jpg', 'Fulgora, mota elétrica da AJP Motos, de perfil, num cavalete, no exterior da fábrica da AJP.', 'Fulgora · visita à fábrica da AJP'),
            ('projetos/interfaces-a-mover/frente-tres-quartos.jpg', 'Fulgora vista de frente, a três quartos, com o painel digital no guiador.', 'Três quartos'),
            ('projetos/interfaces-a-mover/frente.jpg', 'Mota vista de frente, com o farol redondo e os espelhos.', 'Frente'),
            ('projetos/interfaces-a-mover/detalhe-suspensao.jpg', 'Pormenor da suspensão traseira amarela e do motor na roda.', 'Suspensão e motor'),
            ('projetos/interfaces-a-mover/traseira-tres-quartos.jpg', 'Traseira da mota a três quartos, com a matrícula desfocada.', 'Traseira'),
            ('projetos/interfaces-a-mover/traseira.jpg', 'Mota vista de trás, com a matrícula desfocada.', 'Vista traseira'),
            ('projetos/interfaces-a-mover/fabrica.jpg', 'Linha de montagem da fábrica da AJP, com motas e um técnico a trabalhar.', 'Linha de montagem · 22 nov 2024'),
            ('projeto-1.svg', 'Ilustração do painel digital de mota com velocímetro, bateria e indicadores.', 'Conceito do painel'),
        ],
        # Capítulos: ("texto", título, html com <mark> nas palavras-chave) · ("frase", título, texto que acende com o scroll) · ("passos", título, [passos])
        "capitulos": [
            ('texto', 'Contexto', '<p>O A-MoVeR é um projeto de investigação em <mark>mobilidade elétrica</mark>, que inclui a <mark>Fulgora</mark>, o primeiro protótipo de motociclo elétrico desenvolvido pela AJP Motos. As fotografias foram feitas numa <mark>visita à fábrica da AJP</mark>, a 22 de novembro de 2024. <a href="https://amover.utad.pt/fulgora/" target="_blank" rel="noopener">Saber mais sobre a Fulgora<span class="sr-only"> (abre num novo separador)</span></a>. Entre junho de 2024 e junho de 2025, como Bolseiro de Investigação, fui responsável pelo <mark>design de interfaces das soluções digitais</mark> do projeto.</p>'),
            ('frase', 'O desafio', 'Um painel de mota é lido em segundos, em andamento, ao sol, à chuva ou à noite. A informação essencial — velocidade, bateria e navegação — tem de ser percebida de relance, sem distrair o condutor, e servir pessoas com necessidades diferentes.'),
            ('passos', 'O que fiz', ['Revisão de literatura sobre interfaces para veículos e acessibilidade digital.', 'Wireframes e protótipos de baixa e alta fidelidade.', 'Hierarquia visual centrada na informação crítica: velocidade, autonomia e navegação.', 'Avaliação das propostas com utilizadores e iteração do design.']),
            ('texto', 'Acessibilidade', '<p><mark>Contraste elevado</mark> e números de grande dimensão para leitura rápida, <mark>estados que não dependem só da cor</mark> e o estudo de como a Inteligência Artificial pode adaptar a interface a cada condutor — tema do artigo que apresentei na IntelliSys 2025.</p>'),
            ('texto', 'Resultado', '<p>Um <mark>sistema de interfaces coerente</mark> entre o painel e a aplicação móvel, e a base de investigação para a publicação científica de que sou <mark>autor principal</mark>.</p>'),
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
        # Capítulos: ("texto", título, html com <mark> nas palavras-chave) · ("frase", título, texto que acende com o scroll) · ("passos", título, [passos])
        "capitulos": [
            ('texto', 'Contexto', '<p>O website é o <mark>ponto central de comunicação</mark> do A-MoVeR, ao lado das redes sociais e das newsletters que também produzi.</p>'),
            ('frase', 'O desafio', 'Explicar um projeto técnico de forma clara a públicos muito diferentes e manter o site simples de atualizar à medida que a investigação avança.'),
            ('passos', 'O que fiz', ['Arquitetura de informação e estrutura das páginas.', 'Design da interface alinhado com a identidade visual do projeto.', 'Desenvolvimento e publicação do website.', 'Produção de conteúdos multimédia para as páginas.']),
            ('texto', 'Acessibilidade', '<p>Títulos com <mark>estrutura semântica</mark>, contraste adequado, texto alternativo nas imagens e <mark>navegação por teclado</mark>, seguindo as diretrizes WCAG.</p>'),
            ('texto', 'Resultado', '<p>Um website que reúne a informação do projeto <mark>num só lugar</mark> e que liga a comunicação nas redes sociais e nas newsletters.</p>'),
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
        # Capítulos: ("texto", título, html com <mark> nas palavras-chave) · ("frase", título, texto que acende com o scroll) · ("passos", título, [passos])
        "capitulos": [
            ('texto', 'Contexto', '<p>Durante o <mark>estágio curricular</mark> na Câmara Municipal de Mirandela (maio a junho de 2023), trabalhei no <mark>website de turismo</mark> do município e na sua presença digital.</p>'),
            ('frase', 'O desafio', 'Tornar mais fácil encontrar o que ver, fazer e visitar no concelho — tanto no computador como no telemóvel.'),
            ('passos', 'O que fiz', ['Análise do website existente e dos seus problemas de usabilidade.', 'Reorganização da arquitetura de informação.', 'Protótipos para computador e telemóvel.', 'Conteúdos para a presença digital e materiais gráficos promocionais.']),
            ('texto', 'Acessibilidade', '<p><mark>Design responsivo</mark>, hierarquia clara, contraste suficiente e <mark>áreas de toque confortáveis</mark> no telemóvel.</p>'),
            ('texto', 'Resultado', '<p>Uma proposta de redesign <mark>centrada no visitante</mark>, acompanhada de conteúdos digitais e materiais para a promoção turística do concelho.</p>'),
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
        # Capítulos: ("texto", título, html com <mark> nas palavras-chave) · ("frase", título, texto que acende com o scroll) · ("passos", título, [passos])
        "capitulos": [
            ('texto', 'Contexto', '<p>Um projeto de investigação comunica <mark>em muitos sítios ao mesmo tempo</mark>: website, redes sociais, newsletters, vídeos e apresentações.</p>'),
            ('frase', 'O desafio', 'Manter a identidade reconhecível e coerente em formatos, tamanhos e fundos muito diferentes.'),
            ('passos', 'O que fiz', ['Adaptação do logótipo e da paleta de cores a diferentes formatos.', 'Modelos para publicações nas redes sociais e para newsletters.', 'Aplicação da identidade no website e nos vídeos do projeto.']),
            ('texto', 'Acessibilidade', '<p>Combinações de cor com <mark>contraste suficiente para texto</mark> e versões do logótipo para <mark>fundos claros e escuros</mark>.</p>'),
            ('texto', 'Resultado', '<p>Uma comunicação <mark>consistente em todos os canais</mark> do A-MoVeR.</p>'),
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
        # Capítulos: ("texto", título, html com <mark> nas palavras-chave) · ("frase", título, texto que acende com o scroll) · ("passos", título, [passos])
        "capitulos": [
            ('texto', 'Contexto', '<p>As redes sociais foram um dos principais canais de comunicação do A-MoVeR, e <mark>o vídeo o formato com mais alcance</mark>.</p>'),
            ('frase', 'O desafio', 'Explicar investigação em poucos segundos, num feed onde a maioria das pessoas vê os vídeos sem som.'),
            ('passos', 'O que fiz', ['Planeamento e guião de cada vídeo.', 'Captação e edição.', 'Grafismos animados com a identidade visual do projeto.', 'Adaptação a formatos horizontais, verticais e quadrados.']),
            ('texto', 'Acessibilidade', '<p>Mensagem apoiada em texto no ecrã, para ser <mark>percebida sem som</mark>, com contraste suficiente e sem flashes rápidos.</p>'),
            ('texto', 'Resultado', '<p>Uma série de vídeos que acompanhou o projeto nas redes sociais <mark>ao longo de 2024 e 2025</mark>.</p>'),
        ],
        "behance": True,
    },
    {
        "slug": 'primeira-comunhao',
        "titulo": 'Primeira Comunhão',
        "etiqueta": 'Fotografia · Reportagem',
        "resumo": 'Reportagem fotográfica de uma Primeira Comunhão: a alegria de um dia único, contada em retratos.',
        "meta": [('Ano', '2024'), ('Papel', 'Fotografia e vídeo'), ('Contexto', 'Cerimónia religiosa · reportagem de evento'), ('Equipamento', 'Canon EOS R50')],
        # Só imagens com autorização da família (menor de idade). Sem nome da criança. Dados do certificado desfocados.
        "galeria": [
            ('projetos/primeira-comunhao/retrato.jpg', 'Retrato de uma menina vestida de branco, a sorrir, com um fio dourado nas mãos.', 'Retrato'),
            ('projetos/primeira-comunhao/certificado.jpg', 'Menina a sorrir a mostrar o certificado da Primeira Comunhão em frente ao altar.', 'O certificado'),
        ],
        "capitulos": [
            ('texto', 'Contexto', '<p>Reportagem de uma cerimónia de <mark>Primeira Comunhão</mark>, em maio de 2024, em fotografia e vídeo.</p>'),
            ('frase', 'O desafio', 'Captar um dia que só acontece uma vez, sem interferir na cerimónia: luz de igreja, movimento constante e emoções que não se repetem.'),
            ('passos', 'O que fiz', ['Acompanhamento da cerimónia do início ao fim.', 'Fotografia e vídeo em simultâneo.', 'Seleção e edição das imagens.', 'Entrega do trabalho à família.']),
            ('texto', 'Privacidade', '<p>Por se tratar de crianças, só são publicadas imagens <mark>com autorização da família</mark>. O vídeo e as fotografias de grupo ficam reservados, e os dados pessoais visíveis foram desfocados.</p>'),
        ],
        "behance": False,
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
        # Capítulos: ("texto", título, html com <mark> nas palavras-chave) · ("frase", título, texto que acende com o scroll) · ("passos", título, [passos])
        "capitulos": [
            ('texto', 'O artigo', '<p lang="en"><em>New Solution to Old Problems: Leveraging AI to Customize Motorcycle User Interfaces and Guarantee Digital Accessibility</em></p>'),
            ('texto', 'Contexto', '<p>O artigo nasce do trabalho de design de interfaces no projeto A-MoVeR, onde <mark>a acessibilidade foi uma preocupação desde o início</mark>.</p>'),
            ('frase', 'A pergunta', 'As interfaces dos veículos são, em geral, iguais para todos. Como pode a Inteligência Artificial ajudar a adaptá-las a cada condutor, para que ninguém fique de fora?'),
            ('texto', 'Contribuição', '<p>O artigo explora a <mark>personalização de interfaces de motociclos</mark> com Inteligência Artificial como forma de responder a necessidades de acessibilidade digital que as abordagens tradicionais não resolvem.</p>'),
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


def foto(img):
    """Fotografias (jpg/webp/png) mostram-se inteiras no carrossel e com o rosto ao centro nos recortes."""
    return img.lower().endswith((".jpg", ".jpeg", ".webp", ".png"))


def ident(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower().translate(str.maketrans("áàâãéêíóôõúç", "aaaaeeiooouc"))).strip("-")


DEMO = """
          <div class="a11y-demo reveal">
            <p class="demo-label">Experimente</p>
            <div class="demo-toggles" role="group" aria-label="Simular preferências de acessibilidade na pré-visualização">
              <button type="button" class="demo-btn" aria-pressed="false" data-demo="contrast">Contraste elevado</button>
              <button type="button" class="demo-btn" aria-pressed="false" data-demo="large">Texto maior</button>
              <button type="button" class="demo-btn" aria-pressed="false" data-demo="mono">Ver sem cores</button>
              <button type="button" class="demo-btn" aria-pressed="false" data-demo="dark">Modo noite</button>
            </div>
            <div class="demo-card" role="group" aria-label="Pré-visualização de interface">
              <div class="demo-top"><span class="demo-title">{titulo}</span><span class="demo-chip demo-ok"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>Concluído</span></div>
              <p class="demo-metric">68<span>%</span></p>
              <p class="demo-sub">Progresso</p>
              <div class="demo-bar" role="progressbar" aria-label="Progresso" aria-valuenow="68" aria-valuemin="0" aria-valuemax="100"><span></span></div>
              <div class="demo-row"><span class="demo-chip demo-warn"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4l9 16H3zM12 10v4M12 17.5v.5"/></svg>Atenção</span><span class="demo-chip demo-err"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>Erro</span></div>
              <span class="demo-action">Continuar <span aria-hidden="true">→</span></span>
            </div>
            <p class="demo-note">Em todos os modos a informação continua lá: cada estado tem ícone e texto, não só cor.</p>
          </div>"""


def capitulo(p, n, tipo, titulo, conteudo):
    cid = "c-" + ident(titulo)
    img = p["galeria"][(n - 1) % len(p["galeria"])][0]
    extra = ""
    if tipo == "frase":
        corpo = f'<p class="chapter-statement" data-scrub>{esc(conteudo)}</p>'
    elif tipo == "passos":
        itens = "\n".join(
            f'            <li class="step spot reveal"><span class="step-n" aria-hidden="true">{k:02d}</span><p>{esc(t)}</p></li>'
            for k, t in enumerate(conteudo, 1))
        corpo = f'<ol class="steps">\n{itens}\n          </ol>'
    else:
        corpo = f'<div class="chapter-text reveal">{conteudo}</div>'
        if titulo in ("Acessibilidade", "Contribuição"):
            corpo += DEMO.replace("{titulo}", esc(p["titulo"]))
        if titulo == "Resultado":
            extra = " chapter-result"
    return f"""        <section class="chapter chapter-{tipo}{extra}" id="{cid}" aria-labelledby="{cid}-t" data-stage="{n - 1}">
          <p class="chapter-num" aria-hidden="true">{n:02d}</p>
          <figure class="chapter-figure" aria-hidden="true"><img{' class="is-photo"' if foto(img) else ''} src="../assets/img/{img}" alt="" width="800" height="1000" loading="lazy"></figure>
          <h2 class="chapter-title reveal" id="{cid}-t">{esc(titulo)}</h2>
          {corpo}
        </section>"""


def galeria(p):
    g = p["galeria"]
    total = len(g)
    slides = "\n".join(
        f"""          <div class="gallery-slide" role="group" aria-roledescription="diapositivo" aria-label="{k} de {total}: {esc(leg)}">
            <figure><img{' class="is-photo"' if foto(img) else ''} src="../assets/img/{img}" width="800" height="1000" alt="{esc(alt)}"{' loading="lazy"' if k > 1 else ''}><figcaption>{esc(leg)}</figcaption></figure>
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
          <span class="gallery-cursor" aria-hidden="true"></span>
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
    meta = "\n".join(f'          <li class="case-chip glass reveal"><span class="chip-k">{esc(k)}:</span> <span class="chip-v">{esc(v)}</span></li>' for k, v in p["meta"])
    caps = p["capitulos"]
    indice = "\n".join(
        f'            <li><a href="#c-{ident(t)}"><span class="story-n" aria-hidden="true">{n:02d}</span> {esc(t)}</a></li>'
        for n, (tipo, t, c) in enumerate(caps, 1))
    capitulos = "\n".join(capitulo(p, n, *c) for n, c in enumerate(caps, 1))
    palco = "\n".join(
        f'            <img class="stage-img{" is-on" if n == 1 else ""}{" is-photo" if foto(p["galeria"][(n - 1) % len(p["galeria"])][0]) else ""}" data-k="{n - 1}" data-cap="{esc(t)}" '
        f'src="../assets/img/{p["galeria"][(n - 1) % len(p["galeria"])][0]}" alt="" width="800" height="1000"'
        + (' loading="lazy"' if n > 1 else '') + '>'
        for n, (tipo, t, c) in enumerate(caps, 1))
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
        <ul class="case-chips" aria-label="Ficha do projeto">
{meta}
        </ul>
      </header>

{galeria(p)}

      <div class="case-story container">
        <div class="story-aside">
          <div class="story-stage" aria-hidden="true">
{palco}
            <span class="stage-num">01</span>
            <span class="stage-cap">{esc(caps[0][1])}</span>
          </div>
          <nav class="story-index" aria-label="Capítulos deste projeto">
            <ol>
{indice}
            </ol>
            <span class="story-line" aria-hidden="true"><span></span></span>
          </nav>
        </div>
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
          <img class="next-img{' is-photo' if foto(seg["galeria"][0][0]) else ''}" src="../assets/img/{seg["galeria"][0][0]}" alt="" width="800" height="1000" loading="lazy">
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
