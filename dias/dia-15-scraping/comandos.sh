#!/usr/bin/env bash
# =============================================================================
#  Dia 15 — O site clone: raspagem (scraping) de páginas web
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
#
#  O "site clone" da PixVelox está em desafio/site/. Para treinar sem internet
#  (e sem tocar em site de ninguém), nós mesmos o servimos com
#  `python3 -m http.server` numa porta local (127.0.0.1:8015). Cada seção que
#  precisa do site liga o servidor no começo e DESLIGA no fim.
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% Ligando o site clone num servidor local
# `python3 -m http.server PORTA` transforma uma pasta num site.
#   --bind 127.0.0.1   só aceita conexões do próprio computador (seguro)
#   --directory PASTA  qual pasta servir
#   &                  roda em SEGUNDO PLANO (background) e devolve o terminal
#   $!                 guarda o número (PID) do último processo em background
# Depois de usar, `kill PID` desliga o servidor. Sempre desligue!
titulo "Servindo desafio/site em http://127.0.0.1:8015"
PORTA=8015
python3 -m http.server "$PORTA" --bind 127.0.0.1 --directory desafio/site >/dev/null 2>&1 &
SERVIDOR=$!
# Espera o servidor responder (tenta até 20 vezes, 0,2 s cada)
for _ in $(seq 20); do curl -s -o /dev/null "http://127.0.0.1:$PORTA/" && break; sleep 0.2; done
ok "Servidor no ar (PID $SERVIDOR)"
# -I pede só os cabeçalhos: repare no "Server: SimpleHTTP/... Python/..."
curl -sI "http://127.0.0.1:$PORTA/index.html"
kill "$SERVIDOR"; wait "$SERVIDOR" 2>/dev/null
ok "Servidor desligado"

# %% Baixando uma página e lendo o HTML cru
# Raspar = baixar a página (curl) e extrair dela o que interessa (grep/sed).
# Primeiro, olhe o HTML cru com os próprios olhos: `head` mostra o começo.
titulo "HTML cru da página inicial"
PORTA=8015
python3 -m http.server "$PORTA" --bind 127.0.0.1 --directory desafio/site >/dev/null 2>&1 &
SERVIDOR=$!
for _ in $(seq 20); do curl -s -o /dev/null "http://127.0.0.1:$PORTA/" && break; sleep 0.2; done
mkdir -p raspagem
curl -s "http://127.0.0.1:$PORTA/index.html" -o raspagem/index.html   # -o salva em arquivo
head -n 20 raspagem/index.html
kill "$SERVIDOR"; wait "$SERVIDOR" 2>/dev/null
rm -r raspagem

# %% Extraindo links, e-mails e comentários com grep -o e sed
# grep -o imprime SÓ o pedaço que casou (um por linha). Com sed limpamos o resto.
#   links:       href="..."          -> sed tira o href=" e a aspa final
#   e-mails:     algo@algo.example
#   comentários: <!-- ... -->        -> onde o programador "conversa sozinho"
# Comentários HTML não aparecem no navegador, mas estão no código. Ouro em OSINT.
titulo "Links, e-mails e comentários de todas as páginas públicas"
PORTA=8015
python3 -m http.server "$PORTA" --bind 127.0.0.1 --directory desafio/site >/dev/null 2>&1 &
SERVIDOR=$!
for _ in $(seq 20); do curl -s -o /dev/null "http://127.0.0.1:$PORTA/" && break; sleep 0.2; done
BASE="http://127.0.0.1:$PORTA"
for pagina in index.html cashback.html sobre.html contato.html; do
  curl -s "$BASE/$pagina"
done > tudo.html                                  # junta as 4 páginas num arquivo só
echo "--- links ---"
grep -o 'href="[^"]*"' tudo.html | sed 's/^href="//; s/"$//' | sort -u
echo "--- e-mails ---"
grep -oE '[[:alnum:]._-]+@[[:alnum:].-]+\.example' tudo.html | sort -u
echo "--- comentários HTML ---"
grep -o '<!--.*-->' tudo.html | sort -u
echo "--- formulários (para onde vão os dados das vítimas?) ---"
grep -o 'action="[^"]*"' tudo.html | sort -u
rm tudo.html
kill "$SERVIDOR"; wait "$SERVIDOR" 2>/dev/null

