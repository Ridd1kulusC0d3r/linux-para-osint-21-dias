#!/usr/bin/env bash
# Confere a flag do Dia 3 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "e18947613b3fed5d959f7843b34ed0f22f84808abccf13e5baa9319814a6db0a"
