"""Fábrica de evidências do Dia 11 — gera o "vídeo do golpe" e companhia.

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia11.py
Precisa de: Pillow (PIL) e ffmpeg. Tudo é fictício.

Arquivos
--------
desafio/video-golpe.mp4     5 s, 640x360, 1 quadro por segundo de "propaganda".
                            O 4º segundo mostra, por 1 s, o código de resgate.
                            Metadados (título, autor, comentário) com pistas.
desafio/print-suporte.png   "print" de conversa do falso suporte (para OCR).
desafio/audio-golpe.mp3     bipe de 3 s, estéreo 44,1 kHz, com metadados ID3 (artist = mare_alta).

Como a pista funciona
---------------------
Assistindo ao vídeo, o quadro do código passa rápido. Quem extrai os quadros
(ffmpeg -r 1) e passa OCR (tesseract) em cada um, lê a flag no 4º quadro.
O print-suporte.png e os metadados (exiftool/ffprobe) dão o contexto.
"""
from pathlib import Path
import shutil
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-11-video-audio-imagem" / "desafio"
FLAG = "VAZANTE{quadro_a_quadro}"

FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONTE_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

# (cor de fundo, cor do texto, linhas)
QUADROS = [
    ("#0b3d2e", "white", ["PixVelox", "o Pix que devolve"]),
    ("#0b3d2e", "white", ["CASHBACK DE 10%", "em todo Pix"]),
    ("#0b3d2e", "white", ["Fale com o suporte", "e libere o bonus"]),
    ("white", "black", ["CODIGO DE RESGATE:", FLAG]),
    ("#0b3d2e", "white", ["pixvelox.example", "oferta por tempo limitado"]),
]


def quadro(fundo: str, cor: str, linhas: list[str], destino: Path) -> None:
    img = Image.new("RGB", (640, 360), fundo)
    d = ImageDraw.Draw(img)
    mono = cor == "black"
    fonte = ImageFont.truetype(FONTE_MONO if mono else FONTE, 34 if mono else 40)
    y = 120
    for linha in linhas:
        largura = d.textlength(linha, font=fonte)
        d.text(((640 - largura) / 2, y), linha, fill=cor, font=fonte)
        y += 70
    img.save(destino)


def print_suporte(destino: Path) -> None:
    """Imagem que imita um print de conversa (texto em inglês simples p/ o OCR 'eng')."""
    img = Image.new("RGB", (560, 300), "#ece5dd")
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONTE, 22)
    baloes = [
        (20, "#ffffff", "PixVelox Support: your cashback is ready"),
        (60, "#ffffff", "Send me the 6 digit code from the SMS"),
        (100, "#dcf8c6", "Victim 014: ok, the code is 482913"),
        (140, "#ffffff", "PixVelox Support: thank you. Wait 24h"),
        (190, "#ffffff", "operator: mare_alta | pixvelox.example"),
    ]
    for y, cor, texto in baloes:
        w = d.textlength(texto, font=f)
        d.rectangle([14, y - 6, 26 + w, y + 30], fill=cor)
        d.text((20, y), texto, fill="black", font=f)
    img.save(destino)


def main() -> None:
    if not shutil.which("ffmpeg"):
        raise SystemExit("Preciso do ffmpeg para gerar o vídeo: sudo apt install ffmpeg")
    DESAFIO.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        for i, (fundo, cor, linhas) in enumerate(QUADROS, 1):
            quadro(fundo, cor, linhas, t / f"q{i}.png")
        # 1 imagem por segundo + um bipe; H.264 leve; metadados de propósito
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-framerate", "1", "-i", str(t / "q%d.png"),
            "-f", "lavfi", "-i", "sine=frequency=660:duration=5",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "28", "-r", "10",
            "-c:a", "aac", "-b:a", "24k", "-shortest",
            "-metadata", "title=PixVelox cashback - campanha marco",
            "-metadata", "artist=mare_alta",
            "-metadata", "comment=render final - nao postar o quadro 4",
            "-metadata", "creation_time=2026-03-08T22:41:00Z",
            "-map_metadata", "-1", "-fflags", "+bitexact",
            str(DESAFIO / "video-golpe.mp4"),
        ], check=True)
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", "sine=frequency=440:duration=3",
        "-ar", "44100", "-ac", "2", "-c:a", "libmp3lame", "-b:a", "48k",
        "-metadata", "artist=mare_alta",
        "-metadata", "title=audio do golpe - roteiro 3",
        "-metadata", "comment=gravado no celular do suporte",
        "-fflags", "+bitexact",
        str(DESAFIO / "audio-golpe.mp3"),
    ], check=True)
    print_suporte(DESAFIO / "print-suporte.png")
    print(f"Evidências do Dia 11 criadas em {DESAFIO}")


if __name__ == "__main__":
    main()
