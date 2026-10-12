#!/usr/bin/env bash
# =============================================================================
#  Dia 18 — Quem registrou? Investigação de domínio: whois e DNS
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
#
#  Online consultamos só domínios públicos e seguros (registro.br, example.com).
#  Os domínios do caso (*.example) são fictícios: as respostas de whois e dig
#  deles estão salvas em desafio/whois/ e desafio/dns/.
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% whois: a "certidão" de um domínio
# Todo domínio é registrado por alguém, numa data, num registro (o .br é do
# registro.br / NIC.br). O `whois` pergunta isso ao servidor do registro.
# No .br aparecem: dono (owner), contatos (owner-c, tech-c), servidores de
# nome (nserver), datas de criação/alteração/expiração.
titulo "whois registro.br"
precisa whois
if online && whois registro.br > whois_real.txt 2>/dev/null && [ -s whois_real.txt ]; then
  grep -v '^%' whois_real.txt | grep -v '^$' | head -n 25
else
  alerta "offline: usando cópia salva (formato idêntico ao do registro.br)"
  grep -v '^%' desafio/whois/pixvelox.example.txt | grep -v '^$'
fi
rm -f whois_real.txt

# %% Filtrando o whois com grep
# whois devolve muito texto. grep separa o que interessa.
# Domínios .com usam "Creation Date"; o registro.br usa "created".
#   -i   ignora maiúsculas/minúsculas      -E  vários padrões com |
titulo "Só as datas e os contatos"
precisa whois
if online && whois example.com > whois_com.txt 2>/dev/null && [ -s whois_com.txt ]; then
  echo "--- example.com (formato internacional) ---"
  grep -i 'Creation' whois_com.txt | head -n 2
fi
rm -f whois_com.txt
echo "--- pixvelox.example (formato registro.br) ---"
grep -E '^(created|changed|expires):' desafio/whois/pixvelox.example.txt
grep -E '^(owner|owner-c|tech-c|e-mail):' desafio/whois/pixvelox.example.txt

# %% dig: perguntando ao DNS
# DNS é a "lista telefônica" da internet: traduz nome em endereço e guarda
# outras informações. Tipos de registro mais úteis em OSINT:
#   A / AAAA   endereço IPv4 / IPv6 do site
#   MX         servidor que recebe os e-mails do domínio
#   NS         servidores de nome (quem "responde" pelo domínio)
#   TXT        textos livres: SPF, verificações do Google/Microsoft...
# +short mostra só a resposta, sem cabeçalhos.
titulo "dig example.com e registro.br"
precisa dig dnsutils
if online && dig +short example.com A >/dev/null 2>&1 && [ -n "$(dig +short example.com A)" ]; then
  dig example.com                  # saída completa
  echo "--- só as respostas (+short) ---"
  dig +short example.com A
  dig +short registro.br MX
  dig +short registro.br NS
  dig +short registro.br TXT | head -n 5
else
  alerta "offline: usando cópia salva"
  cat desafio/dig_pixvelox.example.txt
fi

# %% Lendo a saída do dig
# Na saída completa, a parte que importa é a ANSWER SECTION:
#   nome.   TTL   classe   tipo   valor
# TTL = quantos segundos a resposta pode ficar guardada em cache.
titulo "A ANSWER SECTION"
grep -A 2 'ANSWER SECTION' desafio/dig_pixvelox.example.txt
echo "--- registros salvos dos domínios do caso (+noall +answer) ---"
cat desafio/dns/pixvelox.example.txt

# %% Separando por tipo com awk
# Cada linha tem 5 colunas: nome, TTL, classe, TIPO, valor. awk filtra a 4ª.
titulo "Registros por tipo"
echo "--- MX ---";  awk '$4 == "MX"'  desafio/dns/pixvelox.example.txt
echo "--- NS ---";  awk '$4 == "NS" {print $5}' desafio/dns/pixvelox.example.txt
echo "--- TXT ---"; awk -F'\t' '$4 == "TXT" {print $5}' desafio/dns/pixvelox.example.txt

