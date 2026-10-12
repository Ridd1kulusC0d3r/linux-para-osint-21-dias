#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 17. Tente sozinho antes!
# Ideia: o .torrent não traz o kit, mas descreve tudo. O comentário de
# mare_alta manda "ler config/ na ordem dos números, pular o 00". Os nomes
# dos arquivos config/01_..., 02_..., 03_..., 04_... formam a flag.
# (Sem transmission-show? `python3 dias/dia-17-*/equivalente.py` decodifica o bencode.)
cd "$(dirname "$0")/../dias/dia-17-compartilhamento-de-arquivos/desafio" || exit 1

# 1. O comentário dá a regra
transmission-show kit_golpe_pixvelox.torrent | grep 'Comment:'

# 2. Lista de arquivos -> só config/NN_palavra.cfg, sem o 00, em ordem
miolo=$(transmission-show -f kit_golpe_pixvelox.torrent \
  | grep -o 'config/[0-9][0-9]_[a-z]*\.cfg' \
  | grep -v '/00_' | sort \
  | sed 's|config/[0-9]*_||; s|\.cfg$||' \
  | paste -sd_)
echo "VAZANTE{$miolo}"
