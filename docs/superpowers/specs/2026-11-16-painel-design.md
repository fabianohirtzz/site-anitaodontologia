# Painel, robô de WhatsApp e relatórios: Dra. Anita Nogiri (design)

Data: 16/11/2026 · Autor: Claude com Fabiano (Freela In Home) · Status: aguardando aprovação do Fabiano (revisado por um leitor independente)

## 1. Intenção e porquê

A proposta comercial aceita pela Dra. Anita (plano mensal, `freelainhome-main/propostas/proposal-RJHjfg6vKpMpwa9HWgm1ivCj`) promete, além do site:

1. **WhatsApp automático** pela plataforma oficial da Meta, no mesmo número do consultório, que responde as dúvidas de sempre, faz a triagem (tratamento, período e dia preferidos), manda sozinho o link da ficha de cadastro quando a consulta é marcada e silencia quando alguém do consultório responde.
2. **Pedido de avaliação no Google** no dia seguinte à consulta marcada como feita, mais um disparo único para a base antiga de pacientes.
3. **Painel de leads e funil**: origem de cada contato (Google Ads, orgânico, Instagram, indicação), cliques no WhatsApp do site, etapas até o tratamento fechado e retorno do investimento.
4. **Tudo editável numa tela simples**: textos do robô, perguntas frequentes, pedidos de avaliação e a galeria de casos do site.

O porquê, nas palavras da proposta: "um painel que mostra de onde veio cada paciente e quanto cada real investido voltou", sem a Dra. parar o atendimento para cuidar de internet. O tráfego pago (Google Ads) começa em **05/12/2026**; a partir daí, cada real precisa ser medido.

Decisões do Fabiano nesta conversa:
- Hospedagem: **HostGator** (estrutura do cliente; não vai para a Vercel, apesar do que diz a proposta). Banco e autenticação: **Supabase**.
- Caminho: **reaproveitar a base da Pereira Oliveira Turismo** (`E:\Clientes\Pereira Oliveira Turismo\po-tu-project`, "PO").
- Avaliações: as novas entram sozinhas; **nota 4 ou 5 vai direto para o site; abaixo de 4 fica pendente com notificação no painel** para a Dra. decidir.
- Casos de Resultados: entram no painel se for simples (e a proposta promete).
- Blog: entra no painel (modelo do Dr. Márcio).

## 2. Metas, não metas, antimetas

**Metas**
- Até 05/12: todo contato que chega pelo WhatsApp (do site, do anúncio ou direto) vira lead com origem, e o painel mostra funil e retorno do investimento.
- Robô no ar assim que a Meta liberar o número.
- A Dra. e a auxiliar operam tudo sem chamar a Freela: mudar texto do robô, marcar consulta, registrar tratamento fechado, moderar avaliação, publicar caso.

**Não metas** (fora do escopo da proposta)
- Agendamento pelo site e integração com Doctoralia ou Easy Dental. A agenda continua neles.
- Responder o paciente pelo painel. A conversa humana continua no celular; o painel só mostra a conversa (como na PO).
- Anúncios em Instagram/Facebook.

**Antimetas** (seria fracasso mesmo funcionando)
- O robô parecer robô "quadradão" ou insistir depois que a auxiliar assumiu a conversa.
- O número do consultório sair do celular, ser bloqueado ou perder conversas.
- Qualquer texto do site, do robô ou dos modelos de mensagem com as palavras "antes" e "depois" (regra de anúncios de saúde do Google, ver CLAUDE.md), promessa de resultado ou preço como chamariz (CFO).
- Guardar dados sensíveis da ficha (CPF, RG, endereço) no nosso banco. A ficha continua sendo o formulário que o consultório já usa; o robô só manda o link.

## 3. Restrições

