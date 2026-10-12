#!/usr/bin/env bash
# =============================================================================
#  Dia 6 — Agulha no vazamento: grep e expressões regulares
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% O tamanho do palheiro
# Antes de procurar, meça. `wc -l` conta linhas. Ninguém lê 3 mil linhas:
# a gente filtra.
titulo "Quantas linhas temos?"
wc -l desafio/denuncias.txt desafio/log-suporte.txt
echo "---"
head -n 3 desafio/denuncias.txt

# %% Busca simples: grep -F
# `grep` imprime só as linhas que contêm o texto procurado.
#   -F  trata o texto como texto fixo (sem regex) — mais rápido e sem surpresas
# Aqui: quantas denúncias citam o domínio do golpe?
titulo "Linhas com 'pixvelox' (sensível a maiúsculas)"
grep -F pixvelox desafio/denuncias.txt | head -n 5
echo "Total: $(grep -cF pixvelox desafio/denuncias.txt)"     # -c conta em vez de mostrar

# %% Ignorando maiúsculas: -i
# Golpista escreve "PixVelox", "PIXVELOX", "pixvelox"... `-i` pega todos.
titulo "Agora ignorando maiúsculas"
echo "Sem -i: $(grep -cF pixvelox desafio/denuncias.txt)"
echo "Com -i: $(grep -ciF pixvelox desafio/denuncias.txt)"

# %% Onde está? Número da linha: -n
# `-n` mostra em qual linha está cada resultado. Ótimo para citar no relatório.
titulo "Denúncias com remetente do suporte, com número da linha"
grep -n "remetente: suporte@" desafio/denuncias.txt | head -n 5

# %% Classes de caracteres: '[0-9]'
# Entre colchetes você diz "qualquer um destes". [0-9] = qualquer dígito.
# Aqui: anotações que contêm algum número.
titulo "Anotações com dígitos"
grep '[0-9]' desafio/anotacoes/*.txt || dica "nenhuma linha com dígito nas anotações"
grep -c '[0-9]' desafio/log-suporte.txt

# %% Vários arquivos e pastas: *.txt e -r
# Com vários arquivos, o grep mostra o nome de cada um antes da linha.
#   *.txt      todos os .txt da pasta (o Bash expande)
#   -r         desce por todas as subpastas
#   -l         só o NOME dos arquivos que têm o termo
titulo "Quem fala de LGPD nas anotações?"
grep -n "LGPD" desafio/anotacoes/*.txt
echo "---"
grep -rl "subdomínio" desafio/

# %% Achando arquivos pelo nome: ls -R | grep
# grep também filtra a saída de OUTROS comandos (o "pipe" |).
titulo "Arquivos .txt em qualquer subpasta"
# shellcheck disable=SC2010  # ls | grep de propósito: é o exemplo do curso original
ls -R desafio | grep ".txt"

# %% Invertendo: -v
# `-v` mostra o que NÃO combina. Útil para tirar ruído.
# Aqui: ações do log que não são "abriu atendimento" nem "encerrou".
titulo "Ações relevantes do falso suporte"
grep -v "abriu atendimento" desafio/log-suporte.txt | grep -v "encerrou" | head -n 5

# %% Regex estendida: extraindo e-mails com -E -o
# `-E` liga as expressões regulares estendidas (+, {2,6}, | ...).
# `-o` imprime só o pedaço que combinou, não a linha inteira.
# Lendo o padrão de e-mail por partes:
#   [A-Za-z0-9._%+-]+   um ou mais caracteres válidos antes do @
#   @                   o arroba
#   [A-Za-z0-9.-]+      domínio (pode ter pontos e hífens)
#   \.[A-Za-z]{2,}     ponto + terminação de 2 ou mais letras
#
# Pegadinha: muita regex por aí usa {2,6}. Terminações novas têm mais de
# 6 letras (.example tem 7, .technology tem 10) e seriam CORTADAS.
# Veja a diferença no bloco seguinte.
titulo "E-mails extraídos do log (amostra)"
grep -Eo "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}" desafio/log-suporte.txt | head -n 5

# %% A pegadinha do {2,6}
# O mesmo e-mail com as duas regex. Com {2,6} o final some.
titulo "{2,6} corta terminações longas"
linha="contato: agente@cofre.exemplo.example"
echo "$linha" | grep -Eo "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}"
echo "$linha" | grep -Eo "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

# %% Contando e-mails únicos
# Encadeando: extrair -> ordenar -> remover repetidos -> contar.
# (sort e uniq aparecem com calma no Dia 10.)
titulo "Quantos e-mails diferentes existem em cada arquivo?"
for arq in desafio/denuncias.txt desafio/log-suporte.txt; do
  qtd="$(grep -Eo "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}" "$arq" | sort -u | wc -l)"
  echo "$arq: $qtd e-mails únicos"
done

# %% Só os domínios
# Uma regex diferente: tudo depois do @. Depois contamos quantos endereços
# há em cada domínio. Repare nos domínios parecidos com o do golpe.
titulo "Domínios no log do suporte"
grep -Eo "@[A-Za-z0-9.-]+\.[A-Za-z]{2,}" desafio/log-suporte.txt | sort | uniq -c | sort -rn
