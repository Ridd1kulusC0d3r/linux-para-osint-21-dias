#!/usr/bin/env bash
# =============================================================================
#  Dia 1 — Arquivos, pastas e o que ninguém vê
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% Onde estou?
# Todo terminal tem um "diretório atual". `pwd` (print working directory)
# mostra qual é. É a primeira pergunta de quem acabou de chegar.
titulo "Onde estou?"
pwd

# %% O que tem aqui?
# `ls` lista o conteúdo da pasta atual.
#   -l  formato longo (permissões, dono, tamanho, data)
#   -h  tamanhos legíveis (K, M, G)
titulo "Conteúdo da pasta do Dia 1"
ls
ls -lh

# %% Entrando no pendrive da Mestra Iara
# `cd` muda de pasta. `cd ..` volta um nível. `cd -` volta para onde você estava.
# Caminhos podem ser relativos (desafio/caso) ou absolutos (/home/...).
titulo "Entrando em desafio/caso"
# Os parênteses criam um "subshell": o cd vale só lá dentro.
# Assim cada bloco começa sempre da pasta do Dia 1.
(
  cd desafio/caso || exit 1
  pwd
  ls
)

# %% Listando tudo, inclusive o que está escondido
# No Linux, arquivo cujo nome começa com ponto (.) é OCULTO.
# `ls` comum não mostra. `ls -a` mostra (all). `ls -la` mostra em detalhes.
# `ls -R` desce por todas as subpastas (recursivo).
titulo "Tudo, recursivamente, incluindo ocultos"
( cd desafio/caso && ls -laR )

# %% Achando arquivos ocultos com find
# `find` procura arquivos por critérios. Aqui: tudo cujo nome começa com ponto.
#   .            começa a busca na pasta atual
#   -type f      só arquivos (não pastas)
#   -name '.*'   nome começando com ponto
titulo "Arquivos ocultos no caso"
( cd desafio/caso && find . -type f -name '.*' )

# %% Lendo arquivos
# `cat` imprime o conteúdo inteiro. Para arquivos grandes, prefira
# `head` (começo), `tail` (fim) ou `less` (navegar, interativo).
titulo "Lendo o LEIA-ME e a lista de vítimas"
cat desafio/caso/LEIA-ME.txt
echo "---"
head -n 3 desafio/caso/vitimas/lista-preliminar.txt

# %% Montando a sua própria pasta de investigação
# Toda investigação séria começa organizada. `mkdir -p` cria a pasta e
# todas as "pais" que faltarem, sem reclamar se já existir.
# As chaves {a,b,c} são expansão do Bash: geram várias pastas de uma vez.
titulo "Criando a estrutura do meu caso"
mkdir -p meu-caso/{evidencias,notas,relatorio}
ls meu-caso

# %% Criando e acrescentando texto
# `>`  grava a saída de um comando num arquivo (SOBRESCREVE).
# `>>` acrescenta no final (NÃO apaga o que já existe).
# `touch` cria um arquivo vazio (ou atualiza a data de um que existe).
titulo "Diário de bordo"
mkdir -p meu-caso/notas
echo "Dia 1 — recebi o pendrive da Mestra Iara" > meu-caso/notas/diario.txt
echo "Dia 1 — aprendi que arquivo oculto começa com ponto" >> meu-caso/notas/diario.txt
touch meu-caso/notas/pistas.txt
cat meu-caso/notas/diario.txt
ls -l meu-caso/notas

# %% Copiando evidências (sem mexer no original!)
# Regra de ouro da investigação: NUNCA trabalhe no original. Copie.
#   cp arquivo destino       copia um arquivo
#   cp -r pasta destino      copia uma pasta inteira (recursivo)
#   cp -p                    preserva datas e permissões (importante p/ evidência)
titulo "Copiando a pasta de vítimas para o meu caso"
mkdir -p meu-caso/evidencias
cp -rp desafio/caso/vitimas meu-caso/evidencias/
ls -R meu-caso/evidencias

# %% Renomeando e movendo
# `mv` serve para as duas coisas: mover e renomear.
titulo "Renomeando um rascunho"
mkdir -p meu-caso/notas
touch meu-caso/notas/rascunho.txt
mv meu-caso/notas/rascunho.txt meu-caso/notas/hipoteses.txt
ls meu-caso/notas

# %% Metadados: quando esse arquivo foi mexido?
# `stat` mostra as datas de acesso, modificação e mudança de um arquivo.
# Em OSINT e forense, datas contam histórias.
titulo "Datas da nota escondida"
stat desafio/caso/vitimas/belo-horizonte/.nota_iara.txt

# %% Apagando com cuidado
# `rm` apaga SEM lixeira. Não existe "desfazer".
#   rm arquivo        apaga um arquivo
#   rm -r pasta       apaga uma pasta e tudo dentro
#   rm -i             pergunta antes de cada exclusão (use quando estiver em dúvida)
# Aqui apagamos só a pasta de treino que nós mesmos criamos.
titulo "Limpando a pasta de treino"
rm -r meu-caso
ls

# %% Pedindo ajuda ao próprio Linux
# Quase todo comando tem manual (`man ls`) ou ajuda rápida (`ls --help`).
# `man` é interativo (sai com q), então aqui usamos --help.
titulo "Ajuda rápida do ls"
ls --help | head -n 15
interativo man ls
