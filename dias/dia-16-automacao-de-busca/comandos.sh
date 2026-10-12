#!/usr/bin/env bash
# =============================================================================
#  Dia 16 — Perguntando ao mundo: automação de buscas
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
#
#  Buscas de verdade precisam de internet (e às vezes de chave de API). Para
#  o curso funcionar offline, cada busca tem uma cópia salva em desafio/.
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% ddgr: DuckDuckGo no terminal
# ddgr faz buscas no DuckDuckGo e mostra o resultado em texto.
#   -n 10        quantos resultados
#   --np         "no prompt": busca e sai (sem o menu interativo)
#   -C           sem cores (bom para salvar em arquivo)
#   -x           mostra a URL completa de cada resultado
# Redirecionar com > salva o resultado para trabalhar depois.
titulo "Buscando com ddgr"
precisa ddgr
if online && ddgr -n 10 --np -C osint > busca_osint.txt 2>/dev/null && [ -s busca_osint.txt ]; then
  head -n 12 busca_osint.txt
  rm busca_osint.txt
else
  alerta "offline (ou DuckDuckGo bloqueou): usando cópia salva"
  head -n 12 desafio/busca_pixvelox.txt
fi

# %% Extraindo só os sites com grep -o
# Na saída de texto, o ddgr mostra o site de cada resultado entre colchetes.
# grep -o '\[.*]' pega só esse pedaço ([ precisa de \ porque é especial).
titulo "Quais sites apareceram?"
grep -o '\[.*]' desafio/busca_pixvelox.txt
echo "--- sem colchetes, contando ---"
grep -o '\[.*]' desafio/busca_pixvelox.txt | tr -d '[]' | sort | uniq -c | sort -rn

# %% ddgr --json + jq: resultados estruturados
# Com --json o ddgr devolve uma LISTA de objetos {title, url, abstract}.
# jq (Dia 14) tira o que você quiser: .[] percorre a lista; -r tira as aspas.
titulo "Resultados em JSON"
precisa jq
if online && ddgr -n 5 --json pixvelox > resultados.json 2>/dev/null && [ -s resultados.json ]; then
  jq -r '.[] | .url' resultados.json
  rm resultados.json
else
  alerta "offline: usando cópia salva"
  jq -r '.[] | .url' desafio/busca_pixvelox.json
fi
echo "--- resultados cujo resumo fala em 'código' ---"
jq -r '.[] | select(.abstract | test("código")) | .title' desafio/busca_pixvelox.json

# %% Operadores de busca (dorks)
# Buscadores entendem operadores que refinam a pergunta:
#   site:dominio      só resultados daquele site
#   filetype:pdf      só arquivos daquele tipo (xlsx, docx, csv...)
#   intitle:palavra   a palavra no TÍTULO da página
#   inurl:palavra     a palavra no ENDEREÇO
#   "frase exata"     entre aspas, exatamente assim
#   -palavra          exclui resultados com a palavra
# Uma lista de dorks prontas está em desafio/dorks.txt.
titulo "Dorks do caso"
cat desafio/dorks.txt
dica "No ddgr: ddgr --np -w social.example pixvelox   (-w = site:)"

# %% Montando URLs de busca (urlencode)
# Toda busca vira uma URL. Espaços, aspas e dois-pontos precisam ser
# "codificados" (urlencode): espaço vira %20, aspas viram %22, : vira %3A...
# O jq faz isso com o filtro @uri. Com a URL pronta, o curl (ou você no
# navegador) abre a busca — e um laço gera dezenas de buscas de uma vez.
titulo "Gerando URLs de busca para cada dork"
precisa jq
while IFS= read -r dork; do
  q=$(jq -rn --arg q "$dork" '$q | @uri')          # urlencode do texto
  echo "https://duckduckgo.com/html/?q=$q"
done < desafio/dorks.txt
dica "Abra no navegador ou use: curl -s -A 'Mozilla/5.0' 'URL' — com moderação."

