#!/usr/bin/env bash
# Confere a flag do Dia 11 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "8296b37e641268b46f9992ab697eeee1618df384b1b02a3ec720522b23b2fc71"
