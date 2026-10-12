#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 7. Tente sozinho antes!
# Ideia: seguir o dinheiro.
#   1. awk soma a coluna "valor" por conta de destino, só nas linhas PIX
#      (estornos não contam; NR>1 pula o cabeçalho)
#   2. sort -rn | head -n 1 pega a conta que MAIS recebeu em reais
#      (atenção: a conta que aparece mais vezes não é a que recebeu mais)
#   3. sed limpa o apelido em contas.txt: tira "CONTA ;", espaços, "##fim"
#      e troca "~" por "_"
cd "$(dirname "$0")/../dias/dia-07-sed-e-awk/desafio" || exit 1

awk -F, 'NR > 1 && $5 == "PIX" { soma[$3] += $4 } END { for (c in soma) printf "%s %.2f\n", c, soma[c] }' extrato.csv \
  | sort -k2 -rn
conta=$(awk -F, 'NR > 1 && $5 == "PIX" { soma[$3] += $4 } END { for (c in soma) printf "%s %.2f\n", c, soma[c] }' extrato.csv \
  | sort -k2 -rn | head -n 1 | cut -d' ' -f1)
echo "Conta que mais recebeu: $conta"

apelido=$(grep "^$conta " contas.txt | sed -e 's/^[^;]*;[[:space:]]*//' -e 's/[[:space:]]*##fim$//' -e 's/~/_/g')
echo "Apelido limpo: $apelido"
echo "VAZANTE{$apelido}"
