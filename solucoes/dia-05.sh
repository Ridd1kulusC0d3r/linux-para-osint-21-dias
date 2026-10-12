#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 5. Tente sozinho antes!
# Ideia: seguir a cadeia de redirecionamentos do link do SMS até o FIM.
#   1. sobe o encurtador falso (cópia local da cadeia salva)
#   2. curl -sIL segue todos os saltos; grep -i ^location filtra os destinos
#   3. tail -n 1 pega o último; o parâmetro "protocolo=" está em Base64
#   4. base64 -d decodifica e revela a flag
# (Sem servidor também dá: grep -i ^location desafio/cabecalhos-link-golpe.txt | tail -n 1)
cd "$(dirname "$0")/../dias/dia-05-curl-e-apis/desafio" || exit 1

python3 encurtador.py 8085 >/dev/null 2>&1 &
servidor=$!
for _ in $(seq 30); do curl -s --noproxy '*' -o /dev/null http://127.0.0.1:8085/ && break; sleep 0.1; done

ultimo=$(curl -sIL --noproxy '*' --connect-to ::127.0.0.1:8085 http://encurta.example/x7Kp9 \
  | grep -i '^location' | tail -n 1 | tr -d '\r')
kill "$servidor"

echo "Destino final: $ultimo"
protocolo=${ultimo#*protocolo=}          # tudo depois de "protocolo="
echo "protocolo (Base64): $protocolo"
echo "$protocolo" | base64 -d
echo
