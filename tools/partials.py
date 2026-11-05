"""Sincroniza header e footer (partials/) em todas as páginas .html da raiz.

Cada página tem os marcadores:
  <!-- HEADER:START --> ... <!-- HEADER:END -->
  <!-- FOOTER:START --> ... <!-- FOOTER:END -->
Uso: python tools/partials.py
"""
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PARTS = {nome: (RAIZ / "partials" / f"{nome.lower()}.html").read_text(encoding="utf-8").strip() for nome in ("HEADER", "FOOTER")}

for pagina in sorted(RAIZ.glob("*.html")):
    txt = pagina.read_text(encoding="utf-8")
    novo = txt
    for nome, conteudo in PARTS.items():
        novo = re.sub(
            rf"(<!-- {nome}:START -->)(.*?)(<!-- {nome}:END -->)",
            lambda m: f"{m.group(1)}\n{conteudo}\n{m.group(3)}",
            novo,
            flags=re.S,
        )
    if novo != txt:
        pagina.write_text(novo, encoding="utf-8")
        print("atualizado", pagina.name)