# %% host e nslookup: os primos do dig
# `host` dá respostas curtas e legíveis; `nslookup` é o mais antigo (existe
# até no Windows). Os dois vêm no mesmo pacote do dig.
titulo "host e nslookup"
precisa host bind9-host
precisa nslookup dnsutils
if online && host example.com >/dev/null 2>&1; then
  host example.com
  host -t MX registro.br
  nslookup -type=NS registro.br | tail -n +4
else
  alerta "offline: só mostrando os comandos"
  mostrar "host example.com"
  mostrar "host -t MX registro.br"
  mostrar "nslookup -type=NS registro.br"
fi

# %% DNS reverso: de IP para nome
# dig -x IP pergunta "qual nome está ligado a este IP?" (registro PTR).
# Em hospedagens compartilhadas, revela o provedor.
titulo "DNS reverso"
precisa dig dnsutils
if online && [ -n "$(dig +short -x 8.8.8.8)" ]; then
  dig +short -x 8.8.8.8
else
  alerta "offline: só mostrando o comando"
  mostrar "dig +short -x 8.8.8.8    # -> dns.google."
fi

# %% Correlação: o que dois domínios têm em comum?
# Golpistas trocam de "laranja" no campo owner, mas costumam reaproveitar
# infraestrutura: o mesmo técnico, o mesmo e-mail, os mesmos servidores DNS.
# Juntamos os campos de todos os whois e contamos repetições.
titulo "Campos repetidos entre os domínios do caso"
for arq in desafio/whois/*.txt; do
  dominio=$(basename "$arq" .txt)
  grep -E '^(tech-c|nserver|e-mail):' "$arq" | sed "s|^|$dominio  |"
done | sort -k2 > campos.txt
cat campos.txt
echo "--- valores que aparecem em MAIS DE UM domínio ---"
awk '{print $2, $3}' campos.txt | sort | uniq -c | awk '$1 > 1'
rm campos.txt

# %% Quais domínios estão ligados pelo mesmo técnico?
# Achamos o handle repetido (tech-c) e listamos os domínios que o usam.
titulo "Domínios do mesmo tech-c"
grep -l '^tech-c: *MAALT12' desafio/whois/*.txt | xargs -n1 basename | sed 's/\.txt$//'
echo "--- e o e-mail desse contato ---"
grep -A 2 '^nic-hdl-br: *MAALT12' desafio/whois/pixvelox.example.txt | grep 'e-mail'

# %% Netlas host (opcional, precisa de API key)
# O Netlas junta whois + DNS + servidores num lugar só.
titulo "netlas host"
mostrar "pip install netlas"
mostrar "netlas savekey SUA_CHAVE"
mostrar "netlas host registro.br"
if online && [ -n "${NETLAS_API_KEY:-}" ] && command -v netlas >/dev/null 2>&1; then
  netlas host -a "$NETLAS_API_KEY" registro.br | head -n 30
else
  dica "Sem NETLAS_API_KEY (ou offline): pulando."
fi

# %% Versão brazuca: RDAP do registro.br
# RDAP é o "whois moderno": mesma informação, mas em JSON (bom para jq).
# O registro.br tem RDAP público em https://rdap.registro.br/domain/<dominio>
titulo "RDAP do registro.br"
precisa jq
if online && curl -s -m 15 https://rdap.registro.br/domain/registro.br -o rdap.json && jq -e . rdap.json >/dev/null 2>&1; then
  jq -r '.ldhName, (.events[] | "\(.eventAction): \(.eventDate)")' rdap.json
  jq -r '.nameservers[].ldhName' rdap.json
else
  alerta "offline: só mostrando o comando"
  mostrar "curl -s https://rdap.registro.br/domain/registro.br | jq '.events'"
fi
rm -f rdap.json
