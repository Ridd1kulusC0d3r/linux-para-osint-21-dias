#!/usr/bin/env bash
# =============================================================================
#  Dia 21 — monta o dossiê da Operação Vazante e abre o selo final.
#
#    bash montar_dossie.sh
#
#  Ele lê as flags que você já acertou (guardadas em .progresso/ pelo checar.sh
#  de cada dia), confere uma por uma e, se as 20 estiverem certas, usa todas
#  juntas como chave para abrir o selo com a flag final.
#
#  Variável opcional: L4O_PROGRESSO=/outra/pasta  (de onde ler as flags)
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

PROGRESSO="${L4O_PROGRESSO:-$L4O_HOME/.progresso}"
SAIDA="dossie-final"
flags=()      # as 20 flags, em ordem
faltam=()     # dias sem flag válida

titulo "Conferindo as 20 pistas"
for n in $(seq 1 20); do
  nn="$(printf '%02d' "$n")"
  pasta="$(echo "$L4O_HOME"/dias/dia-"$nn"-*)"           # pasta do dia N
  if [ ! -f "$pasta/checar.sh" ]; then
    alerta "Dia $nn — pasta do dia não encontrada"; faltam+=("$nn"); continue
  fi
  arquivo="$PROGRESSO/$(basename "$pasta").flag"
  esperado="$(grep -oE '[0-9a-f]{64}' "$pasta/checar.sh" | head -n 1)"

  if [ -f "$arquivo" ]; then
    flag="$(normalizar_flag "$(cat "$arquivo")")"
    if [ "$(printf '%s' "$flag" | sha256sum | cut -d' ' -f1)" = "$esperado" ]; then
      ok "Dia $nn"
      flags+=("$flag")
      continue
    fi
  fi
  alerta "Dia $nn — sem flag válida (rode o checar.sh desse dia com a resposta)"
  faltam+=("$nn")
done

if [ "${#faltam[@]}" -gt 0 ]; then
  echo
  erro "Faltam ${#faltam[@]} pista(s): dias ${faltam[*]}. O selo continua fechado."
  exit 1
fi

titulo "Abrindo o selo"
# A chave é o SHA-256 das 20 flags, uma por linha. O selo é a flag final
# cifrada com XOR (o mesmo byte da chave "liga e desliga" cada bit).
FLAG_FINAL="$(printf '%s\n' "${flags[@]}" | head -c -1 | python3 -c '
import hashlib, sys
chave = hashlib.sha256(sys.stdin.buffer.read()).digest()
selo = bytes.fromhex(open("desafio/selo.hex").read().strip())
print(bytes(b ^ chave[i % len(chave)] for i, b in enumerate(selo)).decode())
')"
ok "Selo aberto!"

titulo "Gerando o dossiê"
mkdir -p "$SAIDA"
{
  echo "# 🗂️ Dossiê — Operação Vazante"
  echo
  echo "Gerado em $(date '+%d/%m/%Y %H:%M') por $(whoami)."
  echo
  echo "| Dia | Pista |"
  echo "|---:|---|"
  for i in "${!flags[@]}"; do
    # shellcheck disable=SC2016  # as crases são markdown, não comando
    printf '| %d | `%s` |\n' "$((i + 1))" "${flags[$i]}"
  done
  echo
  echo "**Selo final:** \`$FLAG_FINAL\`"
} > "$SAIDA/DOSSIE.md"
ok "Dossiê salvo em $SAIDA/DOSSIE.md"

echo
echo "$FLAG_FINAL"
