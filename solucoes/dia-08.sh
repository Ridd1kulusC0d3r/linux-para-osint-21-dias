#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 8. Tente sozinho antes!
# Ideia: no Vim seria  :4242  (ir para a linha) e  :%s/#MARE#/_/g  (desfazer a troca).
# Sem abrir a interface, o modo ex silencioso (-es) faz o mesmo numa cópia.
cd "$(dirname "$0")/../dias/dia-08-vim/desafio" || exit 1
tmp="$(mktemp)"
cp servidor-pixvelox.log "$tmp"                       # nunca mexa no original
vim -es -c '%s/#MARE#/_/g' -c 'wq' "$tmp"             # :%s///g e :wq
vim -es +4242p -cq "$tmp"                             # :4242 e imprime a linha
vim -es +4242p -cq "$tmp" | grep -o 'VAZANTE{[^}]*}'  # só a flag
rm -f "$tmp"
