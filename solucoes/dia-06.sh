#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 6. Tente sozinho antes!
# 1. Extrair todos os e-mails do log com regex (-E -o).
# 2. Ficar só com os do subdomínio "cofre." exato (-F, texto fixo).
#    Repare: "cofre@pixvelox" e "cofre-pixvelox" são iscas.
# 3. A parte antes do @ é a flag.
cd "$(dirname "$0")/../dias/dia-06-grep/desafio" || exit 1
usuario="$(grep -Eo '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' log-suporte.txt \
  | grep -F '@cofre.pixvelox.example' | sort -u | cut -d@ -f1)"
echo "VAZANTE{$usuario}"
