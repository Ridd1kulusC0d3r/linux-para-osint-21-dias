#!/usr/bin/env bash
# Confere a flag do Dia 16 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "a5c42595b534a774007e9013c5d3f581d7e1a594d6f1ed7a8447e5fe9e57457d"
