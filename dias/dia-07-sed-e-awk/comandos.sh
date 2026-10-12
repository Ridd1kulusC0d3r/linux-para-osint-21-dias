#!/usr/bin/env bash
# =============================================================================
#  Dia 7 — Seguindo o dinheiro: sed e awk
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% sed: substituir texto (s/velho/novo/)
# sed = "stream editor": lê o texto linha a linha e aplica uma edição.
# O arquivo original NÃO muda — o resultado sai na tela.
# s/Normal/SUSPEITO/ troca a PRIMEIRA ocorrência de cada linha.
titulo "sed s///"
head -n 4 desafio/relatorio.txt | sed 's/Normal/SUSPEITO/'

# %% Trocar todas as ocorrências: /g
# Sem o g, só a primeira de cada linha muda. Com g (global), todas.
# Aqui trocamos cada dígito por "#": [0-9] significa "qualquer dígito".
titulo "sed s///g"
sed 's/[0-9]/#/g' desafio/digitos.txt
echo "--- sem o g (só o primeiro dígito de cada linha):"
sed 's/[0-9]/#/' desafio/digitos.txt

# %% Imprimir linhas específicas: -n Np
# -n desliga a impressão automática; p imprime só o que você pediu.
titulo "sed -n: linha 7 e intervalo 5 a 9"
sed -n 7p desafio/relatorio.txt
echo "---"
sed -n 5,9p desafio/relatorio.txt

# %% Substituir só num intervalo de linhas
# '1,3 s/a/b/g' aplica a troca só nas linhas 1 a 3.
titulo "sed com intervalo"
sed '1,3 s/Normal/CONFERIDO/g' desafio/relatorio.txt | head -n 6

# %% Apagar linhas e editar uma cópia no lugar
#   sed '/padrão/d'  apaga as linhas que batem
#   sed -i           edita o ARQUIVO (use numa cópia!)
#   -e               várias edições em sequência
titulo "sed d e sed -i (numa cópia)"
sed '/^linha/d' desafio/relatorio.txt
mkdir -p treino
cp desafio/relatorio.txt treino/
sed -i -e 's/Normal/OK/g' -e '/^linha 1[0-4]/d' treino/relatorio.txt
tail -n 3 treino/relatorio.txt
rm -r treino

# %% Limpando dados sujos com sed
# Dados exportados vêm com lixo: espaços, marcadores, separadores estranhos.
# ^ = começo da linha, $ = fim, [[:space:]]* = qualquer quantidade de espaços.
titulo "Limpando contas.txt"
sed -e '/^#/d' -e 's/[[:space:]]*##fim$//' desafio/contas.txt | head -n 3

# %% awk: imprimir linhas ($0) e numerá-las (NR)
# awk lê linha a linha e divide cada uma em CAMPOS ($1, $2, ...).
# $0 é a linha inteira; NR é o número da linha.
titulo "awk \$0 e NR"
awk '{print $0}' desafio/vitimas.csv
echo "---"
awk '{print NR, $0}' desafio/vitimas.csv

# %% Escolhendo colunas: -F
# -F, diz que o separador de campos é a vírgula (CSV).
titulo "awk -F, colunas 1 e 3"
awk -F, '{print $1, $3}' desafio/vitimas.csv
echo "--- primeiras linhas do extrato (data, destino, valor):"
awk -F, 'NR <= 5 {print $1, $3, $4}' desafio/extrato.csv

# %% Filtrando linhas
#   /^v/        linhas que começam com "v"
#   $3 > 1000   linhas cujo 3º campo é maior que 1000
#   $5 == "ESTORNO"   comparação de texto
titulo "awk com filtros"
awk '/^v/' desafio/vitimas.csv
echo "--- prejuízo acima de R\$ 1.000:"
awk -F, 'NR > 1 && $3 > 1000 {print $1, $3}' desafio/vitimas.csv
echo "--- estornos no extrato:"
awk -F, '$5 == "ESTORNO"' desafio/extrato.csv | head -n 3

# %% Somando com awk
# Variáveis do awk começam em zero. O bloco END roda depois da última linha.
titulo "Somas"
awk -F, 'NR > 1 {total += $3} END {print "Prejuízo total:", total}' desafio/vitimas.csv
awk -F, 'NR > 1 && $5 == "PIX" {n++; total += $4} END {printf "PIX: %d transações, R$ %.2f\n", n, total}' desafio/extrato.csv

# %% Somando POR GRUPO: arrays associativos
# soma[$2] += $3 cria uma "gaveta" para cada valor do campo 2 e vai somando.
# É o "GROUP BY" do terminal.
titulo "Prejuízo por cidade"
awk -F, 'NR > 1 {soma[$2] += $3} END {for (c in soma) print soma[c], c}' desafio/vitimas.csv | sort -rn

# %% Contar não é somar
# Quantas vezes cada conta de destino aparece no extrato?
# (Compare depois com a SOMA dos valores — é o desafio de hoje.)
titulo "Quantas transferências por conta de destino"
awk -F, 'NR > 1 {n[$3]++} END {for (c in n) print n[c], c}' desafio/extrato.csv | sort -rn

# %% sed + awk juntos
# O pipe deixa cada ferramenta fazer o que faz melhor: sed limpa, awk calcula.
titulo "sed limpa, awk formata"
sed -e '/^#/d' -e 's/[[:space:]]*##fim$//' -e 's/~/ /g' desafio/contas.txt \
  | awk -F' ; *' '{printf "%-8s -> %s\n", $1, $2}'
dica "Agora some os valores do extrato por conta de destino. Quem recebeu mais?"
