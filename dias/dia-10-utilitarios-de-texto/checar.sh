#!/usr/bin/env bash
# Confere a flag do Dia 10 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "a53ec42b3328fcd7b5872ee8c138157c788762efde4bbb47d46c229537297cf1"
