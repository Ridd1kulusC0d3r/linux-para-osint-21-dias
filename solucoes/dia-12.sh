#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 12. Tente sozinho antes!
# Ideia:
#   1. O texto (pdftotext) diz: o código é a "palavra-chave interna do documento"
#      escrita entre VAZANTE{ e }.
#   2. "Palavra-chave" de um PDF é o metadado Keywords (pdfinfo / exiftool).
#   3. De quebra, Author e Producer entregam o maré_alta.
cd "$(dirname "$0")/../dias/dia-12-pdf/desafio" || exit 1

pdftotext contrato-pixvelox.pdf - | grep -A1 'código de verificação'
exiftool contrato-pixvelox.pdf | grep -E '^(Author|Producer|Keywords)'

chave="$(pdfinfo contrato-pixvelox.pdf | grep '^Keywords:' | awk '{ print $2 }')"
echo "VAZANTE{$chave}"
