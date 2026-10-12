"""Dia 3 — o mesmo do terminal, em Python puro (só biblioteca padrão).

Rode:  python3 equivalente.py

Ponte Linux -> Python:
    command -v zip               -> shutil.which("zip")
    dpkg -l / pip list           -> importlib.metadata.distributions()  (pacotes Python)
    zip archive a.txt b.txt      -> zipfile.ZipFile(..., "w").write()
    zip -sf / unzip -l           -> ZipFile.namelist() / ZipFile.infolist()
    unzip -d pasta               -> ZipFile.extractall(pasta)
    unzip -p arquivo.zip x.txt   -> ZipFile.read("x.txt")
    unzip -P senha               -> ZipFile.read(..., pwd=b"senha")
    unzip -t                     -> ZipFile.testzip()

Atenção: o zipfile do Python LÊ zips com senha (ZipCrypto), mas não CRIA.
"""
from importlib import metadata
from pathlib import Path
import shutil
import tempfile
import zipfile

AQUI = Path(__file__).resolve().parent
DESAFIO = AQUI / "desafio"


def main() -> None:
    # command -v: onde estão os programas?
    for prog in ("zip", "unzip", "ls"):
        print(f"command -v {prog:6} -> {shutil.which(prog) or 'não instalado'}")

    # Pacotes Python instalados (o "dpkg -l" do mundo pip)
    pacotes = sorted({d.metadata["Name"] or "?" for d in metadata.distributions()}, key=str.lower)
    print(f"\nPacotes Python instalados: {len(pacotes)} (primeiros: {', '.join(pacotes[:5])})")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        # zip archive test1.txt test2.txt
        arquivo = tmp / "archive.zip"
        with zipfile.ZipFile(arquivo, "w", zipfile.ZIP_DEFLATED) as z:
            for nome in ("test1.txt", "test2.txt"):
                z.write(DESAFIO / nome, arcname=nome)

        with zipfile.ZipFile(arquivo) as z:
            print("\nzip -sf archive.zip ->", z.namelist())          # listar sem extrair
            print("unzip -t ->", "OK" if z.testzip() is None else "CORROMPIDO")
            z.extractall(tmp / "archive")                            # unzip -d archive
            print("unzip -p test1.txt ->", z.read("test1.txt").decode().strip())
        print("extraídos:", sorted(p.name for p in (tmp / "archive").iterdir()))

    # Os zips do desafio: listar sem extrair
    with zipfile.ZipFile(DESAFIO / "evidencia.zip") as z:
        print("\nunzip -l evidencia.zip:")
        for info in z.infolist():
            trancado = "🔒" if info.flag_bits & 0x1 else "  "
            print(f"  {trancado} {info.file_size:>5}  {info.filename}")
        try:
            z.read("evidencia/relatorio-saque.txt")
        except RuntimeError as e:          # sem senha, o Python recusa
            print("  sem senha ->", e)
    with zipfile.ZipFile(DESAFIO / "inventario.zip") as z:
        print(f"\ninventario.zip tem {len(z.namelist())} entradas. Leia os NOMES com atenção.")


if __name__ == "__main__":
    main()
