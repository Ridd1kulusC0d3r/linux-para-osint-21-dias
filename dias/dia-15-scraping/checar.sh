#!/usr/bin/env bash
# Confere a flag do Dia 15 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "fa35e744b034bcc504be5bf1dbf4ef507c5c5b0137c9acf93f367a459384308f"
