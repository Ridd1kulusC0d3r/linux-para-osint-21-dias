#!/usr/bin/env bash
# selo.sh — monta o "selo" de acesso do painel a partir dos pedaços.
# Escrito às pressas por mare_alta. "Funcionava na minha máquina."
cd "$(dirname "$0")" || exit 1

pasta = "pedacos de selo"

selo=""
for arquivo in $pasta/*.txt; do
  pedaco=$(cat $arquivo 2>/dev/null)
  selo="$selo$pedaco"
done

if [ -z "$selo" ]; then
  echo "Selo vazio. Alguma coisa deu errado..." >&2
  exit 1
fi

# os pedaços estão em ROT13; tr desfaz
echo "$selo" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
