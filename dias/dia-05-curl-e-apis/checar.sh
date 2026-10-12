#!/usr/bin/env bash
# Confere a flag do Dia 5 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "ceea7aadd87686be34311ef97b6a97e335ced6658dc4b98d35bb8250dc7da66e"
