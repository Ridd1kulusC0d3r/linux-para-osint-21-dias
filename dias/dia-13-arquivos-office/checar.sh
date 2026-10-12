#!/usr/bin/env bash
# Confere a flag do Dia 13 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "9237a86fba0e21d1e039cf806d8ebfda71411baf3ec52a9c664743f3310adc41"
