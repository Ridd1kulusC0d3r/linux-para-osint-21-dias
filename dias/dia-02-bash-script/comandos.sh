#!/usr/bin/env bash
# =============================================================================
#  Dia 2 — O script do Bento: variáveis, condições, laços e funções
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% Meu primeiro script
# Um script Bash é só um arquivo de texto com comandos, um por linha.
# A primeira linha (#!/usr/bin/env bash) é o "shebang": diz QUAL programa
# deve executar o arquivo. Aqui criamos um script numa pasta de treino,
# damos permissão de execução (chmod +x) e rodamos de duas formas.
titulo "Criando e rodando um script"
mkdir -p treino
# "cat > arquivo <<'FIM'" grava tudo até a linha FIM dentro do arquivo
cat > treino/ola.sh <<'FIM'
#!/usr/bin/env bash
echo "Olá, recruta. Hoje é $(date +%d/%m/%Y)."
FIM
bash treino/ola.sh          # forma 1: pedir ao bash que leia o arquivo
chmod +x treino/ola.sh      # dá permissão de execução (x = execute)
./treino/ola.sh             # forma 2: executar direto (usa o shebang)
rm -r treino                # limpa a pasta de treino

# %% Variáveis
# Variável guarda um valor para usar depois. Regras de ouro:
#   - SEM espaço ao redor do =   (nome="x" funciona; nome = "x" quebra)
#   - para LER o valor, use $nome — e quase sempre entre aspas: "$nome"
#   - $(comando) guarda a SAÍDA de um comando numa variável
titulo "Variáveis"
alvo="PixVelox"
dominio="pixvelox.example"
descricao="$alvo ($dominio)"          # juntando variáveis
hoje=$(date +%Y-%m-%d)                # saída de um comando
echo "Alvo: $descricao — anotado em $hoje"
echo "O nome do alvo tem ${#alvo} letras"      # ${#var} = tamanho
echo "Em maiúsculas: ${alvo^^}"                # ${var^^} = MAIÚSCULAS

# %% Contas com $(( ))
# O Bash faz contas com números inteiros dentro de $(( )).
titulo "Contas"
vitimas=412
prejuizo_medio=850
echo "Prejuízo estimado: R\$ $(( vitimas * prejuizo_medio ))"
echo "Vítimas por dia (30 dias): $(( vitimas / 30 ))  (resto $(( vitimas % 30 )))"

# %% Condição: if / else
# `if` testa algo e escolhe um caminho. Dentro de (( )) você compara números
# como na matemática (> < >= ==). Dentro de [ ] compara textos (= !=) ou usa
# -gt -lt -eq para números, e -f/-d para saber se arquivo/pasta existe.
# No script original o valor vinha de `read` (o usuário digita). Aqui
# simulamos a digitação com "<<<" para o script não ficar parado esperando.
titulo "if / else"
read -r valor <<< "1200"
if (( valor > 1000 )); then
  echo "R\$ $valor: prejuízo ALTO — prioridade na fila"
else
  echo "R\$ $valor: prejuízo baixo"
fi
if [ -f desafio/pistas.txt ]; then
  ok "desafio/pistas.txt existe"
fi
interativo read -r -p "Quantos anos você tem? " IDADE

# %% elif e case
# `elif` = "senão, se...". `case` compara um texto com vários padrões —
# fica mais limpo que um monte de elif.
titulo "elif e case"
link="https://pixvelox.example/cashback"
case "$link" in
  *pixvelox.example*) echo "Link do golpe!" ;;
  *gov.br*)           echo "Site do governo" ;;
  *)                  echo "Desconhecido" ;;
esac
nota=7
if (( nota >= 9 )); then echo "excelente"
elif (( nota >= 6 )); then echo "aprovado"
else echo "reprovado"
fi

