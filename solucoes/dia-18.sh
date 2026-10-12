#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 18. Tente sozinho antes!
# Ideia: os "donos" (owner) são laranjas diferentes, mas o contato técnico
# (tech-c), o e-mail dele e os servidores DNS são os mesmos em dois domínios.
# Só esses dois estão ligados. Os registros TXT "pxv-verif=NN-palavra" deles,
# ordenados pelo número, formam a flag. O terceiro domínio é isca.
cd "$(dirname "$0")/../dias/dia-18-investigacao-de-dominio/desafio" || exit 1

# 1. Qual tech-c aparece em mais de um whois?
tech=$(grep -h '^tech-c:' whois/*.txt | awk '{print $2}' | sort | uniq -d)
echo "tech-c repetido: $tech"

# 2. Domínios ligados a ele
ligados=$(grep -l "^tech-c: *$tech" whois/*.txt | xargs -n1 basename | sed 's/\.txt$//')
echo "domínios ligados: $(echo "$ligados" | paste -sd" ")"

# 3. TXT pxv-verif só desses domínios, em ordem numérica
miolo=$(for d in $ligados; do
          awk -F'\t' '$4 == "TXT" {print $5}' "dns/$d.txt"
        done | grep -o 'pxv-verif=[0-9]*-[a-z]*' | cut -d= -f2 | sort -n \
             | cut -d- -f2 | paste -sd_)
echo "VAZANTE{$miolo}"
