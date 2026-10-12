#!/usr/bin/env bash
# Confere a flag do Dia 14 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "be29405fcaeedbd5bb70a41b89622b6e154a2977080c8d5fb90262a8164c0e1e"
