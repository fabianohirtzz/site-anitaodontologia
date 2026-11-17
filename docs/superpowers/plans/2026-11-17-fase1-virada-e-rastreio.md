# Fase 1: Virada para a HostGator e rastreio de cliques no WhatsApp

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** colocar o site novo no ar em anitaodontologia.com.br (HostGator) antes de 05/12/2026, já registrando cada clique no WhatsApp com origem e código de referência no Supabase.

**Architecture:** o site continua estático no repositório (fonte da verdade). Um workflow do GitHub publica por FTPS na HostGator e, só na cópia publicada, troca o `noindex` e o `robots.txt` para produção (o GitHub Pages segue como prévia com `noindex`). No navegador, `js/rastreio.js` guarda a origem da visita, acrescenta um código de 5 dígitos ao texto do WhatsApp e avisa `clique.php` por `sendBeacon`. O `clique.php` classifica a origem e grava em `an_cliques` com a service key, que existe só no `config.local.php` do servidor.

**Tech Stack:** HTML/CSS/JS estático, PHP 8 (HostGator, sem Composer), Supabase (projeto compartilhado do HD360, `https://euzmbswywwhmicjlszqw.supabase.co`), GitHub Actions com `SamKirkland/FTP-Deploy-Action@v4.3.5`, Python 3 (ferramentas), Node 24 (`node:test`) para o JS.

**Spec:** [docs/superpowers/specs/2026-11-16-painel-design.md](../specs/2026-11-16-painel-design.md), seções 3, 7, 11 (fase 1) e 12.

## Global Constraints

- Repositório público: nenhuma chave, senha ou dado de paciente no Git. Segredos só em `config.local.php` no servidor (fora do Git) e em secrets do GitHub.
- Tabelas da Dra. com prefixo `an_`, no projeto Supabase do HD360 (compartilhado com PO `po_`, Márcio `mt_`, HD360).
- Nenhuma política `using (true)` em tabela `an_`. Leitura só para quem está em `an_usuarios`.
- As palavras "antes" e "depois" são proibidas em todo conteúdo publicado: texto, comentários, nomes de arquivo, classes, mensagens de erro em PHP/JS servidos ao navegador.
- Copy: sem travessões, sem emojis.
- Não guardar IP nem dado pessoal em `an_cliques`.
- `links.html` continua `noindex, follow` também em produção.
- A virada só acontece com o site antigo copiado inteiro para backup; o e-mail `anita@anitaodontologia.com.br` (mesmo cPanel) não pode ser tocado.
- Telefone do WhatsApp: `5548991450038`.

## Review Focus

1. **Navegador sem `localStorage` ou com `sendBeacon` bloqueado (aba anônima, bloqueador de anúncio):** o WhatsApp precisa abrir mesmo assim, com o código no texto. O rastreio nunca pode impedir o clique. Teste em Task 3 (`abre mesmo sem storage`).
2. **Link `wa.me` com texto que já tem código (clique duplo, voltar e clicar de novo):** o texto não pode acumular "(ref. 12345) (ref. 67890)". Teste em Task 3 (`nao duplica ref`).
3. **POST forjado ou em massa em `clique.php`:** campos enormes, ref fora do formato, `pagina` com URL externa. Deve responder 400 sem gravar, e mais de 30 por minuto do mesmo IP devolve 429. Testes em Task 2.
4. **Visitante que chega pelo anúncio e só clica dias mais tarde, voltando direto:** a origem do anúncio deve valer por 90 dias (último toque não direto). Teste em Task 3 (`direto nao apaga origem paga`).
5. **Login de outro cliente no mesmo Supabase:** zero linhas de `an_*`. Verificação SQL em Task 1.

---

### Task 1: Tabelas `an_usuarios` e `an_cliques` com isolamento

**Files:**
- Create: `supabase/migrations/2026-11-17-an-base.sql`
- Create: `supabase/tests/isolamento.sql`

**Interfaces:**
- Produces: tabela `an_cliques(id bigint identity pk, criado_em timestamptz default now(), ref text not null check (ref ~ '^[0-9]{5}$'), pagina text, origem text not null check (origem in ('google_ads','google_organico','instagram','facebook','doctoralia','outro_site','direto')), utm_source text, utm_medium text, utm_campaign text, utm_term text, gclid text, referrer_host text, texto text)`; índice em `(ref, criado_em desc)`. Tabela `an_usuarios(user_id uuid pk references auth.users on delete cascade, nome text, criado_em timestamptz default now())`. Função `an_eh_usuario() returns boolean` (`security definer`, `stable`, `set search_path = public`) que retorna `exists (select 1 from an_usuarios where user_id = auth.uid())`.

