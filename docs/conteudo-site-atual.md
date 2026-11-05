# Inventário de conteúdo — site atual (anitaodontologia.com.br)

- **Coleta:** 04/11/2026, via curl do HTML bruto (o site é estático PHP/HTML, não depende de JS para o conteúdo).
- **Tecnologia:** template comercial "Medent" (HTML/Bootstrap 3 + jQuery), servidor Apache (hospedagem HostGator — aparece nas páginas de erro). Copyright no rodapé: "© 2016".
- **HTTPS:** responde em https; http também responde 200 sem redirecionar.
- **robots.txt:** existe ("User-agent: *", sem regras nem sitemap). **sitemap.xml:** não existe (404). **/blog:** não existe (erro 500). **Não há blog.**
- Os textos abaixo são copiados literalmente, inclusive erros de digitação (marcados com *[sic]* quando relevante).

## Mapa de páginas

| # | URL | Título (`<title>`) | Status |
|---|---|---|---|
| 1 | https://anitaodontologia.com.br/ (também `/index.php`) | Dra. Anita Nogiri Makowiecky - Consultório Odontológico | OK |
| 2 | /sobre | Sobre - Dra. Anita Nogiri Makowiecky - Consultório Odontológico | OK |
| 3 | /procedimentos | Dra. Anita Nogiri Makowiecky - Consultório Odontológico | OK |
| 4 | /galeria/consultorio | Fotos do Consultório - Dra. Anita Nogiri Makowiecky - Consultório Odontológico | OK |
| 5 | /galeria/procedimentos | Fotos de Procedimentos Realizados - Dra. Anita Nogiri Makowiecky - Consultório Odontológico | OK (mas só placeholders) |
| 6 | /galeria/procedimentos/facetas | (sem `<title>`; fragmento sem cabeçalho/rodapé) | Página órfã — cópia antiga do "Agende" |
| 7 | /contato | Dra. Anita Nogiri Makowiecky - Consultório Odontológico | OK |
| 8 | /agende | Dra. Anita Nogiri Makowiecky - Consultório Odontológico | OK |
| — | /gallery-single.html | Página demo do template "Medent" esquecida no servidor (menu em inglês, conteúdo fictício) | Lixo de template |
| — | /about.html, /team_member.html | 404 — mas são linkados pelo botão "Saiba mais" da página Sobre e pelos títulos dos cards de Procedimentos | Links quebrados |

**Meta description (igual em todas as páginas):** "Consultório Odontológico no João Paulo, Florianópolis. Dra. Anita Nogiri Makowiecky, especialista em Dentística e Odontologia Estética."
**Meta keywords:** "dentista, dentistas, implantes, joao paulo, florianópolis, odontologia, restauração, próteses dentárias"
**Outras metas:** `DC.title` "Dentista no João Paulo, Florianópolis. ", `geo.region` BR-SC, `geo.placename` Florianópolis. Não há Open Graph, canonical, schema.org nem Google Analytics.

---

## Elementos globais (todas as páginas)

### Cabeçalho / menu
Logo (imagem `images/logo-dentista.png`, via CSS) + menu:
- Início (`index.php`)
- Sobre (`/sobre`)
- Procedimentos (`/procedimentos`)
- Galeria (`#`) → submenu: **Consultório** (`galeria/consultorio`) · **Procedimentos Realizados** (`galeria/procedimentos`)
- Contato (`/contato`)
- AGENDE (`/agende`)

Há também um modal de busca oculto herdado do template (placeholder "Search keyword", botão "Pesquisa") — sem função.

### Rodapé
Coluna 1 — logo (`images/logo_bottom.png`) + texto:
> Odontóloga formada em 2000 pela Universidade Federal do Paraná. Em 2009 concluiu o curso de especialização em Dentística Estética Restauradora.

Ícones sociais: Facebook, Twitter, Google, Youtube — **todos com `href="#"` (não levam a lugar nenhum)**.

Coluna 2 — **Contato**
- 48 3030-0038 (ícone de fax)
- 48 99145-0038 (ícone de telefone)
- anita@anitaodontologia.com.br (ícone de "database")

Coluna 3 — **Endereço**
- Rodovia João Paulo, 695 - sala 203
- Bairro: João Paulo
- 09:00 - 19:00

Coluna 4 — widget do Doctoralia (script `platform.docplanner.com/js/widget.js`, tipo "big", com opiniões), link: "Anita Nogiri Makowiecky - Doctoralia.com.br" → https://www.doctoralia.com.br/anita-nogiri-makowiecky/dentista/florianopolis

