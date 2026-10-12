"""Fábrica de evidências do Dia 2 — gera desafio/pistas.txt, desafio/decodificador.sh
e desafio/suspeitos.txt.

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia02.py
Tudo é fictício. Só stdlib.

Como a pista funciona
---------------------
Cada linha de pistas.txt tem o formato  ordem;metodo;dado
  - metodo "inverte": o texto está de trás para frente (o comando `rev` desfaz)
  - metodo "numeros": cada letra virou um número (a=1 ... z=26; 0 = "_"),
    separados por hífen
  - metodo "ruido":   lixo que o Bento colou junto — deve ser IGNORADO
As linhas estão embaralhadas; a coluna "ordem" diz a posição do pedaço.
"""
from pathlib import Path
import random

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-02-bash-script" / "desafio"

# Pedaços da resposta, na ordem certa (a flag é VAZANTE{ + pedaços + }).
PEDACOS = ["o_", "bento_", "sabia_", "que_", "laco_", "resolve"]
RUIDOS = ["cafe_frio", "reuniao_as_9", "senha_errada", "teste_teste", "nao_e_isso"]


def em_numeros(texto: str) -> str:
    """'que_' -> '17-21-5-0'"""
    return "-".join("0" if c == "_" else str(ord(c) - 96) for c in texto)


def gerar_pistas() -> str:
    linhas = []
    for i, pedaco in enumerate(PEDACOS, start=1):
        metodo = "inverte" if i % 2 else "numeros"
        dado = pedaco[::-1] if metodo == "inverte" else em_numeros(pedaco)
        linhas.append(f"{i};{metodo};{dado}")
    for ruido in RUIDOS:
        linhas.append(f"0;ruido;{ruido[::-1]}")
    random.Random(2026).shuffle(linhas)
    cabecalho = (
        "# pistas.txt — copiado do caderno do Bento em 2026-03-02\n"
        "# formato: ordem;metodo;dado   (metodos: inverte, numeros, ruido)\n"
    )
    return cabecalho + "\n".join(linhas) + "\n"


DECODIFICADOR = r'''#!/usr/bin/env bash
# =============================================================================
#  decodificador.sh — rascunho do Bento (INCOMPLETO!)
#  Uso:  bash decodificador.sh pistas.txt
#
#  "Comecei e não terminei. A função de 'inverte' funciona. A de 'numeros'
#   eu deixei pela metade. E falta pular as linhas de ruído e montar a
#   resposta na ordem certa. Termina pra mim? — Bento"
# =============================================================================

ARQUIVO="${1:-pistas.txt}"      # variável com valor padrão

# Função 1 — PRONTA: desfaz o texto invertido
decodificar_inverte() {
  echo "$1" | rev
}

# Função 2 — INCOMPLETA: transforma "17-21-5-0" em "que_"
#   dica: troque os hífens por espaços e use um laço for em cada número;
#   0 vira "_" e N vira a N-ésima letra (o Bento deixou o alfabeto pronto).
decodificar_numeros() {
  local alfabeto="abcdefghijklmnopqrstuvwxyz"
  local resultado=""
  # TODO: laço for sobre os números de "$1"
  echo "${resultado:-[numeros: ainda não implementado]} ($alfabeto)"
}

# Laço principal — lê o arquivo linha por linha
while IFS=';' read -r ordem metodo dado; do
  # TODO: pular comentários (linhas que começam com #) e linhas de "ruido"
  if [ "$metodo" = "inverte" ]; then
    echo "$ordem -> $(decodificar_inverte "$dado")"
  else
    echo "$ordem -> $(decodificar_numeros "$dado")"
  fi
done < "$ARQUIVO"

# TODO: ordenar os pedaços pela coluna "ordem" e juntar tudo em VAZANTE{...}
'''

SUSPEITOS = (
    "vítima 014\n"
    "vítima 022\n"
    "vítima 031\n"
    "vítima 047\n"
    "vítima 058\n"
)


def main() -> None:
    DESAFIO.mkdir(parents=True, exist_ok=True)
    (DESAFIO / "pistas.txt").write_text(gerar_pistas(), encoding="utf-8")
    (DESAFIO / "decodificador.sh").write_text(DECODIFICADOR, encoding="utf-8")
    (DESAFIO / "vitimas.txt").write_text(SUSPEITOS, encoding="utf-8")
    print(f"Evidências do Dia 2 criadas em {DESAFIO}")


if __name__ == "__main__":
    main()
