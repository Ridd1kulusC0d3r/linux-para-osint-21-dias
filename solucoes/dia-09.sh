#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 9. Tente sozinho antes!
# Ideia:
#   1. Pelo extrato, os saques são sempre às 03:17.
#   2. `date -d` mostra que todas as datas caem num domingo.
#   3. Domingo no cron = 0, 7 ou "sun". Hora 03:17 = minuto 17, hora 3.
#   4. Procuramos o job com minuto=17, hora=3, dia=*, mês=* e dia da semana = domingo.
cd "$(dirname "$0")/../dias/dia-09-screen-e-cron/desafio" || exit 1

# passo 2: dia da semana de cada data do extrato (DD/MM/AAAA -> AAAA-MM-DD)
awk 'NR > 2 { split($1, d, "/"); print d[3] "-" d[2] "-" d[1] }' extrato-saques.txt \
  | while read -r data; do echo "$data $(LC_ALL=C date -d "$data" +%A)"; done

# passo 4: o job certo
lote="$(grep -Ev '^(#|$|[A-Z]+=|@)' crontab-robo.txt \
  | awk '$1 == "17" && $2 == "3" && $3 == "*" && $4 == "*" && ($5 == "0" || $5 == "7" || $5 == "sun") { print $NF }')"
echo "VAZANTE{$lote}"
