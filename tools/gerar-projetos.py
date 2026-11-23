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
        "slug": 'futurmedia',
        "tipo": "uiux",
        "demonstracao": None,
        "titulo": 'FuturMedia',
        "etiqueta": 'UI/UX · Design de Interação',
        "resumo": 'Website e versão mobile para uma agência de marketing e comunicação fictícia, do esboço em papel ao protótipo de alta fidelidade em Adobe XD.',
        "meta": [('Ano', '2023'), ('Papel', 'Design de interação · projeto académico'), ('Contexto', 'Mestrado em Tecnologia e Multimédia, UTAD'), ('Ferramentas', 'Adobe XD')],
        "url": "", "url_nome": "FuturMedia",
        "dispositivos": {"desktop": "projetos/futurmedia/site-desktop.jpg", "telemovel": "projetos/futurmedia/site-telemovel.jpg"},
        "comparar": [
            ("Início", "projetos/futurmedia/esboco-inicio.jpg", "projetos/futurmedia/final-inicio.jpg"),
            ("Serviços", "projetos/futurmedia/esboco-servicos.jpg", "projetos/futurmedia/final-servicos.jpg"),
            ("Portfólio", "projetos/futurmedia/esboco-portfolio.jpg", "projetos/futurmedia/final-portfolio.jpg"),
            ("Sobre", "projetos/futurmedia/esboco-sobre.jpg", "projetos/futurmedia/final-sobre.jpg"),
            ("Contactos", "projetos/futurmedia/esboco-contactos.jpg", "projetos/futurmedia/final-contactos.jpg"),
            ("Login", "projetos/futurmedia/esboco-login.jpg", "projetos/futurmedia/final-login.jpg"),
        ],
        "galeria": [
            ('projetos/futurmedia/final-inicio.jpg', 'Página inicial da FuturMedia, em azul-escuro com círculos laranja.', 'Página inicial'),
            ('projetos/futurmedia/final-servicos.jpg', 'Página de serviços com web design, programação, fotografia e design.', 'Serviços'),
            ('projetos/futurmedia/final-portfolio.jpg', 'Página de portfólio com filtros por categoria.', 'Portfólio'),
            ('projetos/futurmedia/final-contactos.jpg', 'Página de contactos com formulário e horário.', 'Contactos'),
            ('projetos/futurmedia/final-login.jpg', 'Ecrã de login com entrada por email ou por Google, Apple e Facebook.', 'Login'),
            ('projetos/futurmedia/esboco-inicio.jpg', 'Esboço em preto e branco da página inicial.', 'Esboço da página inicial'),
        ],
        "capitulos": [
            ('texto', 'Contexto', '<p>Projeto da unidade curricular de Design de Interação do Mestrado em Tecnologia e Multimédia: criar a presença digital da <mark>FuturMedia</mark>, uma agência fictícia de marketing e comunicação para empresas de tecnologia.</p>'),
            ('frase', 'O desafio', 'Apresentar os serviços e o portfólio de uma agência de forma clara, envolvente e acessível a todas as pessoas.'),
            ('passos', 'Processo', ['Pesquisa de mercado: Mediaon, Qreativ, Bleam e Fiverr.', 'Público-alvo, personas e estratégia de comunicação.', 'Esboços das páginas web e mobile.', 'Mockups de alta fidelidade em Adobe XD.']),
            ('texto', 'Acessibilidade', '<p>A pesquisa estudou vários <mark>tipos de deficiência</mark> — visual, auditiva, motora, cognitiva, de fala, epilepsia fotossensível, ataxia e défice de atenção — para orientar as decisões de design.</p>'),
            ('texto', 'Identidade', '<p>A paleta junta o <mark>azul-escuro</mark> (confiança e harmonia) ao <mark>laranja</mark> (criatividade e sociabilidade), com preto e branco, a partir da psicologia da cor de Eva Heller.</p>'),
            ('texto', 'Resultado', '<p>Um website com <mark>sete ecrãs</mark> — início, serviços, portfólio com filtros, sobre, contactos, login e registo — em versão para computador e telemóvel.</p>'),
        ],
        "behance": False,
    },
    {
        "slug": 'festas-romarias-mirandela',
        "tipo": "design",
        "titulo": 'Festas e Romarias 2023',
        "etiqueta": 'Design gráfico · Câmara Municipal de Mirandela',
        "resumo": 'Flyer desdobrável com as festas e romarias das freguesias de Mirandela, de junho a setembro de 2023, criado no estágio curricular na Câmara Municipal.',
        "meta": [('Ano', '2023'), ('Papel', 'Design gráfico · estágio curricular'), ('Cliente', 'Câmara Municipal de Mirandela'), ('Formato', 'Flyer A4 em três painéis')],
        "paleta": [("Verde-lima", "#A8B838"), ("Verde-oliva", "#5A7A36"), ("Branco", "#FFFFFF")],
        "galeria": [
            ('projetos/festas-romarias-mirandela/final-exterior.jpg', 'Exterior do flyer: painéis das freguesias com igrejas e capa com fogo de artifício.', 'Exterior'),
            ('projetos/festas-romarias-mirandela/capa.jpg', 'Capa do flyer: fogo de artifício sobre o rio e o título Festas e Romarias 2023.', 'Capa'),
            ('projetos/festas-romarias-mirandela/paineis.jpg', 'Painéis com a igreja, as datas e o padroeiro de cada freguesia.', 'Painéis das freguesias'),
            ('projetos/festas-romarias-mirandela/final-verso.jpg', 'Verso do flyer com código QR, contactos e mais freguesias.', 'Verso e contactos'),
        ],
        "versoes": [
            ('projetos/festas-romarias-mirandela/versao-v1.jpg', 'Primeira estrutura', 'Primeira versão: estrutura a branco com fotografias e texto provisório.'),
            ('projetos/festas-romarias-mirandela/versao-v2.jpg', 'Mapa das freguesias', 'Segunda versão com o mapa colorido das freguesias.'),
            ('projetos/festas-romarias-mirandela/versao-v3.jpg', 'Primeiras cores', 'Terceira versão com os primeiros painéis verdes.'),
            ('projetos/festas-romarias-mirandela/versao-v4.jpg', 'Painéis em verde', 'Quarta versão com todos os painéis em verde.'),
            ('projetos/festas-romarias-mirandela/versao-v5.jpg', 'Interior e capa', 'Quinta versão com o interior completo e a capa com o rio.'),
            ('projetos/festas-romarias-mirandela/versao-v6.jpg', 'Versão final', 'Versão final: painéis das freguesias e capa com fogo de artifício.'),
        ],
        "capitulos": [
            ('texto', 'Contexto', '<p>No <mark>estágio curricular na Câmara Municipal de Mirandela</mark> (2023), criei o flyer que reúne as festas e romarias das freguesias do concelho, de junho a setembro.</p>'),
            ('frase', 'O desafio', 'Juntar dezenas de freguesias, datas e padroeiros num só desdobrável, fácil de consultar e com vontade de ir à festa.'),
            ('passos', 'O que fiz', ['Organização das freguesias, datas e padroeiros.', 'Estrutura em três painéis, frente e verso.', 'Fotografia de cada igreja e mapa do concelho.', 'Capa, código QR e contactos úteis.']),
            ('texto', 'Resultado', '<p>Um flyer pronto a imprimir que leva o visitante <mark>de freguesia em freguesia</mark>, com a ligação ao Visit Mirandela à distância de um código QR.</p>'),
        ],
        "behance": False,
    },
    {
        "slug": 'amover-comunicacao',
        "tipo": "design",
        "titulo": 'A-MoVeR · Comunicação e eventos',
        "etiqueta": 'Design gráfico · Comunicação',
        "resumo": 'Comunicação visual do projeto A-MoVeR: dois Dias da Inovação na UTAD, formação e redes sociais, do roll-up ao post de Instagram.',
        "meta": [('Ano', '2024–26'), ('Papel', 'Design gráfico e comunicação'), ('Projeto', 'A-MoVeR · Agenda Mobilizadora'), ('Peças', 'Cartazes, roll-ups, crachás, folhetos, posts')],
        "paleta": [("Azul-noite", "#001C61"), ("Verde", "#528E4F"), ("Verde-claro", "#A4CE99"), ("Branco", "#FFFFFF")],
        "galeria": [
            ('projetos/amover-comunicacao/2026-ecra.jpg', 'Ecrã do Dia da Inovação 2026 com o logótipo A-MoVeR e a data 3 de junho.', 'Dia da Inovação 2026'),
            ('projetos/amover-comunicacao/2025-evento-rollups.jpg', 'Roll-ups do Dia da Inovação 2025 montados à entrada do auditório.', 'Roll-ups no evento'),
            ('projetos/amover-comunicacao/2025-evento-ecra.jpg', 'Sessão do Dia da Inovação 2025 com o logótipo A-MoVeR projetado.', 'Dia da Inovação 2025'),
            ('projetos/amover-comunicacao/redes-quem-sou-eu-1.jpg', 'Post da série Quem sou eu, com o retrato de um bolseiro do projeto.', 'Série Quem sou eu'),
        ],
        "pecas": [
            ('projetos/amover-comunicacao/2025-rollup.jpg', 'Roll-up', '2025', '91 × 206 cm', 'Roll-up do Dia da Inovação A-MoVeR, 27 de fevereiro de 2025.'),
            ('projetos/amover-comunicacao/2025-cartaz.jpg', 'Cartaz com programa', '2025', '44 × 61 cm', 'Cartaz com o programa da manhã e da tarde do Dia da Inovação 2025.'),
            ('projetos/amover-comunicacao/2025-folheto-frente.jpg', 'Folheto · frente', '2025', 'A5', 'Frente do folheto do Dia da Inovação 2025.'),
            ('projetos/amover-comunicacao/2025-folheto-verso.jpg', 'Folheto · verso', '2025', 'A5', 'Verso do folheto com o programa do Dia da Inovação 2025.'),
            ('projetos/amover-comunicacao/2025-cracha.jpg', 'Crachá', '2025', 'A6', 'Crachá do Dia da Inovação 2025.'),
            ('projetos/amover-comunicacao/2026-cartaz.jpg', 'Cartaz com programa', '2026', 'A3', 'Cartaz do Dia da Inovação 2026 com o programa da tarde.'),
            ('projetos/amover-comunicacao/2026-ecra.jpg', 'Ecrã de projeção', '2026', '16:9', 'Ecrã de projeção do Dia da Inovação 2026.'),
            ('projetos/amover-comunicacao/2026-post-1.jpg', 'Post · capa', '2026', '1080 × 1080 px', 'Primeiro post do carrossel de Instagram do Dia da Inovação 2026.'),
            ('projetos/amover-comunicacao/2026-post-2.jpg', 'Post · programa', '2026', '1080 × 1080 px', 'Segundo post do carrossel com o programa do Dia da Inovação 2026.'),
            ('projetos/amover-comunicacao/2026-cracha.jpg', 'Crachá', '2026', '8,6 × 5,4 cm', 'Crachá em formato de cartão do Dia da Inovação 2026.'),
            ('projetos/amover-comunicacao/redes-quem-sou-eu-1.jpg', 'Quem sou eu · retrato', 'Redes sociais', 'Instagram', 'Post Quem sou eu com o retrato de um bolseiro.'),
            ('projetos/amover-comunicacao/redes-quem-sou-eu-2.jpg', 'Quem sou eu · perfil', 'Redes sociais', 'Instagram', 'Post Quem sou eu com o percurso e as funções do bolseiro.'),
            ('projetos/amover-comunicacao/redes-quem-sou-eu-3.jpg', 'Quem sou eu · citação', 'Redes sociais', 'Instagram', 'Post com a citação: A-MoVeR é investir num futuro inteligente e sustentável.'),
            ('projetos/amover-comunicacao/2024-formacao-kotlin.jpg', 'Cartaz da formação Android com Kotlin', 'Formação', 'Cartaz', 'Cartaz da formação de desenvolvimento Android com Kotlin, junho de 2024.'),
        ],
        "capitulos": [
            ('texto', 'Contexto', '<p>O <mark>A-MoVeR</mark> é uma agenda mobilizadora para a mobilidade verde que junta a UTAD, a AJP, a AUMOVIO (Continental), o INESC TEC, a Neoception e a up_motion. Fui responsável pela comunicação visual dos seus eventos, formação e redes sociais.</p>'),
            ('frase', 'O desafio', 'Dar uma imagem única a um consórcio de seis parceiros, do roll-up de dois metros ao crachá no bolso.'),
            ('passos', 'O que fiz', ['Dia da Inovação 2025 (27 de fevereiro, UTAD): cartaz, roll-up, folheto e crachá.', 'Dia da Inovação 2026 (3 de junho, UTAD): cartaz, ecrã, crachá e carrossel de Instagram.', 'Série Quem sou eu para apresentar a equipa nas redes sociais.', 'Cartaz da formação em desenvolvimento Android com Kotlin.']),
            ('texto', 'Resultado', '<p>Um sistema visual <mark>reconhecível de um ano para o outro</mark>: as mesmas cores, o logótipo e os parceiros sempre presentes, adaptados a cada formato.</p>'),
        ],
        "behance": False,
    },
    {
        "slug": 'amover-visitas',
        "tipo": "fotografia",
        "titulo": 'A-MoVeR · Visitas e eventos',
        "etiqueta": 'Fotografia e vídeo · Reportagem',
        "resumo": 'Reportagem fotográfica do projeto A-MoVeR: visitas à AUMOVIO, à AJP Motos e ao INESC TEC em 2024 e o Dia da Inovação 2026 na UTAD.',
        "meta": [('Período', '2024–26'), ('Papel', 'Fotografia e vídeo'), ('Projeto', 'A-MoVeR · Agenda Mobilizadora'), ('Equipamento', 'Canon EOS 850D · Sony ZV-E10')],
        "video": {"src": "projetos/amover-visitas/dia2026-video.mp4", "poster": "projetos/amover-visitas/dia2026-video-poster.jpg", "titulo": "Dia da Inovação 2026 em 45 segundos.",
                  "descricao": "Vídeo sem som: a sessão de abertura no auditório, as apresentações dos parceiros do consórcio, um painel de perguntas e, no fim, a Fulgora em andamento no campus da UTAD."},
        "galeria": [
            ('projetos/amover-visitas/ajp-perfil.jpg', 'Fulgora, mota elétrica da AJP Motos, de perfil no exterior da fábrica.', 'Fulgora', 'AJP Motos'),
            ('projetos/amover-visitas/ajp-tres-quartos.jpg', 'Fulgora vista de frente a três quartos.', 'Fulgora · três quartos', 'AJP Motos'),
            ('projetos/amover-visitas/ajp-suspensao.jpg', 'Pormenor da suspensão traseira e do motor da Fulgora.', 'Suspensão e motor', 'AJP Motos'),
            ('projetos/amover-visitas/ajp-linha.jpg', 'Linha de montagem da AJP com motas e um técnico a trabalhar.', 'Linha de montagem', 'AJP Motos'),
            ('projetos/amover-visitas/ajp-soldadura.jpg', 'Técnico com máscara a soldar uma peça na oficina da AJP.', 'Soldadura', 'AJP Motos'),
            ('projetos/amover-visitas/ajp-armazem.jpg', 'Armazém da fábrica com motas e peças em bancadas.', 'Armazém', 'AJP Motos'),
            ('projetos/amover-visitas/aumovio-equipa.jpg', 'Equipa da AUMOVIO de bata branca sentada a uma mesa de reuniões.', 'Equipa', 'AUMOVIO'),
            ('projetos/amover-visitas/aumovio-laboratorio.jpg', 'Engenheiro da AUMOVIO a mostrar um componente a dois visitantes.', 'Laboratório', 'AUMOVIO'),
            ('projetos/amover-visitas/aumovio-componentes.jpg', 'Componentes eletrónicos de um painel dispostos numa mesa.', 'Componentes', 'AUMOVIO'),
            ('projetos/amover-visitas/aumovio-edificio.jpg', 'Edifício da AUMOVIO ao fim da tarde.', 'Edifício', 'AUMOVIO'),
            ('projetos/amover-visitas/inesc-camara.jpg', 'Câmara anecoica do INESC TEC com cones de absorção nas paredes.', 'Câmara anecoica', 'INESC TEC'),
            ('projetos/amover-visitas/inesc-laboratorio.jpg', 'Laboratório do INESC TEC com bancada de testes.', 'Laboratório', 'INESC TEC'),
            ('projetos/amover-visitas/inesc-conversa.jpg', 'Dois investigadores conversam num laboratório.', 'Conversa', 'INESC TEC'),
            ('projetos/amover-visitas/dia2026-chegada.jpg', 'Participantes a chegar ao auditório para o Dia da Inovação.', 'Chegada', 'Dia da Inovação 2026'),
            ('projetos/amover-visitas/dia2026-auditorio.jpg', 'Auditório cheio com o ecrã do Dia da Inovação A-MoVeR.', 'Auditório', 'Dia da Inovação 2026'),
            ('projetos/amover-visitas/dia2026-abertura.jpg', 'Oradora na sessão de abertura junto ao ecrã do evento.', 'Sessão de abertura', 'Dia da Inovação 2026'),
            ('projetos/amover-visitas/dia2026-plateia.jpg', 'Plateia nas cadeiras azuis do auditório.', 'Plateia', 'Dia da Inovação 2026'),
            ('projetos/amover-visitas/dia2026-painel.jpg', 'Painel de oradores no palco do auditório.', 'Painel', 'Dia da Inovação 2026'),
            ('projetos/amover-visitas/dia2026-realidade-virtual.jpg', 'Demonstração com óculos de realidade virtual na mostra tecnológica.', 'Realidade virtual', 'Dia da Inovação 2026'),
            ('projetos/amover-visitas/dia2026-demonstracao.jpg', 'Visitantes numa demonstração da mostra tecnológica.', 'Mostra tecnológica', 'Dia da Inovação 2026'),
            ('projetos/amover-visitas/dia2026-simulador.jpg', 'Visitantes junto a um simulador com ecrã grande.', 'Simulador', 'Dia da Inovação 2026'),
            ('projetos/amover-visitas/dia2026-convivio.jpg', 'Participantes reunidos no exterior, no campus da UTAD.', 'Networking', 'Dia da Inovação 2026'),
            ('projetos/amover-visitas/dia2026-mota.jpg', 'Mota elétrica em demonstração no exterior, rodeada de participantes.', 'Mota em demonstração', 'Dia da Inovação 2026'),
        ],
        "capitulos": [
            ('texto', 'Contexto', '<p>Como bolseiro do <mark>A-MoVeR</mark>, acompanhei com a câmara as visitas aos parceiros do consórcio — AUMOVIO e INESC TEC em novembro de 2024 e a <mark>fábrica da AJP Motos</mark> a 22 de novembro de 2024 — e o Dia da Inovação na UTAD a 3 de junho de 2026.</p>'),
            ('frase', 'O desafio', 'Mostrar investigação e indústria com pessoas reais, em laboratórios, fábricas e auditórios com luz difícil, sem interromper ninguém.'),
            ('passos', 'O que fiz', ['Fotografia das visitas aos parceiros.', 'Reportagem fotográfica e vídeo do Dia da Inovação.', 'Seleção e edição das imagens.', 'Montagem de um vídeo curto para as redes sociais.']),
            ('texto', 'Privacidade', '<p>São eventos institucionais e públicos do projeto. O rosto de quem não foi possível confirmar foi <mark>desfocado</mark>, e as imagens foram publicadas sem dados de localização.</p>'),
        ],
        "behance": False,
    },
    {
        "slug": 'batizado',
        "tipo": "fotografia",
        "titulo": 'Batizado',
        "etiqueta": 'Fotografia · Reportagem de evento',
        "resumo": 'Reportagem fotográfica de um batizado, da cerimónia na igreja à festa com a família, num dia de verão de 2024.',
        "meta": [('Ano', '2024'), ('Papel', 'Fotografia'), ('Contexto', 'Evento familiar'), ('Equipamento', 'Canon EOS 1100D')],
        # Autorização da família. Sem o nome da criança; letras com o nome desfocadas.
        "galeria": [
            ('projetos/batizado/sorriso.jpg', 'Menina de vestido branco a sorrir junto à mesa da festa.', 'O sorriso'),
            ('projetos/batizado/madrinha.jpg', 'Mulher de vestido rosa com a menina ao colo na igreja.', 'Ao colo'),
            ('projetos/batizado/cerimonia.jpg', 'Família reunida junto à pia batismal durante a cerimónia.', 'A cerimónia'),
            ('projetos/batizado/padrinhos.jpg', 'Pais e padrinhos com a menina à porta da igreja.', 'À porta da igreja'),
            ('projetos/batizado/familia-exterior.jpg', 'Três mulheres e a menina num jardim com vista.', 'Em família'),
            ('projetos/batizado/mesa.jpg', 'Mulher e uma menina a sorrir à mesa da festa.', 'À mesa'),
        ],
        "capitulos": [
            ('texto', 'Contexto', '<p>Reportagem de um <mark>batizado</mark> em agosto de 2024: a cerimónia na igreja e a festa com a família, ao longo de uma tarde.</p>'),
            ('frase', 'O desafio', 'Ser invisível num dia de família: captar os sorrisos verdadeiros, sem pedir poses.'),
            ('passos', 'O que fiz', ['Acompanhamento da cerimónia e da festa.', 'Retratos espontâneos e de grupo.', 'Seleção e edição das fotografias.', 'Entrega à família.']),
            ('texto', 'Privacidade', '<p>Publicado <mark>com autorização da família</mark>. O nome da criança não aparece e as letras decorativas com o nome foram desfocadas.</p>'),
        ],
        "behance": False,
    },
    {
        "slug": 'primeira-comunhao',
        "tipo": "fotografia",
        "titulo": 'Primeira Comunhão',
        "etiqueta": 'Fotografia · Reportagem de evento',
        "resumo": 'Reportagem fotográfica de uma Primeira Comunhão em maio de 2024: a alegria de um dia único, contada em retratos.',
        "meta": [('Ano', '2024'), ('Papel', 'Fotografia e vídeo'), ('Contexto', 'Cerimónia religiosa'), ('Equipamento', 'Canon EOS R50')],
        # Só imagens com autorização da família (menor). Sem nome. Dados do certificado desfocados.
        "galeria": [
            ('projetos/primeira-comunhao/retrato.jpg', 'Retrato de uma menina vestida de branco, a sorrir, com um fio dourado nas mãos.', 'Retrato'),
            ('projetos/primeira-comunhao/certificado.jpg', 'Menina a sorrir a mostrar o certificado da Primeira Comunhão em frente ao altar.', 'O certificado'),
        ],
        "capitulos": [
            ('texto', 'Contexto', '<p>Reportagem de uma cerimónia de <mark>Primeira Comunhão</mark>, a 30 de maio de 2024, em fotografia e vídeo.</p>'),
            ('frase', 'O desafio', 'Captar um dia que só acontece uma vez, sem interferir na cerimónia: luz de igreja, movimento constante e emoções que não se repetem.'),
            ('passos', 'O que fiz', ['Acompanhamento da cerimónia do início ao fim.', 'Fotografia e vídeo em simultâneo.', 'Seleção e edição das imagens.', 'Entrega do trabalho à família.']),
            ('texto', 'Privacidade', '<p>Por se tratar de crianças, só são publicadas imagens <mark>com autorização da família</mark>. O vídeo e as fotografias de grupo ficam reservados, e os dados pessoais do certificado foram desfocados.</p>'),
        ],
        "behance": False,
    },
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
        "slug": 'ia-acessibilidade-digital',
        "tipo": "investigacao",
        "demonstracao": "mota",  # o artigo é sobre painéis que se adaptam: faz sentido a demonstração
        "titulo": 'IA e acessibilidade digital',
        "etiqueta": 'Investigação · Acessibilidade',
        "resumo": 'Artigo científico publicado pela Springer (IntelliSys 2025): o modelo CAIA usa Inteligência Artificial para adaptar as interfaces de motociclos elétricos a cada pessoa.',
        "meta": [('Ano', '2025'), ('Papel', 'Autor principal'), ('Publicação', 'Springer · LNNS, vol. 1553'), ('Páginas', '155–169')],
        "publicacao": {
            "titulo": "New Solution to Old Problems: Leveraging AI to Customize User Motorcycle Interfaces and Guarantee Digital Accessibility",
            "autores": ["João Mendo", "Joana Oliveira", "Tiago Pinto", "Tânia Rocha"],
            "evento": "IntelliSys 2025 · Intelligent Systems and Applications", "ano": "Springer, 2025",
            "palavras": ["Computação centrada no ser humano", "Acessibilidade digital", "Design de interação", "Inteligência Artificial", "Motociclos elétricos", "Adaptação dinâmica de interfaces"],
            "detalhes": [("Série", "Lecture Notes in Networks and Systems, vol. 1553"), ("Publicado", "3 de setembro de 2025"), ("Páginas", "155–169"), ("DOI", "10.1007/978-3-031-99958-1_12")],
            "url": "https://doi.org/10.1007/978-3-031-99958-1_12",
            "resumo": "Despite the proliferation of guidelines, standards, and best practices for digital accessibility, many platforms and websites remain inaccessible to people with disabilities. Although global awareness is slowly increasing, little has been done to overcome this issue. This study explores the potential of Artificial Intelligence (AI) and Machine Learning to address this problem, focusing on the personalization of user interfaces (UIs) in electric motorcycles. Unlike static guidelines, AI-driven solutions can dynamically adapt to the specific needs of users, creating more inclusive digital experiences. We propose a CAIA (Comprehensive AI Accessibility) framework model as a way to integrate AI into electric motorcycle interfaces, allowing users to configure their accessibility preferences and for AI to automatically adjust the display and controls of the motorcycle, promoting a human-centered computing approach and an adaptive system. The model has shown to effectively improve user models and personalization, ensuring a personalized and inclusive experience. The study concludes that AI-driven systems, when ethically implemented, can enhance digital inclusion while providing a more tailored and adaptive user experience. It also discusses the ethical implications, privacy concerns, and the role of human involvement in the development of assistive technologies and interaction design, offering a comprehensive solution to improve digital inclusion for all types of users.",
            "citacao": "Mendo, J., Oliveira, J., Pinto, T., Rocha, T. (2025). New Solution to Old Problems: Leveraging AI to Customize User Motorcycle Interfaces and Guarantee Digital Accessibility. In: Arai, K. (eds) Intelligent Systems and Applications. IntelliSys 2025. Lecture Notes in Networks and Systems, vol 1553. Springer, Cham. https://doi.org/10.1007/978-3-031-99958-1_12",
        },
        "galeria": [
            ('projeto-6.svg', 'Ilustração de um artigo científico com gráfico e o símbolo de acessibilidade.', 'O artigo'),
            ('projeto-1.svg', 'Ilustração do painel digital de um motociclo elétrico.', 'Interfaces de motociclos'),
            ('hero.svg', 'Ilustração de um painel de mota ao lado de uma aplicação móvel.', 'Painel e aplicação'),
        ],
        "capitulos": [
            ('texto', 'Contexto', '<p>Apesar das diretrizes, normas e boas práticas de acessibilidade digital, muitas plataformas continuam <mark>inacessíveis a pessoas com deficiência</mark>. O estudo nasce do trabalho de design de interfaces no projeto A-MoVeR, centrado em motociclos elétricos.</p>'),
            ('frase', 'A pergunta', 'E se, em vez de uma interface igual para todos, a mota se adaptasse a cada condutor?'),
            ('passos', 'O modelo CAIA', ['O condutor configura as suas preferências de acessibilidade.', 'A Inteligência Artificial ajusta automaticamente o ecrã e os controlos da mota.', 'O sistema adapta-se de forma contínua a quem o usa.', 'A pessoa continua no centro e envolvida nas decisões.']),
            ('texto', 'Contribuição', '<p>O artigo propõe o modelo <mark>CAIA (Comprehensive AI Accessibility)</mark> para integrar Inteligência Artificial nas interfaces de motociclos elétricos. O modelo mostrou melhorar os modelos de utilizador e a personalização, garantindo uma experiência inclusiva.</p>'),
            ('texto', 'Ética e privacidade', '<p>A IA só aumenta a inclusão digital quando é <mark>implementada de forma ética</mark>. O artigo discute as implicações éticas, a privacidade e o papel das pessoas no desenvolvimento de tecnologias de apoio e no design de interação.</p>'),
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
    grupos, cameras, datas = [], [], []
    for k, item in enumerate(p["galeria"]):
        img, alt, leg = item[:3]
        grupo = item[3] if len(item) > 3 else ""
        if grupo and grupo not in grupos:
            grupos.append(grupo)
        params, e = _parametros(img)
        if e.get("camera") and e["camera"] not in cameras:
            cameras.append(e["camera"])
        dd = (e.get("data") or "")[:10]
        if dd:
            datas.append(dd)
        camera = camera or e.get("camera", "")
        data = data or (e.get("data") or "")[:10].replace(":", "-")
        chips = "".join(f'<li><span class="sr-only">{nomes[n]}: </span>{esc(v)}</li>' for n, v in params)
        g_attr = f' data-grupo="{esc(grupo)}"' if grupo else ""
        g_chip = f'<li><span class="sr-only">Local: </span>{esc(grupo)}</li>' if grupo else ""
        itens.append(f"""          <li class="foto reveal"{g_attr}>
            <button type="button" class="foto-abrir" data-foto="{k}" aria-label="Ver em ecrã inteiro: {esc(leg)}">
              <img src="../assets/img/{img}" alt="{esc(alt)}" width="800" height="1000" loading="lazy">
            </button>
            <div class="foto-info"><p class="foto-leg">{esc(leg)}</p><ul class="foto-params" aria-label="Parâmetros da fotografia">{g_chip}{chips}</ul></div>
          </li>""")
    fmt = lambda d: "/".join(reversed(d.split(":")))
    periodo = ""
    if datas:
        a, b = min(datas), max(datas)
        periodo = fmt(a) if a == b else f"{fmt(a)} – {fmt(b)}"
    ficha = [("Câmara" if len(cameras) < 2 else "Câmaras", " · ".join(cameras)), ("Data" if len(set(datas)) < 2 else "Período", periodo), ("Fotografias", str(len(p["galeria"])))]
    filtros = ""
    if len(grupos) > 1:
        filtros = ('<div class="pecas-filtros" role="group" aria-label="Filtrar fotografias">'
                   '<button type="button" class="pecas-filtro" data-grupo="" aria-pressed="true">Todas</button>'
                   + "".join(f'<button type="button" class="pecas-filtro" data-grupo="{esc(g)}" aria-pressed="false">{esc(g)}</button>' for g in grupos)
                   + '</div><p class="sr-only pecas-status" aria-live="polite"></p>')
    video = ""
    v = p.get("video")
    if v:
        video = f"""          <figure class="foto-video reveal">
            <video controls preload="none" playsinline muted poster="../assets/img/{v['poster']}" aria-describedby="video-desc">
              <source src="../assets/img/{v['src']}" type="video/mp4">
            </video>
            <figcaption><strong>{esc(v['titulo'])}</strong> <span id="video-desc">{esc(v['descricao'])}</span></figcaption>
          </figure>
"""
    ficha_html = "".join(f'<li><span class="ficha-k">{esc(a)}:</span> <span class="ficha-v">{esc(b)}</span></li>' for a, b in ficha if b)
    return f"""      <section class="modulo modulo-foto" aria-labelledby="mod-foto">
        <div class="container">
          <div class="modulo-head">
            <p class="eyebrow">Fotografia</p>
            <h2 id="mod-foto" class="modulo-title">Galeria</h2>
            <ul class="foto-ficha" aria-label="Ficha técnica">{ficha_html}</ul>
          </div>
{video}          {filtros}
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
    fonte, uso = fontes[0] if fontes else ("", "")
    amostra = ('''          <div class="tipo-amostra reveal" style="--fonte:'' + esc(fonte) + ''">
            <div class="tipo-cab">
              <p class="tipo-nome">' + esc(fonte) + '</p>
              <p class="tipo-uso">' + esc(uso) + '</p>
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
''') if fonte else ""
    titulo_mod = "Cores e tipografia" if fonte else "Cores"
    return f"""      <section class="modulo modulo-design" aria-labelledby="mod-design">
        <div class="container">
          <div class="modulo-head">
            <p class="eyebrow">Sistema visual</p>
            <h2 id="mod-design" class="modulo-title">{titulo_mod}</h2>
            <p class="modulo-lead">Clique numa cor para copiar o código HEX. O contraste indicado é o melhor entre texto branco e preto (WCAG).</p>
          </div>
          <ul class="paleta">
{chr(10).join(cores)}
          </ul>
          <p class="sr-only copiar-status" aria-live="polite"></p>
{amostra}          </div>
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
    detalhes = "".join(f'<li><span class="ficha-k">{esc(k)}:</span> <span class="ficha-v">{esc(v)}</span></li>'
                       for k, v in pub.get("detalhes", []))
    detalhes = f'<ul class="paper-detalhes" aria-label="Dados da publicação">{detalhes}</ul>' if detalhes else ""
    resumo = (f'<div class="paper-resumo reveal"><h3 class="paper-sub">Resumo <span lang="en">(Abstract)</span></h3>'
              f'<p lang="en">{esc(pub["resumo"])}</p></div>') if pub.get("resumo") else ""
    ler = (f'<a class="btn btn-primary" href="{pub["url"]}" target="_blank" rel="noopener">Ler o artigo na Springer <span aria-hidden="true">↗</span>'
           f'<span class="sr-only"> (abre num novo separador)</span></a>') if pub.get("url") else ""
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
            {detalhes}
            <p class="paper-ler">{ler}</p>
          </article>
          {resumo}
          <div class="paper-citar reveal">
            <h3 class="paper-sub">Como citar</h3>
            <p class="paper-citacao" id="citacao">{esc(pub["citacao"])}</p>
            <button type="button" class="btn btn-ghost" data-copiar-de="citacao">Copiar citação</button>
            <p class="sr-only copiar-status" aria-live="polite"></p>
          </div>
        </div>
      </section>"""


def modulo_uiux(p):
    """UI/UX: comparador esboço ↔ versão final (arrastar) e, se houver, simulador de dispositivos."""
    pares = p.get("comparar", [])
    html = ""
    if pares:
        botoes = "".join(
            f'<button type="button" class="comp-btn" data-par="{k}" aria-pressed="{"true" if k == 0 else "false"}">{esc(nome)}</button>'
            for k, (nome, esb, fin) in enumerate(pares))
        nome0, esb0, fin0 = pares[0]
        dados = "".join(f'<li data-esboco="../assets/img/{esb}" data-final="../assets/img/{fin}" data-nome="{esc(nome)}"></li>' for nome, esb, fin in pares)
        html += f"""      <section class="modulo modulo-comparar" aria-labelledby="mod-comp">
        <div class="container">
          <div class="modulo-head">
            <p class="eyebrow">Processo</p>
            <h2 id="mod-comp" class="modulo-title">Do esboço ao ecrã final</h2>
            <p class="modulo-lead">Arraste a linha (ou use as setas do teclado) para comparar o esboço em papel com o mockup de alta fidelidade.</p>
          </div>
          <div class="comp-botoes" role="group" aria-label="Escolher o ecrã">{botoes}</div>
          <div class="comp-palco" style="--pos:50%">
            <img class="comp-esboco" src="../assets/img/{esb0}" alt="Esboço em papel do ecrã {esc(nome0)}.">
            <img class="comp-final" src="../assets/img/{fin0}" alt="Mockup de alta fidelidade do ecrã {esc(nome0)}.">
            <span class="comp-linha" aria-hidden="true"><span class="comp-pega"></span></span>
            <span class="comp-rotulo comp-rotulo-a" aria-hidden="true">Esboço</span>
            <span class="comp-rotulo comp-rotulo-b" aria-hidden="true">Final</span>
            <input class="comp-range" id="comp-range" aria-label="Comparar esboço e versão final" type="range" min="0" max="100" value="50" aria-valuetext="50% versão final">
          </div>
          <ul class="comp-dados" hidden>{dados}</ul>
        </div>
      </section>"""
    if p.get("dispositivos"):
        html += "\n" + modulo_web(p)
    return html


MODULOS = {"uiux": modulo_uiux, "fotografia": modulo_fotografia, "design": modulo_design, "web": modulo_web,
           "video": modulo_video, "investigacao": modulo_investigacao}


def modulo_pecas(p):
    pecas = p.get("pecas", [])
    if not pecas:
        return ""
    grupos = []
    for pc in pecas:
        if pc[2] not in grupos:
            grupos.append(pc[2])
    filtros = '<button type="button" class="pecas-filtro" data-grupo="" aria-pressed="true">Todas</button>' + "".join(
        f'<button type="button" class="pecas-filtro" data-grupo="{esc(g)}" aria-pressed="false">{esc(g)}</button>' for g in grupos)
    itens = []
    for k, (img, nome, grupo, medida, alt) in enumerate(pecas):
        chips = f'<li><span class="sr-only">Grupo: </span>{esc(grupo)}</li>' + (f'<li><span class="sr-only">Medida: </span>{esc(medida)}</li>' if medida else "")
        itens.append(f"""          <li class="foto peca reveal" data-grupo="{esc(grupo)}">
            <button type="button" class="foto-abrir" data-foto="{k}" aria-label="Ver em ecrã inteiro: {esc(nome)}">
              <img src="../assets/img/{img}" alt="{esc(alt)}" loading="lazy">
            </button>
            <div class="foto-info"><p class="foto-leg">{esc(nome)}</p><ul class="foto-params" aria-label="Detalhes da peça">{chips}</ul></div>
          </li>""")
    return f"""      <section class="modulo modulo-pecas" aria-labelledby="mod-pecas">
        <div class="container">
          <div class="modulo-head">
            <p class="eyebrow">Peças</p>
            <h2 id="mod-pecas" class="modulo-title">Kit de comunicação</h2>
            <p class="modulo-lead">Cada peça com o seu formato real. Abra qualquer uma em ecrã inteiro.</p>
          </div>
          <div class="pecas-filtros" role="group" aria-label="Filtrar peças">{filtros}</div>
          <p class="sr-only pecas-status" aria-live="polite"></p>
          <ul class="pecas-grelha">
{chr(10).join(itens)}
          </ul>
        </div>
        <dialog class="lightbox" aria-label="Peça em ecrã inteiro">
          <div class="lightbox-inner">
            <figure class="lightbox-fig"><img src="" alt=""><figcaption><span class="lightbox-leg"></span><span class="lightbox-params"></span></figcaption></figure>
            <button type="button" class="lightbox-btn lightbox-prev" aria-label="Peça anterior"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button>
            <button type="button" class="lightbox-btn lightbox-next" aria-label="Peça seguinte"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button>
            <button type="button" class="lightbox-btn lightbox-close" aria-label="Fechar"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
            <p class="sr-only lightbox-status" aria-live="polite"></p>
          </div>
        </dialog>
      </section>"""


def modulo_versoes(p):
    vs = p.get("versoes", [])
    if len(vs) < 2:
        return ""
    total = len(vs)
    imgs = "".join(
        f'<img class="evo-img{" is-on" if k == total - 1 else ""}" data-k="{k}" src="../assets/img/{img}" alt="{esc(alt)}" loading="lazy">'
        for k, (img, nome, alt) in enumerate(vs))
    nomes = "".join(f'<li data-nome="{esc(nome)}"></li>' for img, nome, alt in vs)
    ultimo = vs[-1][1]
    return f"""      <section class="modulo modulo-evo" aria-labelledby="mod-evo">
        <div class="container">
          <div class="modulo-head">
            <p class="eyebrow">Processo</p>
            <h2 id="mod-evo" class="modulo-title">Evolução</h2>
            <p class="modulo-lead">Percorra as versões, da primeira estrutura à versão final.</p>
          </div>
          <div class="evo-controlos">
            <label for="evo-range" class="evo-label">Versão <output id="evo-out" for="evo-range">{total} de {total} · {esc(ultimo)}</output></label>
            <input type="range" id="evo-range" class="evo-range" min="1" max="{total}" value="{total}" step="1" aria-controls="evo-palco">
          </div>
          <div class="evo-palco" id="evo-palco">{imgs}</div>
          <ul class="evo-nomes" hidden>{nomes}</ul>
        </div>
      </section>"""


def modulo(p):
    f = MODULOS.get(p.get("tipo", "uiux"))
    return (f(p) if f else "") + modulo_pecas(p) + modulo_versoes(p)


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

# Demonstração com um painel de mota (usar com "demonstracao": "mota" no projeto)
DEMO_MOTA = """
          <div class="a11y-demo reveal">
            <p class="demo-label">Experimente: o painel adapta-se a si</p>
            <div class="demo-toggles" role="group" aria-label="Simular preferências do condutor no painel de exemplo">
              <button type="button" class="demo-btn" aria-pressed="false" data-demo="contrast">Contraste elevado</button>
              <button type="button" class="demo-btn" aria-pressed="false" data-demo="large">Texto maior</button>
              <button type="button" class="demo-btn" aria-pressed="false" data-demo="mono">Ver sem cores</button>
              <button type="button" class="demo-btn" aria-pressed="false" data-demo="dark">Modo noite</button>
            </div>
            <div class="demo-card demo-mota" role="group" aria-label="Painel de mota de exemplo">
              <div class="demo-top"><span class="demo-title">Painel de exemplo</span><span class="demo-chip demo-ok"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>Pronto a andar</span></div>
              <p class="demo-metric">72<span> km/h</span></p>
              <p class="demo-sub">Velocidade</p>
              <div class="demo-bar" role="progressbar" aria-label="Bateria" aria-valuenow="68" aria-valuemin="0" aria-valuemax="100"><span></span></div>
              <p class="demo-sub">Bateria 68 % · autonomia 54 km</p>
              <div class="demo-row"><span class="demo-chip demo-nav"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 19V11a4 4 0 0 1 4-4h8M14 3l4 4-4 4"/></svg>Direita em 200 m</span><span class="demo-chip demo-warn"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4l9 16H3zM12 10v4M12 17.5v.5"/></svg>Pressão do pneu traseiro</span></div>
            </div>
            <p class="demo-note">Como no modelo CAIA: cada condutor escolhe as suas preferências e o painel ajusta-se, sem perder informação.</p>
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
        # Demonstração interativa: nos artigos só quando faz sentido para o tema ("demonstracao" no projeto)
        demo = p.get("demonstracao", "geral" if p.get("tipo", "uiux") == "uiux" else None)
        if demo and titulo in ("Acessibilidade", "Contribuição"):
            corpo += DEMO_MOTA if demo == "mota" else DEMO.replace("{titulo}", esc(p["titulo"]))
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
