"""Dia 6 — grep em Python puro (só biblioteca padrão).

Rode:  python3 equivalente.py

Ponte Linux -> Python:
    grep -F texto      -> if "texto" in linha
    grep -i            -> linha.lower()
    grep -n            -> enumerate(linhas, start=1)
    grep -v            -> if "texto" not in linha
    grep -E -o regex   -> re.findall(regex, texto)
    grep -r            -> Path.rglob("*")
    sort | uniq -c     -> collections.Counter
"""
import re
from collections import Counter
from pathlib import Path

DESAFIO = Path(__file__).resolve().parent / "desafio"
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def main() -> None:
    denuncias = (DESAFIO / "denuncias.txt").read_text(encoding="utf-8").splitlines()
    log = (DESAFIO / "log-suporte.txt").read_text(encoding="utf-8").splitlines()

    # grep -c / grep -ci
    print("grep -cF pixvelox :", sum("pixvelox" in l for l in denuncias))
    print("grep -ciF pixvelox:", sum("pixvelox" in l.lower() for l in denuncias))

    # grep -n
    for n, linha in enumerate(denuncias, start=1):
        if "remetente: suporte@" in linha:
            print(f"grep -n -> {n}: {linha[:60]}…")
            break

    # grep -r -l
    com_lgpd = [p.name for p in sorted(DESAFIO.rglob("*.txt")) if "LGPD" in p.read_text(encoding="utf-8")]
    print("grep -rl LGPD ->", com_lgpd)

    # grep -Eo + sort -u
    emails = set(EMAIL.findall("\n".join(log)))
    print("e-mails únicos no log:", len(emails))

    # domínios: grep -Eo '@...' | sort | uniq -c
    dominios = Counter(e.split("@", 1)[1] for e in EMAIL.findall("\n".join(log)))
    for dominio, qtd in dominios.most_common():
        print(f"  {qtd:5d}  {dominio}")


if __name__ == "__main__":
    main()