Barra final: "© 2016 Consultório Dra. Anita Nogiri Makowiecky"

### Mapa
Iframe do Google Maps com o lugar "Consultório Odontológico Dra. Anita Nogiri Makowiecky" (coord. aprox. -27.5666, -48.5181). Também há um script antigo de Google Maps API com chave exposta e geocodificação para "695 Rodovia João Paulo, Florianópolis, SC 90401" (CEP errado) e marcador "Map title / Map HTML description" (texto de template).

---

## 1. Início — https://anitaodontologia.com.br/

### Slider (hero, 3 slides)
| Slide | Imagem | Título (h3) | Texto | CTA → link |
|---|---|---|---|---|
| 1 | images/dentista2.jpg (alt "Dentistas Florianópolis") | Odontologia Integrada | Beleza e saúde andam juntos. | **Agende uma avaliação** → /agende |
| 2 | images/dentista.jpg (alt "Dentistas João Paulo") | Cuide do seu sorriso | O sorriso define a personalidade. Tenha um sorriso marcante! | **Marque sua consulta** → /agende |
| 3 | images/dentista3.jpg (alt "Dentista Floripa") | Saúde Bucal | Diversos tratamentos para realçar o seu sorriso. | **Marque uma consulta** → /agende |

### Faixa de diferenciais (4 boxes)
- **Especialista** — "A Dra. Anita Nogiri Makowiecky é especialista em Dentística Restauradora pela UFPR."
- **Estrutura** — "Consultório moderno e técnicas precisas para garantir resultado de qualidade."
- **Experiência** — "Dentista com mais de 15 anos de experiência e inúmeros tratamentos realizados."
- **Biosegurança** *[sic]* — "O controle de infecção é nossa preocupação na prevenção de transmissão de doenças."

### Sobre (bloco resumo)
Imagem: images/consultorio-dra-anita.jpg (alt "Consultório Dra. Anita Nogiri Makowiecky") — colagem de 6 fotos do consultório com moldura azul.

Título: **Sobre**
> Dra Anita Nogiri Makowiecky, é odontóloga, formada em 2000 pela Universidade Federal do Paraná. Em 2009 concluiu o curso de especialização em Dentística Estética Restauradora, onde apresentou um trabalho de conclusão sobre a reabilitação estética de um sorriso com resina e facetas de porcelana. Trabalho que ganhou relevância e foi publicado Revista Clínica.

Barras de "habilidade" (todas em 100%): Profilaxia e Remoção de Tártato *[sic]* · Facetas de Porcelana · Clareamento · Implantes · Extração · Restaurações · Próteses em geral

CTA: **Saiba mais** → /sobre

### Procedimentos (8 ícones, todos linkando para /procedimentos, sem descrição)
Restaurações Estéticas · Próteses · Periodontia · Profilaxia e Limpeza · Clareamento · Implantes dentários · Extrações · Endodontia

### Blocos comentados no HTML (não aparecem para o visitante)
- "Galeria de procedimentos" com 6 imagens (facetas-home, clareamento-home, dentista-jp, facetas-protese, restauracoes-horizontal [título "Implantes Dentários"], protese-total) — fotos de banco de imagem.
- "Depoimentos" (os mesmos 3 da página Sobre, com fotos face01–03 = placeholder idêntico).

### Call to action
> Dentista para quem ama sorrir!
> (48) 3030-0038

Botão **Agende uma consulta** → `#` (link morto na home).

Depois: mapa + rodapé.

---

## 2. Sobre — /sobre

Breadcrumb: Início › Sobre (h1 "Sobre")

Bloco idêntico ao "Sobre" da home (mesma imagem, mesmo parágrafo, mesmas barras 100%). O botão **Saiba mais** aqui aponta para `about.html` → **404**.

### Call to action
> Dentista pra quem ama sorrir!
> 48 3030-0038

Botão **Marque sua consulta** → /agende

### Depoimentos (carrossel, 3 itens)
1. "Sempre tive medo de dentista, mas a Dra. Anita me fez relaxar. Ela é demais, melhor dentista do mundo!" — **Ana Sophia** (foto images/ana-sophia.jpg, 80×80)
2. "Profissional dedicada e estudiosa. Fico super tranquila a ser tratada por ela. O resultado sempre é maravilhoso. " — **Sandra** (images/sandra.jpg)
3. "Minha dentista preferida. Sempre muito profissional, tenho plena segurança quando sento em sua cadeira." — **José Maurício** (images/jose-mauricio.jpg)

