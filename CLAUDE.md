# Site Dra. Anita Nogiri — Odontologia

Reconstrução do zero do site **anitaodontologia.com.br** (Dra. Anita Nogiri Makowiecky, dentista).
Projeto da Freela In Home. Responder sempre em pt-BR.

## Briefing (em construção)
- **Site atual:** https://anitaodontologia.com.br/ (aproveitar conteúdo, cruzando com a ata da reunião)
- **Doctoralia:** https://www.doctoralia.com.br/perfil/anita-nogiri-makowiecky (dados + avaliações)
- **Ata da reunião:** `docs/ata-reuniao.md` (03/11/2026). Base do site para apresentação até 10/11; tráfego pago a partir de 05/12
- **Agendamento:** WhatsApp com robô (igual Pereira Oliveira). NÃO usar agendamento do Doctoralia
- **Avaliações:** Google (5.0, 71) e Doctoralia (200+), exibidas separadas
- **Serviços:** resumidos em UMA página de procedimentos, abordando um pouco cada um. As páginas longas de captação por procedimento ficam para DEPOIS, quando iniciar o tráfego pago (dezembro). Ela NÃO é especialista em implantodontia: nunca usar "especialista em implantes". Destacar facetas de porcelana e de resina
- **Formação:** Odontologia UFPR (2000), especialização (2009)
- **Cores da marca:** `#89c6cc` (turquesa claro, traço do dente) e `#00565d` (petróleo, nome). Assinatura: "Odontologia Integrada"
- **Logo:** `assets/logo/` (logo-colorido.png, logo-branco.png 250x100; favicon.png 512). Ideal ter SVG exportado do .ai
- **Blog:** sim, no mesmo modelo do site do Dr. Márcio (`E:\Clientes\Marcio Dermato\site-marciodermato`: `blog/<slug>/index.html` + gerador em `tools/blog`)
- **Galeria:** fotos atuais em baixa resolução, extrair e melhorar com IA
- **Logo:** `E:\Clientes\Dra. Anita Nogiri\Logo\logo dra anita.ai`

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
- Fase: 1. Descoberta / levantamento de conteúdo
- Próximo: receber ata, cruzar com conteúdo atual, definir mapa de páginas e design skill
