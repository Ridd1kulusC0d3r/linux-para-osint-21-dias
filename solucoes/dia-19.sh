#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 19. Tente sozinho antes!
# Ideia: maré_alta commitou um config.env com a chave do painel e, 14 minutos
# depois, apagou o arquivo em outro commit. Apagar só muda o presente: o
# conteúdo continua no histórico. `git log -p` (ou `git show`) recupera.
cd "$(dirname "$0")/../dias/dia-19-git-e-github" || exit 1
tmp=$(mktemp -d)                                   # pasta temporária, some no final
trap 'rm -rf "$tmp"' EXIT

git clone -q desafio/vazantes.bundle "$tmp/pxv-site"
cd "$tmp/pxv-site" || exit 1

# 1. Qual commit apagou arquivos?
git log --diff-filter=D --name-only --format='%h %s'

# 2. O commit anterior a ele (^) ainda tinha o arquivo: mostramos o conteúdo
apagou=$(git log --diff-filter=D --format=%h -- config.env)
git show "${apagou}^:config.env" | grep -o 'VAZANTE{[^}]*}'
