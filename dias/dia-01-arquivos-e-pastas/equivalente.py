"""Dia 1 — o mesmo do terminal, em Python puro (só biblioteca padrão).

Rode:  python3 equivalente.py

Ponte Linux -> Python:
    pwd            -> Path.cwd()
    ls -la         -> Path.iterdir()  (Python mostra ocultos por padrão!)
    find -name     -> Path.rglob()
    cat            -> Path.read_text()
    mkdir -p       -> Path.mkdir(parents=True, exist_ok=True)
    echo >>        -> open(..., "a")
    cp -r          -> shutil.copytree()
    stat           -> Path.stat()
"""
from datetime import datetime
from pathlib import Path
import shutil
import tempfile

AQUI = Path(__file__).resolve().parent          # pasta do Dia 1
CASO = AQUI / "desafio" / "caso"


def listar(pasta: Path) -> None:
    """Equivale a `ls -la`: mostra tudo, inclusive arquivos ocultos."""
    for item in sorted(pasta.iterdir()):
        tipo = "d" if item.is_dir() else "-"
        print(f"  {tipo} {item.stat().st_size:>6}  {item.name}")


def ocultos(pasta: Path) -> list[Path]:
    """Equivale a `find . -type f -name '.*'`."""
    return sorted(p for p in pasta.rglob(".*") if p.is_file())


def main() -> None:
    print("pwd ->", Path.cwd())

    print("\nls -la desafio/caso")
    listar(CASO)

    print("\nArquivos ocultos encontrados:")
    for arq in ocultos(CASO):
        print("  ", arq.relative_to(CASO))

    # stat: quando o arquivo foi modificado?
    nota = CASO / "vitimas" / "belo-horizonte" / ".nota_iara.txt"
    quando = datetime.fromtimestamp(nota.stat().st_mtime)
    print(f"\nstat .nota_iara.txt -> modificado em {quando:%d/%m/%Y %H:%M}")

    # mkdir -p + echo >> + cp -r, numa pasta temporária (some ao final)
    with tempfile.TemporaryDirectory() as tmp:
        meu_caso = Path(tmp) / "meu-caso"
        for sub in ("evidencias", "notas", "relatorio"):
            (meu_caso / sub).mkdir(parents=True, exist_ok=True)

        diario = meu_caso / "notas" / "diario.txt"
        with open(diario, "a", encoding="utf-8") as f:   # "a" = append (>>)
            f.write("Dia 1 — recebi o pendrive da Mestra Iara\n")

        shutil.copytree(CASO / "vitimas", meu_caso / "evidencias" / "vitimas")
        copiados = sum(1 for p in (meu_caso / "evidencias").rglob("*") if p.is_file())
        print(f"\ncp -r -> {copiados} arquivos copiados para o meu caso (temporário)")
        print("cat diario.txt ->", diario.read_text(encoding="utf-8").strip())


if __name__ == "__main__":
    main()
