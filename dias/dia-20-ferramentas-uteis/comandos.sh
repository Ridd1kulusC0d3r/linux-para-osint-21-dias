#!/usr/bin/env bash
# =============================================================================
#  Dia 20 — O script quebrado: ferramentas que facilitam a vida no terminal
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% shellcheck: o corretor ortográfico do Bash
# O programa shellcheck lê um script SEM executá-lo e aponta erros e armadilhas.
# Cada aviso tem um código (SC2086, SC2283...) com explicação na wiki:
#   https://www.shellcheck.net/wiki/SC2086
# Níveis: error (vai quebrar), warning (provavelmente errado),
#         info/style (melhor prática).
titulo "shellcheck no script de maré_alta"
precisa shellcheck
shellcheck desafio/script_quebrado.sh || true      # || true: avisos não param o curso
echo "--- formato resumido (uma linha por aviso) ---"
shellcheck -f gcc desafio/script_quebrado.sh || true

# %% O exemplo clássico do cipher387
# O script original do curso (wrong_code.sh) tem erros "de lógica" que só o
# o shellcheck vê: uma opção -v tratada no case mas não declarada no getopts,
# e $$(uname), que vira o número do processo + "(uname)".
titulo "Erros que o Bash não reclama, mas o shellcheck sim"
precisa shellcheck
mkdir -p treino
cat > treino/wrong_code.sh <<'FIM'
#!/bin/bash
while getopts "nf:" param; do
  case "$param" in
    f) file="$OPTARG" ;;
    v) set -x ;;
  esac
done
case "$file" in
  *.gz) gzip -d "$file" ;;
  *) echo "Unknown filetype" ;;
esac
if [[ "$$(uname)" == "Linux" ]]; then echo "Using Linux"; fi
FIM
bash treino/wrong_code.sh            # roda "sem erro"... e não faz o que devia
shellcheck treino/wrong_code.sh || true
rm -r treino

# %% Rodando o script quebrado
# Do jeito que está, o script de maré_alta falha. Leia a mensagem de erro:
# "pasta: command not found" — o Bash achou que "pasta" era um COMANDO.
titulo "Executando o script quebrado"
bash desafio/script_quebrado.sh || alerta "falhou, como esperado"

