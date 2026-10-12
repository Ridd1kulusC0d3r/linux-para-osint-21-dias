#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 11. Tente sozinho antes!
# Ideia:
#   1. O comentário nos metadados ("nao postar o quadro 4") diz onde olhar.
#   2. Extrair 1 quadro por segundo do vídeo com ffmpeg.
#   3. Passar OCR (tesseract) em cada quadro e procurar VAZANTE{...}.
cd "$(dirname "$0")/../dias/dia-11-video-audio-imagem/desafio" || exit 1
tmp="$(mktemp -d)"

exiftool -Comment video-golpe.mp4                                 # a pista
ffmpeg -loglevel error -i video-golpe.mp4 -vf fps=1 "$tmp/quadro%d.png"
for q in "$tmp"/quadro*.png; do
  tesseract "$q" - 2>/dev/null
done | grep -o 'VAZANTE{[^}]*}' | head -n 1

rm -rf "$tmp"
