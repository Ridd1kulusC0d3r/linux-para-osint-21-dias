#!/usr/bin/env bash
# Confere a flag do Dia 7 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "200016680ba56140146771375edab7221d8c1337e16de6d6e0e836d8a8a1c621"
