#!/usr/bin/env bash
# Confere a flag do Dia 4 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "a600b9f98216d949ec105f714a48e03a8bbd8c1899e2004fe8d98bb01a9c0e7f"