(Fonte/origem desses depoimentos não é indicada no site. Os textos não aparecem no Doctoralia; lá existe uma "Sandra" (06/10/2021) com outro texto, e não há "Ana Sophia" nem "José Maurício".)

---

## 3. Procedimentos — /procedimentos

Breadcrumb: Início › Procedimentos (h1 "Procedimentos")

6 cards (imagem quadrada 460×460 + título + texto). Os títulos linkam para `team_member.html` → **404**.

### Facetas de Porcelana
Imagem: images/facetas-de-porcelana.jpg
> As facetas são um meio rápido de conseguir um sorriso esteticamente perfeito. Com elas conseguimos alterar forma e cor, sendo indicadas em dentes escurecidos por tratamento de canal, lascados, com formas atípicas, em dentes mal posicionados ou apresentando espaços entre eles, os famosos diastemas.

### Lentes de contato
Imagem: images/lente-de-contato-dental.jpg (alt "Lentes de Contato dentária")
> São versões mais modernas do que as facetas, porem com algumas restrições em suas indicações. A diferença está no desgaste do remanescente dentário, onde fazemos um mínimo desgaste ou até mesmo sem desgastes para obtermos um resultado estético marcante. Veja mais: Lentes de Contato

Link externo: "Veja mais: Lentes de Contato" → http://www.ivoclarvivadent.com.br/pt-br/facetas-laminadas-do-tipo-lente-de-contato (site de fabricante; manda o paciente para fora).

### Restaurações Estéticas
Imagem: images/restauracoes.jpg (alt "Restaurações Estéticas em Resina")
> São procedimentos para recuperar lesões cariosas ou fragmentos fraturados. Podem ser feitos em resina comum ou cerâmica, recuperando a estética e a saúde bucal.

### Implantes
Imagem: images/implantes.jpg (alt "Implantes dentários")
> Os implantes são estruturas de titânio, colocadas cirurgicamente no osso da maxila ou mandíbula, para substituir as raízes de dentes perdidos ou inexistentes permitindo assim a colocação de próteses sobre esses mesmo, devolvendo a função de um dente natural. Para receber um implante, é preciso que o paciente tenha gengivas saudáveis e ossos adequados para sustentá-lo. O paciente também deve comprometer-se a manter estas estruturas saudáveis. Uma higiene bucal meticulosa e visitas regulares ao dentista são essenciais para o sucesso a longo prazo dos implantes.

### Clareamento
Imagem: images/clareamento-dental-caseiro.jpg (alt "Clareamento Dental Caseiro")
> O clareamento é um procedimento clínico usado para clarear a cor de dentes amarelados ou manchados, devolvendo a estética e naturalidade do seu sorriso. Pode ser feito no consultório, um procedimento mais rápido onde em algumas sessões chegamos à um resultado satisfatório ou o caseiro, onde é feito uma moldeira personalizada e as aplicações são feitas em casa pelo próprio paciente. Para resultados ainda mais brilhantes, podemos fazer uma combinações das duas técnicas.

### Próteses
Imagem: images/proteses-dentarias.jpg (alt "Prótestes dentárias" *[sic]*)
> A falta de dentes, além de desagradável, pode causar diversos problemas. Prejudica a mastigação, a fonética e a estética do paciente. Neste caso é necessária a confecção de próteses dentárias. Este procedimentos é bastante comum e visa repor um ou mais dentes perdidos. Hoje contamos com materiais e técnicas que deixam o seu sorriso o mais natural possível.

Depois: mapa + rodapé. Não há CTA de agendamento nesta página.

---

## 4. Galeria › Consultório — /galeria/consultorio

Breadcrumb: Início › Galeria › Consultório (h1 "Fotos do Consultório")

6 fotos (todas 438×292, abrem em lightbox prettyPhoto com título "Consultório Dra. Anita Nogiri Makowiecky"):

| Imagem | alt | Legenda |
|---|---|---|
| images/gallery/consultorio-joao-paulo.jpg | Consultório Odontológico João Paulo | Consultório |
| images/gallery/dentista-florianopolis.jpg | Dentistas Florianópolis | Escritório |
| images/gallery/dentista-joao-paulo.jpg | Dentista no João Paulo | Recepção |
| images/gallery/dentistas-joao-paulo.jpg | Dentistas em João Paulo | Recepção |
| images/gallery/dentistas-florianopolis.jpg | Dentistas em Florianópolis | Consultório |
| images/gallery/odonto-joao-paulo.jpg | Consultório Odontológico no João Paulo | Escritório |

