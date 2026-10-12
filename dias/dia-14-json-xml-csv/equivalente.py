"""Dia 14 — JSON, XML e CSV em Python puro (só biblioteca padrão).

Rode:  python3 equivalente.py

Os três formatos têm módulo pronto na stdlib: json, xml.etree.ElementTree e
csv. Os filtros do jq viram compreensões de lista ("list comprehensions").

Ponte Linux -> Python:
    jq '.membros[0].handle'          -> dados["membros"][0]["handle"]
    jq '.membros[].handle'           -> [m["handle"] for m in dados["membros"]]
    jq 'select(.admin)'              -> [m for m in ... if m["admin"]]
    jq 'map(.id)'                    -> [m["id"] for m in ...]
    jq 'group_by | length'           -> collections.Counter
    jq -r '... | @csv'               -> csv.writer
    xmlstarlet sel -t -m //loc -v .  -> ElementTree.iter("{ns}loc")
    csvcut -c dominio,porta          -> csv.DictReader + escolher chaves
    csvgrep -c 2 -m PixVelox         -> if "PixVelox" in linha["titulo"]
    in2csv -k membros                -> csv.DictWriter(dados["membros"])
"""
from collections import Counter
from pathlib import Path
import csv
import json
import sys
import xml.etree.ElementTree as ET

AQUI = Path(__file__).resolve().parent
DESAFIO = AQUI / "desafio"
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def main() -> None:
    dados = json.loads((DESAFIO / "export-grupo.json").read_text(encoding="utf-8"))

    print("jq '.membros[0].handle' ->", dados["membros"][0]["handle"])
    print("jq '.membros[].handle'  ->", [m["handle"] for m in dados["membros"]])
    print("select(.admin)          ->", [m["handle"] for m in dados["membros"] if m["admin"]])
    print("map(.id) (5 primeiras)  ->", [m["id"] for m in dados["mensagens"][:5]])
    print("ranking por autor       ->", Counter(m["autor"]["handle"] for m in dados["mensagens"]).most_common(3))

    # select(.apagada and .autor.handle == "mare_alta") | .texto_original
    pedacos = [m["texto_original"] for m in dados["mensagens"]
               if m["apagada"] and m["autor"]["handle"] == "mare_alta"]
    print("flag ->", "".join(pedacos))

    # in2csv -k membros  (direto na tela)
    print("\nin2csv -k membros ->")
    escritor = csv.DictWriter(sys.stdout, fieldnames=list(dados["membros"][0]), lineterminator="\n")
    escritor.writeheader()
    escritor.writerows(dados["membros"])

    # xmlstarlet sel -t -m "//_:url" -v "_:loc"
    raiz = ET.parse(DESAFIO / "sitemap.xml").getroot()
    print("\nxmlstarlet (prioridade < 0.5) ->")
    for url in raiz.iter(f"{NS}url"):
        if float(url.findtext(f"{NS}priority")) < 0.5:
            print("  ", url.findtext(f"{NS}loc"))

    # csvgrep -c 2 -m PixVelox | csvcut -c dominio,porta
    print("\ncsvgrep + csvcut ->")
    with open(DESAFIO / "dominios.csv", encoding="utf-8", newline="") as f:
        for linha in csv.DictReader(f):
            if "PixVelox" in linha["titulo"]:
                print(f"   {linha['dominio']},{linha['porta']}")


if __name__ == "__main__":
    main()