# %% Automatizando várias buscas (com pausa!)
# Para muitas buscas: laço + sleep entre elas, para não ser bloqueado.
# O ddgr aceita --proxy se você precisar trocar de saída de rede.
titulo "Laço de buscas (simulado offline)"
precisa ddgr
while IFS= read -r dork; do
  arquivo="busca_$(echo "$dork" | tr -c '[:alnum:]' '_' | cut -c1-30).txt"
  if online; then
    mostrar "ddgr -n 10 --np -C '$dork' > $arquivo ; sleep 3"
  else
    mostrar "(offline) ddgr -n 10 --np -C '$dork' > $arquivo"
  fi
done < desafio/dorks.txt

# %% Netlas: o buscador de servidores (opcional, precisa de API key)
# Buscadores "de IP" (Netlas, Shodan, Censys) não indexam páginas, e sim
# SERVIDORES: cada IP, porta, título da página, certificado...
# Plano gratuito do Netlas: crie conta em app.netlas.io e copie sua API key.
#   pip install netlas
#   netlas savekey SUA_CHAVE
#   netlas download -c 20 "http.body:*pixvelox*" > netlas_resultados.json
# Outros filtros: http.title:  domain:  port:  geo.city:  geo.country:  ip:
titulo "Netlas"
precisa_pip netlas netlas || true
mostrar "netlas savekey SUA_CHAVE"
mostrar 'netlas download -c 20 "http.body:*pixvelox*" > netlas_resultados.json'
if online && [ -n "${NETLAS_API_KEY:-}" ] && command -v netlas >/dev/null 2>&1; then
  netlas download -a "$NETLAS_API_KEY" -c 5 'http.title:"Example Domain"' > netlas_teste.json \
    && jq -r '.data.host' netlas_teste.json
  rm -f netlas_teste.json
else
  dica "Sem NETLAS_API_KEY (ou offline): vamos usar a cópia salva em desafio/netlas_resultados.json"
fi

# %% jq nos resultados do Netlas
# O netlas download grava UM objeto JSON por linha (formato "JSON Lines").
# O jq processa linha por linha naturalmente.
titulo "Títulos das páginas encontradas pelo Netlas"
precisa jq
jq .data.http.title desafio/netlas_resultados.json
echo "--- IP, porta e host, em colunas ---"
jq -r '[.data.ip, .data.port, .data.host] | @tsv' desafio/netlas_resultados.json
echo "--- quantos servidores por IP ---"
jq -r '.data.ip' desafio/netlas_resultados.json | sort | uniq -c | sort -rn

# %% Cruzando as duas buscas
# Um site apareceu no DuckDuckGo. Será que ele aparece também no Netlas?
# comm (Dia 10) mostra o que é comum a duas listas ORDENADAS.
titulo "Sites que estão nas duas buscas"
precisa jq
grep -o '\[.*]' desafio/busca_pixvelox.txt | tr -d '[]' | sort -u > ddg.txt
jq -r '.data.host' desafio/netlas_resultados.json | sort -u > netlas.txt
comm -12 ddg.txt netlas.txt
rm ddg.txt netlas.txt
dica "Algum desses não é um site 'de vitrine'... olhe as portas dele."

# %% Versão brazuca: buscando em diários oficiais (Querido Diário)
# O Querido Diário (Open Knowledge Brasil) indexa diários oficiais de
# municípios e tem API pública, sem chave. Montamos a URL com urlencode.
titulo "Querido Diário"
precisa jq
termo="licitação pix"
q=$(jq -rn --arg q "$termo" '$q | @uri')
URL="https://api.queridodiario.ok.org.br/gazettes?querystring=$q&size=3&excerpt_size=200&number_of_excerpts=1"
echo "$URL"
if online && curl -s -m 20 "$URL" -o qd.json && jq -e '.gazettes' qd.json >/dev/null 2>&1; then
  jq -r '.total_gazettes as $t | "total de diários: \($t)"' qd.json
  jq -r '.gazettes[] | "\(.date)  \(.territory_name) (\(.state_code))  \(.url)"' qd.json
else
  alerta "offline (ou API indisponível): veja a URL acima e abra quando tiver internet"
fi
rm -f qd.json
