#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 4. Tente sozinho antes!
# Ideia: das 200 conversas, só 5 têm uma fala do operador "mare_alta".
#   1. find lista todos os .txt; xargs grep -l filtra os que citam mare_alta
#   2. sort ordena pelo caminho (data/número da conversa = ordem cronológica)
#   3. para cada arquivo, grep pega a fala "guarda isso: ..." e sed tira o pedaço
#   4. tr -d '\n' cola os pedaços
# Cuidado com a pista falsa: "a maré tá alta" (com acento e espaço) não é o operador.
cd "$(dirname "$0")/../dias/dia-04-processamento-em-lote/desafio" || exit 1

arquivos=$(find conversas -name '*.txt' -type f -print0 | xargs -0 grep -l 'mare_alta' | sort)
echo "Conversas com o operador:"
echo "$arquivos"

pedacos=$(echo "$arquivos" | xargs grep -h '| mare_alta |' | sed 's/.*guarda isso: //' | tr -d '\n')
echo "VAZANTE{$pedacos}"
