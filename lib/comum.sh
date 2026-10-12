#!/usr/bin/env bash
# =============================================================================
#  lib/comum.sh — funções compartilhadas por todos os dias do curso
# -----------------------------------------------------------------------------
#  Este arquivo NÃO é executado sozinho: ele é "carregado" (source) no começo
#  de cada comandos.sh e de cada célula dos notebooks Colab.
#
#      source "$L4O_HOME/lib/comum.sh"
#
#  Por que existe? Para que os scripts de cada dia fiquem curtos e legíveis:
#  instalar pacotes, testar internet e conferir flags vira uma linha só.
#  Leia com calma — tudo aqui também é material de estudo de Bash.
# =============================================================================

# --- Onde está o repositório? ------------------------------------------------
# Se a variável L4O_HOME já existe (Colab define), usamos ela.
# Senão, descobrimos a partir da localização deste próprio arquivo.
if [ -z "${L4O_HOME:-}" ]; then
  L4O_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi
export L4O_HOME

# --- Cores (só se a saída for um terminal de verdade) ------------------------
if [ -t 1 ] || [ -n "${COLAB_RELEASE_TAG:-}" ] || [ -n "${L4O_CORES:-}" ]; then
  C_AZUL=$'\e[1;34m'; C_VERDE=$'\e[1;32m'; C_AMARELO=$'\e[1;33m'
  C_VERMELHO=$'\e[1;31m'; C_CINZA=$'\e[0;90m'; C_FIM=$'\e[0m'
else
  C_AZUL=""; C_VERDE=""; C_AMARELO=""; C_VERMELHO=""; C_CINZA=""; C_FIM=""
fi

# --- Mensagens padronizadas --------------------------------------------------
titulo()  { printf '\n%s━━━ %s ━━━%s\n' "$C_AZUL" "$*" "$C_FIM"; }   # cabeçalho de seção
dica()    { printf '%s💡 %s%s\n' "$C_CINZA" "$*" "$C_FIM"; }         # comentário didático
ok()      { printf '%s✔ %s%s\n' "$C_VERDE" "$*" "$C_FIM"; }          # deu certo
alerta()  { printf '%s⚠ %s%s\n' "$C_AMARELO" "$*" "$C_FIM"; }        # atenção
erro()    { printf '%s✘ %s%s\n' "$C_VERMELHO" "$*" "$C_FIM" >&2; }   # deu errado
mostrar() { printf '%s$ %s%s\n' "$C_CINZA" "$*" "$C_FIM"; }          # exibe um comando sem rodar

# --- sudo só quando precisa --------------------------------------------------
# No Colab você já é root (id -u = 0), então "sudo" é dispensável.
if [ "$(id -u)" -eq 0 ]; then SUDO=""; else SUDO="sudo"; fi

# --- precisa <comando> [pacote-apt] ------------------------------------------
# Garante que um programa existe. Se não existir, instala via apt.
#   precisa jq                 -> instala o pacote "jq"
#   precisa dig dnsutils       -> o comando é "dig", o pacote é "dnsutils"
_APT_ATUALIZADO=""
precisa() {
  local cmd="$1" pacote="${2:-$1}"
  if command -v "$cmd" >/dev/null 2>&1; then return 0; fi
  if ! command -v apt-get >/dev/null 2>&1; then
    alerta "'$cmd' não encontrado e não há apt-get aqui. Instale '$pacote' manualmente."
    return 1
  fi
  alerta "Instalando '$pacote' (pode levar alguns segundos)..."
  if [ -z "$_APT_ATUALIZADO" ]; then
    $SUDO apt-get update -qq >/dev/null 2>&1 || true
    _APT_ATUALIZADO=1
  fi
  if $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y -qq "$pacote" >/dev/null 2>&1; then
    ok "'$pacote' instalado."
  else
    erro "Não consegui instalar '$pacote'. Tente: $SUDO apt-get install $pacote"
    return 1
  fi
}

# --- precisa_pip <comando> [pacote-pip] --------------------------------------
precisa_pip() {
  local cmd="$1" pacote="${2:-$1}"
  if command -v "$cmd" >/dev/null 2>&1; then return 0; fi
  alerta "Instalando '$pacote' via pip..."
  python3 -m pip install -q "$pacote" 2>/dev/null \
    || python3 -m pip install -q --break-system-packages "$pacote" 2>/dev/null \
    || { erro "Falhou: pip install $pacote"; return 1; }
  ok "'$pacote' instalado."
}

# --- online ------------------------------------------------------------------
# Retorna sucesso (0) se houver internet. Exporte L4O_OFFLINE=1 para forçar o
# modo offline (útil em aula, em avião ou quando a rede bloqueia).
online() {
  [ -n "${L4O_OFFLINE:-}" ] && return 1
  curl -s -m 5 -o /dev/null https://www.google.com 2>/dev/null
}

# --- interativo <comando...> -------------------------------------------------
# Comandos que "prendem" o terminal (vim, screen, less) não funcionam bem num
# script ou no Colab. Por padrão só mostramos o comando; com L4O_INTERATIVO=1
# ele é executado de verdade.
interativo() {
  if [ -n "${L4O_INTERATIVO:-}" ]; then
    "$@"
  else
    mostrar "$*"
    dica "Comando interativo: rode no seu terminal (ou exporte L4O_INTERATIVO=1)."
  fi
}

# --- normalizar_flag / checar_flag -------------------------------------------
# As flags nunca ficam escritas no repositório: guardamos só o SHA-256 delas.
# Assim você pode conferir a resposta sem levar spoiler.
normalizar_flag() {
  # remove espaços nas pontas e quebras de linha
  printf '%s' "$1" | tr -d '\r\n' | sed 's/^[[:space:]]*//; s/[[:space:]]*$//'
}

checar_flag() {
  local resposta="$1" esperado="$2" hash
  if [ -z "$resposta" ]; then
    alerta "Uso: bash checar.sh 'VAZANTE{...}'"
    return 2
  fi
  hash="$(normalizar_flag "$resposta" | sha256sum | cut -d' ' -f1)"
  if [ "$hash" = "$esperado" ]; then
    ok "Flag correta! Pista registrada no seu dossiê. 🦉"
    mkdir -p "$L4O_HOME/.progresso"
    normalizar_flag "$resposta" > "$L4O_HOME/.progresso/$(basename "$PWD").flag"
    return 0
  else
    erro "Ainda não é essa. Releia a missão e tente de novo."
    return 1
  fi
}