- [ ] **Step 1: Escrever a migração**

RLS ligada nas duas tabelas. `an_cliques`: só `select` para `authenticated` com `using (an_eh_usuario())`; sem política de insert (quem grava é a service key, que ignora RLS). `an_usuarios`: `select` com `using (user_id = auth.uid())`. `revoke all on an_cliques, an_usuarios from anon`.

- [ ] **Step 2: Escrever `supabase/tests/isolamento.sql`**

Numa transação com `rollback` no fim: insere 1 linha em `an_cliques`; `set local role authenticated`; `set local request.jwt.claims = '{"sub":"00000000-0000-0000-0000-000000000001"}'`; `select count(*) from an_cliques` deve dar `0`. Em seguida insere esse uuid em `auth.users` e `an_usuarios` (como `postgres`, antes de trocar o papel) numa segunda transação e confirma `count = 1`. Também `set local role anon` e `select` deve falhar com `permission denied`.

- [ ] **Step 3: Aplicar no projeto do HD360**

Pelo MCP do Supabase: `list_tables` (conferir que nenhuma tabela `an_` existe), `apply_migration` com o arquivo, depois `execute_sql` com `supabase/tests/isolamento.sql`.
Esperado: `0`, depois `1`, depois erro de permissão para `anon`. Rodar `get_advisors` (security) e confirmar nenhum aviso novo sobre `an_`.

- [ ] **Step 4: Commit**

```bash
git add supabase/
git commit -m "Tabelas an_cliques e an_usuarios com RLS isolada no Supabase compartilhado"
```

### Task 2: `clique.php` com classificação de origem

**Files:**
- Create: `lib/an-config.php`, `lib/an-db.php`, `lib/an-origem.php`, `clique.php`, `config.local.example.php`
- Create: `tests/run.php`, `tests/test-origem.php`, `tests/test-clique.php`
- Modify: `.gitignore` (acrescentar `config.local.php`)

**Interfaces:**
- Consumes: tabela `an_cliques` (Task 1).
- Produces:
  - `an_config(): array` lê `config.local.php` da raiz (variáveis `$SUPABASE_URL`, `$SUPABASE_SERVICE_KEY`); ausente devolve `[]`.
  - `an_db_set_transport(?callable $f): void` e `an_db_insert(string $tabela, array $linha): bool` (POST no PostgREST `/rest/v1/<tabela>`, headers `apikey` e `Authorization: Bearer`, `Prefer: return=minimal`; true em 2xx). Mesmo ponto único de rede de `po/lib/wa-db.php` para o teste trocar o transporte.
  - `an_origem(array $d): string` com `$d` = `['utm_source','utm_medium','gclid','referrer_host','pagina']`, devolvendo um dos 7 valores do check da Task 1.
  - `an_clique_valida(array $entrada): ?array` devolve a linha limpa para `an_cliques` ou `null`.
  - `clique.php`: aceita só `POST` com corpo JSON `{ref, pagina, texto, utm_source, utm_medium, utm_campaign, utm_term, gclid, referrer}`; responde `204` gravado, `400` inválido, `405` outro método, `429` limite. Corpo da resposta sempre vazio.

- [ ] **Step 1: Copiar o runner de testes**

`tests/run.php` = cópia de `E:/Clientes/Pereira Oliveira Turismo/po-tu-project/tests/run.php` (roda `tests/test-*.php` e `tests/test-*.mjs`).

- [ ] **Step 2: Escrever `tests/test-origem.php`**

Casos e resultado esperado de `an_origem`:
- `gclid=abc` → `google_ads`
- `utm_source=google, utm_medium=cpc` → `google_ads`
- `referrer_host=www.google.com.br` → `google_organico`
- `utm_source=instagram` → `instagram`; `referrer_host=l.instagram.com` → `instagram`; `pagina=/links.html` sem nada mais → `instagram`
- `referrer_host=m.facebook.com` → `facebook`
- `referrer_host=www.doctoralia.com.br` → `doctoralia`
- `referrer_host=exemplo.com` → `outro_site`
- `referrer_host=anitaodontologia.com.br` (navegação interna) e vazio → `direto`
- prioridade: `gclid` presente com `referrer_host=l.instagram.com` → `google_ads`

