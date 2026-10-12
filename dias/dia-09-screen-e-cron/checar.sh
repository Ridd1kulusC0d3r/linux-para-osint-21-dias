#!/usr/bin/env bash
# Confere a flag do Dia 9 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "e1c19de2bd7d90b6c5c91bf7964e5b205a403606eab791029874a547242e3125"
