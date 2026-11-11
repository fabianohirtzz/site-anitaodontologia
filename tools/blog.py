"""Gera o blog (modelo do site do Dr. Márcio, em Python e sem dependências).

Fonte:   conteudo/blog/posts.json  (metadados, FAQ)  +  conteudo/blog/<slug>.html  (corpo)
Saída:   blog.html (grade + schema), blog/<slug>/index.html, sitemap.xml
Depois roda tools/partials.py para aplicar header e footer.
Uso: python tools/blog.py
"""
import datetime as dt
import html
import json
import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://anitaodontologia.com.br/"
WA = "https://wa.me/5548991450038?text=Ol%C3%A1%2C%20Dra.%20Anita!%20Gostaria%20de%20agendar%20uma%20avalia%C3%A7%C3%A3o."
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
NOMES_PROC = {
    "facetas": "Facetas de porcelana e de resina", "lentes-de-contato": "Lentes de contato dental",
    "clareamento": "Clareamento dental", "restauracoes-esteticas": "Restaurações estéticas",
}


def data_br(iso):
    d = dt.date.fromisoformat(iso)
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def esc(s):
    return html.escape(s, quote=True)


def card(p, prefixo, destaque=False):
    meta = f'<p class="post-card__meta"><span class="post-card__cat">{esc(p["categoria"])}</span><time datetime="{p["data"]}">{data_br(p["data"])}</time><span>· {p["leitura"]} min de leitura</span></p>'
    img = f'<div class="post-card__img"><img src="{prefixo}{p["capa"]}" alt="{esc(p["capa_alt"])}" width="1248" height="832" loading="lazy"></div>'
    url = f'{prefixo}blog/{p["slug"]}/index.html'
    if destaque:
        return (f'<a class="post-card post-card--destaque" href="{url}" data-reveal>{img}'
                f'<div>{meta}<h2><span>{esc(p["titulo"])}</span></h2><p>{esc(p["descricao"])}</p>'
                f'<span class="card__mais">Ler artigo<svg aria-hidden="true"><use href="{prefixo}assets/icons.svg#seta"/></svg></span></div></a>')
    return (f'<a class="post-card" href="{url}" data-reveal>{img}{meta}<h2><span>{esc(p["titulo"])}</span></h2>'
            f'<p>{esc(p["descricao"])}</p></a>')


def schema_post(p):
    url = f'{SITE}blog/{p["slug"]}/'
    grafo = [
        {"@type": "BlogPosting", "headline": p["titulo"], "description": p["descricao"], "image": SITE + p["capa"],
         "datePublished": p["data"], "dateModified": p.get("atualizado", p["data"]), "inLanguage": "pt-BR",
         "mainEntityOfPage": url, "articleSection": p["categoria"],
         "author": {"@type": "Person", "@id": SITE + "#dra-anita", "name": "Dra. Anita Nogiri Makowiecky",
                    "jobTitle": "Cirurgiã-dentista, especialista em Dentística Restauradora (UFPR)", "url": SITE + "sobre.html"},
         "publisher": {"@type": "Dentist", "@id": SITE + "#consultorio", "name": "Dra. Anita Nogiri Makowiecky · Odontologia Integrada",
                       "logo": {"@type": "ImageObject", "url": SITE + "favicon.png"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "blog.html"},
            {"@type": "ListItem", "position": 3, "name": p["titulo"], "item": url}]},
    ]
    if p.get("faq"):
        grafo.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in p["faq"]]})
    return json.dumps({"@context": "https://schema.org", "@graph": grafo}, ensure_ascii=False, indent=1)


def pagina_post(p, outros):
    P = "../../"
    corpo = (RAIZ / "conteudo" / "blog" / f'{p["slug"]}.html').read_text(encoding="utf-8").strip()
    faq = "".join(f'<details><summary>{esc(f["q"])}<svg aria-hidden="true"><use href="{P}assets/icons.svg#mais"/></svg></summary><p>{esc(f["a"])}</p></details>' for f in p.get("faq", []))
    proc = p.get("procedimento")
    link_proc = (f'<a class="link" href="{P}procedimentos.html#{proc}">{esc(NOMES_PROC.get(proc, "Ver procedimento"))}'
                 f'<svg aria-hidden="true"><use href="{P}assets/icons.svg#seta"/></svg></a>') if proc else ""
    relacionados = "".join(card(o, P) for o in outros[:3])
    url = f'{SITE}blog/{p["slug"]}/'
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{esc(p["titulo"])} | Dra. Anita Nogiri</title>
<meta name="description" content="{esc(p["descricao"])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{esc(p["titulo"])}">
<meta property="og:description" content="{esc(p["descricao"])}">
<meta property="og:image" content="{SITE}{p["capa"]}">
<meta property="article:published_time" content="{p["data"]}">
<meta name="author" content="Dra. Anita Nogiri Makowiecky">
<meta name="theme-color" content="#00565d">
<link rel="icon" href="{P}favicon.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=Fraunces:ital,opsz,wght@0,9..144,300..500;1,9..144,300..500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{P}css/site.css">
<script>document.documentElement.classList.add("js")</script>
<script type="application/ld+json">
{schema_post(p)}
</script>
</head>
<body data-pagina="blog">
<!-- HEADER:START -->
<!-- HEADER:END -->

