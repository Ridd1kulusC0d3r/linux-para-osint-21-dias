#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 10. Tente sozinho antes!
# Ideia:
#   1. Extrair só a coluna de telefone de cada grupo (cut), sem cabeçalho (tail -n +2).
#   2. Ordenar sem repetição (sort -u) — o comm exige listas ordenadas.
#   3. comm -12 mostra só o que está nos DOIS grupos.
#   4. Achar o apelido desse número em cada grupo, padronizar (tr) e juntar com _.
cd "$(dirname "$0")/../dias/dia-10-utilitarios-de-texto/desafio" || exit 1

comum="$(comm -12 \
  <(tail -n +2 grupo-a-cashback-vip.csv | cut -d, -f1 | sort -u) \
  <(tail -n +2 grupo-b-suporte-pix.txt | cut -d';' -f2 | sort -u))"
echo "número nos dois grupos: $comum"

apelido_a="$(grep -F "$comum" grupo-a-cashback-vip.csv | head -n 1 | cut -d, -f2)"
apelido_b="$(grep -F "$comum" grupo-b-suporte-pix.txt | cut -d';' -f1 | tr '[:upper:]' '[:lower:]')"
echo "grupo A: $apelido_a · grupo B: $apelido_b"
echo "VAZANTE{${apelido_a}_${apelido_b}}"
