#!/usr/bin/env bash
# =============================================================================
#  Dia 14 — O export do grupo: JSON com jq, XML com xmlstarlet, CSV com csvkit
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
#  Pacotes: jq, xmlstarlet (apt) e csvkit (pip)
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% Os três formatos de dados que você mais vai ver
# JSON: o formato das APIs e dos exports de apps (WhatsApp, Telegram, Discord).
# XML:  sitemaps, feeds RSS, arquivos de configuração, documentos Office.
# CSV:  planilhas, bases de dados abertos, vazamentos.
titulo "O que chegou da perícia"
ls -lh desafio/
head -c 400 desafio/export-grupo.json; echo
head -n 4 desafio/sitemap.xml
head -n 3 desafio/dominios.csv

# %% jq: o primeiro filtro
# `jq` lê JSON e aplica um FILTRO. O ponto (.) é "o documento inteiro".
#   jq '.'                  imprime bonito e colorido (pretty print)
#   jq '.grupo'             entra na chave "grupo"
#   jq '.grupo.nome'        chave dentro de chave
#   jq -r                   "raw": tira as aspas das strings
titulo "jq: navegando por chaves"
precisa jq
jq '.grupo' desafio/export-grupo.json
jq -r '.grupo.criado_por' desafio/export-grupo.json

# %% jq: listas (arrays)
#   .membros[0]             o primeiro item (começa do zero!)
#   .membros[0].handle      a chave "handle" do primeiro membro
#   .membros[].handle       a chave "handle" de TODOS os membros
#   .membros | length       quantos itens a lista tem
titulo "jq: índices e [ ]"
precisa jq
jq '.membros[0].handle' desafio/export-grupo.json
jq -r '.membros[].handle' desafio/export-grupo.json
jq '.mensagens | length' desafio/export-grupo.json

# %% jq: select (filtrar) e map (transformar)
# `select(condição)` deixa passar só os itens em que a condição é verdadeira.
# `map(f)` aplica f a cada item de uma lista e devolve outra lista.
# O cano `|` dentro do jq funciona como no Bash: passa o resultado adiante.
titulo "jq: select e map"
precisa jq
echo "--- membros que são admin:"
jq -r '.membros[] | select(.admin) | .handle' desafio/export-grupo.json
echo "--- as 3 primeiras mensagens do lucas_suporte:"
jq -r '.mensagens[] | select(.autor.handle == "lucas_suporte") | "\(.data)  \(.texto)"' desafio/export-grupo.json | head -n 3
echo "--- map: só os ids das 5 primeiras mensagens"
jq -c '.mensagens[:5] | map(.id)' desafio/export-grupo.json

# %% jq: contando e agrupando
# Quem mais fala no grupo? group_by agrupa, length conta, sort_by ordena.
titulo "Ranking de mensagens por autor"
precisa jq
jq -r '.mensagens | group_by(.autor.handle) | map({autor: .[0].autor.handle, total: length})
       | sort_by(-.total) | .[] | "\(.total)\t\(.autor)"' desafio/export-grupo.json
echo "--- mensagens apagadas no export:"
jq '[.mensagens[] | select(.apagada)] | length' desafio/export-grupo.json
dica "Mensagem apagada que ainda tem texto_original no export... interessante, não?"

# %% jq: transformando JSON em CSV
# @csv converte um array em linha CSV. Ótimo para levar para a planilha.
titulo "JSON -> CSV com jq"
precisa jq
jq -r '.membros[] | [.handle, .nome_exibido, .admin] | @csv' desafio/export-grupo.json

# %% xmlstarlet: consultando XML
# `xmlstarlet sel` (select) usa XPath para achar elementos:
#   -t                 começa um "template" de saída
#   -m "//TITLE"       para cada elemento TITLE em qualquer lugar (match)
#   -v .               imprime o valor do elemento atual
#   -n                 quebra de linha
# Sitemaps usam um "namespace" (xmlns=...). No xmlstarlet o atalho _: resolve.
titulo "xmlstarlet: as URLs do sitemap"
precisa xmlstarlet
xmlstarlet sel -t -m "//_:url" -v "_:loc" -o "  prioridade=" -v "_:priority" -n desafio/sitemap.xml
echo "--- só as páginas com prioridade baixa (< 0.5):"
xmlstarlet sel -t -m "//_:url[_:priority < 0.5]" -v "_:loc" -n desafio/sitemap.xml

# %% xmlstarlet sem namespace (como no curso original)
# Num XML sem xmlns, o XPath é direto: //TITLE.
titulo "XML simples"
precisa xmlstarlet
mkdir -p treino
printf '<CATALOG><CD><TITLE>Maré Alta</TITLE></CD><CD><TITLE>Vazante</TITLE></CD></CATALOG>\n' > treino/xml_sample.xml
xmlstarlet sel -t -m "//TITLE" -v . -n treino/xml_sample.xml
rm -r treino

# %% csvkit: CSV com ferramentas que entendem cabeçalho e aspas
# O `cut` (Dia 10) quebra quando um campo tem vírgula dentro de aspas.
# O csvkit entende CSV de verdade.
#   csvlook          mostra como tabela
#   csvcut -c a,b    escolhe colunas pelo NOME
#   csvgrep -c 2 -m texto    filtra linhas em que a coluna 2 contém "texto"
#   csvgrep -c porta -r '^80$'   com expressão regular
titulo "csvkit"
precisa_pip csvlook csvkit
csvlook desafio/dominios.csv
echo "--- só domínio e porta:"
csvcut -c dominio,porta desafio/dominios.csv
echo "--- títulos que mencionam PixVelox (coluna 2):"
csvgrep -d ',' -c 2 -m 'PixVelox' desafio/dominios.csv

# %% in2csv: JSON (e Excel) -> CSV
#   in2csv -k membros arq.json   converte a lista que está na chave "membros"
#   in2csv planilha.xlsx         também converte Excel!
#   csvstat                      estatísticas por coluna
titulo "in2csv e csvstat"
precisa_pip in2csv csvkit
mkdir -p treino
in2csv -k membros desafio/export-grupo.json > treino/membros.csv
cat treino/membros.csv
csvcut -c dominio,porta desafio/dominios.csv > treino/cut_csv.csv
csvstat -c porta treino/cut_csv.csv | head -n 12
rm -r treino

# %% Dados reais de uma API (online)
# APIs públicas devolvem JSON — e o jq é o par perfeito do curl (Dia 5).
# Exemplo: dados públicos de um CEP pela BrasilAPI (01001000 = Praça da Sé, SP).
titulo "curl + jq numa API pública"
precisa jq
if online; then
  curl -s -m 10 https://brasilapi.com.br/api/cep/v1/01001000 | jq '{cep, city, neighborhood, street}'
else
  alerta "offline: usando cópia salva"
  jq '{cep, city, neighborhood, street}' desafio/cep-01001000.json
fi
