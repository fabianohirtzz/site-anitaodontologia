"""Sincroniza header e footer (partials/) em todas as páginas do site.

Cada página tem os marcadores:
  <!-- HEADER:START --> ... <!-- HEADER:END -->
  <!-- FOOTER:START --> ... <!-- FOOTER:END -->
Páginas em subpastas (blog/<slug>/index.html) recebem os caminhos relativos com o prefixo certo (../../).
Uso: python tools/partials.py
"""
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PARTS = {nome: (RAIZ / "partials" / f"{nome.lower()}.html").read_text(encoding="utf-8").strip() for nome in ("HEADER", "FOOTER")}
ABSOLUTO = re.compile(r"^(https?:|mailto:|tel:|#|/|data:)")


def prefixar(html: str, prefixo: str) -> str:
    if not prefixo:
        return html

    def troca(m):
        attr, url = m.group(1), m.group(2)
        return m.group(0) if ABSOLUTO.match(url) else f'{attr}="{prefixo}{url}"'

    return re.sub(r'\b(href|src)="([^"]*)"', troca, html)


def paginas():
    yield from sorted(RAIZ.glob("*.html"))
    yield from sorted(RAIZ.glob("blog/*/index.html"))


for pagina in paginas():
    prefixo = "../" * (len(pagina.relative_to(RAIZ).parts) - 1)
    txt = pagina.read_text(encoding="utf-8")
    novo = txt
    for nome, conteudo in PARTS.items():
        bloco = prefixar(conteudo, prefixo)
        novo = re.sub(
            rf"(<!-- {nome}:START -->)(.*?)(<!-- {nome}:END -->)",
            lambda m: f"{m.group(1)}\n{bloco}\n{m.group(3)}",
            novo,
            flags=re.S,
        )
    if novo != txt:
        pagina.write_text(novo, encoding="utf-8")
        print("atualizado", pagina.relative_to(RAIZ).as_posix())