- **HostGator compartilhada**: PHP, sem Node e sem processo contínuo. Tarefas agendadas pelo cron do cPanel. Webhook da Meta precisa de HTTPS no domínio.
- **Site estático** (HTML gerado por `tools/*.py`), repositório público `fabianohirtzz/site-anitaodontologia`. Nada de segredo ou dado de paciente no repositório.
- **Supabase: projeto do HD360** (`euzmbswywwhmicjlszqw`), o compartilhado entre clientes de baixo volume de dados (decisão do Fabiano, 17/11). Tabelas da Dra. Anita com prefixo **`an_`**.
- **Meta**: conexão em modo de convivência (o app WhatsApp Business continua no celular), via app Tech Provider da Freela, como em `po/conectar-numero.php`. Verificação leva de alguns dias a duas semanas. Mensagem fora da janela de 24h só com **modelo aprovado** e é cobrada (aprox. R$ 0,31 por contato na campanha da base antiga, centavos no pedido de avaliação).
- **LGPD**: telefone e nome do paciente ficam no Supabase com RLS. Como o projeto é compartilhado, "autenticado" não basta: toda tabela `an_*` tem política que exige o usuário estar em `an_usuarios` (`exists (select 1 from an_usuarios where user_id = auth.uid())`). Nenhuma política `using (true)` em tabela `an_`. Um login de outro cliente no mesmo projeto não lê nada da Dra. Teste obrigatório: logar com usuário que não é da Dra. e confirmar zero linhas.
- **Risco herdado**: o robô da PO **nunca rodou com cliente real** (cron não cadastrado, webhook não inscrito, fluxos desligados; `po/CLAUDE.md:1673-1676`). O código tem ~94 testes, mas a primeira operação real será a da Dra. Anita ou a da PO, o que vier primeiro.

## 4. Abordagens consideradas

| | Abordagem | Troca | Decisão |
|---|---|---|---|
| A | **Reaproveitar a base PHP da PO** na HostGator (webhook, motor do robô, cron, campanhas, painel HTML/JS com Supabase), adaptando para odontologia | Mais rápido até 05/12 e mesma operação de deploy que a Freela já conhece; herda as manhas da hospedagem compartilhada (cache, FTP) e o risco de nunca ter rodado em produção | **Escolhida** |
| B | Painel na HostGator, mas robô e tarefas agendadas em Supabase Edge Functions e pg_cron | Não depende do host para o crítico; exige reescrever o back-end da PO em TypeScript, mais lento e arriscado para o prazo | Descartada |
| C | Robô de plataforma pronta (ManyChat, BotConversa) + painel próprio | Mensalidade e menos controle; a proposta promete robô sem custo fixo | Descartada |

## 5. Arquitetura (o que o Fabiano decidiu e o que eu proponho)

```
Site estático (HostGator)          Painel /painel (HostGator, HTML/JS)
  │ clique no WhatsApp                │ supabase-js (login, RLS)
  ▼                                   ▼
clique.php ──grava──► Supabase (tabelas an_*) ◄── PHP com service key
                                      ▲
Meta Cloud API ──webhook──► whatsapp.php ──► motor do robô (lib/wa-*)
                                      ▲
cron do cPanel ──► wa-cron.php: prazos 24h, perdidos por inatividade,
                   fila agendada (avaliação D+1, ficha), campanha,
                   importação diária de avaliações
Botão "Publicar" (painel) ──► GitHub Actions: tools/*.py lendo Supabase
                              ──► commit ──► FTPS para a HostGator
```

- **Back-end**: cópia adaptada da PO (`whatsapp.php`, `wa-cron.php`, `conectar-numero.php`, `templates.php`, `campanha.php`, `lib/wa-*`, `lib/po-auth.php` renomeado), prefixo `an_`, sem o que é só de turismo (roteiros, PDFs com Gemini, datas de saída, destinos, lista de espera, importador do CRM do Toninho).
- **Publicação do site** (avaliações, casos, blog): mesmo modelo do Dr. Márcio (`site-marciodermato/.github/workflows/publish-blog.yml`): o painel marca "alterações não publicadas"; o botão "Publicar" dispara o workflow, que roda `tools/avaliacoes.py`, `tools/blog.py` e o gerador de casos lendo o Supabase, faz commit e sobe por FTPS. O repositório continua sendo a fonte da verdade do site estático.
- **Painel**: base `po/painel` (HTML/JS, supabase-js por CDN), com a identidade visual da Dra. Anita (tokens da skill `anita-design`), um único login como na PO, mais um segundo usuário para a auxiliar se o Supabase Auth permitir sem papéis (mesmos poderes).

## 6. Funil (status do lead)

| Etapa | Como avança | Efeito |
|---|---|---|
| Contato feito | Automático: primeira mensagem no WhatsApp | Grava nome, telefone, origem |
| Qualificado | Automático: robô coletou tratamento de interesse e preferência de período/dia | |
| Consulta marcada | Um clique da auxiliar no painel (ou atalho `#marcada` digitado no celular) | Envia o link da ficha de cadastro (texto livre se a janela de 24h estiver aberta; senão, modelo aprovado) |
| Consulta feita | Um clique (ou `#feita`) | Agenda o pedido de avaliação para o dia seguinte, 10h |
| Tratamento fechado | Um clique com **tratamento** (lista dos 10 procedimentos do site + "outro") e **valor** (ou `#fechou 4800 facetas`) | Entra no faturamento e no retorno do investimento |
| Perdido | Automático: sem resposta no fim da janela de 24h (como na PO) **ou** N dias sem avançar depois de Qualificado (N=30, configurável) | |

