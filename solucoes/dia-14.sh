#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 14. Tente sozinho antes!
# Ideia:
#   1. No export, mensagens apagadas têm "apagada": true e, por descuido do app,
#      ainda guardam "texto_original".
#   2. Filtrar com select: apagadas E escritas pelo mare_alta.
#   3. As mensagens já estão em ordem cronológica: juntar os pedaços.
cd "$(dirname "$0")/../dias/dia-14-json-xml-csv/desafio" || exit 1

jq -c '.mensagens[] | select(.apagada) | {autor: .autor.handle, texto_original}' export-grupo.json

jq -r '.mensagens[]
       | select(.apagada and .autor.handle == "mare_alta")
       | .texto_original' export-grupo.json | tr -d '\n'
echo
