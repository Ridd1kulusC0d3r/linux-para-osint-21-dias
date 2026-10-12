#!/usr/bin/env bash
# =============================================================================
#  Dia 0 — O pendrive: preparando o ambiente
#  Rodar tudo:  bash comandos.sh
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% Quem sou eu e onde estou?
# Três perguntas que todo terminal responde:
#   whoami   -> qual usuário está logado
#   hostname -> nome da máquina
#   pwd      -> em que pasta você está
titulo "Identificação"
whoami
hostname
pwd

# %% Que sistema é este?
# /etc/os-release diz a distribuição (Ubuntu, Debian...).
# uname -a mostra o kernel (o "coração" do Linux).
titulo "Sistema operacional"
grep -E '^(PRETTY_NAME|VERSION_ID)=' /etc/os-release
uname -a

# %% Quanto espaço e memória eu tenho?
# df -h  -> espaço em disco (h = legível para humanos)
# free -h -> memória RAM
titulo "Recursos da máquina"
df -h . | tail -n 1
free -h | head -n 2

# %% Conferindo as ferramentas do curso
# Este script mostra o que já está instalado. Não se preocupe com o que falta:
# cada dia instala sozinho o que precisar, na hora certa.
titulo "Ferramentas"
bash ../../ferramentas/verificar_ambiente.sh

# %% Seu primeiro comando de verdade
# echo imprime texto. date mostra data e hora. O $( ) roda um comando
# e coloca o resultado dentro do texto.
titulo "Diário aberto"
echo "Recruta pronto(a) para a Operação Vazante em $(date '+%d/%m/%Y às %H:%M')"
