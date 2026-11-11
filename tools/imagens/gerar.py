"""Gera imagens de ambientação (texto -> imagem) com o Gemini do gerador da Vocical.

A chave fica no .env de lá (não copiar para este repo). Nunca gerar "paciente" ou "resultado".
Uso: python -I tools/imagens/gerar.py <saida.webp> <largura> <altura> "<prompt>"
"""
import io
import sys

GER = r"E:/Freela In Home/posts-project/vocical/gerador"
sys.path.insert(0, GER)
from dotenv import load_dotenv  # noqa: E402

load_dotenv(GER + "/.env")
from gemini_wrapper import GeminiWrapper  # noqa: E402
from PIL import Image  # noqa: E402

ESTILO = (
    " Photorealistic editorial photography, soft natural daylight, airy and clean, cool light palette "
    "(off-white, very light mint, small deep teal accents), shallow depth of field, calm and premium. "
    "No people, no faces, no hands, no teeth close-ups, no patients, no before/after. No text, no logos, no watermark. "
    "Not CGI, not glossy 3D render."
)


def main():
    out, w, h, prompt = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    data = GeminiWrapper().generate(prompt + ESTILO, w, h)
    img = Image.open(io.BytesIO(data)).convert("RGB")
    img.save(out, "WEBP", quality=84, method=6)
    print("ok", out, img.size)


if __name__ == "__main__":
    main()
