"""Trata e comprime as fotos do consultório para o site.

Passos: orientação EXIF, recorte das bordas (onde a grande-angular mais estica),
recuperação dos altos quase estourados, leve contraste nos médios, menos ciano nos
vidros, redimensionamento, nitidez e WebP comprimido.

Uso: python -I tools/imagens/tratar_consultorio.py <pasta_origem> <pasta_destino>
O mapa FOTOS liga o arquivo original ao nome usado no site.
"""
import pathlib
import sys

import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps

FOTOS = {
    "112": "consultorio-sala-1",
    "103": "consultorio-recepcao",
    "131": "consultorio-sala-2",
    "144": "consultorio-escritorio",
    "141": "consultorio-sala-3",
    "105": "consultorio-recepcao-2",
}
LADO = 1600       # lado maior exportado
CORTE = 0.05      # fração recortada de cada borda
QUALIDADE = 78


def curva():
    """Curva de tons: segura os altos (sem estourar) e dá um contraste suave nos médios."""
    x = np.arange(256, dtype=np.float32) / 255
    s = x + 0.06 * np.sin(2 * np.pi * x) * (1 - x) * 1.6     # contraste em S suave
    s = np.where(s > 0.82, 0.82 + (s - 0.82) * 0.82, s)       # comprime os altos
    return np.clip(s * 255, 0, 255).astype(np.uint8)


def menos_ciano(rgb):
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    h = hsv[..., 0]                                  # OpenCV: matiz 0..180
    peso = np.clip(1 - np.abs(h - 92) / 18, 0, 1)    # ciano/turquesa em torno de 92
    hsv[..., 1] *= 1 - 0.35 * peso
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)


def tratar(origem, destino):
    im = ImageOps.exif_transpose(Image.open(origem)).convert("RGB")
    w, h = im.size
    im = im.crop((int(w * CORTE), int(h * CORTE), int(w * (1 - CORTE)), int(h * (1 - CORTE))))
    im.thumbnail((LADO, LADO), Image.LANCZOS)
    arr = np.array(im)
    arr = cv2.LUT(arr, curva())
    arr = menos_ciano(arr)
    im = Image.fromarray(arr).filter(ImageFilter.UnsharpMask(radius=1.2, percent=55, threshold=2))
    im.save(destino, "WEBP", quality=QUALIDADE, method=6)
    return im.size, destino.stat().st_size


def main():
    org, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    for k, nome in FOTOS.items():
        tam, peso = tratar(org / f"{k}.jpg", dst / f"{nome}.webp")
        print(f"{k} -> {nome}.webp  {tam[0]}x{tam[1]}  {peso // 1024} KB")


if __name__ == "__main__":
    main()
