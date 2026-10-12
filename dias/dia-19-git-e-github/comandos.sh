#!/usr/bin/env bash
# =============================================================================
#  Dia 19 — O commit apagado: Git e GitHub
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
#
#  O repositório d'Os Vazantes vem num arquivo só: desafio/vazantes.bundle
#  (um "git bundle"). Dá para clonar dele exatamente como de um GitHub —
#  sem internet. Cada seção clona numa pasta de trabalho e apaga no final.
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% Instalando e conferindo o git
# Git guarda o HISTÓRICO de uma pasta: cada "commit" é uma fotografia de
# todos os arquivos, com autor, e-mail, data e mensagem.
titulo "git instalado?"
precisa git
git --version

# %% Clonando o repositório
# `git clone ORIGEM PASTA` copia o repositório inteiro, COM todo o histórico.
# A origem pode ser um endereço do GitHub ou, como aqui, um arquivo .bundle.
titulo "git clone do bundle"
git bundle verify desafio/vazantes.bundle        # confere se o pacote está íntegro
git clone -q desafio/vazantes.bundle trabalho/pxv-site
(
  cd trabalho/pxv-site || exit 1
  ls -la                    # repare na pasta oculta .git: é ali que mora o histórico
  cat README.md
)
rm -rf trabalho

# %% git log: a linha do tempo
# Cada commit tem um identificador (hash). `--oneline` mostra um por linha.
# `--stat` mostra quais arquivos cada commit mexeu.
titulo "git log"
git clone -q desafio/vazantes.bundle trabalho/pxv-site
(
  cd trabalho/pxv-site || exit 1
  git log --oneline
  echo "---"
  git log --stat --format='%h %ad %s' --date=short
)
rm -rf trabalho

# %% OSINT clássico: quem são os autores?
# Todo commit grava NOME e E-MAIL de quem o fez — e muita gente esquece de
# configurar um e-mail "de fachada" numa das máquinas.
#   %an nome   %ae e-mail   %ad data   %s mensagem
titulo "Autores e e-mails dos commits"
git clone -q desafio/vazantes.bundle trabalho/pxv-site
(
  cd trabalho/pxv-site || exit 1
  git log --format='%an <%ae>' | sort | uniq -c
  echo "--- horários dos commits (hábitos do autor) ---"
  git log --format='%ad  %s' --date=format:'%d/%m %H:%M'
)
rm -rf trabalho

# %% git show e git diff: o que mudou?
# `git show HASH` mostra o commit e a diferença que ele introduziu.
# `git diff A B` compara duas versões. Linhas com + entraram, com - saíram.
# HEAD é o commit atual; HEAD~1 o anterior; HEAD~2 o de antes...
titulo "git show e git diff"
git clone -q desafio/vazantes.bundle trabalho/pxv-site
(
  cd trabalho/pxv-site || exit 1
  git show --stat HEAD
  echo "--- diferença do README entre o primeiro commit e agora ---"
  git diff "$(git rev-list --max-parents=0 HEAD)" HEAD -- README.md
)
rm -rf trabalho

# %% O truque: apagado não é esquecido
# Apagar um arquivo e fazer commit só tira ele do PRESENTE. Todas as versões
# antigas continuam dentro do .git — e qualquer um que clonar recebe tudo.
#   git log --diff-filter=D   commits que APAGARAM (Deleted) arquivos
#   git log -p                mostra o conteúdo de cada mudança (patch)
titulo "Arquivos apagados no histórico"
git clone -q desafio/vazantes.bundle trabalho/pxv-site
(
  cd trabalho/pxv-site || exit 1
  ls                                             # config.env não está aqui...
  echo "--- ...mas o histórico lembra ---"
  git log --diff-filter=D --name-only --format='commit %h: %s'
  echo "--- histórico só desse arquivo, com o conteúdo (-p) ---"
  git log -p --format='commit %h %s' -- config.env | grep -v 'PAINEL_CHAVE' || true
)
rm -rf trabalho
dica "Escondemos a linha da chave de propósito. Recupere-a no desafio. 😉"

# %% Procurando segredos em TODO o histórico
# `git log -p --all` despeja todas as mudanças de todos os ramos; grep procura
# padrões típicos de segredo. -S "texto" acha commits que adicionaram/removeram o texto.
titulo "Caçando segredos"
git clone -q desafio/vazantes.bundle trabalho/pxv-site
(
  cd trabalho/pxv-site || exit 1
  git log -p --all | grep -E '^[+-][A-Z_]+(URL|USER|GATEWAY)=' || true
  echo "--- commits que mexeram em 'PAINEL_' ---"
  git log -S 'PAINEL_' --oneline
)
rm -rf trabalho

# %% Seu primeiro commit e o git status
# O ciclo do dia a dia:  editar -> git add -> git commit -> git push
# `git status` diz o que mudou e o que já está "preparado" (staged).
titulo "add, commit e status"
git clone -q desafio/vazantes.bundle trabalho/pxv-site
(
  cd trabalho/pxv-site || exit 1
  git config user.name "Recruta Coruja"                 # identidade SÓ neste repositório
  git config user.email "recruta@nucleo-coruja.example"
  ls > test.txt                                         # cria um arquivo novo
  git status --short                                    # ?? = arquivo não rastreado
  git add test.txt                                      # prepara
  git status --short                                    # A  = adicionado
  git commit -q -m "anotações do recruta"               # -m: mensagem sem abrir editor
  git log --oneline -n 2
  git status                                            # tudo limpo
)
rm -rf trabalho
interativo git commit       # sem -m o git abre um editor para a mensagem

# %% git push (para um "GitHub" local)
# `git push` envia seus commits para o repositório remoto (GitHub, GitLab...).
# Para treinar sem conta, criamos um repositório "bare" (só o .git) numa pasta.
titulo "git push para um remoto local"
mkdir -p trabalho
git init -q --bare --initial-branch=main trabalho/remoto.git   # remoto vazio, ramo principal "main"
git clone -q desafio/vazantes.bundle trabalho/pxv-site
(
  cd trabalho/pxv-site || exit 1
  git config user.name "Recruta Coruja"
  git config user.email "recruta@nucleo-coruja.example"
  git remote add coruja ../remoto.git                  # um segundo "remoto"
  echo "Relatório preliminar" > relatorio.txt
  git add relatorio.txt && git commit -q -m "relatório"
  git push -q coruja main                              # envia!
)
echo "--- o remoto recebeu: ---"
git --git-dir=trabalho/remoto.git log --oneline -n 3
rm -rf trabalho
dica "No GitHub de verdade: git push origin main (pede login/token na primeira vez)."

# %% No mundo real: clonando do GitHub
# Clonar repositório público não precisa de conta. --depth 1 baixa só a versão
# mais recente (rápido), mas SEM o histórico — para OSINT você quer o histórico!
# `git ls-remote` lista os ramos de um repositório sem baixar nada.
titulo "GitHub de verdade"
if online && git ls-remote https://github.com/okfn-brasil/querido-diario HEAD > ls_remote.txt 2>/dev/null; then
  cat ls_remote.txt
else
  alerta "offline: só mostrando os comandos"
fi
rm -f ls_remote.txt
mostrar "git clone https://github.com/okfn-brasil/querido-diario"
mostrar "git clone --depth 1 https://github.com/okfn-brasil/querido-diario   # só o presente"