"Consulta feita" é uma etapa nova em relação à proposta, necessária para disparar a avaliação; um paciente pode ir de Consulta feita para Tratamento fechado ou parar ali (só consulta).

## 7. Origem do contato e cliques no WhatsApp do site

O site não tem formulário: quase todo contato chega pelo WhatsApp. Para saber se veio de anúncio ou orgânico:

1. Todo link `data-wa` do site passa por `clique.php` (ou um `fetch` com `keepalive` antes de abrir o `wa.me`), que grava em `an_cliques`: página, UTM, `gclid`, referrer e um **código curto** gerado na hora.
2. O texto pré-preenchido do WhatsApp termina com esse código (ex.: "Olá, Dra. Anita! Gostaria de agendar uma avaliação. (ref. 4821)").
3. Na primeira mensagem, o motor procura o código, liga o lead ao clique e herda a origem (pago se `gclid`/`utm_medium=cpc`, orgânico, social, direto, como `classifyChannel` da PO).
4. Contato sem código: origem "WhatsApp direto"; a auxiliar pode corrigir à mão (`origem_manual`, já existe na PO).
5. Cada clique também é conversão no Google Ads (`gtag('event', 'conversion')`), que a gestão do Ads usa para otimizar.

## 8. Avaliações

- **Importação diária** (cron): Google pela Places API (New) com o `place_id` já levantado (`data/avaliacoes-google.json`); a API devolve só as mais recentes, por isso diária. Doctoralia: leitura da página pública do perfil, como foi feito para montar `data/avaliacoes.json` (sem API oficial).
- Primeira carga: os dois JSON atuais de `data/` (Doctoralia 232, Google 36), respeitando `suspeita: true` como reprovada.
- **Regra**: nota 4 ou 5 entra como aprovada; abaixo de 4, `pendente`, com contador vermelho no menu do painel e aviso no topo. A Dra. aprova ou reprova; reprovada nunca vai ao site.
- O site continua mostrando as avaliações escolhidas a dedo no marquee da home (curadoria em `tools/avaliacoes.py`), mais as notas e totais atualizados. O painel deixa marcar "destaque" para entrar no marquee.
- **Pedido de avaliação** (D+1 de Consulta feita): modelo aprovado com o link direto de avaliação do Google; uma vez por paciente; respeita SAIR.
- **Base antiga**: campanha única via Transmissão da PO (importar contatos, revisão, fila com custo estimado antes de disparar).

## 9. Casos de Resultados e blog no painel

- **Casos**: cadastro com tratamento (filtro), título, descrição, região (para o `alt` "registro fotográfico 1/2") e duas fotos. O alinhamento automático de `tools/imagens/alinhar_casos.py` roda no workflow de publicação; a Dra. confere o comparador no preview do painel. Os 8 casos atuais entram como carga inicial. Os textos seguem a regra das palavras proibidas; o painel avisa se alguém digitar "antes" ou "depois".
- **Blog**: modelo do Dr. Márcio (lista, editor, capa, SEO, agendamento). Os 3 posts de `conteudo/blog/` entram como carga inicial; `tools/blog.py` passa a ler do Supabase no workflow.

## 10. Relatórios

Os da PO (`po/painel/app.js:517-558`), ajustados: leads por origem, conversão por etapa, custo por lead, ROAS e ROI só sobre pagos, orçado × fechado, ticket médio, tempo até fechar, **faturamento por tratamento**, cliques no WhatsApp por página e por origem. Investimento em anúncio digitado por mês (`an_ad_spend`), como na PO.

## 11. Fases (decisão do Fabiano, 16/11: "fazer todo o painel, gerando as telas, depois ligamos tudo")