# %% robots.txt: o mapa do que o dono NÃO quer que vejam
# robots.txt é um pedido educado para robôs de busca não visitarem certas
# pastas. Não é tranca nenhuma — e ainda entrega onde está o que é "secreto".
titulo "Lendo o robots.txt"
PORTA=8015
python3 -m http.server "$PORTA" --bind 127.0.0.1 --directory desafio/site >/dev/null 2>&1 &
SERVIDOR=$!
for _ in $(seq 20); do curl -s -o /dev/null "http://127.0.0.1:$PORTA/" && break; sleep 0.2; done
curl -s "http://127.0.0.1:$PORTA/robots.txt"
echo "--- só os caminhos proibidos ---"
curl -s "http://127.0.0.1:$PORTA/robots.txt" | grep '^Disallow' | awk '{print $2}'
echo "--- quais deles existem? (código HTTP de cada um) ---"
for caminho in $(curl -s "http://127.0.0.1:$PORTA/robots.txt" | grep '^Disallow' | awk '{print $2}'); do
  codigo=$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORTA$caminho")
  echo "$codigo  $caminho"        # 200 = existe; 404 = não existe
done
kill "$SERVIDOR"; wait "$SERVIDOR" 2>/dev/null

# %% Um mini-crawler em Bash (o que o katana faz, em versão de bolso)
# Crawler = robô que abre uma página, pega os links, abre esses links, e assim
# por diante. Aqui: uma FILA de páginas a visitar e uma lista das já visitadas.
# Só seguimos links internos (que não começam com http, mailto etc.).
titulo "Mini-crawler a partir do painel interno"
PORTA=8015
python3 -m http.server "$PORTA" --bind 127.0.0.1 --directory desafio/site >/dev/null 2>&1 &
SERVIDOR=$!
for _ in $(seq 20); do curl -s -o /dev/null "http://127.0.0.1:$PORTA/" && break; sleep 0.2; done
BASE="http://127.0.0.1:$PORTA"
fila=("/painel-interno/index.html")    # começamos pelo que o robots.txt entregou
visitadas=()
while [ "${#fila[@]}" -gt 0 ]; do
  atual="${fila[0]}"; fila=("${fila[@]:1}")              # tira o primeiro da fila
  [[ " ${visitadas[*]} " == *" $atual "* ]] && continue    # já visitei? pula
  visitadas+=("$atual")
  codigo=$(curl -s -o pagina.tmp -w '%{http_code}' "$BASE$atual")   # baixa e guarda o código HTTP
  echo "$codigo  $atual"
  [ "$codigo" = "200" ] || continue                       # página não existe: não segue links
  pasta="${atual%/*}"                                    # pasta da página atual
  # lê os links um por linha; "< <(comando)" alimenta o while com a saída do comando
  while read -r link; do
    case "$link" in
      http*|mailto:*|/*) continue ;;                     # externo ou absoluto: ignora
      *) fila+=("$pasta/$link") ;;                       # interno: entra na fila
    esac
  done < <(grep -o 'href="[^"]*"' pagina.tmp | sed 's/^href="//; s/"$//')
done
rm -f pagina.tmp
echo "Endereços testados: ${#visitadas[@]} (os 200 existem; os 404 eram links quebrados do clone)"
kill "$SERVIDOR"; wait "$SERVIDOR" 2>/dev/null

# %% html2text: do HTML para texto legível
# html2text tira as tags e mostra só o texto, como o navegador mostraria.
# Ele também traduz ENTIDADES HTML (&#86; vira V, &amp; vira &...). Um grep no
# HTML cru não enxerga texto escrito em entidades — o html2text enxerga.
#   -utf8   lê e escreve em UTF-8 (acentos certinhos)
#   -nobs   sem "backspaces" de negrito (saída limpa para grep)
titulo "html2text no site clone"
precisa html2text
html2text -utf8 -nobs desafio/site/sobre.html
echo "--- a mesma página, só as linhas com @ ---"
html2text -utf8 -nobs desafio/site/sobre.html | grep '@' || true
dica "Agora rode html2text nas páginas do painel interno. 😉"

# %% Raspando várias páginas de uma vez com wget
# `wget -r` (recursivo) segue os links sozinho e baixa o site inteiro.
#   -l 2         até 2 níveis de profundidade
#   -nH          não cria pasta com o nome do servidor
#   -P pasta     onde salvar
# Por padrão o wget RESPEITA o robots.txt — por isso não baixa o painel.
titulo "wget recursivo (espelho do site)"
precisa wget
PORTA=8015
python3 -m http.server "$PORTA" --bind 127.0.0.1 --directory desafio/site >/dev/null 2>&1 &
SERVIDOR=$!
for _ in $(seq 20); do curl -s -o /dev/null "http://127.0.0.1:$PORTA/" && break; sleep 0.2; done
wget -q -r -l 2 -nH -P espelho "http://127.0.0.1:$PORTA/index.html" || true
find espelho -type f | sort
rm -r espelho
kill "$SERVIDOR"; wait "$SERVIDOR" 2>/dev/null
dica "Com '-e robots=off' o wget ignora o robots.txt. Use só onde você tem autorização."

# %% katana (ProjectDiscovery) — crawler profissional (opcional)
# katana é escrito em Go e instalado com `go install`. Ele acha links, arquivos
# JavaScript, formulários... muito mais rápido que o nosso mini-crawler.
# Instalar precisa de internet e de Go (no Colab: apt install golang-go).
titulo "katana (opcional)"
mostrar "go install github.com/projectdiscovery/katana/cmd/katana@latest"
mostrar "export PATH=\"\$PATH:\$(go env GOPATH)/bin\""
mostrar "katana -u https://example.com -d 2 -silent"
mostrar "katana -list dominios.txt -o resultados.txt"
if command -v katana >/dev/null 2>&1; then
  PORTA=8015
  python3 -m http.server "$PORTA" --bind 127.0.0.1 --directory desafio/site >/dev/null 2>&1 &
  SERVIDOR=$!
  for _ in $(seq 20); do curl -s -o /dev/null "http://127.0.0.1:$PORTA/" && break; sleep 0.2; done
  katana -u "http://127.0.0.1:$PORTA/" -d 3 -silent || alerta "katana falhou"
  kill "$SERVIDOR"; wait "$SERVIDOR" 2>/dev/null
else
  dica "katana não instalado — tudo bem, o mini-crawler acima faz o mesmo em pequena escala."
fi

# %% nuclei com template de extração (opcional)
# nuclei roda "templates" YAML contra uma lista de URLs. Além de achar falhas,
# serve para EXTRAIR dados (e-mails, links de redes sociais, títulos...).
# O cipher387 mantém templates prontos: github.com/cipher387/juicyinfo-nuclei-templates
# Deixamos um template próprio em desafio/extrair-emails.yaml.
titulo "nuclei (opcional)"
cat desafio/extrair-emails.yaml
mostrar "go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
mostrar "git clone https://github.com/cipher387/juicyinfo-nuclei-templates"
mostrar "nuclei -t juicyinfo-nuclei-templates/juicy_info/title.yaml -l resultados.txt"
if command -v nuclei >/dev/null 2>&1; then
  PORTA=8015
  python3 -m http.server "$PORTA" --bind 127.0.0.1 --directory desafio/site >/dev/null 2>&1 &
  SERVIDOR=$!
  for _ in $(seq 20); do curl -s -o /dev/null "http://127.0.0.1:$PORTA/" && break; sleep 0.2; done
  for p in index.html sobre.html contato.html; do echo "http://127.0.0.1:$PORTA/$p"; done > urls.txt
  nuclei -t desafio/extrair-emails.yaml -l urls.txt -silent || alerta "nuclei falhou"
  rm -f urls.txt
  kill "$SERVIDOR"; wait "$SERVIDOR" 2>/dev/null
else
  dica "nuclei não instalado — o grep -oE das seções anteriores faz a mesma extração."
fi

# %% No mundo real: raspando uma página pública
# Mesma técnica num site de verdade (example.com é feito para testes).
titulo "Raspando example.com"
precisa html2text
if online; then
  curl -s https://example.com -o pagina.html
else
  alerta "offline: usando cópia salva"
  cp desafio/example.com.html pagina.html
fi
echo "Título: $(grep -o '<title>[^<]*' pagina.html | sed 's/<title>//')"
grep -o 'href="[^"]*"' pagina.html | sed 's/^href="//; s/"$//'
html2text -utf8 -nobs pagina.html
rm pagina.html
