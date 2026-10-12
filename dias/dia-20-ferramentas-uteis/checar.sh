#!/usr/bin/env bash
# Confere a flag do Dia 20 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "f6e8d15a113af8cd7890ea8430dca4dd425bb8aaf3191d90436dbb521eacb960"
