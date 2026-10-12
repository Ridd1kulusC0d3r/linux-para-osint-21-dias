#!/usr/bin/env bash
# =============================================================================
#  Instala de uma vez as ferramentas usadas no curso (Ubuntu/Debian).
#
#    bash ferramentas/instalar_tudo.sh          # básico (rápido, ~1 min)
#    bash ferramentas/instalar_tudo.sh completo # + mídia, PDF, Office (mais pesado)
#
#  Não é obrigatório: cada dia instala sozinho o que precisa (função "precisa").
#  Este script é para quem quer deixar a máquina pronta antes de começar.
# =============================================================================
cd "$(dirname "$0")/.." || exit 1
source lib/comum.sh

BASICO=(
  zip unzip curl jq tree file whois dnsutils git vim screen cron
  shellcheck html2text xmlstarlet libimage-exiftool-perl poppler-utils
  bsdextrautils binutils wget bind9-host transmission-cli aria2 lftp fzf
)
COMPLETO=(
  ffmpeg tesseract-ocr tesseract-ocr-por ghostscript pandoc
  libreoffice-writer-nogui libreoffice-calc-nogui translate-shell
)
PIP=(csvkit)

pacotes=("${BASICO[@]}")
[ "${1:-}" = "completo" ] && pacotes+=("${COMPLETO[@]}")

titulo "Instalando ${#pacotes[@]} pacotes via apt"
$SUDO apt-get update -qq
DEBIAN_FRONTEND=noninteractive $SUDO apt-get install -y -qq "${pacotes[@]}" \
  && ok "Pacotes apt instalados."

titulo "Instalando ferramentas Python (pip)"
python3 -m pip install -q "${PIP[@]}" 2>/dev/null \
  || python3 -m pip install -q --break-system-packages "${PIP[@]}" \
  && ok "Pacotes pip instalados."

bash ferramentas/verificar_ambiente.sh
