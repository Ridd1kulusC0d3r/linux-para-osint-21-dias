#!/usr/bin/env bash
# Confere a flag do Dia 8 sem revelar a resposta (comparamos só o SHA-256).
# Uso:  bash checar.sh 'VAZANTE{...}'
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh
checar_flag "${1:-}" "92d19bd6dc09563e4527fa4a9f3203f35b841e348ee71a01404f25c3deb90b74"
