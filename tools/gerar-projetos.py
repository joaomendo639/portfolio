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
    # -----------------------------------------------------------------------
    # PÁGINAS DE EXEMPLO — uma por tipo de template ("demo": True).
    # Para inserir um trabalho real: copiar o bloco do tipo certo, mudar slug/textos/imagens,
    # retirar "demo" e acrescentar o cartão em index.html (<ul class="projects">).
    # Tipos: uiux · fotografia · design · web · video · investigacao
    # -----------------------------------------------------------------------
    {
        "slug": 'exemplo-fotografia', "demo": True,
        "tipo": "fotografia",
        "titulo": 'Fotografia',
        "etiqueta": 'Template · Fotografia',
        "resumo": 'Exemplo do template de fotografia: galeria em mosaico, ecrã inteiro e os parâmetros de cada fotografia.',
        "meta": [('Ano', 'AAAA'), ('Papel', 'Fotografia'), ('Contexto', 'Cliente ou evento'), ('Equipamento', 'Câmara e objetivas')],
        # Fotografias: os parâmetros (abertura, velocidade, ISO, focal) vêm de tools/exif-fotos.json
        "galeria": [
            ('exemplos/foto-1.jpg', 'Paisagem de exemplo com colinas ao entardecer.', 'Fotografia 1'),
            ('exemplos/foto-2.jpg', 'Paisagem de exemplo em tons de azul.', 'Fotografia 2'),
            ('exemplos/foto-3.jpg', 'Paisagem de exemplo em tons quentes.', 'Fotografia 3'),
            ('exemplos/foto-4.jpg', 'Paisagem de exemplo em tons verdes.', 'Fotografia 4'),
        ],
        "capitulos": [
            ('texto', 'Contexto', '<p>Para quem, onde e quando foi feita a <mark>sessão fotográfica</mark>.</p>'),
            ('frase', 'O desafio', 'A dificuldade principal da sessão: luz, tempo, movimento ou o que tornou este trabalho especial.'),
            ('passos', 'O que fiz', ['Preparação e planeamento.', 'Sessão fotográfica.', 'Seleção e edição.', 'Entrega ao cliente.']),
            ('texto', 'Privacidade', '<p>Só se publicam imagens de pessoas <mark>com autorização</mark>; dados pessoais visíveis são desfocados.</p>'),
        ],
        "behance": False,
    },
    {
        "slug": 'exemplo-design', "demo": True,
        "tipo": "design",
        "titulo": 'Design de marca',
        "etiqueta": 'Template · Branding',
        "resumo": 'Exemplo do template de design: paleta de cores para copiar, contraste de cada cor e amostra tipográfica ajustável.',
        "meta": [('Ano', 'AAAA'), ('Papel', 'Design gráfico e branding'), ('Contexto', 'Cliente'), ('Ferramentas', 'Adobe Illustrator, Figma')],
        "paleta": [("Cobre", "#6F4520"), ("Areia", "#E6B282"), ("Carvão", "#1D1A16"), ("Marfim", "#F5F1EB")],
        "tipografia": [("Manrope", "Letra de exemplo para títulos e texto")],
        "galeria": [
            ('projeto-4.svg', 'Ilustração de exemplo de um logótipo com paleta de cores.', 'Logótipo'),
            ('projeto-2.svg', 'Ilustração de exemplo da marca aplicada num website.', 'Aplicação digital'),
        ],
        "capitulos": [
            ('texto', 'Contexto', '<p>Quem é o cliente e <mark>o que a marca precisa de comunicar</mark>.</p>'),
            ('frase', 'O desafio', 'O problema de comunicação que a identidade visual resolve.'),
            ('passos', 'O que fiz', ['Pesquisa e conceito.', 'Logótipo e variações.', 'Cores e tipografia.', 'Aplicações e manual de normas.']),
            ('texto', 'Resultado', '<p>Uma marca <mark>reconhecível e coerente</mark> em todos os suportes.</p>'),
        ],
        "behance": False,
    },
    {
        "slug": 'exemplo-web', "demo": True,
        "tipo": "web",
        "titulo": 'Website',
        "etiqueta": 'Template · Web',
        "resumo": 'Exemplo do template web: simulador de computador, tablet e telemóvel com a página real.',
        "meta": [('Ano', 'AAAA'), ('Papel', 'Design e desenvolvimento'), ('Contexto', 'Cliente'), ('Tecnologia', 'HTML, CSS, WordPress…')],
        "url": "", "url_nome": "o website",
        # Capturas de página inteira (largura 1200 / 780 / 390 px) em assets/img/
        "dispositivos": {"desktop": "exemplos/site-desktop.jpg", "tablet": "exemplos/site-tablet.jpg", "telemovel": "exemplos/site-telemovel.jpg"},
        "galeria": [
            ('projeto-2.svg', 'Ilustração de exemplo de um website num browser.', 'Página inicial'),
            ('projeto-3.svg', 'Ilustração de exemplo de um website em computador e telemóvel.', 'Responsivo'),
        ],
        "capitulos": [
            ('texto', 'Contexto', '<p>Para que serve o website e <mark>quem o vai usar</mark>.</p>'),
            ('frase', 'O desafio', 'O que o website tinha de resolver para quem o visita.'),
            ('passos', 'O que fiz', ['Arquitetura de informação.', 'Wireframes e protótipo.', 'Design visual.', 'Desenvolvimento e publicação.']),
            ('texto', 'Acessibilidade', '<p>Estrutura semântica, contraste e navegação por teclado, <mark>segundo as WCAG</mark>.</p>'),
        ],
        "behance": False,
    },
    {
        "slug": 'exemplo-video', "demo": True,
        "tipo": "video",
        "titulo": 'Vídeo',
        "etiqueta": 'Template · Vídeo',
        "resumo": 'Exemplo do template de vídeo: os formatos em que cada peça foi entregue.',
        "meta": [('Ano', 'AAAA'), ('Papel', 'Realização e edição'), ('Contexto', 'Cliente ou campanha'), ('Ferramentas', 'Edição de vídeo')],
        "formatos": [("16:9", "Horizontal", "Website e ecrãs largos"), ("9:16", "Vertical", "Histórias e vídeos curtos"), ("1:1", "Quadrado", "Feed das redes sociais")],
        "galeria": [
            ('projeto-5.svg', 'Ilustração de exemplo de um leitor de vídeo.', 'Vídeo'),
            ('hero.svg', 'Ilustração de exemplo de ecrãs com conteúdo.', 'Aplicação'),
        ],
        "capitulos": [
            ('texto', 'Contexto', '<p>Para que serviu o vídeo e <mark>onde foi publicado</mark>.</p>'),
            ('frase', 'O desafio', 'A mensagem que tinha de passar em poucos segundos.'),
            ('passos', 'O que fiz', ['Guião e planeamento.', 'Captação.', 'Edição e grafismos.', 'Adaptação aos formatos.']),
            ('texto', 'Acessibilidade', '<p>Legendas e texto no ecrã para <mark>ver sem som</mark>; sem flashes rápidos.</p>'),
        ],
        "behance": False,
    },
    {
        "slug": 'exemplo-investigacao', "demo": True,
        "tipo": "investigacao",
        "titulo": 'Investigação',
        "etiqueta": 'Template · Investigação',
        "resumo": 'Exemplo do template de investigação: ficha do artigo, palavras-chave e citação para copiar.',
        "meta": [('Ano', 'AAAA'), ('Papel', 'Autor'), ('Publicação', 'Conferência ou revista'), ('Autores', 'Nomes dos autores')],
        "publicacao": {
            "titulo": "Title of the article (example)",
            "autores": ["Autor 1", "Autor 2"],
            "evento": "Nome da conferência ou revista", "ano": "AAAA",
            "palavras": ["Palavra-chave 1", "Palavra-chave 2", "Palavra-chave 3"],
            "citacao": "Apelido, A., & Apelido, B. (AAAA). Title of the article (example). Nome da conferência ou revista.",
        },
        "galeria": [('projeto-6.svg', 'Ilustração de exemplo de um artigo científico.', 'Artigo')],
        "capitulos": [
            ('texto', 'Contexto', '<p>Onde nasceu a investigação e <mark>porque é importante</mark>.</p>'),
            ('frase', 'A pergunta', 'A pergunta de investigação, numa frase.'),
            ('texto', 'Contribuição', '<p>O que o artigo <mark>acrescenta</mark> ao conhecimento existente.</p>'),
        ],
        "behance": False,
    },
    {
        "slug": 'exemplo-uiux', "demo": True,
        "tipo": "uiux",
        "titulo": 'UI/UX',
        "etiqueta": 'Template · UI/UX',
        "resumo": 'Exemplo do template de UI/UX: carrossel, capítulos do processo e demonstração de acessibilidade.',
        "meta": [('Ano', 'AAAA'), ('Papel', 'UI/UX Designer'), ('Contexto', 'Cliente ou projeto'), ('Ferramentas', 'Figma')],
        "galeria": [
            ('projeto-1.svg', 'Ilustração de exemplo de um painel digital.', 'Interface'),
            ('hero.svg', 'Ilustração de exemplo de um painel e de uma aplicação móvel.', 'Aplicação'),
            ('projeto-3.svg', 'Ilustração de exemplo de um website responsivo.', 'Responsivo'),
        ],
        "capitulos": [
            ('texto', 'Contexto', '<p>Quem são os utilizadores e <mark>que problema tinham</mark>.</p>'),
            ('frase', 'O desafio', 'O desafio de design, do ponto de vista de quem usa.'),
            ('passos', 'O que fiz', ['Investigação com utilizadores.', 'Wireframes.', 'Protótipo de alta fidelidade.', 'Testes de usabilidade.']),
            ('texto', 'Acessibilidade', '<p>Contraste, tamanho de letra e estados que <mark>não dependem só da cor</mark>.</p>'),
            ('texto', 'Resultado', '<p>O impacto do trabalho, <mark>de preferência com dados</mark>.</p>'),
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


# ---------------------------------------------------------------------------
# Módulos próprios de cada tipo de trabalho (cada página tem o seu "fator diferencial")
#   fotografia   — galeria em mosaico, ecrã inteiro e parâmetros de cada foto (EXIF)
#   design       — paleta de cores (copiar HEX/RGB) e amostra tipográfica ajustável
#   web          — simulador de dispositivos com a página real
#   video        — formatos de vídeo (16:9, 9:16, 1:1)
#   investigacao — ficha da publicação e citação para copiar
#   uiux         — capítulos + demonstração de acessibilidade (sem módulo extra)
# ---------------------------------------------------------------------------
import json as _json

TIPOS = {
    "uiux": "UI/UX", "fotografia": "Fotografia", "design": "Design de marca",
    "web": "Web", "video": "Vídeo", "investigacao": "Investigação",
}
try:
    EXIF = _json.loads((RAIZ / "tools" / "exif-fotos.json").read_text(encoding="utf-8"))
except FileNotFoundError:
    EXIF = {}


def _parametros(img):
    e = EXIF.get(img.replace("projetos/", "", 1), {})
    return [(k, e[k]) for k in ("abertura", "velocidade", "iso", "focal") if e.get(k)], e


def _lum(hexcor):
    r, g, b = (int(hexcor[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def _contraste(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def modulo_fotografia(p):
    nomes = {"abertura": "Abertura", "velocidade": "Velocidade", "iso": "Sensibilidade", "focal": "Distância focal"}
    itens = []
    camera = data = ""
    for k, (img, alt, leg) in enumerate(p["galeria"]):
        params, e = _parametros(img)
        camera = camera or e.get("camera", "")
        data = data or (e.get("data") or "")[:10].replace(":", "-")
        chips = "".join(f'<li><span class="sr-only">{nomes[n]}: </span>{esc(v)}</li>' for n, v in params)
        itens.append(f"""          <li class="foto reveal">
            <button type="button" class="foto-abrir" data-foto="{k}" aria-label="Ver em ecrã inteiro: {esc(leg)}">
              <img src="../assets/img/{img}" alt="{esc(alt)}" width="800" height="1000" loading="lazy">
            </button>
            <div class="foto-info"><p class="foto-leg">{esc(leg)}</p><ul class="foto-params" aria-label="Parâmetros da fotografia">{chips}</ul></div>
          </li>""")
    ficha = [("Câmara", camera), ("Data", "-".join(reversed(data.split("-"))) if data else ""), ("Fotografias", str(len(p["galeria"])))]
    ficha_html = "".join(f'<li><span class="ficha-k">{esc(a)}:</span> <span class="ficha-v">{esc(b)}</span></li>' for a, b in ficha if b)
    return f"""      <section class="modulo modulo-foto" aria-labelledby="mod-foto">
        <div class="container">
          <div class="modulo-head">
            <p class="eyebrow">Fotografia</p>
            <h2 id="mod-foto" class="modulo-title">Galeria</h2>
            <ul class="foto-ficha" aria-label="Ficha técnica">{ficha_html}</ul>
          </div>
          <ul class="foto-grelha">
{chr(10).join(itens)}
          </ul>
        </div>
        <dialog class="lightbox" aria-label="Fotografia em ecrã inteiro">
          <div class="lightbox-inner">
            <figure class="lightbox-fig"><img src="" alt=""><figcaption><span class="lightbox-leg"></span><span class="lightbox-params"></span></figcaption></figure>
            <button type="button" class="lightbox-btn lightbox-prev" aria-label="Fotografia anterior"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button>
            <button type="button" class="lightbox-btn lightbox-next" aria-label="Fotografia seguinte"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button>
            <button type="button" class="lightbox-btn lightbox-close" aria-label="Fechar"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
            <p class="sr-only lightbox-status" aria-live="polite"></p>
          </div>
        </dialog>
      </section>"""


def modulo_design(p):
    cores = []
    for nome, hexcor in p.get("paleta", []):
        r, g, b = (int(hexcor[i:i + 2], 16) for i in (1, 3, 5))
        cb, cp = _contraste(hexcor, "#FFFFFF"), _contraste(hexcor, "#000000")
        texto = "#FFFFFF" if cb >= cp else "#000000"
        melhor = max(cb, cp)
        nivel = "AAA" if melhor >= 7 else ("AA" if melhor >= 4.5 else "AA texto grande")
        cores.append(f"""          <li class="cor reveal">
            <button type="button" class="cor-copiar" data-copiar="{hexcor}" style="--cor:{hexcor};--cor-texto:{texto}" aria-label="Copiar {esc(nome)}, {hexcor}">
              <span class="cor-amostra" aria-hidden="true"></span>
            </button>
            <p class="cor-nome">{esc(nome)}</p>
            <p class="cor-valores"><span>{hexcor}</span> <span>RGB {r} {g} {b}</span></p>
            <p class="cor-contraste">Texto {'branco' if texto == '#FFFFFF' else 'preto'}: {melhor:.1f}:1 · {nivel}</p>
          </li>""")
    fontes = p.get("tipografia", [])
    fonte, uso = fontes[0] if fontes else ("Manrope", "")
    return f"""      <section class="modulo modulo-design" aria-labelledby="mod-design">
        <div class="container">
          <div class="modulo-head">
            <p class="eyebrow">Sistema visual</p>
            <h2 id="mod-design" class="modulo-title">Cores e tipografia</h2>
            <p class="modulo-lead">Clique numa cor para copiar o código HEX. O contraste indicado é o melhor entre texto branco e preto (WCAG).</p>
          </div>
          <ul class="paleta">
{chr(10).join(cores)}
          </ul>
          <p class="sr-only copiar-status" aria-live="polite"></p>
          <div class="tipo-amostra reveal" style="--fonte:'{esc(fonte)}'">
            <div class="tipo-cab">
              <p class="tipo-nome">{esc(fonte)}</p>
              <p class="tipo-uso">{esc(uso)}</p>
            </div>
            <p class="tipo-texto" id="tipo-texto">Mobilidade verde para todos</p>
            <div class="tipo-controlos">
              <label for="tipo-tamanho">Tamanho <output id="tipo-valor" for="tipo-tamanho">48 px</output></label>
              <input type="range" id="tipo-tamanho" min="16" max="120" value="48" step="2" aria-controls="tipo-texto">
              <div class="tipo-pesos" role="group" aria-label="Peso da letra">
                <button type="button" aria-pressed="false" data-peso="300">Light</button>
                <button type="button" aria-pressed="true" data-peso="500">Medium</button>
                <button type="button" aria-pressed="false" data-peso="700">Bold</button>
              </div>
            </div>
          </div>
        </div>
      </section>"""


def modulo_web(p):
    d = p.get("dispositivos", {})
    if not d:
        return ""
    nomes = [("desktop", "Computador"), ("tablet", "Tablet"), ("telemovel", "Telemóvel")]
    botoes = "".join(
        f'<button type="button" class="disp-btn" data-disp="{k}" aria-pressed="{"true" if k == "desktop" else "false"}">{n}</button>'
        for k, n in nomes if k in d)
    imgs = "".join(
        f'<img class="disp-img{" is-on" if k == "desktop" else ""}" data-disp="{k}" src="../assets/img/{d[k]}" alt="Página inicial de {esc(p.get("url_nome", "o website"))} vista num {n.lower()}." loading="lazy">'
        for k, n in nomes if k in d)
    url = p.get("url", "")
    link = (f'<a class="btn btn-ghost" href="{url}" target="_blank" rel="noopener">Visitar {esc(p.get("url_nome", "o website"))} <span aria-hidden="true">↗</span>'
            f'<span class="sr-only"> (abre num novo separador)</span></a>') if url else ""
    return f"""      <section class="modulo modulo-web" aria-labelledby="mod-web">
        <div class="container">
          <div class="modulo-head">
            <p class="eyebrow">Website</p>
            <h2 id="mod-web" class="modulo-title">Em todos os ecrãs</h2>
            <p class="modulo-lead">Escolha o dispositivo e percorra a página dentro do ecrã.</p>
          </div>
          <div class="disp-botoes" role="group" aria-label="Dispositivo">{botoes}</div>
          <div class="disp-palco" data-atual="desktop">
            <div class="disp-moldura">
              <div class="disp-barra" aria-hidden="true"><i></i><i></i><i></i><span>{esc(url.replace("https://", ""))}</span></div>
              <div class="disp-ecra" tabindex="0" role="region" aria-label="Captura da página: percorra com as setas do teclado">{imgs}</div>
            </div>
          </div>
          <p class="disp-link">{link}</p>
        </div>
      </section>"""


def modulo_video(p):
    fmts = p.get("formatos", [])
    if not fmts:
        return ""
    itens = "".join(f"""          <li class="fmt reveal" style="--ar:{a.replace(':', '/')}">
            <div class="fmt-ecra" aria-hidden="true"><span class="fmt-play"></span><span class="fmt-tempo"></span></div>
            <p class="fmt-ar">{esc(a)}</p><p class="fmt-nome">{esc(n)}</p><p class="fmt-uso">{esc(u)}</p>
          </li>""" for a, n, u in fmts)
    return f"""      <section class="modulo modulo-video" aria-labelledby="mod-video">
        <div class="container">
          <div class="modulo-head">
            <p class="eyebrow">Vídeo</p>
            <h2 id="mod-video" class="modulo-title">Um vídeo, vários formatos</h2>
            <p class="modulo-lead">Cada peça foi adaptada ao ecrã onde ia ser vista.</p>
          </div>
          <ul class="formatos">
{itens}
          </ul>
        </div>
      </section>"""


def modulo_investigacao(p):
    pub = p.get("publicacao")
    if not pub:
        return ""
    chips = "".join(f"<li>{esc(k)}</li>" for k in pub.get("palavras", []))
    autores = ", ".join(pub["autores"])
    return f"""      <section class="modulo modulo-paper" aria-labelledby="mod-paper">
        <div class="container paper">
          <div class="modulo-head">
            <p class="eyebrow">Publicação científica</p>
            <h2 id="mod-paper" class="modulo-title">Ficha do artigo</h2>
          </div>
          <article class="paper-ficha reveal" aria-labelledby="paper-titulo">
            <p class="paper-evento">{esc(pub["evento"])} · {esc(pub["ano"])}</p>
            <h3 class="paper-titulo" id="paper-titulo" lang="en">{esc(pub["titulo"])}</h3>
            <p class="paper-autores">{esc(autores)}</p>
            <ul class="paper-chaves" aria-label="Palavras-chave">{chips}</ul>
          </article>
          <div class="paper-citar reveal">
            <h3 class="paper-sub">Como citar</h3>
            <p class="paper-citacao" id="citacao">{esc(pub["citacao"])}</p>
            <button type="button" class="btn btn-ghost" data-copiar-de="citacao">Copiar citação</button>
            <p class="sr-only copiar-status" aria-live="polite"></p>
          </div>
        </div>
      </section>"""


MODULOS = {"fotografia": modulo_fotografia, "design": modulo_design, "web": modulo_web,
           "video": modulo_video, "investigacao": modulo_investigacao}


def modulo(p):
    f = MODULOS.get(p.get("tipo", "uiux"))
    return f(p) if f else ""


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
    robots = '  <meta name="robots" content="noindex">\n' if p.get("demo") else ''
    aviso = ('      <p class="demo-aviso container"><strong>Página de exemplo.</strong> '
             'Mostra o template deste tipo de trabalho; o conteúdo real entra em breve.</p>\n') if p.get("demo") else ''
    return f"""<!doctype html>
<html lang="pt-PT">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(titulo)}</title>
  <meta name="description" content="{esc(p["resumo"])}">
  <meta name="author" content="João Mendo">
{robots}  <meta name="theme-color" content="#121110" media="(prefers-color-scheme: dark)">
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
<body class="page-case tipo-{p.get("tipo", "uiux")}">
{sprite}
  <a class="skip-link" href="#conteudo">Saltar para o conteúdo</a>
  <div class="scroll-progress" aria-hidden="true"><span></span></div>
  <div class="cursor-glow" aria-hidden="true"></div>

{cabecalho}
  <main id="conteudo" tabindex="-1">
    <article class="case">
{aviso}      <header class="case-hero container">
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

{'' if p.get('tipo') in ('fotografia', 'investigacao') else galeria(p)}
{modulo(p)}

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
for antiga in SAIDA.glob('*.html'):
    if antiga.stem not in {q['slug'] for q in PROJETOS}:
        antiga.unlink(); print('apagado:', antiga.name)
for i, p in enumerate(PROJETOS):
    (SAIDA / f'{p["slug"]}.html').write_text(pagina(i, p), encoding="utf-8", newline="\n")
    print("gerado:", f'projetos/{p["slug"]}.html')
