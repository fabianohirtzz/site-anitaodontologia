"""Melhora fotos reais (baixa resolução) com o Gemini, usando a própria foto como referência.

Usa o GeminiWrapper do gerador da Vocical e a chave do .env de lá (não copiar a chave para este repo).
Uso: python -I tools/imagens/melhorar.py <entrada> <saida.png> <largura> <altura> [tipo]
tipo: retrato | ambiente (padrão)
"""
import sys

GER = r"E:/Freela In Home/posts-project/vocical/gerador"
sys.path.insert(0, GER)
from dotenv import load_dotenv  # noqa: E402

load_dotenv(GER + "/.env")
import os  # noqa: E402

if os.environ.get("ANITA_IMG_BACKEND", "openai") == "gemini":
    from gemini_wrapper import GeminiWrapper as Motor  # noqa: E402
else:
    from openai_wrapper import OpenAIWrapper as _O  # noqa: E402

    def Motor():
        return _O(quality="high")

BASE = (
    "Restore and enhance THIS EXACT photograph. Output the same photo at higher resolution: sharper details, "
    "less noise and compression artifacts, clean natural daylight, true-to-life colors, slightly brighter and airy. "
    "Keep the composition, framing, every object, furniture, layout and proportions identical. "
    "Do not add, remove or invent anything. No text, no logos, no watermark. Photorealistic, not glossy, not CGI."
)
EXTRA = {
    "retrato": " Keep the woman's face, identity, expression, hair, skin texture and clothing exactly the same. Do not beautify or retouch the face.",
    "ambiente": " If the photo has fisheye/wide-angle distortion, gently straighten vertical lines while keeping the same view.",
}


def main():
    src, out, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    tipo = sys.argv[5] if len(sys.argv) > 5 else "ambiente"
    data = Motor().generate(BASE + EXTRA[tipo], w, h, ref_paths=[src])
    with open(out, "wb") as fh:
        fh.write(data)
    print("ok", out)


if __name__ == "__main__":
    main()
