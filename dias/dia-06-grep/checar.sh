#!/usr/bin/env bash
# Confere a flag do Dia 6 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "b19ed7eb61ba8c248f6ce5c5df305edf4e23e5a70e9d91768af37408a527d07b"