# %% Os três erros mais comuns de Bash
# 1) Espaço em volta do =    nome = "x"   -> roda o comando "nome" com args "=" e "x"
# 2) Variável sem aspas      $pasta       -> "pedacos de selo" vira 3 palavras
# 3) Nome de arquivo com espaço sem aspas -> "parte 01.txt" vira "parte" e "01.txt"
# Regra de ouro: SEMPRE "$variavel" entre aspas duplas.
titulo "Demonstração: aspas fazem diferença"
mkdir -p "treino/pasta com espaco"
echo "oi" > "treino/pasta com espaco/arquivo 1.txt"
pasta="treino/pasta com espaco"
echo "--- sem aspas (quebra nos espaços) ---"
# shellcheck disable=SC2231  # (erro proposital, para você ver o problema)
for a in $pasta/*.txt; do echo "[$a]"; done
echo "--- com aspas ---"
for a in "$pasta"/*.txt; do echo "[$a]"; done
echo "--- set -x mostra cada comando ANTES de rodar (modo depuração) ---"
# shellcheck disable=SC2016  # (aspas simples de propósito: o $p é do bash -c)
bash -x -c 'p="a b"; ls $p' 2>&1 | head -n 3 || true
rm -r treino

# %% history: tudo que você digitou
# O Bash guarda os comandos digitados em ~/.bash_history.
#   history          lista com números
#   history | grep   procura um comando antigo
#   !123             repete o comando número 123
#   !!               repete o último (sudo !! = o último, com sudo)
#   Ctrl+R           busca reversa interativa: digite um pedaço e aperte Ctrl+R de novo
# Num script não há o que você digitou, então carregamos (history -r) um
# histórico "esquecido" por maré_alta (uma cópia, para não tocar no seu).
titulo "O histórico de maré_alta"
HISTFILE=$(mktemp)                       # cópia temporária
cp desafio/historico_mare_alta.txt "$HISTFILE"
history -c                               # começa vazio
history -r "$HISTFILE"                   # lê o arquivo para a memória
history
echo "--- só os comandos de git ---"
history | grep ' git '
echo "--- os 3 últimos ---"
history 3
rm -f "$HISTFILE"
dica "O último comando dele foi 'history -c' (apagar o histórico)... mas o arquivo já estava salvo."

# %% alias: apelidos para comandos longos
# alias cria um atalho. Para ficar permanente, coloque no ~/.bashrc.
# Em scripts, aliases vêm desligados; `shopt -s expand_aliases` liga.
titulo "Aliases"
shopt -s expand_aliases
alias ll='ls -lah'
alias meuip='curl -s https://ifconfig.me; echo'
alias hashes='sha256sum'
alias                                    # lista os aliases definidos
ll desafio
mostrar "echo \"alias ll='ls -lah'\" >> ~/.bashrc && source ~/.bashrc   # permanente"

# %% Completar com Tab e outras teclas que economizam a vida
# Tab        completa nomes de comandos, arquivos e pastas (2x Tab = opções)
# Ctrl+R     busca no histórico            Ctrl+A / Ctrl+E  início / fim da linha
# Ctrl+C     cancela o comando             Ctrl+L           limpa a tela
# Ctrl+U     apaga a linha                 Alt+.            último argumento do comando anterior
# Tab é a melhor amiga de quem tem pasta com espaço: ela põe as \ ou aspas sozinha.
titulo "Teclas de atalho"
dica "Digite: cat desafio/ped<Tab>  -> vira  cat desafio/pedacos\\ de\\ selo/"
complete -p git 2>/dev/null || dica "No seu terminal, 'complete -p' lista as regras de autocompletar."

# %% tldr: o manual resumido
# man é completo, mas longo. tldr mostra só os exemplos mais usados.
# Na primeira vez ele baixa as páginas (precisa de internet).
titulo "tldr"
precisa tldr
if online; then
  tldr tar 2>/dev/null | head -n 25 || alerta "tldr não conseguiu baixar as páginas"
else
  alerta "offline: tldr precisa baixar as páginas na primeira vez"
  mostrar "tldr tar"
  mostrar "tldr --update"
fi

# %% fzf: busca difusa em qualquer lista
# fzf recebe uma lista e deixa você filtrar digitando pedaços (fuzzy).
# Interativo no terminal; com --filter funciona em script.
# Depois de instalado, Ctrl+R e Ctrl+T no terminal ganham superpoderes com ele.
titulo "fzf"
precisa fzf
find desafio -type f | fzf --filter='parte 03'
echo "--- 'difuso': letras na ordem, não precisam estar juntas ---"
find desafio -type f | fzf --filter='hstmar'
interativo fzf

# %% explainshell: o que esse comando faz?
# explainshell.com explica cada pedaço de um comando. Montamos a URL com
# urlencode (jq @uri). Bom para comandos copiados da internet ou de um chatbot
# — nunca rode o que você não entende.
titulo "explainshell"
precisa jq
cmd="find . -type f -name '*.txt' -exec sha256sum {} +"
echo "https://explainshell.com/explain?cmd=$(jq -rn --arg c "$cmd" '$c | @uri')"

# %% Depurando o script de maré_alta com sed (sem mexer no original)
# Copie, corrija a cópia, rode a cópia. O original fica intacto como evidência.
# Aqui corrigimos SÓ o primeiro erro, para ver que ainda não basta.
titulo "Corrigindo um erro de cada vez"
precisa shellcheck
cp desafio/script_quebrado.sh desafio/teste_parcial.sh
sed -i 's/^pasta = /pasta=/' desafio/teste_parcial.sh     # tira os espaços do =
grep -n '^pasta' desafio/teste_parcial.sh
bash desafio/teste_parcial.sh || alerta "ainda quebrado: faltam as aspas"
shellcheck desafio/teste_parcial.sh || true
rm desafio/teste_parcial.sh
