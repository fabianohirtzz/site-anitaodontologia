"""Upscale fiel de fotos reais via Fal.ai (não redesenha a imagem).

Usa a FAL_KEY do .env do gerador da Vocical (não copiar a chave para este repo público).
Uso: python tools/imagens/upscale.py <entrada> <saida> [modelo] [escala]
modelo: esrgan (padrão, mais fiel) | clarity (mais nítido, pode inventar textura)
"""
import sys
import httpx
from dotenv import load_dotenv

load_dotenv(r"E:/Freela In Home/posts-project/vocical/gerador/.env")
import fal_client  # noqa: E402

ENDPOINTS = {
    "esrgan": lambda url, s: ("fal-ai/esrgan", {"image_url": url, "scale": s, "model": "RealESRGAN_x4plus", "face": True}),
    "clarity": lambda url, s: ("fal-ai/clarity-upscaler", {"image_url": url, "upscale_factor": s, "creativity": 0.2, "resemblance": 0.9,
                                                          "prompt": "photo, sharp, natural light, high detail"}),
}


def main():
    src, out = sys.argv[1], sys.argv[2]
    modelo = sys.argv[3] if len(sys.argv) > 3 else "esrgan"
    escala = float(sys.argv[4]) if len(sys.argv) > 4 else 3
    url = fal_client.upload_file(src)
    endpoint, args = ENDPOINTS[modelo](url, escala)
    res = fal_client.subscribe(endpoint, arguments=args, with_logs=False)
    img = res.get("image") or (res.get("images") or [{}])[0]
    with open(out, "wb") as fh:
        fh.write(httpx.get(img["url"], timeout=120, follow_redirects=True).content)
    print("ok", out)


if __name__ == "__main__":
    main()
