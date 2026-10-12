#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 2. Tente sozinho antes!
# Ideia: completar o decodificador do Bento.
#   1. while + read lê pistas.txt linha por linha, separando os campos por ";"
#   2. if pula comentários e linhas de "ruido"
#   3. uma função desfaz "inverte" (laço de trás para frente, igual ao `rev`) e outra desfaz "numeros" (laço for)
#   4. sort -n coloca os pedaços na ordem e tr -d '\n' junta tudo
cd "$(dirname "$0")/../dias/dia-02-bash-script/desafio" || exit 1

decodificar_inverte() {
  # mesmo efeito do `rev`, só com Bash: percorre o texto do fim para o começo
  local texto="$1" saida="" i
  for (( i = ${#texto} - 1; i >= 0; i-- )); do saida+="${texto:i:1}"; done
  echo "$saida"
}

decodificar_numeros() {
  local alfabeto="abcdefghijklmnopqrstuvwxyz" resultado="" n
  for n in ${1//-/ }; do                   # "17-21-5-0" vira "17 21 5 0"
    if [ "$n" -eq 0 ]; then
      resultado+="_"
    else
      resultado+="${alfabeto:n-1:1}"         # pega 1 letra na posição n-1
    fi
  done
  echo "$resultado"
}

pedacos=$(
  while IFS=';' read -r ordem metodo dado; do
    case "$ordem" in '#'*|'') continue ;; esac   # comentário ou linha vazia
    [ "$metodo" = "ruido" ] && continue           # lixo do Bento
    if [ "$metodo" = "inverte" ]; then
      echo "$ordem $(decodificar_inverte "$dado")"
    else
      echo "$ordem $(decodificar_numeros "$dado")"
    fi
  done < pistas.txt | sort -n | cut -d' ' -f2 | tr -d '\n'
)

echo "Pedaços em ordem: $pedacos"
echo "VAZANTE{$pedacos}"
