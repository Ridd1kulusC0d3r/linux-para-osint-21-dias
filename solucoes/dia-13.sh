#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 13. Tente sozinho antes!
# Ideia:
#   1. O comentário de revisão do roteiro (word/comments.xml) manda olhar
#      "a aba que ninguém vê" da planilha.
#   2. xl/workbook.xml mostra que a aba "controle" tem state="hidden".
#   3. As abas são listadas em ordem: "controle" é a 2ª -> xl/worksheets/sheet2.xml.
#   4. A coluna B ("parte") tem a flag em pedaços, na ordem da coluna A.
#      Basta juntar.
cd "$(dirname "$0")/../dias/dia-13-arquivos-office/desafio" || exit 1

unzip -p roteiro-atendimento.docx word/comments.xml | sed 's/<[^>]*>//g'; echo
unzip -p planilha-contas.xlsx xl/workbook.xml | grep -o '<sheet [^>]*hidden[^>]*>'

# Cada célula de texto da coluna B vem como <c r="B2" t="inlineStr"><is><t>...</t>
unzip -p planilha-contas.xlsx xl/worksheets/sheet2.xml \
  | grep -o '<c r="B[0-9]*"[^>]*><is><t>[^<]*' \
  | sed 's/.*<t>//' \
  | tail -n +2 \
  | tr -d '\n'
echo