CTA: **Conheça a Dra. Anita** → /sobre

---

## 5. Galeria › Procedimentos Realizados — /galeria/procedimentos

Breadcrumb: Início › Procedimentos (h1 "Procedimentos")

9 itens — **todas as 9 imagens (images/gallery/01.jpg … 09.jpg) são retângulos azuis lisos de placeholder do template, sem nenhuma foto real.** Legendas:

1. Facetas de Porcelana (link → galeria/procedimentos/facetas — página órfã, ver abaixo)
2. Lentes de Contato (link → gallery-single.html — demo do template)
3. Implantes
4. Próteses
5. Restaurações
6. Extrações
7. Raspagem de Tártato *[sic]* e Profilaxia
8. Tratamento de Canal
9. Raspagem de Tártato *[sic]* e Profilaxia (repetido)

CTA: **Veja mais** → `#` (link morto).

---

## 6. /galeria/procedimentos/facetas (página órfã)

Fragmento sem cabeçalho, rodapé ou CSS — é uma cópia antiga da página "Agende" (h1 "Agende", "Agende sua consulta por e-mail"), com placeholders do formulário **em inglês** ("Full Name", "Subject", "Phone number", "Email", "Message") e **outro WhatsApp: 48 99644-4433** (diferente do atual 48 99145-0038). Endereço/horário/telefone fixo iguais.

---

## 7. Contato — /contato

Breadcrumb: Início › Contato (h1 "Contato"). Mapa no topo.

3 blocos:
- **Telefone:** 48 3030-0038 / **Whatsapp:** 48 99145-0038
- Rodovia João Paulo, 695 - sala 203 / Bairro: João Paulo / Florianópolis, SC
- anita@anitaodontologia.com.br + ícones Twitter, Facebook, Google, Pinterest (todos `href="#"`)

Formulário: Nome completo · E-mail · Assunto · Mensagem → botão **Enviar Mensagem**. O `action` é "/" (envia para a home) — **não há indício de processamento; provavelmente não envia nada.**

---

## 8. Agende — /agende

Breadcrumb: Início › Agende sua Consulta (h1 "Agende")

Título do formulário: **Agende sua consulta por e-mail**
Campos: Nome Completo · Assunto · Telefone · E-mail · Mensagem → botão **Enviar Messagem** *[sic]* (mesmo problema: `action="/"`).

Coluna "Contato":
- Rodovia João Paulo, 695 - sala 203
- 09:00 - 19:00
- 48 3030-0038
- 48 99145-0038 (Whatsapp)

Não há link de WhatsApp clicável (wa.me) em nenhuma página, nem link para o agendamento online do Doctoralia.

---

## Contatos consolidados

| Item | Valor no site | Observação |
|---|---|---|
| Telefone fixo | (48) 3030-0038 | igual no Doctoralia |
| WhatsApp | (48) 99145-0038 | igual no Doctoralia; não clicável. Página órfã mostra 48 99644-4433 (antigo?) |
| E-mail | anita@anitaodontologia.com.br | só texto, sem `mailto:` |
| Endereço | Rodovia João Paulo, 695 - sala 203 — Bairro João Paulo — Florianópolis, SC | CEP não aparece no site; Doctoralia: 88030300 (no script do mapa aparece "90401", errado) |
| Horário | 09:00 - 19:00 | não indica dias da semana |
| Facebook | — (`#`) | real: https://www.facebook.com/consultorioanitanogiri/ (via Doctoralia) |
| Instagram | — (não existe no site) | real: https://www.instagram.com/draanitanogiri/ (via Doctoralia) |
| Twitter / Google / YouTube / Pinterest | ícones com `#` | sem perfil informado |
| Doctoralia | widget no rodapé | https://www.doctoralia.com.br/perfil/anita-nogiri-makowiecky |

## Tratamentos/serviços citados no site

| Tratamento | Onde aparece | Tem descrição? |
|---|---|---|
| Facetas de Porcelana | Procedimentos, Sobre (barra), Galeria | Sim |
| Lentes de contato | Procedimentos, Galeria | Sim |
| Restaurações Estéticas | Home, Procedimentos, Sobre, Galeria | Sim |
| Implantes (dentários) | Home, Procedimentos, Sobre, Galeria | Sim |
| Clareamento | Home, Procedimentos, Sobre | Sim |
| Próteses (em geral) | Home, Procedimentos, Sobre, Galeria | Sim |
| Periodontia | Home | Não |
| Profilaxia e Limpeza / Remoção (Raspagem) de Tártaro | Home, Sobre, Galeria | Não |
| Extrações | Home, Sobre, Galeria | Não |
| Endodontia / Tratamento de Canal | Home, Galeria | Não |

