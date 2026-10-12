#!/usr/bin/env bash
# Confere a flag do Dia 12 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "8633958c013d1852b4e603c0c23b427cbd3e8b3a3dddb4f5d19b0d6fb2199baf"
