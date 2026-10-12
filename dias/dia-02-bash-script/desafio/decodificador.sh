#!/usr/bin/env bash
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
