#!/usr/bin/env bash
# Confere a flag do Dia 17 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "96b8a428719bd16ef9dd4ad832dac73e8c494becc98da331efb5dcdcbdc39d8b"
