"""Gera docs/dados.js (lista dos dias + hashes das flags) para o site do curso.

Uso:  python3 ferramentas/gerar_site.py            # gera
      python3 ferramentas/gerar_site.py --checar   # confere se está em dia (CI)

Lê o mapa de capítulos de historia/README.md e o hash de cada checar.sh.
Só biblioteca padrão.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / "docs" / "dados.js"


def rank(n: int) -> str:
    if n <= 7:
        return "D"
    if n <= 14:
        return "C"
    if n <= 19:
        return "B"
    return "A" if n == 20 else "S"


def main() -> int:
    mapa = {}
    texto = (RAIZ / "historia" / "README.md").read_text(encoding="utf-8")
    for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", texto, flags=re.M):
        mapa[int(m.group(1))] = (m.group(2), m.group(3))

    dias = []
    for pasta in sorted((RAIZ / "dias").glob("dia-*")):
        n = int(pasta.name.split("-")[1])
        capitulo, tema = mapa.get(n, (pasta.name, ""))
        checar = pasta / "checar.sh"
        h = ""
        if checar.exists():
            achado = re.search(r"\b([0-9a-f]{64})\b", checar.read_text(encoding="utf-8"))
            h = achado.group(1) if achado else ""
        dias.append({
            "n": n, "slug": pasta.name, "capitulo": capitulo,
            "tema": tema.replace("`", ""), "rank": rank(n), "hash": h,
            "interativo": n in (8, 9),
        })

    conteudo = (
        "// Gerado por ferramentas/gerar_site.py — não edite à mão.\n"
        "window.DIAS = " + json.dumps(dias, ensure_ascii=False, indent=1) + ";\n"
    )
    if "--checar" in sys.argv:
        if not DESTINO.exists() or DESTINO.read_text(encoding="utf-8") != conteudo:
            print("docs/dados.js desatualizado. Rode: python3 ferramentas/gerar_site.py")
            return 1
        return 0
    DESTINO.parent.mkdir(exist_ok=True)
    DESTINO.write_text(conteudo, encoding="utf-8")
    print(f"✔ {DESTINO.relative_to(RAIZ)} ({len(dias)} dias)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
