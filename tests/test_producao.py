"""tools/producao.py: libera a indexação só na cópia publicada."""
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
import producao  # noqa: E402

PAG = '<!doctype html>\n<html><head>\n<meta charset="utf-8">\n{meta}\n<title>x</title></head><body></body></html>\n'
NOINDEX = '<meta name="robots" content="noindex, nofollow">'
LINKS = '<meta name="robots" content="noindex, follow">'


class Producao(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = pathlib.Path(self.tmp.name)
        (self.d / "index.html").write_text(PAG.format(meta=NOINDEX), encoding="utf-8")
        (self.d / "links.html").write_text(PAG.format(meta=LINKS), encoding="utf-8")
        (self.d / "404.html").write_text(PAG.format(meta=NOINDEX), encoding="utf-8")
        (self.d / "blog" / "post").mkdir(parents=True)
        (self.d / "blog" / "post" / "index.html").write_text(PAG.format(meta=NOINDEX), encoding="utf-8")
        (self.d / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def ler(self, nome):
        return (self.d / nome).read_text(encoding="utf-8")

    def test_tira_noindex_das_paginas(self):
        producao.prepara(self.d)
        self.assertNotIn("noindex", self.ler("index.html"))
        self.assertNotIn("noindex", self.ler("blog/post/index.html"))

    def test_links_e_404_continuam_fora_da_busca(self):
        producao.prepara(self.d)
        self.assertIn(LINKS, self.ler("links.html"))
        self.assertIn(NOINDEX, self.ler("404.html"))

    def test_robots_de_producao(self):
        producao.prepara(self.d)
        r = self.ler("robots.txt")
        self.assertIn("Allow: /", r)
        self.assertNotIn("Disallow: /\n", r.replace("Disallow: /lib/", ""))
        self.assertIn("Sitemap: https://anitaodontologia.com.br/sitemap.xml", r.splitlines())

    def test_idempotente(self):
        producao.prepara(self.d)
        estado1 = {p: p.read_bytes() for p in self.d.rglob("*") if p.is_file()}
        alterados = producao.prepara(self.d)
        self.assertEqual(alterados, [])
        self.assertEqual(estado1, {p: p.read_bytes() for p in self.d.rglob("*") if p.is_file()})


if __name__ == "__main__":
    unittest.main()
