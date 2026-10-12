#!/usr/bin/env bash
# =============================================================================
#  Dia 5 — Bater na porta: curl, downloads, cabeçalhos, redirecionamentos e APIs
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
#  Sem internet? Tudo tem cópia salva em desafio/salvos/ (ou: export L4O_OFFLINE=1)
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% curl: o navegador sem janela
# `curl URL` pede uma página e imprime a resposta no terminal. Sem imagens,
# sem JavaScript, sem cookies de rastreamento: só o que o servidor mandou.
#   -s   silencioso (sem barra de progresso)
#   -m 10  desiste depois de 10 segundos
titulo "Primeiro pedido: example.com"
precisa curl
if online; then
  curl -s -m 10 https://example.com | head -n 8
else
  alerta "offline: este bloco precisa de internet (example.com). Pulando."
fi

# %% Baixando para um arquivo: -o e -O
#   -o nome   salva com o nome que VOCÊ escolher
#   -O        salva com o nome que está no fim da URL
#   -L        segue redirecionamentos (muitos links de download redirecionam)
# Baixamos a RFC 2606, o documento que reservou o domínio .example.
titulo "Download com -o"
precisa curl
mkdir -p treino
if online; then
  curl -sL -m 20 https://www.rfc-editor.org/rfc/rfc2606.txt -o treino/rfc2606.txt
else
  alerta "offline: usando cópia salva"
  cp desafio/salvos/rfc2606-resumo.txt treino/rfc2606.txt
fi
ls -l treino
head -n 5 treino/rfc2606.txt
rm -r treino

# %% Download em lote: xargs + curl -O
# O original fazia:  xargs -n 1 curl -O < urls.txt
# xargs lê a lista de URLs e chama `curl -O` uma vez para cada (-n 1).
# Offline, subimos um servidor web local com `python3 -m http.server`
# servindo desafio/salvos/ — é o jeito mais simples de "ter um site" em casa.
titulo "Baixando uma lista de URLs"
precisa curl
mkdir -p treino
if online; then
  ( cd treino && xargs -n 1 curl -s -m 20 -O < ../desafio/urls.txt )
else
  alerta "offline: usando cópia salva (servidor local em 127.0.0.1:8086)"
  python3 -m http.server 8086 --bind 127.0.0.1 --directory desafio/salvos >/dev/null 2>&1 &
  servidor=$!
  for _ in $(seq 30); do curl -s --noproxy '*' -o /dev/null http://127.0.0.1:8086/ && break; sleep 0.1; done
  ( cd treino && xargs -n 1 curl -s --noproxy '*' -O < ../desafio/urls-locais.txt )
  kill "$servidor"
fi
ls -l treino
rm -r treino

# %% Só os cabeçalhos: -I
# Toda resposta HTTP tem duas partes: CABEÇALHOS (metadados) e CORPO (a página).
# `curl -I` pede só os cabeçalhos (método HEAD). Eles contam:
#   código de status (200 ok, 301/302 redirecionou, 404 não existe)
#   Server (software do servidor), Date, Last-Modified, Content-Type...
titulo "Cabeçalhos de example.com"
precisa curl
if online; then
  curl -sI -m 10 https://example.com
else
  alerta "offline: usando cópia salva"
  cat desafio/salvos/cabecalhos-example.com.txt
fi

# %% Redirecionamentos: -L e o cabeçalho Location
# Links encurtados respondem 301/302 com um cabeçalho `Location:` apontando o
# próximo endereço. `curl -sIL` segue TODOS os saltos mostrando os cabeçalhos
# de cada um. Filtrando só as linhas "location", você vê a cadeia inteira
# SEM abrir o site no navegador.
#     curl -sIL https://link-encurtado | grep -i ^location
titulo "Seguindo uma cadeia de redirecionamentos (exemplo real)"
precisa curl
if online; then
  # http://registro.br redireciona para https://registro.br/
  curl -sIL -m 10 http://registro.br | grep -iE '^(HTTP|location)'
else
  alerta "offline: este exemplo precisa de internet. Veja a cadeia do golpe no próximo bloco."