<main id="conteudo">
  <section class="artigo-topo">
    <div class="container">
      <ol class="migalhas" aria-label="Você está em"><li><a href="{P}index.html">Início</a></li><li><a href="{P}blog.html">Blog</a></li><li><span aria-current="page">{esc(p["categoria"])}</span></li></ol>
      <p class="post-card__meta"><span class="post-card__cat">{esc(p["categoria"])}</span><time datetime="{p["data"]}">{data_br(p["data"])}</time><span>· {p["leitura"]} min de leitura</span></p>
      <h1>{p["titulo_html"]}</h1>
      <p class="lead">{esc(p["descricao"])}</p>
    </div>
  </section>

  <div class="container">
    <figure class="artigo-capa"><img src="{P}{p["capa"]}" alt="{esc(p["capa_alt"])}" width="1248" height="832" fetchpriority="high"></figure>
  </div>

  <section class="secao" style="padding-top:clamp(3rem,5vw,4rem)">
    <div class="container artigo">
      <article class="prosa">
{corpo}

        <h2>Perguntas frequentes</h2>
        <div class="faq"><div class="faq__lista">{faq}</div></div>

        <p class="aviso">Conteúdo informativo, escrito pela Dra. Anita Nogiri Makowiecky, cirurgiã-dentista (CRO-SC 10010). Não substitui a avaliação presencial: a indicação de qualquer tratamento depende do exame de cada paciente.</p>
      </article>

      <aside class="artigo__lado">
        <a class="autor" href="{P}sobre.html">
          <img src="{P}assets/img/dra-anita-retrato.webp" alt="" width="60" height="60" loading="lazy">
          <div><b>Dra. Anita Nogiri</b><span>Especialista em Dentística Restauradora pela UFPR · CRO-SC 10010</span></div>
        </a>
        <div class="cta-lado">
          <strong>Quer saber se é indicado para você?</strong>
          <p>Agende uma avaliação no consultório, no João Paulo, em Florianópolis.</p>
          <a class="btn btn--branco btn--compacto" data-wa href="{WA}" target="_blank" rel="noopener"><svg aria-hidden="true"><use href="{P}assets/icons.svg#wa"/></svg><span>Agendar pelo WhatsApp</span></a>
        </div>
        {link_proc}
      </aside>
    </div>
  </section>

  <section class="secao secao--branca" aria-labelledby="t-mais">
    <div class="container">
      <div class="cabeca"><h2 class="titulo" id="t-mais" data-reveal>Continue <em>lendo</em></h2></div>
      <div class="posts">{relacionados}</div>
    </div>
  </section>
</main>

<!-- FOOTER:START -->
<!-- FOOTER:END -->

<script src="{P}js/site.js" defer></script>
</body>
</html>
"""


def troca(texto, nome, novo):
    return re.sub(rf"(<!-- {nome}:START -->)(.*?)(<!-- {nome}:END -->)", lambda m: f"{m.group(1)}\n{novo}\n{m.group(3)}", texto, flags=re.S)


def main():
    posts = json.loads((RAIZ / "conteudo" / "blog" / "posts.json").read_text(encoding="utf-8"))
    posts.sort(key=lambda p: p["data"], reverse=True)

    for p in posts:
        destino = RAIZ / "blog" / p["slug"] / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina_post(p, [o for o in posts if o is not p]), encoding="utf-8")
        print("ok blog/" + p["slug"] + "/index.html")

    grade = card(posts[0], "", destaque=True)
    if len(posts) > 1:
        grade += '\n<div class="posts">' + "".join(card(p, "") for p in posts[1:]) + "</div>"
    schema = {"@context": "https://schema.org", "@type": "Blog", "name": "Blog da Dra. Anita Nogiri", "url": SITE + "blog.html", "inLanguage": "pt-BR",
              "publisher": {"@id": SITE + "#consultorio"},
              "blogPost": [{"@type": "BlogPosting", "headline": p["titulo"], "url": f'{SITE}blog/{p["slug"]}/', "datePublished": p["data"], "image": SITE + p["capa"]} for p in posts]}
    blog = RAIZ / "blog.html"
    txt = troca(blog.read_text(encoding="utf-8"), "POSTS", grade)
    txt = troca(txt, "SCHEMA", '<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=1) + "\n</script>")
    blog.write_text(txt, encoding="utf-8")
    print("ok blog.html:", len(posts), "posts")

    # sitemap: páginas da raiz (sem a de links da bio) + posts
    hoje = dt.date.today().isoformat()
    urls = [(SITE, hoje, "1.0")]
    for nome, prio in [("sobre.html", "0.8"), ("procedimentos.html", "0.9"), ("resultados.html", "0.7"), ("blog.html", "0.7"), ("contato.html", "0.8")]:
        if (RAIZ / nome).exists():
            urls.append((SITE + nome, hoje, prio))
    urls += [(f'{SITE}blog/{p["slug"]}/', p.get("atualizado", p["data"]), "0.6") for p in posts]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod><priority>{pr}</priority></url>\n" for u, d, pr in urls)
    (RAIZ / "sitemap.xml").write_text(xml + "</urlset>\n", encoding="utf-8")
    print("ok sitemap.xml:", len(urls), "urls")

    subprocess.run([sys.executable, str(RAIZ / "tools" / "partials.py")], check=True)


if __name__ == "__main__":
    main()
