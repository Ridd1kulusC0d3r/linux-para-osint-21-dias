#!/usr/bin/env bash
# Confere a flag final (Dia 21) sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "3faa7e631c3b879476ffda443a0243e001ef67dd6ba12203dbdf38191ec18e4b"