- [ ] **Step 3: Rodar e ver falhar**

Run: `php tests/run.php`
Esperado: FAIL em `test-origem.php` (função não definida).

- [ ] **Step 4: Implementar `lib/an-origem.php`**

Ordem de decisão: gclid ou (google + cpc/ppc/paid) → utm_source conhecido → host do referrer (sufixos `google.`, `instagram.com`, `facebook.com`/`fb.com`, `doctoralia.com.br`) → `pagina` termina em `/links.html` → host próprio ou vazio = `direto` → resto `outro_site`.

- [ ] **Step 5: Escrever `tests/test-clique.php`**

Com `an_db_set_transport` capturando a chamada:
- entrada válida (`ref=48213`, `pagina=/procedimentos.html`, `referrer=https://www.google.com/`) → `an_clique_valida` devolve linha com `origem=google_organico`, `referrer_host=www.google.com` e **sem** campo de IP; `an_db_insert('an_cliques', ...)` chama `POST .../rest/v1/an_cliques`.
- `ref=4821` (4 dígitos), `ref=abcde` → `null`.
- `pagina=https://outro.com/x` → `null` (só caminho começando em `/`, até 200 caracteres).
- qualquer campo texto acima de 300 caracteres → truncado em 300; `texto` acima de 500 → truncado em 500.
- `an_limite_ok(string $chave, int $max, int $janela_s, string $dir): bool` (em `lib/an-db.php`): 30 chamadas passam, a 31ª na mesma janela de 60 s devolve `false`. A chave é `sha1(IP)`; o arquivo vai em `$dir` (teste usa `sys_get_temp_dir()` + nome único).

- [ ] **Step 6: Rodar e ver falhar**

Run: `php tests/run.php` → FAIL em `test-clique.php`.

- [ ] **Step 7: Implementar `lib/an-config.php`, `lib/an-db.php`, `clique.php`, `config.local.example.php`**

`clique.php`: `header('Cache-Control: no-store')`; método ≠ POST → 405; `an_limite_ok` falso → 429; `json_decode(file_get_contents('php://input'), true)` com limite de 4 KB → `an_clique_valida` → 400 se `null`; senão `http_response_code(204)`, `fastcgi_finish_request()` se existir, e só então `an_db_insert`. Falha de rede vai para `error_log`, nunca para a resposta. `config.local.example.php` documenta `$SUPABASE_URL` e `$SUPABASE_SERVICE_KEY` com valores de exemplo, no estilo do da PO.

- [ ] **Step 8: Rodar e ver passar**

Run: `php tests/run.php`
Esperado: todos `OK`.

- [ ] **Step 9: Teste manual local**

Run: `php -S 127.0.0.1:8770` na raiz e `curl -i -X POST 127.0.0.1:8770/clique.php -d '{"ref":"12345","pagina":"/"}'`
Esperado: `204` (sem config, o insert só registra no log). `curl -i 127.0.0.1:8770/clique.php` → `405`.

- [ ] **Step 10: Commit**

```bash
git add lib/ clique.php config.local.example.php tests/ .gitignore
git commit -m "clique.php: registra cliques no WhatsApp com origem classificada"
```

### Task 3: `js/rastreio.js` nos links do WhatsApp

**Files:**
- Create: `js/rastreio.js`, `tests/test-rastreio.mjs`
- Modify: `partials/` (o arquivo de rodapé que hoje carrega `js/site.js`) e `links.html`, para carregar `js/rastreio.js` com `defer` antes de `site.js`; depois `python tools/partials.py` e `python tools/blog.py`.

**Interfaces:**
- Consumes: `POST /clique.php` (Task 2).
- Produces: objeto global `AnRastreio` com
  - `ref(rand?: () => number): string`, 5 dígitos, zeros à esquerda.
  - `comRef(href: string, ref: string): string` acrescenta ` (ref. NNNNN)` ao parâmetro `text` do link `wa.me`, substituindo um `(ref. …)` já existente.
  - `capturaOrigem(url: string, referrer: string, agora: number, salvo: object|null): object|null` devolve a origem a salvar: `{utm_source, utm_medium, utm_campaign, utm_term, gclid, referrer, ts}` quando a visita tem UTM, gclid ou referrer externo; `salvo` quando é direta ou interna e `salvo` tem menos de 90 dias; `null` caso contrário.
  - `AnRastreio.ADS = { id: '', rotulo: '' }`: ID e rótulo da conversão do Google Ads da conta da Dra. Vazios até a conta existir.

