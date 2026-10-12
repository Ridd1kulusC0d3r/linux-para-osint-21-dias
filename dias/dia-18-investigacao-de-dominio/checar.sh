#!/usr/bin/env bash
# Confere a flag do Dia 18 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "5c289c5837c515dde484d8cedc860cfc81fdcba2e5a71978c19a4c27441c208a"