1. **Virada do site para a HostGator, antes de 05/12** (confirmado pelo Fabiano): site novo no domínio anitaodontologia.com.br, troca combinada com o Guilherme, `noindex` retirado, `robots.txt` liberado com sitemap, tabelas `an_` criadas no Supabase do HD360, `an_cliques` + `clique.php` + código de referência no texto do WhatsApp e conversão do Google Ads. Assim o tráfego começa medido.
2. **Painel completo, telas primeiro**: todas as telas (Leads, Funil, Conversa, Relatórios, Investimento, Fluxo do robô, Modelos, Transmissão, Avaliações com moderação, Casos, Blog, Pacientes atuais) construídas sobre as tabelas `an_*` com dados de exemplo, navegáveis e aprovadas pela Dra. antes da integração.
3. **Ligar tudo**: webhook e motor do robô com os textos da Dra., ficha, atalhos, perdido por inatividade, modelos aprovados na Meta, pedido de avaliação D+1, importação noturna de avaliações, workflow de publicação, campanha da base antiga, cron conferido em produção.

## 11b. Pacientes atuais (decisão do Fabiano, 16/11)

O robô **não atende quem já é paciente**. O Fabiano levanta a lista de pacientes no sistema que a Dra. usa há anos; ela entra no painel (tela de importação, reaproveitando `po/contatos-importar.php` + Revisão) como `an_contatos.ja_paciente = true` **antes de o robô ser ligado**. Mensagem de número marcado como paciente vai direto para a auxiliar, sem lead e sem triagem. Reforço (decisão do Claude): a primeira mensagem do robô para número desconhecido tem a opção "Já sou paciente", que marca o número e passa para a auxiliar sem criar lead. A mesma lista serve de público para a campanha única de avaliação da base antiga.

## 12. Deploy e operação

- Upload por FTPS como na PO (hash decide se subiu; `?v=` com lock por SHA; `confere-deploy.sh`), e o workflow do GitHub para o site estático.
- Segredos só em `config.local.php` no servidor e em secrets do GitHub (FTP, Supabase service key). Nunca no repositório público.
- Cron do cPanel a cada hora (`wa-cron.php`), mais um diário de madrugada para importar avaliações. **Cadastrar e conferir que rodou** (falha registrada na PO).
- Treinamento da Dra. e da auxiliar com passo a passo por escrito (prometido na proposta).

## 12b. Decisões do Claude após a revisão (conferir)

- ~~Supabase separado~~: **revogado pelo Fabiano (17/11)**. Fica no projeto compartilhado do HD360, com o isolamento por `an_usuarios` descrito em Restrições (LGPD). As políticas copiadas da PO (`to authenticated using (true)`) **não** podem vir junto: todas reescritas.
- **Silêncio do robô**: calado enquanto a conversa estiver com a equipe; volta a responder depois de 7 dias sem mensagem humana. Um contato que escreve de novo depois de 90 dias sem lead aberto vira **novo atendimento** (novo lead ligado ao mesmo telefone), para o funil e o retorno contarem cada tratamento. Atalhos `#marcada`, `#feita`, `#fechou` funcionam mesmo com o robô calado (como na PO).
- **Avaliações aprovadas publicam sozinhas**: a importação noturna dispara o workflow de publicação só quando algo mudou. O marquee da home passa a ter as curadas mais as 6 aprovadas mais recentes; notas e totais se atualizam. Moderação (abaixo de 4) continua manual.
- **Doctoralia**: leitura da página pública uma vez por dia, baixo volume. Se falhar ou for bloqueada, o painel avisa e as novas entram à mão (tela de cadastro).
- **Google**: chave da Places API no projeto Google Cloud da Freela (uso dentro do crédito mensal gratuito). **Google Ads na conta da Dra., com e-mail dela** (decisão do Fabiano, 17/11); a Freela gerencia como acesso de gestor e cria nela a conversão "Clique no WhatsApp" antes de 05/12.

## 13. O que fica para o construtor

Nomes de arquivos e colunas; como dividir o JS do painel; se o código de referência vai em `clique.php` com redirecionamento ou em `fetch keepalive`; textos do robô (escritos com a Dra.); desenho das telas dentro da identidade `anita-design`; testes (seguir o padrão de `po/tests`).

## 14. Pendências do cliente

1. Documentos do consultório para verificação na Meta.
2. Acesso à HostGator (cPanel e FTP), com o Guilherme.
3. Link da ficha de cadastro (formulário atual).
4. Perguntas frequentes do WhatsApp e valor da consulta.
5. Lista de pacientes atuais exportada do sistema do consultório (Fabiano levanta): base do "já paciente" e da campanha de avaliação.

6. Conta do Google Ads criada com o e-mail da Dra. (com acesso de gestão para a Freela).

Do lado da Freela: tabelas `an_` no Supabase do HD360, chave da Places API, conversão "Clique no WhatsApp" na conta de Ads da Dra., combinar a virada com o Guilherme.
