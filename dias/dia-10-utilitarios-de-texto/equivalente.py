"""Dia 10 — cut, sort, uniq, comm, diff, tr e paste em Python puro (só stdlib).

Rode:  python3 equivalente.py

A grande sacada: `comm` é uma INTERSEÇÃO DE CONJUNTOS. Em Python, `set`
faz isso direto (e nem precisa ordenar antes).

Ponte Linux -> Python:
    cat a b > c           -> c.write_text(a.read_text() + b.read_text())
    cut -d, -f1           -> linha.split(",")[0]          (ou o módulo csv)
    cut -c 5-10           -> linha[4:10]
    sort / sort -r        -> sorted(x) / sorted(x, reverse=True)
    sort -u               -> sorted(set(x))
    uniq -c | sort -rn    -> collections.Counter(x).most_common()
    wc -l                 -> len(linhas)
    comm -12 a b          -> set(a) & set(b)
    comm -23 a b          -> set(a) - set(b)
    diff -u a b           -> difflib.unified_diff(a, b)
    tr 'A-Z' 'a-z'        -> texto.lower()
    paste -d, a b         -> ",".join(par) for par in zip(a, b)
"""
from collections import Counter
from pathlib import Path
import csv
import difflib

AQUI = Path(__file__).resolve().parent
DESAFIO = AQUI / "desafio"


def ler_csv(caminho: Path, separador: str) -> list[dict]:
    """Lê um CSV com cabeçalho e devolve uma lista de dicionários."""
    with open(caminho, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=separador))


def main() -> None:
    grupo_a = ler_csv(DESAFIO / "grupo-a-cashback-vip.csv", ",")
    grupo_b = ler_csv(DESAFIO / "grupo-b-suporte-pix.txt", ";")
    print(f"wc -l -> grupo A: {len(grupo_a)} linhas · grupo B: {len(grupo_b)} linhas")

    # cut -c 5-10 na primeira linha
    print("cut -c 5-10 ->", grupo_a[0]["telefone"][4:10])

    # sort | uniq -c | sort -rn
    contagem = Counter(l["telefone"] for l in grupo_a)
    print("uniq -c (top 3) ->", contagem.most_common(3))

    # comm -12: telefones nos DOIS grupos
    tel_a = {l["telefone"] for l in grupo_a}
    tel_b = {l["TELEFONE"] for l in grupo_b}
    comuns = sorted(tel_a & tel_b)
    print("comm -12 ->", comuns)
    print("comm -23 -> só no grupo A:", len(tel_a - tel_b), "telefones")

    for tel in comuns:
        apelido_a = next(l["apelido"] for l in grupo_a if l["telefone"] == tel)
        apelido_b = next(l["APELIDO"] for l in grupo_b if l["TELEFONE"] == tel).lower()  # tr
        print("flag -> VAZANTE{" + f"{apelido_a}_{apelido_b}" + "}")

    # diff -u: quem entrou e quem saiu
    ontem = (DESAFIO / "grupo-a-ontem.csv").read_text(encoding="utf-8").splitlines()
    hoje = (DESAFIO / "grupo-a-cashback-vip.csv").read_text(encoding="utf-8").splitlines()
    print("\ndiff -u (só mudanças):")
    for linha in difflib.unified_diff(ontem, hoje, lineterm="", n=0):
        if linha[:1] in "+-" and not linha.startswith(("+++", "---")):
            print("  ", linha)

    # paste -d,
    tels = [l["TELEFONE"] for l in grupo_b[:3]]
    apelidos = [l["APELIDO"].lower() for l in grupo_b[:3]]
    print("\npaste -d, ->")
    for par in zip(tels, apelidos):
        print("  ", ",".join(par))


if __name__ == "__main__":
    main()