- [ ] **Step 1: Escrever `tests/test-rastreio.mjs`**

Carrega o arquivo com `vm.runInNewContext(codigo, contexto)` (contexto sem `window.localStorage`) e testa:
- `ref(() => 0)` = `"00000"`; `ref(() => 0.99999)` = `"99999"`.
- `comRef('https://wa.me/5548991450038?text=Ol%C3%A1%2C%20Dra.%20Anita!', '48213')`: o `text` decodificado é `Olá, Dra. Anita! (ref. 48213)`.
- `nao duplica ref`: aplicar `comRef` duas vezes com `48213` e `67890` deixa só `(ref. 67890)`.
- `capturaOrigem('https://anitaodontologia.com.br/?gclid=X', '', T, null).gclid === 'X'`.
- `direto nao apaga origem paga`: com `salvo = {gclid:'X', ts: T - 10*864e5}`, `capturaOrigem('https://anitaodontologia.com.br/sobre.html', '', T, salvo)` devolve `salvo`; com `ts: T - 91*864e5` devolve `null`.
- referrer `https://anitaodontologia.com.br/` conta como interno (não sobrescreve `salvo`).
- `abre mesmo sem storage`: com `localStorage` que lança erro e sem `navigator.sendBeacon`, chamar o manipulador de clique sobre um `<a data-wa>` falso não lança e altera o `href` com o ref.

- [ ] **Step 2: Rodar e ver falhar**

Run: `node --test tests/test-rastreio.mjs` → FAIL (arquivo não existe).

- [ ] **Step 3: Implementar `js/rastreio.js`**

Script clássico (sem módulo), IIFE que define `globalThis.AnRastreio`. Ao carregar: lê `localStorage['an_origem']` (try/catch), aplica `capturaOrigem` com `location.href`, `document.referrer`, `Date.now()` e grava. Escuta `click` em `document` (fase de captura) para `a[data-wa]`: gera o ref, troca o `href` pelo `comRef` **sincronamente** (o navegador segue o link já alterado), e envia `navigator.sendBeacon('clique.php', Blob JSON)` com `ref`, `pagina: location.pathname`, `texto` decodificado e os campos da origem salva; se `sendBeacon` não existir, `fetch` com `keepalive: true` dentro de try/catch. Se `ADS.id` e `window.gtag` existirem, `gtag('event','conversion',{send_to: ADS.id + '/' + ADS.rotulo})`. O caminho de `clique.php` sai da posição do próprio script, para funcionar também no ensaio em `/novo/` e nos posts em `blog/<slug>/`: `new URL('../clique.php', document.currentScript.src)` calculado no carregamento. No GitHub Pages (host `fabianohirtzz.github.io`) não enviar nada.

- [ ] **Step 4: Rodar e ver passar**

Run: `node --test tests/test-rastreio.mjs` e `php tests/run.php`
Esperado: PASS nos dois.

- [ ] **Step 5: Incluir nas páginas e regenerar**

Run: `python tools/partials.py && python tools/blog.py`
Depois: `grep -L "js/rastreio.js" *.html blog/*/index.html` não lista nenhum arquivo.

- [ ] **Step 6: Conferir no navegador**

Servidor local em 8765 já rodando. Com Playwright, abrir `http://localhost:8765/?utm_source=google&utm_medium=cpc&gclid=teste`, ir para `procedimentos.html`, clicar no primeiro `a[data-wa]` (interceptar a abertura da nova aba) e conferir: `href` termina com `%20(ref.%20NNNNN)`, uma requisição `POST /clique.php` foi feita com `gclid: "teste"`, console sem erros.

- [ ] **Step 7: Commit**

```bash
git add js/rastreio.js tests/test-rastreio.mjs partials/ *.html blog/
git commit -m "Código de referência e origem nos cliques do WhatsApp"
```

### Task 4: Produção na cópia publicada, `.htaccess` e redirecionamentos do site antigo

**Files:**
- Create: `tools/producao.py`, `tests/test_producao.py`, `.htaccess`, `404.html`

