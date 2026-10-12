#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 20. Tente sozinho antes!
# Ideia: o shellcheck aponta 3 erros no script de maré_alta:
#   SC2283  espaços em volta do =          -> pasta="pedacos de selo"
#   SC2231  $pasta sem aspas no for        -> "$pasta"/*.txt
#   SC2086  $arquivo sem aspas no cat      -> cat "$arquivo"
# Corrigimos uma CÓPIA com sed (o original fica intacto) e rodamos a cópia.
cd "$(dirname "$0")/../dias/dia-20-ferramentas-uteis/desafio" || exit 1

shellcheck -f gcc script_quebrado.sh || true      # mostra os avisos (e não para)

corrigido=$(mktemp ./selo_corrigido.XXXX.sh)       # cópia na mesma pasta (o script usa caminhos relativos)
trap 'rm -f "$corrigido"' EXIT
# shellcheck disable=SC2016  # o $ dentro das aspas simples é texto para o sed, de propósito
sed -e 's/^pasta = /pasta=/' \
    -e 's|for arquivo in \$pasta/\*\.txt|for arquivo in "$pasta"/*.txt|' \
    -e 's|cat \$arquivo|cat "$arquivo"|' \
    script_quebrado.sh > "$corrigido"

shellcheck "$corrigido" && echo "shellcheck: nenhum aviso" >&2
bash "$corrigido"