# %% Laço for — repetir para cada item
# `for x in lista; do ...; done` executa o bloco uma vez para cada item.
# Um "array" (lista) é declarado com parênteses e lido com "${lista[@]}".
titulo "for com lista"
declare -a suspeitos=("lucas_suporte" "mare_alta" "atendente_pix" "bot_cashback")
for nome in "${suspeitos[@]}"; do
  echo "Verificando: $nome"
done
echo "Total de suspeitos: ${#suspeitos[@]}"

# %% for com sequência e com arquivos
# {1..5} gera 1 2 3 4 5. E "for arquivo in pasta/*" passa por cada arquivo.
titulo "for com sequência e arquivos"
for i in {1..3}; do
  echo "Rodada $i"
done
for arquivo in desafio/*; do
  echo "Arquivo: $arquivo ($(wc -l < "$arquivo") linhas)"
done

# %% Criando várias pastas com um laço
# O script original criava 3 pastas com 3 linhas de mkdir. Com um laço,
# 3 ou 300 pastas custam o mesmo esforço.
titulo "mkdir em laço"
mkdir -p treino
for pasta in primeira segunda terceira; do
  mkdir -p "treino/$pasta"
done
ls treino
rm -r treino

# %% Laço while — repetir ENQUANTO for verdade
# Muito usado para ler um arquivo linha por linha:
#   while read -r linha; do ...; done < arquivo
titulo "while contando e lendo arquivo"
x=1
while [ "$x" -le 5 ]; do
  echo "x = $x"
  x=$(( x + 1 ))
done
echo "--- lendo desafio/vitimas.txt linha por linha"
n=0
while read -r linha; do
  n=$(( n + 1 ))
  echo "$n: $linha"
done < desafio/vitimas.txt

# %% Laço until — repetir ATÉ ficar verdade
# É o contrário do while: roda enquanto a condição é FALSA.
titulo "until (contagem regressiva)"
x=15
until [ "$x" -lt 10 ]; do
  echo "$x"
  x=$(( x - 1 ))
done

# %% Funções — dar nome a um bloco de comandos
# Uma função é um "mini-script" dentro do script. Os argumentos chegam
# como $1, $2... e `local` cria variáveis que só existem dentro dela.
titulo "Funções"
saudar() {
  local nome="$1"
  echo "Bem-vindo ao Núcleo Coruja, $nome!"
}
contar_ate() {
  local i
  for (( i = 1; i <= $1; i++ )); do printf '%s ' "$i"; done
  echo
}
saudar "recruta"
contar_ate 5
contar_ate 3

# %% Função que roda todos os laços (como no original)
# Funções podem chamar outras e ser chamadas quantas vezes quiser.
titulo "Função que agrupa laços"
rodar_lacos() {
  for nome in Iara Bento Jurema; do echo "for: $nome"; done
  local y=1
  while [ "$y" -le 2 ]; do echo "while: $y"; y=$(( y + 1 )); done
  y=12
  until [ "$y" -lt 11 ]; do echo "until: $y"; y=$(( y - 1 )); done
}
rodar_lacos
rodar_lacos

# %% Lendo um arquivo com separador (IFS)
# IFS diz ao read qual caractere separa os campos. Com IFS=';' a linha
# "1;inverte;_o" vira três variáveis. É a base do desafio de hoje!
titulo "Campos separados por ;"
while IFS=';' read -r ordem metodo dado; do
  case "$ordem" in '#'*) continue ;; esac   # continue = pula para a próxima linha
  echo "ordem=$ordem  metodo=$metodo  dado=$dado"
done < desafio/pistas.txt | head -n 4

# %% Olhando o rascunho do Bento
# O decodificador do Bento roda, mas está incompleto: a parte "numeros"
# não foi feita e ele não sabe pular o ruído. Completar é o seu desafio.
titulo "O script incompleto do Bento"
precisa rev bsdextrautils   # o rascunho usa `rev` (inverte texto)
bash desafio/decodificador.sh desafio/pistas.txt | head -n 6
dica "Copie o script, complete os TODO e rode de novo (veja o README)."