**Interfaces:**
- Produces: `python tools/producao.py <pasta>` altera arquivos **na pasta indicada** (o workflow passa a cópia do checkout): remove `<meta name="robots" content="noindex, nofollow">` de todo `.html` exceto `links.html`; reescreve `robots.txt` como `User-agent: *` / `Allow: /` / `Disallow: /lib/` / `Sitemap: https://anitaodontologia.com.br/sitemap.xml`. Função `prepara(pasta: Path) -> list[str]` devolve os arquivos alterados.

- [ ] **Step 1: Levantar URLs do site antigo**

Baixar `https://anitaodontologia.com.br/sitemap.xml` (e, se for WordPress, `/wp-sitemap.xml` ou `/sitemap_index.xml`), listar todas as URLs e mapear cada uma para a página nova equivalente (serviços → `procedimentos.html#<âncora>`, sobre → `sobre.html`, contato → `contato.html`, posts antigos → `blog.html` ou o post novo do mesmo tema). Registrar o mapa em comentário no `.htaccess`.

- [ ] **Step 2: Escrever `tests/test_producao.py`**

Com `tempfile.TemporaryDirectory` contendo `index.html` e `links.html` com as metas atuais e um `robots.txt` com `Disallow: /`:
- depois de `prepara`, `index.html` não contém `noindex`; `links.html` ainda contém `noindex, follow`.
- `robots.txt` contém `Allow: /` e a linha `Sitemap:` exata.
- rodar `prepara` duas vezes dá o mesmo resultado.

- [ ] **Step 3: Rodar e ver falhar**

Run: `python -m unittest tests/test_producao.py` → FAIL (módulo não existe).

- [ ] **Step 4: Implementar `tools/producao.py`**

- [ ] **Step 5: Rodar e ver passar**

Run: `python -m unittest tests/test_producao.py` → OK.

- [ ] **Step 6: Escrever `.htaccess` e `404.html`**

`.htaccess`: forçar HTTPS e domínio sem `www` (301); `ErrorDocument 404 /404.html`; `Options -Indexes`; negar acesso web a `lib/`, `tests/`, `config.local.php`, `*.md`, `*.py`; `Redirect 301` de cada URL antiga do Step 1; cache longo (`max-age=31536000`) para `assets/` e `.webp`, curto para `.html`; `AddType image/webp .webp`. `404.html` no padrão das páginas internas (partials, `noindex`), título "Página não encontrada" e links para Início, Procedimentos e WhatsApp.

- [ ] **Step 7: Conferir sintaxe**

Run: `python tools/partials.py` (inclui o 404 nos partials) e abrir `404.html` no Playwright em 390 e 1440: sem rolagem horizontal, sem erro no console.

- [ ] **Step 8: Commit**

```bash
git add tools/producao.py tests/test_producao.py .htaccess 404.html
git commit -m "Produção: robots e noindex na cópia publicada, .htaccess e 404"
```

### Task 5: Workflow de publicação por FTPS

**Files:**
- Create: `.github/workflows/publicar.yml`

**Interfaces:**
- Consumes: `tools/producao.py` (Task 4); secrets `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`, `FTP_SERVER_DIR`.

- [ ] **Step 1: Escrever o workflow**

`on: workflow_dispatch` **apenas** (o gatilho `push` em `main` entra no dia da virada, Task 6). Passos: checkout; checagem que falha alto se algum dos 4 secrets estiver vazio; `python -m unittest tests/test_producao.py`; `python tools/producao.py .`; `SamKirkland/FTP-Deploy-Action@v4.3.5` com `protocol: ftps`, `security: strict`, `timeout: 60000`, `local-dir: ./`, e `exclude` com: `**/.git*`, `**/.git*/**`, `**/.github/**`, `docs/**`, `tools/**`, `tests/**`, `supabase/**`, `conteudo/**`, `data/**`, `partials/**`, `assets/original/**`, `**/*.md`, `config.local.example.php`, `.gitignore`. O `llms.txt` **vai**. `concurrency: publicar`.

- [ ] **Step 2: Validar a sintaxe**

