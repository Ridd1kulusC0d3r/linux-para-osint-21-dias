#!/usr/bin/env bash
# Confere a flag do Dia 2 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "15a9dd698149a645e7d0089f285e99a089f1534052466506b9504462e8e43bb5"