---

## Imagens do site

Todas baixadas em `assets/original/` (ver `assets/original/INVENTARIO.md` para dimensões). URL base: `https://anitaodontologia.com.br/`. O site não usa srcset nem variantes de tamanho (não é WordPress); a URL direta é o único tamanho existente — diretórios `/images/` e `/images/gallery/` não são listáveis (403).

| URL | Página / contexto | Arquivo local | Observação |
|---|---|---|---|
| images/dentista.jpg | Home, slide 2 | outros/site-slider-dentista.jpg | Banco de imagem (boca com espelho) |
| images/dentista2.jpg | Home, slide 1 | outros/site-slider-dentista2.jpg | Banco de imagem (dentista de touca/máscara — não é a Dra.) |
| images/dentista3.jpg | Home, slide 3 | outros/site-slider-dentista3.jpg | Banco de imagem (instrumentais) |
| images/consultorio-dra-anita.jpg | Home e Sobre, bloco "Sobre" | consultorio/site-consultorio-dra-anita.jpg | Colagem real do consultório, 500×665 |
| images/gallery/consultorio-joao-paulo.jpg | Galeria Consultório | consultorio/site-galeria-consultorio-joao-paulo.jpg | Real, 438×292 |
| images/gallery/dentista-florianopolis.jpg | Galeria Consultório | consultorio/site-galeria-dentista-florianopolis.jpg | Real, 438×292 |
| images/gallery/dentista-joao-paulo.jpg | Galeria Consultório | consultorio/site-galeria-dentista-joao-paulo.jpg | Real, 438×292 |
| images/gallery/dentistas-joao-paulo.jpg | Galeria Consultório | consultorio/site-galeria-dentistas-joao-paulo.jpg | Real, 438×292 |
| images/gallery/dentistas-florianopolis.jpg | Galeria Consultório | consultorio/site-galeria-dentistas-florianopolis.jpg | Real, 438×292 |
| images/gallery/odonto-joao-paulo.jpg | Galeria Consultório | consultorio/site-galeria-odonto-joao-paulo.jpg | Real, 438×292 |
| images/gallery/01.jpg … 09.jpg | Galeria Procedimentos Realizados | galeria/site-galeria-01.jpg … 09.jpg | **Placeholders azuis lisos** |
| images/gallery/facetas-home.jpg | Home (bloco comentado) | galeria/site-galeria-facetas-home.jpg | Banco de imagem — tem marca "Shutterstock" |
| images/gallery/clareamento-home.jpg | Home (comentado) | galeria/site-galeria-clareamento-home.jpg | Banco de imagem (antes/depois genérico) |
| images/gallery/dentista-jp.jpg | Home (comentado) | galeria/site-galeria-dentista-jp.jpg | Banco de imagem |
| images/gallery/facetas-protese.jpg | Home (comentado) | galeria/site-galeria-facetas-protese.jpg | Banco de imagem |
| images/gallery/restauracoes-horizontal.jpg | Home (comentado) | galeria/site-galeria-restauracoes-horizontal.jpg | Banco de imagem |
| images/gallery/protese-total.jpg | Home (comentado) | galeria/site-galeria-protese-total.jpg | Banco de imagem |
| images/facetas-de-porcelana.jpg | Procedimentos | galeria/site-procedimento-facetas-de-porcelana.jpg | Foto clínica/ilustrativa, 460×460 |
| images/lente-de-contato-dental.jpg | Procedimentos | galeria/site-procedimento-lente-de-contato-dental.jpg | Ilustrativa, 460×460 |
| images/restauracoes.jpg | Procedimentos | galeria/site-procedimento-restauracoes.jpg | Ilustrativa, 460×460 |
| images/implantes.jpg | Procedimentos | galeria/site-procedimento-implantes.jpg | Ilustração 3D, 460×460 |
| images/clareamento-dental-caseiro.jpg | Procedimentos | galeria/site-procedimento-clareamento-dental-caseiro.jpg | Banco de imagem, 460×460 |
| images/proteses-dentarias.jpg | Procedimentos | galeria/site-procedimento-proteses-dentarias.jpg | Ilustrativa, 460×460 |
| images/ana-sophia.jpg, sandra.jpg, jose-mauricio.jpg | Sobre, depoimentos | outros/site-depoimento-*.jpg | 80×80 |
| images/face01.jpg, face02.jpg, face03.jpg | Home, depoimentos (comentado) | outros/site-depoimento-face0*.jpg | Placeholder idêntico, 80×80 |
| images/logo-dentista.png | Cabeçalho (via CSS) | outros/site-logo-dentista.png | 260×74 — antigo, baixa resolução |
| images/logo_bottom.png | Rodapé (via CSS) | outros/site-logo_bottom.png | 180×52 |
| favicon.ico | Todas | outros/site-favicon.ico | 32×34 |
| images/parallax/services.jpg, bottom.jpg, breadcrumbs.jpg, map.jpg; images/banner-section-bg.jpg | Fundos via CSS | outros/site-bg-*.jpg | services/bottom/breadcrumbs = placeholders azuis; map = mapa genérico; banner = textura |
| img/certification.png, time.png, personal.png, like.png, marker.png, ícones de serviço | Ícones do template | não baixados | ícones genéricos do tema |

