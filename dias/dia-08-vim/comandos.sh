#!/usr/bin/env bash
# =============================================================================
#  Dia 8 — A linha 4242: o editor Vim (e como usá-lo sem ficar preso nele)
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
#  O Vim é INTERATIVO: aqui mostramos o comando e rodamos o equivalente
#  não interativo (vim -es / ex / sed). Para treinar de verdade, use um
#  terminal (Codespaces, VM ou o seu Linux) ou exporte L4O_INTERATIVO=1.
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% Instalando e conferindo o Vim
# O Vim quase sempre já vem instalado (às vezes numa versão "mínima", vim-tiny).
# `precisa vim` instala o pacote completo se o comando não existir.
# `vim --version | head -n 1` mostra a versão sem abrir o editor.
titulo "Vim instalado?"
precisa vim
vim --version | head -n 1

# %% Abrindo um arquivo (modo interativo)
# `vim arquivo` abre o editor. Ele começa no MODO NORMAL: as teclas viram
# comandos, não texto. Os modos que você precisa hoje:
#   NORMAL   (Esc)  navegar e dar comandos (dd, yy, p, /busca)
#   INSERÇÃO (i)    digitar texto como num bloco de notas
#   COMANDO  (:)    linha no rodapé: :w salva, :q sai, :wq salva e sai, :q! sai SEM salvar
# Num script ou no Colab o Vim "prende" a célula — por isso usamos `interativo`.
titulo "Abrindo o log no Vim"
interativo vim desafio/servidor-pixvelox.log
dica "Dentro do Vim: Esc e depois :q! para sair sem salvar. Respire. Funciona sempre."

# %% Quantas linhas tem esse log?
# Antes de mergulhar, meça o tamanho do problema. `wc -l` conta linhas.
# Dentro do Vim, Ctrl+G mostra a mesma informação no rodapé.
titulo "Tamanho do log"
wc -l desafio/servidor-pixvelox.log
cat desafio/bilhete-iara.txt

# %% Pulando direto para uma linha: :N
# No Vim, digite :4242 e Enter (ou 4242G no modo normal). Para abrir o
# arquivo JÁ na linha:  vim +4242 arquivo
# Sem interface, o Vim tem o "modo ex silencioso" (-es): roda comandos de
# dois pontos e sai. `+4242p` = vá para a linha 4242 e imprima (p = print).
# `-cq` = execute o comando :q no fim. `ex` é o mesmo editor, só com outro nome.
titulo "Linha 4242 — três jeitos"
interativo vim +4242 desafio/servidor-pixvelox.log
vim -es +4242p -cq desafio/servidor-pixvelox.log
ex -s +'4242p' +'q!' desafio/servidor-pixvelox.log
sed -n '4242p' desafio/servidor-pixvelox.log      # o mesmo com sed (Dia 7)

# %% Buscando com /
# No modo normal, /texto procura para frente; n vai para a próxima ocorrência,
# N volta. ?texto procura para trás. `:set hlsearch` destaca os resultados.
# Equivalente não interativo: o comando :g/padrão/# lista as linhas que batem,
# com o número na frente (igual a `grep -n`).
titulo "Todas as linhas com mare_alta (só as 5 primeiras)"
interativo vim +/mare_alta desafio/servidor-pixvelox.log
vim -es -c 'g/mare_alta/#' -c 'q!' desafio/servidor-pixvelox.log | head -n 5
dica "São mais de 20 rascunhos. Quase todos são isca — confie no bilhete."

# %% Substituir em todo o arquivo: :%s/velho/novo/g
#   %   em todas as linhas
#   s   substituir (substitute)
#   g   todas as ocorrências da linha, não só a primeira
# O maré_alta trocou '_' por '#MARE#'. Vamos desfazer NUMA CÓPIA (nunca no
# original!) e salvar com :wq. O '#' não é especial no Vim, então vai direto.
titulo "Desfazendo a troca numa cópia"
mkdir -p treino
cp desafio/servidor-pixvelox.log treino/copia.log
interativo vim treino/copia.log
mostrar ":%s/#MARE#/_/g   e depois   :wq"
vim -es -c '%s/#MARE#/_/g' -c 'wq' treino/copia.log
vim -es +4242p -cq treino/copia.log
rm -r treino

# %% Apagar, copiar e colar: dd, yy, p
#   dd   apaga (recorta) a linha do cursor       3dd apaga 3 linhas
#   yy   copia (yank) a linha do cursor          5yy copia 5 linhas
#   p    cola abaixo do cursor                   P cola acima
#   u    desfaz (undo)                           Ctrl+R refaz
# Com `:normal` dá para mandar essas teclas pelo modo ex, sem interface.
titulo "dd, yy e p num arquivo de treino"
mkdir -p treino
cp desafio/treino-vim.txt treino/
interativo vim treino/treino-vim.txt
# 1G = vai para a linha 1; yy = copia; G = vai para o fim; p = cola
vim -es -c 'normal 1GyyGp' -c 'wq' treino/treino-vim.txt
# 2G = vai para a linha 2; dd = apaga
vim -es -c 'normal 2Gdd' -c 'wq' treino/treino-vim.txt
# e a substituição do próprio arquivo de treino
vim -es -c '%s/PixVeloz/PixVelox/g' -c 'wq' treino/treino-vim.txt
cat treino/treino-vim.txt
rm -r treino

# %% Salvar e sair: o resumo que salva vidas
# :w        salva                 :w novo.txt   salva com outro nome
# :q        sai (se não mudou nada)
# :wq ou :x salva e sai           ZZ (modo normal) faz o mesmo
# :q!       sai DESCARTANDO tudo — o seu botão de pânico
# Se o Vim travar com "swap file", alguém (talvez você) deixou o arquivo aberto:
# o Vim criou um .swp. Escolha (R)ecover ou (D)elete e siga em frente.
titulo "Guia de sobrevivência"
printf '%-12s %s\n' "Esc" "volta para o modo normal (aperte duas vezes na dúvida)" \
  ":q!" "sai sem salvar" ":wq" "salva e sai" "i" "começa a digitar" \
  "/texto" "busca" ":4242" "vai para a linha 4242" "u" "desfaz"

# %% vimtutor: 30 minutos que valem o curso
# O próprio Vim traz um tutorial interativo, em português se o seu sistema
# estiver em pt_BR. Faça pelo menos as lições 1 e 2.
titulo "Tutorial oficial"
interativo vimtutor
interativo vimtutor pt
