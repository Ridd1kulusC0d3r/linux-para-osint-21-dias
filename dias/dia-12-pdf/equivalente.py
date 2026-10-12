"""Dia 12 — metadados, texto e imagens de um PDF em Python puro (só stdlib).

Rode:  python3 equivalente.py

Um PDF é um arquivo com "objetos" numerados. Os metadados ficam num
dicionário (/Info), o texto fica em "streams" com comandos como (Olá) Tj, e as
imagens JPEG ficam em streams marcados com /DCTDecode. Este script lê tudo
isso com expressões regulares — funciona no NOSSO contrato, que não é
comprimido. PDFs do mundo real costumam comprimir os streams (/FlateDecode);
aí entra zlib.decompress() ou uma biblioteca como pypdf (veja o README).

Ponte Linux -> Python:
    pdfinfo / exiftool    -> regex no dicionário /Info
    pdftotext             -> regex nos operadores (texto) Tj dos streams
    pdfimages -all        -> recortar os bytes entre stream/endstream dos /DCTDecode
    grep ^Producer        -> info.get("Producer")
"""
from pathlib import Path
import re
import tempfile

AQUI = Path(__file__).resolve().parent
PDF = AQUI / "desafio" / "contrato-pixvelox.pdf"


def desescapar(texto: bytes) -> str:
    """Desfaz os escapes de string de PDF: \\( \\) \\\\ ."""
    return re.sub(rb"\\([()\\])", rb"\1", texto).decode("latin-1")


def ler_info(dados: bytes) -> dict:
    num = re.search(rb"/Info (\d+) 0 R", dados).group(1)
    corpo = re.search(rb"\n" + num + rb" 0 obj\n<<(.*?)>>\nendobj", dados, re.S).group(1)
    return {k.decode(): desescapar(v) for k, v in re.findall(rb"/(\w+) \(((?:\\.|[^\\)])*)\)", corpo)}


def ler_texto(dados: bytes) -> list[str]:
    linhas = []
    for bloco in re.findall(rb"BT(.*?)ET", dados, re.S):
        linhas += [desescapar(t) for t in re.findall(rb"\(((?:\\.|[^\\)])*)\) Tj", bloco)]
    return linhas


def extrair_jpegs(dados: bytes, pasta: Path) -> list[Path]:
    saidas = []
    for i, m in enumerate(re.finditer(rb"/Filter /DCTDecode[^>]*>>\nstream\n", dados)):
        fim = dados.index(b"\nendstream", m.end())
        arq = pasta / f"imagem-{i:03d}.jpg"
        arq.write_bytes(dados[m.end():fim])
        saidas.append(arq)
    return saidas


def main() -> None:
    dados = PDF.read_bytes()
    print("cabeçalho ->", dados[:8].decode())

    info = ler_info(dados)
    print("\npdfinfo ->")
    for chave, valor in info.items():
        print(f"  {chave:<13} {valor}")
    print("grep ^Producer ->", info.get("Producer"))

    texto = ler_texto(dados)
    print("\npdftotext (linhas com 'verificação') ->")
    for i, linha in enumerate(texto):
        if "verificação" in linha:
            print("  ", linha, "|", texto[i + 1])

    with tempfile.TemporaryDirectory() as tmp:
        imagens = extrair_jpegs(dados, Path(tmp))
        print(f"\npdfimages -all -> {len(imagens)} imagens:",
              ", ".join(f"{p.name} ({p.stat().st_size} bytes)" for p in imagens))

    print("\nflag -> VAZANTE{" + info["Keywords"] + "}")


if __name__ == "__main__":
    main()