Run: `python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/publicar.yml'))"` → sem erro. Conferir que `config.local.php` nunca está no repositório: `git ls-files | grep -c config.local.php` = `0`.

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/publicar.yml
git commit -m "Workflow de publicação na HostGator por FTPS (disparo manual)"
```

### Task 6: Virada (roteiro com acesso real; executada junto com o Fabiano)

**Files:**
- Create: `docs/virada-hostgator.md` (roteiro com caixas de seleção; sem senhas)
- Modify: `.github/workflows/publicar.yml` (acrescentar `push: branches: [main]` só no fim), `CLAUDE.md` (estado atual)

Pré-requisitos (pendências do cliente): acesso cPanel/FTP da HostGator combinado com o Guilherme; conta do Google Ads da Dra. com acesso de gestão para a Freela.

- [ ] **Step 1: Escrever o roteiro** com os passos abaixo, um por linha, e seguir.
- [ ] **Step 2: Backup** do `public_html` inteiro (arquivos e banco do WordPress, se houver) por FTP para `E:/Clientes/Dra. Anita Nogiri/backup-site-antigo-<data>/`, fora do repo. Conferir contagem de arquivos e tamanho. Não mexer em `mail/`, `etc/` nem nas contas de e-mail.
- [ ] **Step 3: Secrets e config** no GitHub (`FTP_SERVER` com o hostname do servidor da HostGator, para o certificado bater; `FTP_SERVER_DIR` apontando para uma pasta de teste `public_html/novo/` nesta primeira rodada). No servidor, criar `config.local.php` pelo gerenciador de arquivos do cPanel com a URL e a service key do projeto do HD360.
- [ ] **Step 4: Publicação de ensaio** em `public_html/novo/` pelo `workflow_dispatch`. Conferir em `https://anitaodontologia.com.br/novo/` com Playwright: páginas abrem, imagens carregam, `curl -i -X POST .../novo/clique.php -d '{"ref":"12345","pagina":"/"}'` → `204` e uma linha nova em `an_cliques` (`execute_sql`); `https://anitaodontologia.com.br/novo/lib/an-db.php` e `/novo/config.local.php` → `403`. Se a FTPS `strict` falhar por certificado, trocar o host para o hostname que o certificado cobre (não afrouxar para `loose` sem avisar o Fabiano).
- [ ] **Step 4b: Handler do PHP.** Antes de sobrescrever, abrir o `.htaccess` atual do `public_html` e copiar para o `.htaccess` versionado o bloco `# php -- BEGIN cPanel-generated handler ... # php -- END` (MultiPHP Manager); commitar. No ensaio, conferir a versão do PHP com um `phpinfo` temporário (apagar logo depois) e confirmar 8.x. Conferir também se o mod_security deixa passar o POST do `sendBeacon` (clique real no navegador gravando em `an_cliques`).
- [ ] **Step 5: Virada.** Mover os arquivos do site antigo (não os de e-mail) para fora do `public_html` (por exemplo `~/site-antigo-<data>/`; o `.htaccess` também bloqueia `/_antigo/` se alguém usar esse nome), apontar `FTP_SERVER_DIR` para `public_html/`, publicar, mover `config.local.php` para a raiz, apagar `public_html/novo/`. Conferir: home 200, `robots.txt` com `Allow`, sem `noindex` no HTML da home, `links.html` com `noindex`, cada URL antiga do mapa da Task 4 dá 301 para a nova, `http://` e `www.` redirecionam, um clique real no celular grava em `an_cliques` com origem certa.
- [ ] **Step 6: Google.** Na conta de Ads da Dra., criar a conversão "Clique no WhatsApp" (categoria contato), colar ID e rótulo em `AnRastreio.ADS`, incluir a tag `gtag.js` do Ads no partial do cabeçalho, regenerar e publicar; nas campanhas, modelo de acompanhamento com `utm_source=google&utm_medium=cpc` (o Safari remove `gclid`, e no iOS o Ads usa `gbraid`/`wbraid`, ambos já tratados como anúncio); conferir no Tag Assistant que a conversão dispara. Search Console: propriedade do domínio, enviar `sitemap.xml`.
- [ ] **Step 7: Ligar o push automático** no `publicar.yml`, atualizar o `CLAUDE.md` (fase, URL de produção, que o GitHub Pages segue como prévia com `noindex`) e commitar.

```bash
git add docs/virada-hostgator.md .github/workflows/publicar.yml CLAUDE.md js/rastreio.js partials/ *.html blog/
git commit -m "Virada: site novo no ar na HostGator, conversão do Ads e publicação automática"
```

---

**Fases seguintes:** a Fase 2 (todas as telas do painel com dados de exemplo) e a Fase 3 (ligar robô, Meta, publicação e cron) ganham planos próprios depois deste, porque dependem do que a virada revelar sobre a hospedagem (versão do PHP, `fastcgi_finish_request`, cron do cPanel).
