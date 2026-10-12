#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 16. Tente sozinho antes!
# Ideia: na busca do DuckDuckGo (busca_pixvelox.txt), um dos sites entre
# colchetes não é vitrine: é o painel da quadrilha. No Netlas, esse host tem
# vários servidores (portas). Ordenando por porta, os pedaços entre colchetes
# dos títulos formam a flag.
cd "$(dirname "$0")/../dias/dia-16-automacao-de-busca/desafio" || exit 1

# 1. Sites do resultado de busca; o suspeito tem "painel" no nome
host=$(grep -o '\[.*]' busca_pixvelox.txt | tr -d '[]' | grep painel)
echo "host suspeito: $host"

# 2. Servidores desse host no Netlas: porta + título, ordenados pela porta
jq -r --arg h "$host" 'select(.data.host == $h and .data.http.title != "")
                        | "\(.data.port) \(.data.http.title)"' netlas_resultados.json | sort -n

# 3. Pedaços entre colchetes, na ordem das portas, unidos com _
miolo=$(jq -r --arg h "$host" 'select(.data.host == $h) | "\(.data.port) \(.data.http.title)"' \
          netlas_resultados.json | sort -n | grep -o '\[[^]]*\]' | tr -d '[]' | paste -sd_)
echo "VAZANTE{$miolo}"
