"""Dia 7 — o mesmo do terminal, em Python puro (só biblioteca padrão).

Rode:  python3 equivalente.py

Ponte Linux -> Python:
    sed 's/a/b/'          -> linha.replace("a", "b", 1)
    sed 's/a/b/g'         -> linha.replace("a", "b")   ou  re.sub(r"a", "b", linha)
    sed 's/[0-9]/#/g'     -> re.sub(r"[0-9]", "#", linha)
    sed -n 7p             -> linhas[6]
    sed -n 5,9p           -> linhas[4:9]
    sed '/padrão/d'       -> [l for l in linhas if not re.search("padrão", l)]
    awk '{print NR, $0}'  -> for nr, linha in enumerate(linhas, 1)
    awk -F, '{print $1}'  -> csv.reader(...)  ->  campos[0]
    awk '/^v/'            -> if linha.startswith("v")
    soma[$3] += $4        -> collections.defaultdict(float)
"""
from collections import Counter, defaultdict
from pathlib import Path
import csv
import re

AQUI = Path(__file__).resolve().parent
DESAFIO = AQUI / "desafio"


def main() -> None:
    relatorio = (DESAFIO / "relatorio.txt").read_text(encoding="utf-8").splitlines()
    print("sed s///   ->", relatorio[0].replace("Normal", "SUSPEITO", 1))
    print("sed -n 7p  ->", relatorio[6])
    print("sed -n 5,9p->", relatorio[4:9])
    print("sed s/[0-9]/#/g ->", re.sub(r"[0-9]", "#", "454545 contas"))
    sem_linhas = [l for l in relatorio if not l.startswith("linha")]   # sed '/^linha/d'
    print("sed /^linha/d -> sobraram", len(sem_linhas), "linhas")

    # awk -F, com csv.DictReader (entende cabeçalho e aspas)
    with open(DESAFIO / "vitimas.csv", encoding="utf-8", newline="") as f:
        vitimas = list(csv.DictReader(f))
    for nr, v in enumerate(vitimas, start=2):
        print(f"awk NR={nr}: {v['Nome']} {v['Prejuizo']}")
    por_cidade = defaultdict(int)
    for v in vitimas:
        por_cidade[v["Cidade"]] += int(v["Prejuizo"])
    print("soma por cidade ->", dict(por_cidade))

    # Extrato: contar x somar
    with open(DESAFIO / "extrato.csv", encoding="utf-8", newline="") as f:
        pix = [t for t in csv.DictReader(f) if t["tipo"] == "PIX"]
    contagem = Counter(t["destino"] for t in pix)
    print("\nTransferências por conta (contagem):", contagem.most_common(3))
    print("Total em PIX: R$ %.2f" % sum(float(t["valor"]) for t in pix))
    print("(Somar por conta e limpar o apelido fica para você!)")

    # Limpeza do contas.txt (sed -e '/^#/d' -e 's/ *##fim$//' -e 's/~/ /g')
    for linha in (DESAFIO / "contas.txt").read_text(encoding="utf-8").splitlines():
        if linha.startswith("#"):
            continue
        conta, apelido = [p.strip() for p in re.sub(r"\s*##fim$", "", linha).split(";")]
        print(f"{conta:8} -> {apelido.replace('~', ' ')}")


if __name__ == "__main__":
    main()
