"""Prepara a cópia publicada na HostGator para produção.

O repositório fica com noindex (o GitHub Pages é só prévia). O workflow de
publicação roda este script na cópia do checkout, antes do FTP:
  - remove o meta robots noindex de todas as páginas, menos links.html
    (página da bio) e 404.html;
  - reescreve o robots.txt liberando a indexação, com o sitemap.
Uso: python tools/producao.py <pasta>
"""
import pathlib
import re
import sys

MANTER_NOINDEX = {"links.html", "404.html"}
META = re.compile(r'[ \t]*<meta name="robots" content="noindex[^"]*"\s*/?>\r?\n?')
# Qualquer meta com noindex, em qualquer ordem de atributos ou aspas.
SOBRA = re.compile(r"<meta\b[^>]*\bnoindex\b[^>]*>", re.I)
ROBOTS = (
    "User-agent: *\n"
    "Allow: /\n"
    "Disallow: /lib/\n"
    "\n"
    "Sitemap: https://anitaodontologia.com.br/sitemap.xml\n"
)


def prepara(pasta) -> list[str]:
    pasta = pathlib.Path(pasta)
    alterados = []
    for pag in sorted(pasta.rglob("*.html")):
        if pag.relative_to(pasta).as_posix() in MANTER_NOINDEX:
            continue
        txt = pag.read_text(encoding="utf-8")
        novo = META.sub("", txt)
        if novo != txt:
            pag.write_text(novo, encoding="utf-8", newline="")
            alterados.append(pag.relative_to(pasta).as_posix())
    robots = pasta / "robots.txt"
    if not robots.exists() or robots.read_text(encoding="utf-8") != ROBOTS:
        robots.write_text(ROBOTS, encoding="utf-8", newline="\n")
        alterados.append("robots.txt")
    return alterados


def sobras(pasta) -> list[str]:
    """Páginas que ainda têm noindex fora das exceções (formato inesperado)."""
    pasta = pathlib.Path(pasta)
    return [
        p.relative_to(pasta).as_posix()
        for p in sorted(pasta.rglob("*.html"))
        if p.relative_to(pasta).as_posix() not in MANTER_NOINDEX
        and SOBRA.search(p.read_text(encoding="utf-8"))
    ]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("uso: python tools/producao.py <pasta>")
    for a in prepara(sys.argv[1]):
        print("produção:", a)
    resto = sobras(sys.argv[1])
    if resto:
        sys.exit("noindex ainda presente em: " + ", ".join(resto))
