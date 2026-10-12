"""Dia 4 — o mesmo do terminal, em Python puro (só biblioteca padrão).

Rode:  python3 equivalente.py

Ponte Linux -> Python:
    find pasta -name '*.txt' -type f   -> Path("pasta").rglob("*.txt")
    find ... -size +400c               -> p.stat().st_size > 400
    for i in $(find ...); do ...       -> for p in sorted(...):
    sed 's/ | /;/g' a > "${a%.txt}.csv" -> p.with_suffix(".csv").write_text(texto.replace(" | ", ";"))
    xargs grep -l palavra              -> [p for p in arquivos if "palavra" in p.read_text()]
    xargs rm -f                        -> p.unlink(missing_ok=True)
    xargs -I x zip arq.zip x           -> zipfile.ZipFile(...).write(x)
    xargs -P 4                         -> concurrent.futures.ThreadPoolExecutor(4)
    sort | uniq -c | sort -rn          -> collections.Counter(...).most_common()
"""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import zipfile

AQUI = Path(__file__).resolve().parent
CONVERSAS = AQUI / "desafio" / "conversas"


def main() -> None:
    arquivos = sorted(CONVERSAS.rglob("*.txt"))                       # find -name '*.txt'
    print(f"Arquivos .txt: {len(arquivos)}")
    grandes = [p for p in arquivos if p.stat().st_size > 400]          # find -size +400c
    print(f"Com mais de 400 bytes: {len(grandes)}")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        # conversão em massa .txt -> .csv (numa cópia)
        for p in CONVERSAS.joinpath("2026-03-01").glob("*.txt"):
            (tmp / p.name).with_suffix(".csv").write_text(
                p.read_text(encoding="utf-8").replace(" | ", ";"), encoding="utf-8")
        print("CSVs criados:", len(list(tmp.glob("*.csv"))))

        # xargs -I: zipar só as selecionadas
        lista = (AQUI / "desafio" / "selecionadas.txt").read_text(encoding="utf-8").split()
        with zipfile.ZipFile(tmp / "selecionadas.zip", "w") as z:
            for nome in lista:
                z.write(CONVERSAS / nome, arcname=nome)
            print("zip com selecionadas:", z.namelist())

        # xargs rm -f: apagar em lote
        for nome in ("a.zip", "b.zip"):
            (tmp / nome).touch()
        for p in tmp.glob("[ab].zip"):
            p.unlink(missing_ok=True)

    # cut -d'|' -f2 | sort | uniq -c | sort -rn
    quem = Counter()
    for p in arquivos:
        for linha in p.read_text(encoding="utf-8").splitlines():
            quem[linha.split("|")[1].strip()] += 1
    print("Mais ativos:", quem.most_common(5))

    # xargs -P 4: contar palavras em paralelo
    with ThreadPoolExecutor(4) as pool:
        total = sum(pool.map(lambda p: len(p.read_text(encoding="utf-8").split()), arquivos))
    print("Total de palavras:", total)

    # xargs grep -l: quais arquivos citam o operador?
    citam = [p for p in arquivos if "mare_alta" in p.read_text(encoding="utf-8")]
    print(f"Arquivos que citam mare_alta: {len(citam)} (a flag fica para você!)")


if __name__ == "__main__":
    main()
