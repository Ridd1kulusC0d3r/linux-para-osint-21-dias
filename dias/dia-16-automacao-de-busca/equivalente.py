"""Dia 16 — o mesmo do terminal, em Python puro (só biblioteca padrão).

Rode:  python3 equivalente.py

Ponte Linux -> Python:
    grep -o '\\[.*]'           -> re.findall(r"\\[(.*)\\]", linha)
    jq -r '.[] | .url'         -> [r["url"] for r in json.load(f)]
    jq (JSON Lines)            -> json.loads(linha) para cada linha
    jq '$q | @uri'             -> urllib.parse.quote(q)
    sort -n                    -> sorted(..., key=...)
    comm -12 a b               -> set(a) & set(b)
    paste -sd_                 -> "_".join(lista)
"""
from pathlib import Path
from urllib.parse import quote
import json
import re

AQUI = Path(__file__).resolve().parent
DESAFIO = AQUI / "desafio"


def main() -> None:
    # 1. Sites entre colchetes na saída de texto do ddgr
    texto = (DESAFIO / "busca_pixvelox.txt").read_text(encoding="utf-8")
    sites = re.findall(r"\[(.*)\]", texto)
    print("sites no DuckDuckGo:", sites)

    # 2. Resultados JSON do ddgr: filtrar por palavra no resumo
    resultados = json.loads((DESAFIO / "busca_pixvelox.json").read_text(encoding="utf-8"))
    print("\nresumos que falam em 'código':")
    for r in resultados:
        if "código" in r["abstract"]:
            print("  -", r["title"])

    # 3. Dorks -> URLs de busca (urlencode)
    print("\nURLs de busca:")
    for dork in (DESAFIO / "dorks.txt").read_text(encoding="utf-8").splitlines():
        print("  https://duckduckgo.com/html/?q=" + quote(dork, safe=""))

    # 4. Netlas: JSON Lines (um objeto por linha)
    linhas = (DESAFIO / "netlas_resultados.json").read_text(encoding="utf-8").splitlines()
    servidores = [json.loads(l)["data"] for l in linhas if l.strip()]
    print(f"\n{len(servidores)} servidores no Netlas")

    # 5. comm -12: hosts que aparecem nas duas buscas
    comuns = sorted(set(sites) & {s["host"] for s in servidores})
    print("nas duas buscas:", comuns)

    # 6. O host do painel, portas em ordem, pedaços entre colchetes
    painel = [s for s in servidores if "painel" in s["host"] and s["http"]["title"]]
    painel.sort(key=lambda s: s["port"])
    pedacos = [re.search(r"\[([^]]*)\]", s["http"]["title"]).group(1) for s in painel]
    print("pedaços em ordem de porta:", len(pedacos), "(junte com _ e confira no checar.sh)")


if __name__ == "__main__":
    main()