Logos vetoriais/atuais **já existem fora do site**, em `E:\Clientes\Dra. Anita Nogiri\Logo\` (logo dra anita.ai, logo-colorido.png, logo-branco.png, favicon.png) e em `anita-project/assets/logo/` — usar esses em vez do logo do site.

---

## O que parece desatualizado ou fraco

**Quebrado / técnico**
- Galeria "Procedimentos Realizados" inteira com placeholders azuis — a página não mostra nenhum caso real.
- Links quebrados: "Saiba mais" (Sobre) → about.html 404; títulos dos cards de Procedimentos → team_member.html 404; "Agende uma consulta" (home) → `#`; "Veja mais" (galeria) → `#`; "Lentes de Contato" na galeria → página demo do template.
- Ícones de redes sociais todos com `#`, e as redes reais (Instagram @draanitanogiri, Facebook consultorioanitanogiri) não aparecem.
- Formulários de Contato/Agende com `action="/"` — provavelmente não enviam nada (leads perdidos).
- WhatsApp não é clicável; não há botão flutuante; e-mail sem `mailto:`; telefone sem `tel:`.
- Página órfã /galeria/procedimentos/facetas com WhatsApp antigo (48 99644-4433) e placeholders em inglês — indexável.
- /gallery-single.html (demo "Medent") publicada no servidor.
- `<title>` repetido em várias páginas, mesma meta description em todas, sem OG/canonical/schema/sitemap.
- Script do Google Maps com chave de API exposta e CEP errado (90401); marcador "Map title".
- Encoding misto (algumas páginas com acentos corrompidos no HTML-fonte).
- Copyright "© 2016"; template de ~2016 (Bootstrap 3, jQuery, IE8 shims).

**Conteúdo**
- "mais de 15 anos de experiência" → defasado (formada em 2000 = 26 anos, como diz o Doctoralia).
- Barras de "habilidade" a 100% (Profilaxia, Facetas, Clareamento, Implantes, Extração...) — recurso de template, pouco crível.
- Erros de digitação: "Tártato" (2×), "Biosegurança", "Messagem", "Prótestes", "foi publicado Revista Clínica", "esses mesmo", "chegamos à um", "uma combinações", "Este procedimentos", "Dentista pra quem ama sorrir" vs "para".
- Só 6 tratamentos têm descrição; Periodontia, Profilaxia, Extração e Endodontia aparecem só como ícone. Faltam serviços que o Doctoralia lista (ortodontia/alinhadores/Invisalign, placa de bruxismo, gengivoplastia, coroas de cerâmica, recontorno estético, piercing dental etc.).
- Sem foto da Dra. Anita no site (o slider usa banco de imagem com outra pessoa de touca e máscara). A foto real existe no Doctoralia.
- Sem CRO visível (CRO-SC 10010 está no Doctoralia), sem menção a "atende só particular", formas de pagamento, estacionamento, idioma inglês.
- Depoimentos do site: só 3, sem fonte, com fotos genéricas — enquanto o Doctoralia tem 232 avaliações 5★ reais.
- Horário "09:00 - 19:00" sem dias da semana.
- Imagens de banco de imagem (uma com marca Shutterstock) e fotos reais do consultório em baixa resolução (438×292).
- Link externo para site de fabricante (Ivoclar) tirando o paciente do site.
