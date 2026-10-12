#!/usr/bin/env bash
# =============================================================================
#  Dia 4 — Duzentas conversas: processamento em lote (find, xargs, laços)
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% Quanta coisa tem aqui?
# Antes de processar em lote, meça o lote. `find` lista arquivos em qualquer
# profundidade; `wc -l` conta as linhas da saída (= quantos arquivos).
titulo "Tamanho do lote"
ls desafio/conversas
echo "Arquivos .txt: $(find desafio/conversas -name '*.txt' -type f | wc -l)"
du -sh desafio/conversas          # espaço ocupado

# %% find: achando arquivos por critério
#   -name '*.txt'   nome bate com o padrão (use aspas!)
#   -type f         só arquivos (d = só pastas)
#   -newer / -mtime / -size   filtram por data e tamanho
titulo "find com critérios"
find desafio/conversas -name "*.txt" -type f | head -n 5
echo "..."
echo "--- só as conversas do dia 2026-03-05:"
find desafio/conversas -path '*2026-03-05*' -name '*.txt' | sort | head -n 3
echo "--- conversas com mais de 400 bytes:"
find desafio/conversas -type f -size +400c | wc -l

# %% Laço for sobre o resultado do find (o script original)
# O script original fazia:  for i in `find txt_files/. -name "*.txt"`; do echo "$i"; done
# Funciona, mas quebra se um nome tiver espaço. A forma segura é
# `find ... -print0 | while IFS= read -r -d '' arquivo` (separa por caractere nulo).
titulo "Imprimindo nomes com um laço"
find desafio/conversas/2026-03-01 -name "*.txt" -type f -print0 | sort -z |
  while IFS= read -r -d '' arquivo; do
    echo "$arquivo"
  done | head -n 5

# %% Laço com contador: quantas linhas tem cada conversa?
# Dentro do laço você pode fazer qualquer coisa com cada arquivo.
titulo "Linhas por conversa (amostra)"
for arquivo in desafio/conversas/2026-03-01/conversa-00{1..5}.txt; do
  printf '%-45s %s linhas\n' "$arquivo" "$(wc -l < "$arquivo")"
done

# %% Conversão em massa: .txt -> .csv
# O original trocava espaços por vírgulas com sed e salvava como .csv.
# Nossas conversas usam " | " como separador; trocamos por ";" (CSV brasileiro).
# "${arquivo%.txt}" remove o final ".txt" do nome — e acrescentamos ".csv".
# Trabalhamos numa CÓPIA (treino/) para não mexer na evidência.
titulo "Convertendo um dia inteiro para CSV"
mkdir -p treino
cp -r desafio/conversas/2026-03-01 treino/
for arquivo in treino/2026-03-01/*.txt; do
  sed 's/ | /;/g' "$arquivo" > "${arquivo%.txt}.csv"
done
ls treino/2026-03-01 | head -n 4
head -n 2 treino/2026-03-01/conversa-001.csv
rm -r treino

# %% xargs: transformando uma lista em argumentos
# `xargs` pega a lista que chega pela entrada e passa como argumentos para
# outro comando. É o "faça isso com cada um" mais rápido do Linux.
#   find ... | xargs wc -l        → wc recebe todos os arquivos de uma vez
#   -0  (com find -print0)       → aguenta nomes com espaço
titulo "find + xargs"
find desafio/conversas/2026-03-01 -name '*.txt' -print0 | xargs -0 wc -l | tail -n 1
echo "--- quem mais aparece como atendente em TODAS as conversas:"
find desafio/conversas -name '*.txt' -print0 | xargs -0 cut -d'|' -f2 | sort | uniq -c | sort -rn | head -n 6

# %% xargs com grep -l: QUAIS arquivos contêm uma palavra?
# grep -l imprime só o NOME dos arquivos que têm a palavra (não as linhas).
titulo "Arquivos que citam 'cashback'"
find desafio/conversas -name '*.txt' -print0 | xargs -0 grep -l 'cashback' | wc -l

# %% Apagando em lote (com cuidado!)
# O original apagava zips esquecidos:  find txt_files -name "*.zip" | xargs rm -f
# Antes de apagar, SEMPRE rode só o find para ver a lista.
titulo "Apagando arquivos temporários em lote"
mkdir -p treino
touch treino/a.zip treino/b.zip treino/manter.txt
echo "Vou apagar:"; find treino -name "*.zip" -type f
find treino -name "*.zip" -type f -print0 | xargs -0 rm -f
echo "Sobrou:"; ls treino
rm -r treino

# %% xargs -I: colocar cada item num lugar específico do comando
# Com -I NOME, o xargs troca NOME por cada linha da entrada.
# O original zipava os arquivos listados em file_names.txt um a um.
titulo "Zipando só as conversas selecionadas"
precisa zip
mkdir -p treino
xargs -I nomearq zip -q treino/selecionadas desafio/conversas/nomearq < desafio/selecionadas.txt
unzip -l treino/selecionadas.zip
rm -r treino

# %% xargs -P: em paralelo
# -P 4 roda até 4 processos ao mesmo tempo; -n 1 passa um arquivo por vez.
# Em milhares de arquivos (ou downloads), isso corta o tempo pela metade ou mais.
titulo "Contando palavras em paralelo"
find desafio/conversas -name '*.txt' -print0 | xargs -0 -n 20 -P 4 cat | wc -w

# %% find -exec: a alternativa ao xargs
# `-exec comando {} +` faz o mesmo que xargs, sem precisar de pipe.
# {} é o lugar do nome do arquivo; o + junta vários arquivos numa chamada.
titulo "find -exec"
find desafio/conversas -name 'conversa-00[1-3].txt' -exec wc -l {} +

# %% Pista: o operador apareceu?
# O nome do operador d'Os Vazantes é mare_alta. Será que ele escorregou?
titulo "Procurando o operador"
find desafio/conversas -name '*.txt' -print0 | xargs -0 grep -l 'mare_alta' | wc -l
dica "Alguns arquivos citam mare_alta. Ordene e leia o que ele mandou guardar."
