#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 15. Tente sozinho antes!
# Ideia: o robots.txt aponta /painel-interno/. Lá dentro, seguindo os links,
# chega-se ao rascunho da campanha. O código está escrito em entidades HTML
# (&#86;&#65;...), por isso um grep no HTML cru não acha "VAZANTE" — mas o
# html2text converte as entidades em texto normal.
cd "$(dirname "$0")/../dias/dia-15-scraping" || exit 1

PORTA=8015
python3 -m http.server "$PORTA" --bind 127.0.0.1 --directory desafio/site >/dev/null 2>&1 &
SERVIDOR=$!
trap 'kill "$SERVIDOR" 2>/dev/null' EXIT          # desliga o servidor aconteça o que acontecer
for _ in $(seq 20); do curl -s -o /dev/null "http://127.0.0.1:$PORTA/" && break; sleep 0.2; done
BASE="http://127.0.0.1:$PORTA"

# 1. O que o robots.txt esconde?
curl -s "$BASE/robots.txt" | grep '^Disallow'

# 2. Links do painel interno
curl -s "$BASE/painel-interno/" | grep -o 'href="[^"]*"' | sed 's/^href="//; s/"$//'

# 3. Para cada página do painel, html2text + grep da flag
for p in metas-semana.html rascunho-campanha-v2.html; do
  curl -s "$BASE/painel-interno/$p" -o pagina.html
  html2text -utf8 -nobs pagina.html | grep -o 'VAZANTE{[^}]*}'
done | tail -n 1
rm -f pagina.html
