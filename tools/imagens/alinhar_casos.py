"""Alinha pares de fotos clínicas (registro 1 e registro 2) para o comparador de arrastar.

Para cada par: acha pontos em comum (SIFT), estima uma transformação de similaridade
(escala + rotação + translação) que leva a foto B para o enquadramento da A, recorta a
área comum numa proporção fixa e exporta <slug>-a.webp e <slug>-b.webp.

Uso: python -I tools/imagens/alinhar_casos.py <pasta_origem> <pasta_destino>
Os pares ficam na lista CASOS abaixo (arquivo A, arquivo B ou "split" para foto já montada).
"""
import pathlib
import sys

import cv2
import numpy as np

PROP = 4 / 3      # largura / altura do recorte final
LARG = 1200       # largura exportada

CASOS = [
    ("caso-01", "06_", "09_"),
    ("caso-02", "07_", "08_"),
    ("caso-03", "10_", "split"),
    ("caso-04", "11_", "12_"),
    ("caso-05", "13_", "15_"),
    ("caso-06", "14_", "16_"),
    ("caso-07", "24_", "25_"),
    ("caso-08", "28_", "29_"),
    ("caso-09", "17_", "22_"),
]


def ler(pasta, prefixo):
    arq = next(pasta.glob(prefixo + "*.jpg"))
    return cv2.imread(str(arq))


def alinhar(a, b):
    """Retorna b transformada para o espaço de a, e a máscara de pixels válidos."""
    sift = cv2.SIFT_create(4000)
    ga, gb = (cv2.cvtColor(x, cv2.COLOR_BGR2GRAY) for x in (a, b))
    ka, da = sift.detectAndCompute(ga, None)
    kb, db = sift.detectAndCompute(gb, None)
    pares = cv2.BFMatcher().knnMatch(db, da, k=2)
    bons = [m for m, n in (p for p in pares if len(p) == 2) if m.distance < 0.72 * n.distance]
    if len(bons) < 12:
        raise RuntimeError(f"poucos pontos em comum ({len(bons)})")
    pb = np.float32([kb[m.queryIdx].pt for m in bons])
    pa = np.float32([ka[m.trainIdx].pt for m in bons])
    M, inl = cv2.estimateAffinePartial2D(pb, pa, method=cv2.RANSAC, ransacReprojThreshold=4.0)
    h, w = a.shape[:2]
    bw = cv2.warpAffine(b, M, (w, h), flags=cv2.INTER_CUBIC)
    mask = cv2.warpAffine(np.full(b.shape[:2], 255, np.uint8), M, (w, h)) > 0
    escala = float(np.sqrt(abs(np.linalg.det(M[:, :2]))))
    return bw, mask, int(inl.sum()), len(bons), escala


def maior_retangulo(mask):
    """Maior retângulo com proporção PROP dentro da máscara, centrado no centro de massa."""
    ys, xs = np.where(mask)
    cy, cx = ys.mean(), xs.mean()
    h, w = mask.shape
    melhor = None
    for alt in range(h, 50, -8):
        lar = int(alt * PROP)
        if lar > w:
            continue
        x0 = int(np.clip(cx - lar / 2, 0, w - lar)); y0 = int(np.clip(cy - alt / 2, 0, h - alt))
        if mask[y0:y0 + alt, x0:x0 + lar].all():
            melhor = (x0, y0, lar, alt)
            break
    if not melhor:
        raise RuntimeError("sem área comum suficiente")
    return melhor


def salvar(img, caminho):
    alt = int(LARG / PROP)
    img = cv2.resize(img, (LARG, alt), interpolation=cv2.INTER_AREA)
    cv2.imwrite(str(caminho), img, [cv2.IMWRITE_WEBP_QUALITY, 86])


def main():
    org, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)
    for slug, pa, pb in CASOS:
        a = ler(org, pa)
        if pb == "split":
            meio = a.shape[0] // 2
            a, b = a[:meio], a[meio:]
        else:
            b = ler(org, pb)
        try:
            bw, mask, inl, tot, esc = alinhar(a, b)
            x, y, w, h = maior_retangulo(mask)
            info = f"alinhado: {inl}/{tot} pontos, escala {esc:.2f}, recorte {w}x{h}"
        except RuntimeError as e:
            # sem alinhamento confiável: só recorta as duas no centro
            bw = cv2.resize(b, (a.shape[1], a.shape[0]))
            x, y, w, h = maior_retangulo(np.ones(a.shape[:2], bool))
            info = f"SEM alinhamento ({e}), recorte central"
        salvar(a[y:y + h, x:x + w], dst / f"{slug}-a.webp")
        salvar(bw[y:y + h, x:x + w], dst / f"{slug}-b.webp")
        print(slug, info)


if __name__ == "__main__":
    main()
