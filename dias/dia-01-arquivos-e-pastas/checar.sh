#!/usr/bin/env bash
# Confere a flag do Dia 1 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "577deb184ed1429354054ce0c88a6754f65cba61630b6c4f6b04e6cc2fb61111"
