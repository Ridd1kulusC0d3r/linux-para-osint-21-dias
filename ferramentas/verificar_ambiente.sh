#!/usr/bin/env bash
# =============================================================================
#  Mostra quais ferramentas do curso já estão disponíveis nesta máquina.
#    bash ferramentas/verificar_ambiente.sh
# =============================================================================
cd "$(dirname "$0")/.." || exit 1
source lib/comum.sh

# formato: comando:dia-em-que-aparece
FERRAMENTAS=(
  bash:1 find:1 zip:3 unzip:3 xargs:4 curl:5 grep:6 sed:7 awk:7 vim:8
  screen:9 crontab:9 sort:10 comm:10 ffmpeg:11 tesseract:11 pdftotext:12
  exiftool:12 libreoffice:13 pandoc:13 jq:14 xmlstarlet:14 csvgrep:14
  html2text:15 python3:15 whois:18 dig:18 git:19 shellcheck:20
)

titulo "Verificando o ambiente"
faltando=0
for item in "${FERRAMENTAS[@]}"; do
  cmd="${item%%:*}"; dia="${item##*:}"
  if command -v "$cmd" >/dev/null 2>&1; then
    printf '  %s✔%s %-12s (Dia %s)\n' "$C_VERDE" "$C_FIM" "$cmd" "$dia"
  else
    printf '  %s·%s %-12s (Dia %s) — será instalado quando precisar\n' "$C_AMARELO" "$C_FIM" "$cmd" "$dia"
    faltando=$((faltando + 1))
  fi
done

echo
if online; then ok "Internet: disponível"; else alerta "Internet: indisponível (os dias usam cópias salvas)"; fi
if [ "$faltando" -eq 0 ]; then
  ok "Tudo pronto!"
else
  dica "$faltando ferramenta(s) ainda não instaladas. Tudo bem: cada dia instala o que usa."
fi
