#!/usr/bin/env bash
# Confere a flag do Dia 19 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "aa67169c5b3e7f83d8771f0ec9429721f36be3799d90690be5fbf2947e9613e1"
