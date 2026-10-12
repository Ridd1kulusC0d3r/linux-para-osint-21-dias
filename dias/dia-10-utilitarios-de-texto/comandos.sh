#!/usr/bin/env bash
# =============================================================================
#  Dia 10 — Dois grupos, um número: cat, cut, sort, uniq, wc, comm, diff, tr, paste
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
#  Todos estes programas fazem parte do "coreutils": já vêm em qualquer Linux.
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% Olhando as duas listas
# Duas exportações de grupos de "suporte" d'Os Vazantes. Repare: formatos
# diferentes! O grupo A é CSV com vírgula; o grupo B usa ponto e vírgula,
# outra ordem de colunas e apelidos em MAIÚSCULAS. Mundo real é assim.
titulo "As primeiras linhas de cada grupo"
head -n 4 desafio/grupo-a-cashback-vip.csv
echo "---"
head -n 4 desafio/grupo-b-suporte-pix.txt

# %% wc: medindo o tamanho
# `wc` (word count) conta linhas (-l), palavras (-w) e caracteres (-c / -m).
# Sem opção, mostra as três contagens.
titulo "Contando"
wc desafio/grupo-a-cashback-vip.csv
wc -l desafio/*.csv desafio/*.txt

# %% cat: concatenar (juntar) arquivos
# `cat` não serve só para ler: o nome vem de "concatenate".
#   cat a b > c        junta a e b num arquivo novo c
#   cat *.txt > d/x    junta todos os .txt dentro de outra pasta
titulo "Juntando arquivos"
mkdir -p treino/alltext
echo "Primeiro arquivo" > treino/file1.txt
echo "Segundo arquivo" > treino/file2.txt
cat treino/file1.txt treino/file2.txt > treino/file3.txt
cat treino/file3.txt
cat treino/*.txt > treino/alltext/file4.txt
wc -l treino/alltext/file4.txt
rm -r treino

# %% cut: recortando colunas e caracteres
#   cut -c 1        só o 1º caractere de cada linha
#   cut -c 5-10     do 5º ao 10º caractere
#   cut -d, -f1     separa por vírgula (-d = delimitador) e pega o campo 1 (-f)
#   cut -d';' -f2   o ; precisa de aspas, senão o Bash acha que é fim de comando
titulo "cut por caractere e por campo"
head -n 3 desafio/grupo-a-cashback-vip.csv | cut -c 1
head -n 3 desafio/grupo-a-cashback-vip.csv | cut -c 5-10
head -n 3 desafio/grupo-a-cashback-vip.csv | cut -d, -f1
head -n 3 desafio/grupo-b-suporte-pix.txt | cut -d';' -f2

# %% tail -n +2: pulando o cabeçalho
# A primeira linha de cada lista é o cabeçalho. `tail -n +2` começa da linha 2.
titulo "Sem cabeçalho"
tail -n +2 desafio/grupo-a-cashback-vip.csv | head -n 3

# %% sort: ordenando
#   sort       ordem alfabética        sort -r    ordem invertida
#   sort -n    numérica                sort -u    ordena e remove repetidos
#   sort -t, -k2   ordena pela coluna 2 usando vírgula como separador
titulo "Ordenando"
tail -n +2 desafio/grupo-a-cashback-vip.csv | sort | head -n 3
echo "--- invertido"
tail -n +2 desafio/grupo-a-cashback-vip.csv | sort -r | head -n 3
echo "--- pela coluna apelido"
tail -n +2 desafio/grupo-a-cashback-vip.csv | sort -t, -k2 | head -n 3

# %% uniq: repetidos
# `uniq` só remove repetidos que estão GRUDADOS (linhas vizinhas). Por isso
# quase sempre vem depois de `sort`.
#   uniq       remove duplicatas vizinhas
#   uniq -c    conta quantas vezes cada linha aparece
#   uniq -d    mostra só as que se repetem
titulo "Linhas duplicadas na exportação do grupo A"
tail -n +2 desafio/grupo-a-cashback-vip.csv | wc -l
tail -n +2 desafio/grupo-a-cashback-vip.csv | sort | uniq | wc -l
tail -n +2 desafio/grupo-a-cashback-vip.csv | sort | uniq -d

# %% O ranking: sort | uniq -c | sort -rn
# Combinação clássica de OSINT: "quem aparece mais?"
titulo "Telefones que mais se repetem no grupo A"
tail -n +2 desafio/grupo-a-cashback-vip.csv | cut -d, -f1 | sort | uniq -c | sort -rn | head -n 5

# %% tr: trocando caracteres
#   tr '[:upper:]' '[:lower:]'   maiúsculas -> minúsculas
#   tr ';' ','       troca um separador por outro
#   tr -d '() -'     apaga parênteses, hífens e espaços
titulo "Padronizando o grupo B"
tail -n +2 desafio/grupo-b-suporte-pix.txt | head -n 3 | tr '[:upper:]' '[:lower:]' | tr ';' ','
head -n 3 desafio/grupo-b-suporte-pix.txt | cut -d';' -f2 | tr -d '() -'

# %% comm: o que está em um, no outro ou nos dois
# `comm` compara DUAS listas JÁ ORDENADAS e imprime três colunas:
#   1ª só no arquivo 1 · 2ª só no arquivo 2 · 3ª nos dois
#   comm -12  esconde as colunas 1 e 2 -> sobra só o que é comum
#   comm -23  só o que está no 1º e não no 2º
titulo "Telefones de cada grupo, ordenados e sem repetição"
mkdir -p treino
tail -n +2 desafio/grupo-a-cashback-vip.csv | cut -d, -f1 | sort -u > treino/tel-a.txt
tail -n +2 desafio/grupo-b-suporte-pix.txt | cut -d';' -f2 | sort -u > treino/tel-b.txt
wc -l treino/tel-a.txt treino/tel-b.txt
echo "--- só no grupo A (primeiros 3):"
comm -23 treino/tel-a.txt treino/tel-b.txt | head -n 3
dica "Agora tente comm -12 você mesmo: é o desafio de hoje."
rm -r treino

# %% diff: o que mudou de ontem para hoje?
# `diff` mostra as diferenças linha a linha entre dois arquivos.
#   <  linha que só existe no 1º (saiu)      >  linha que só existe no 2º (entrou)
#   -u  formato "unificado" (o mesmo do Git): - saiu, + entrou
titulo "Quem entrou e quem saiu do grupo A"
diff desafio/grupo-a-ontem.csv desafio/grupo-a-cashback-vip.csv || true
echo "--- formato unificado"
diff -u desafio/grupo-a-ontem.csv desafio/grupo-a-cashback-vip.csv | grep '^[+-](' || true

# %% paste: colando arquivos lado a lado
# `paste` junta arquivos COLUNA a COLUNA (o cat junta linha embaixo de linha).
#   paste a b          separa por TAB
#   paste -d, a b      separa por vírgula
#   paste -sd+ arq     junta todas as linhas de um arquivo numa só, com +
titulo "Lado a lado"
mkdir -p treino
tail -n +2 desafio/grupo-b-suporte-pix.txt | head -n 3 | cut -d';' -f2 > treino/tel.txt
tail -n +2 desafio/grupo-b-suporte-pix.txt | head -n 3 | cut -d';' -f1 | tr '[:upper:]' '[:lower:]' > treino/apelido.txt
paste -d, treino/tel.txt treino/apelido.txt
conta="$(printf '3\n5\n8\n' | paste -sd+)"
echo "$conta = $((conta))"     # o Bash faz a conta com $(( ))
rm -r treino
