# Site Dra. Anita Nogiri — Odontologia

Reconstrução do zero do site **anitaodontologia.com.br** (Dra. Anita Nogiri Makowiecky, dentista).
Projeto da Freela In Home. Responder sempre em pt-BR.

## Briefing (em construção)
- **Site atual:** https://anitaodontologia.com.br/ (aproveitar conteúdo, cruzando com a ata da reunião)
- **Doctoralia:** https://www.doctoralia.com.br/perfil/anita-nogiri-makowiecky (dados + avaliações)
- **Ata da reunião:** `docs/ata-reuniao.md` (03/11/2026). Base do site para apresentação até 10/11; tráfego pago a partir de 05/12
- **Agendamento:** WhatsApp com robô (igual Pereira Oliveira). NÃO usar agendamento do Doctoralia
- **Avaliações:** exibidas separadas. Google: 4,9 com 36 avaliações (`data/avaliacoes-google.json`; a ata dizia 5.0/71, estava errado). Doctoralia: 5,0 com 232 (`data/avaliacoes.json`). NUNCA exibir as marcadas `suspeita: true` (Marcos Arnoldo com vídeo de riacho; José Aldo 1 estrela)
- **Imagens IA:** usar `GeminiWrapper` de `E:/Freela In Home/posts-project/vocical/gerador/gemini_wrapper.py` carregando o `.env` de lá (NÃO copiar a chave para este repo público). Script local em `tools/imagens/`. Nunca gerar "paciente" ou "resultado"
- **Serviços:** resumidos em UMA página de procedimentos, abordando um pouco cada um. As páginas longas de captação por procedimento ficam para DEPOIS, quando iniciar o tráfego pago (dezembro). Ela NÃO é especialista em implantodontia: nunca usar "especialista em implantes". Destacar facetas de porcelana e de resina
- **Mapa de páginas (aprovado):** Início, Sobre, Procedimentos (1 página, 10 procedimentos da ata com âncoras; SEM os extras do Doctoralia), Resultados, Blog, Contato, Links (bio). Ver `docs/cruzamento-e-mapa.md`
- **Horário:** segunda a sexta, 09:00 às 19:00
- **Redes (ícones):** Instagram @draanitanogiri, Facebook /consultorioanitanogiri, Google Meu Negócio (https://share.google/ItDjzE6pBWaWPDW2j), Doctoralia
- **Formação:** Odontologia UFPR (2000), especialista em Dentística Restauradora UFPR (2009), CRO-SC 10010. Atende em português e inglês. Só particular (PIX, cartões, transferência, dinheiro)
- **Contato:** WhatsApp (48) 99145-0038, tel (48) 3030-0038, anita@anitaodontologia.com.br, Rod. João Paulo, 695, sala 203, João Paulo, Florianópolis/SC, 88030-300
- **Cores da marca:** `#89c6cc` (turquesa claro, traço do dente) e `#00565d` (petróleo, nome). Assinatura: "Odontologia Integrada"
- **Logo:** `assets/logo/` (logo-colorido.png, logo-branco.png 250x100; favicon.png 512). Ideal ter SVG exportado do .ai
- **Blog:** sim, no mesmo modelo do site do Dr. Márcio (`E:\Clientes\Marcio Dermato\site-marciodermato`: `blog/<slug>/index.html` + gerador em `tools/blog`)
- **Galeria:** o site atual não tem foto real de procedimento (placeholders + banco). Fotos reais só do consultório (baixa res, melhorar com IA). Antes e depois virão do iCloud
- **Logo vetorial:** `E:\Clientes\Dra. Anita Nogiri\Logo\logo dra anita.ai`

## Stack
- HTML/CSS/JS estático (mesmo padrão do site do Márcio), sem build obrigatório
- Preview: GitHub Pages em `fabianohirtzz/site-anitaodontologia` (com `noindex` até produção)

## Regras de copy (padrão Freela)
- Sem travessões, sem emojis, números concretos
- Odontologia: respeitar regras do CFO para publicidade (sem promessa de resultado, sem preço como chamariz, antes/depois só conforme norma vigente)

## Estrutura
- `docs/` levantamentos, ata, specs
- `data/` dados estruturados (avaliações etc.)
- `assets/original/` imagens extraídas do site atual (brutas)
- `assets/` imagens tratadas para o site

## Estado atual
- Fase: 3. Build. Layout aprovado pela Dra. (11/11). Todas as páginas prontas (11/11): home, sobre, procedimentos, resultados (placeholders até as fotos do iCloud), contato, blog (3 posts), links
- Próximo: fotos de antes e depois em resultados.html; revisão dos artigos pela Dra.; produção (tirar noindex, robots Allow + Sitemap)
- Build: header/footer em `partials/` → `python tools/partials.py` (também atualiza blog/<slug>/ com ../../); avaliações da home → `python tools/avaliacoes.py`
- Blog: posts em `conteudo/blog/posts.json` + `conteudo/blog/<slug>.html` → `python tools/blog.py` (gera blog.html, posts, sitemap.xml e roda partials). Capas IA: `python -I tools/imagens/gerar.py <saida.webp> <w> <h> "<prompt>"` (Gemini, com crédito desde 05/11)
- SEO/GEO: cada página com title/description/canonical/OG, JSON-LD (Dentist, Person, FAQPage, BreadcrumbList, BlogPosting), caixa `.resposta` (resposta direta) e `llms.txt` na raiz
- Logo: `assets/logo/logo.svg` (vertical), `logo-horizontal.svg` (menu), `dente.svg` (elemento gráfico), versões brancas. Extraídos do .ai via PyMuPDF
- Fotos: `assets/img/*.webp`. Upscale fiel via Fal ESRGAN (`tools/imagens/upscale.py`). Gemini e OpenAI do gerador da Vocical estão SEM crédito (05/11)
- Obs.: repo antigo `site-anitaodontologia-travado` ficou corrompido no GitHub (503); recriado. Excluir o travado manualmente
