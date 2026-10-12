"""Dia 11 — metadados de vídeo, áudio e imagem em Python puro (só stdlib).

Rode:  python3 equivalente.py

Python sem bibliotecas extras não decodifica vídeo nem faz OCR. Mas consegue
LER A ESTRUTURA dos arquivos — e é ali que moram os metadados. E, quando o
ffmpeg/tesseract existem, `subprocess` chama os dois do mesmo jeito que o
terminal.

Ponte Linux -> Python:
    exiftool video.mp4     -> percorrer as "caixas" (atoms) do MP4 com struct
    exiftool audio.mp3     -> ler a etiqueta ID3v2 no começo do MP3
    exiftool -ImageSize    -> ler largura/altura no cabeçalho do PNG
    ffmpeg -ar 16000 -ac 1 -> módulo wave (gera/lê WAV)
    ffmpeg ... / tesseract -> subprocess.run([...])
"""
from pathlib import Path
import math
import shutil
import struct
import subprocess
import tempfile
import wave

AQUI = Path(__file__).resolve().parent
DESAFIO = AQUI / "desafio"
CAIXAS_COM_FILHAS = {b"moov", b"udta", b"ilst"}


def atoms_mp4(dados: bytes, inicio: int = 0, fim: int | None = None):
    """Percorre as caixas de um MP4: [tamanho 4 bytes][tipo 4 bytes][conteúdo]."""
    fim = len(dados) if fim is None else fim
    pos = inicio
    while pos + 8 <= fim:
        tamanho, tipo = struct.unpack(">I4s", dados[pos:pos + 8])
        if tamanho < 8:
            break
        yield tipo, pos + 8, pos + tamanho
        if tipo in CAIXAS_COM_FILHAS:
            yield from atoms_mp4(dados, pos + 8, pos + tamanho)
        elif tipo == b"meta":                       # "meta" tem 4 bytes extras
            yield from atoms_mp4(dados, pos + 12, pos + tamanho)
        pos += tamanho


def metadados_mp4(caminho: Path) -> dict:
    dados = caminho.read_bytes()
    nomes = {b"\xa9nam": "Title", b"\xa9ART": "Artist", b"\xa9cmt": "Comment"}
    achados = {}
    for tipo, ini, fim in atoms_mp4(dados):
        if tipo in nomes:
            # dentro vem uma caixa "data": 8 de cabeçalho + 8 de flags, depois o texto
            achados[nomes[tipo]] = dados[ini + 16:fim].decode("utf-8", "replace")
    return achados


def metadados_id3(caminho: Path) -> dict:
    """Lê os quadros de texto (TIT2, TPE1...) de uma etiqueta ID3v2.3/2.4."""
    dados = caminho.read_bytes()
    if dados[:3] != b"ID3":
        return {}
    tam = 0
    for b in dados[6:10]:                       # tamanho "synchsafe": 7 bits por byte
        tam = (tam << 7) | b
    pos, achados = 10, {}
    while pos < 10 + tam:
        quadro, t = dados[pos:pos + 4], dados[pos + 4:pos + 8]
        if not quadro.strip(b"\x00"):
            break
        t = sum(b << (7 * (3 - i)) for i, b in enumerate(t)) if dados[3] == 4 else struct.unpack(">I", t)[0]
        conteudo = dados[pos + 10:pos + 10 + t]
        if quadro.startswith(b"T") and conteudo:
            cod = {0: "latin-1", 1: "utf-16", 3: "utf-8"}.get(conteudo[0], "latin-1")
            achados[quadro.decode()] = conteudo[1:].decode(cod, "replace").replace("\x00", " ").strip()
        pos += 10 + t
    return achados


def tamanho_png(caminho: Path) -> tuple[int, int]:
    """No PNG, largura e altura ficam nos bytes 16-24 (bloco IHDR)."""
    return struct.unpack(">II", caminho.read_bytes()[16:24])


def main() -> None:
    print("exiftool video-golpe.mp4 ->", metadados_mp4(DESAFIO / "video-golpe.mp4"))
    print("exiftool audio-golpe.mp3 ->", metadados_id3(DESAFIO / "audio-golpe.mp3"))
    print("exiftool -ImageSize print-suporte.png -> %dx%d" % tamanho_png(DESAFIO / "print-suporte.png"))

    with tempfile.TemporaryDirectory() as tmp:
        # WAV 16 kHz mono com o módulo wave (1 s de bipe a 440 Hz)
        wav = Path(tmp) / "bipe_16000.wav"
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(16000)
            w.writeframes(b"".join(struct.pack("<h", int(8000 * math.sin(2 * math.pi * 440 * i / 16000)))
                                   for i in range(16000)))
        with wave.open(str(wav)) as w:
            print(f"wave -> {w.getframerate()} Hz, {w.getnchannels()} canal(is), {w.getnframes()} amostras")

        # Se ffmpeg e tesseract existirem, o Python os chama como o terminal faria
        if shutil.which("ffmpeg") and shutil.which("tesseract"):
            subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(DESAFIO / "video-golpe.mp4"),
                            "-vf", "fps=1", f"{tmp}/q%d.png"], check=True)
            for q in sorted(Path(tmp).glob("q*.png")):
                texto = subprocess.run(["tesseract", str(q), "-"], capture_output=True, text=True).stdout
                print(f"OCR {q.name}: {' / '.join(texto.split(chr(10))[:2]).strip()}")
        else:
            print("ffmpeg/tesseract não instalados: pulando os quadros e o OCR.")


if __name__ == "__main__":
    main()
