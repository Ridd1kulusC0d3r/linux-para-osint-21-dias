#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 1. Tente sozinho antes!
# Ideia: listar arquivos ocultos e procurar a palavra VAZANTE dentro deles.
cd "$(dirname "$0")/../dias/dia-01-arquivos-e-pastas/desafio/caso" || exit 1
find . -type f -name '.*' -exec grep -ho 'VAZANTE{[^}]*}' {} + | head -n 1