fi

# %% A cadeia do link do golpe (cópia salva)
# Alguém já rodou `curl -sIL` no link do SMS e salvou a saída.
# Cada bloco começa com "HTTP/1.1 <código>"; o Location diz para onde foi.
titulo "Cabeçalhos salvos do link do SMS"
cat desafio/sms-golpe.txt
echo "---"
grep -iE '^(HTTP|location)' desafio/cabecalhos-link-golpe.txt
echo "Saltos: $(grep -ci '^location' desafio/cabecalhos-link-golpe.txt)"

# %% Reproduzindo o golpe num servidor local
# desafio/encurtador.py é um servidor (só Python stdlib) que responde
# exatamente com a cadeia salva. Assim você treina curl de verdade, sem
# internet e SEM tocar no servidor dos golpistas.
#   --connect-to ::127.0.0.1:8085   manda todos os domínios para o seu PC
#   --noproxy '*'                   não passa por proxy (é local)
titulo "curl -sIL contra o encurtador falso"
precisa curl
python3 desafio/encurtador.py 8085 >/dev/null 2>&1 &
servidor=$!
for _ in $(seq 30); do curl -s --noproxy '*' -o /dev/null http://127.0.0.1:8085/ && break; sleep 0.1; done
curl -sIL --noproxy '*' --connect-to ::127.0.0.1:8085 http://encurta.example/x7Kp9 | grep -iE '^(HTTP|location)'
echo "--- e com -w, só o endereço final:"
curl -sL --noproxy '*' --connect-to ::127.0.0.1:8085 -o /dev/null -w '%{url_effective}\n' http://encurta.example/x7Kp9 | cut -c1-60
kill "$servidor"

# %% APIs: pedindo DADOS em vez de páginas
# Uma API responde em JSON, um formato de dados que programas leem fácil.
# A BrasilAPI é gratuita e sem cadastro. Consultamos o CEP do Palácio do
# Planalto. O `jq` (Dia 14) formata o JSON; `-H` manda um cabeçalho.
titulo "BrasilAPI: CEP"
precisa curl
precisa jq
if online; then
  curl -s -m 15 -H 'accept: application/json' https://brasilapi.com.br/api/cep/v1/70150900 | jq .
else
  alerta "offline: usando cópia salva"
  jq . desafio/salvos/cep-70150900.json
fi

# %% API com método explícito e resultado salvo em arquivo
# O original usava:  curl -X 'GET' 'URL' -H 'accept: application/json' > resultado.txt
#   -X GET   o método (GET = ler; POST = enviar). GET é o padrão.
#   >        redireciona a saída para um arquivo
# Consultamos o CNPJ do Banco do Brasil (empresa pública).
titulo "BrasilAPI: CNPJ de empresa pública"
precisa curl
precisa jq
mkdir -p treino
if online; then
  curl -s -m 15 -X 'GET' 'https://brasilapi.com.br/api/cnpj/v1/00000000000191' \
    -H 'accept: application/json' > treino/api_resultado.json
else
  alerta "offline: usando cópia salva"
  cp desafio/salvos/cnpj-00000000000191.json treino/api_resultado.json
fi
jq '{razao_social, uf, municipio, descricao_situacao_cadastral}' treino/api_resultado.json
rm -r treino

# %% Opções que você vai usar muito
#   -A "texto"     muda o User-Agent (como o site te identifica)
#   -w '%{http_code}'  imprime só o código de status
#   --retry 3      tenta de novo se falhar
#   -x URL         usa um proxy (ex.: Tor em socks5h://127.0.0.1:9050)
titulo "Só o código de status"
precisa curl
if online; then
  curl -s -m 10 -o /dev/null -w '%{http_code}\n' https://example.com
  curl -s -m 10 -o /dev/null -w '%{http_code}\n' https://example.com/nao-existe
else
  alerta "offline: este bloco precisa de internet. Mostrando os comandos:"
  mostrar "curl -s -o /dev/null -w '%{http_code}\n' https://example.com"
fi
