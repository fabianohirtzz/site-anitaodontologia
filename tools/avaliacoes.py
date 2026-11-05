"""Gera o marquee de avaliações (HTML estático) a partir de data/*.json.

Seleção curada por autor (nunca edita o texto). Ignora avaliações marcadas como suspeitas.
Escreve entre <!-- AVALIACOES:START --> e <!-- AVALIACOES:END --> em index.html.
Uso: python tools/avaliacoes.py
"""
import html
import json
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
G = json.loads((RAIZ / "data/avaliacoes-google.json").read_text(encoding="utf-8"))
D = json.loads((RAIZ / "data/avaliacoes.json").read_text(encoding="utf-8"))

LINHA_1 = [
    ("D", "P.B."), ("G", "Igor Borgio"), ("D", "Roberto Simon"), ("G", "Clarissa SP"),
    ("D", "Verônica F.  Alves da Silva"), ("G", "Pedro Vitor"), ("D", "Andréia Maria de Oliveira Costa"),
]
LINHA_2 = [
    ("G", "Franklin Lindolf Bloedorn"), ("D", "Martha Wallauer"), ("G", "Leandro Vieira"),
    ("D", "RC"), ("G", "daniela de souza"), ("D", "Mariza"), ("G", "Edson Oliveira"),
]


def achar(fonte, autor):
    if fonte == "G":
        for a in G["avaliacoes"]:
            if a["autor"] == autor and not a.get("suspeita"):
                return a, "Google", "google", (a.get("data_aprox") or "")[:4]
    else:
        for a in D:
            if a["autor"] == autor:
                return a, "Doctoralia", "doctoralia", (a.get("data") or "")[:4]
    raise SystemExit(f"avaliação não encontrada: {fonte} {autor}")


def card(fonte, autor):
    a, nome, icone, ano = achar(fonte, autor)
    texto = html.escape(a["texto"].strip().strip("“”\""))
    return (
        f'<figure class="depo"><div class="chip__estrelas" aria-label="{a["nota"]} de 5 estrelas">'
        + '<svg aria-hidden="true"><use href="assets/icons.svg#estrela"/></svg>' * int(a["nota"])
        + f'</div><blockquote>{texto}</blockquote><figcaption><span><b>{html.escape(a["autor"].strip())}</b>'
        + (f" · {ano}" if ano else "")
        + f'</span><span class="depo__fonte"><svg aria-hidden="true"><use href="assets/icons.svg#{icone}"/></svg>{nome}</span></figcaption></figure>'
    )


def linha(itens, rev=False):
    grupo = "".join(card(*i) for i in itens)
    cls = "marquee__linha marquee__linha--rev" if rev else "marquee__linha"
    return (f'<div class="{cls}"><div class="marquee__grupo">{grupo}</div>'
            f'<div class="marquee__grupo" aria-hidden="true">{grupo}</div></div>')


bloco = '<div class="marquee" tabindex="0" aria-label="Avaliações de pacientes">' + linha(LINHA_1) + linha(LINHA_2, True) + "</div>"
pag = RAIZ / "index.html"
txt = pag.read_text(encoding="utf-8")
novo = re.sub(r"(<!-- AVALIACOES:START -->)(.*?)(<!-- AVALIACOES:END -->)", lambda m: f"{m.group(1)}\n{bloco}\n{m.group(3)}", txt, flags=re.S)
pag.write_text(novo, encoding="utf-8")
print("avaliações:", len(LINHA_1) + len(LINHA_2))
