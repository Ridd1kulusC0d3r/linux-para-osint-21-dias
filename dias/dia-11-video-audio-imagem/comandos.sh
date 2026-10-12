#!/usr/bin/env bash
# =============================================================================
#  Dia 11 — O vídeo do golpe: ffmpeg, OCR com tesseract, metadados e tradução
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
#  Pacotes: ffmpeg, tesseract-ocr, libimage-exiftool-perl
#  (opcionais: tesseract-ocr-por, translate-shell, pocketsphinx)
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% Instalando as ferramentas de mídia
# ffmpeg  = o "canivete suíço" de vídeo e áudio (converte, corta, extrai)
# ffprobe = vem junto com o ffmpeg; só INSPECIONA (não altera nada)
# tesseract = OCR: transforma texto de imagem em texto de verdade
# exiftool  = lê (e escreve) metadados de quase qualquer arquivo
titulo "Ferramentas"
precisa ffmpeg
precisa tesseract tesseract-ocr
precisa exiftool libimage-exiftool-perl
ffmpeg -version | head -n 1
tesseract --version 2>&1 | head -n 1
ls -lh desafio/

# %% Metadados do vídeo: ffprobe e exiftool
# Antes de assistir, PERGUNTE ao arquivo quem ele é: duração, resolução,
# codec, data de criação e campos de texto (título, autor, comentário).
#   -hide_banner         esconde o cabeçalho enorme do ffmpeg
#   -show_entries ...    escolhe só os campos que interessam
titulo "ffprobe"
precisa ffprobe ffmpeg
ffprobe -hide_banner desafio/video-golpe.mp4 2>&1 | grep -E 'Duration|Stream|title|artist|comment|creation_time'
echo "--- só a duração, em segundos:"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 desafio/video-golpe.mp4
titulo "exiftool"
precisa exiftool libimage-exiftool-perl
exiftool -Title -Artist -Comment -CreateDate -ImageSize -Duration desafio/video-golpe.mp4

# %% Quadro a quadro: extraindo imagens do vídeo
# Um vídeo é uma sequência de imagens. Com ffmpeg tiramos "prints" dele.
#   -i arquivo     entrada
#   -r 1           1 imagem por segundo de vídeo (comando do curso original)
#   -vf fps=1      jeito mais preciso de fazer o mesmo (sem quadros repetidos)
#   frame%d.png    %d vira 1, 2, 3...
titulo "Extraindo quadros"
precisa ffmpeg
mkdir -p treino
ffmpeg -loglevel error -i desafio/video-golpe.mp4 -r 1 treino/frame%d.png
ls treino
rm -r treino

# %% Um quadro específico
# -ss 2.5 pula para 2,5 s; -frames:v 1 tira UMA imagem. Útil para vídeo longo.
titulo "Só o quadro do segundo 2,5"
precisa ffmpeg
mkdir -p treino
ffmpeg -loglevel error -ss 2.5 -i desafio/video-golpe.mp4 -frames:v 1 treino/quadro.png
ls -l treino
rm -r treino

# %% Extraindo o áudio
#   -map a     pega só a(s) faixa(s) de áudio
#   -q:a 0     melhor qualidade possível no MP3
#   -vn        "no video" (outra forma de dizer: descarte a imagem)
titulo "Áudio do vídeo -> MP3"
precisa ffmpeg
mkdir -p treino
ffmpeg -loglevel error -i desafio/video-golpe.mp4 -q:a 0 -map a treino/audio.mp3
ls -l treino
rm -r treino

# %% Convertendo áudio para reconhecimento de fala
# Programas de transcrição costumam exigir WAV, 16 kHz, mono.
#   -ar 16000   taxa de amostragem 16 000 Hz
#   -ac 1       um canal (mono)
titulo "MP3 -> WAV 16 kHz mono"
precisa ffmpeg
mkdir -p treino
ffmpeg -loglevel error -i desafio/audio-golpe.mp3 -ar 16000 -ac 1 treino/audio_16000.wav
ffprobe -v error -show_entries stream=sample_rate,channels -of default=nw=1 treino/audio_16000.wav
rm -r treino

# %% Fala -> texto com pocketsphinx (opcional e pesado)
# O curso original usa o pocketsphinx (offline, modelo em inglês). Ele é
# pesado e erra bastante; o nosso áudio é só um bipe. Fica como referência:
titulo "pocketsphinx (só referência)"
mostrar "sudo apt install pocketsphinx pocketsphinx-en-us"
mostrar "pocketsphinx_continuous -infile audio_16000.wav 2> pocketsphinx.log > fala.txt"
dica "Versões novas trocaram o comando por: pocketsphinx single audio_16000.wav"
dica "Hoje o Whisper (Além do curso) transcreve português muito melhor."

# %% OCR: lendo o texto de uma imagem
# `tesseract imagem saida` grava saida.txt (ele acrescenta o .txt sozinho!).
# Use `-` como saída para imprimir direto na tela.
#   -l eng      idioma do modelo (eng vem por padrão)
#   -l por      português: precisa do pacote tesseract-ocr-por
titulo "OCR no print da conversa"
precisa tesseract tesseract-ocr
mkdir -p treino
tesseract desafio/print-suporte.png treino/print 2>/dev/null
cat treino/print.txt
rm -r treino

# %% OCR em português
# Para textos com acento, instale o modelo português e use -l por.
# Se não estiver instalado, o tesseract avisa e nós seguimos com o inglês.
titulo "Idiomas disponíveis no tesseract"
precisa tesseract tesseract-ocr
tesseract --list-langs 2>&1 | tail -n +2
if tesseract --list-langs 2>&1 | grep -qx por; then
  tesseract desafio/print-suporte.png - -l por 2>/dev/null | head -n 3
else
  dica "Sem o modelo 'por'. Instale com: sudo apt install tesseract-ocr-por"
fi

# %% Metadados do áudio e da imagem
# Áudio e imagem também carregam metadados: autor, software, data, GPS...
titulo "exiftool no áudio e na imagem"
precisa exiftool libimage-exiftool-perl
exiftool -Artist -Title -UserDefinedText -SampleRate -Duration desafio/audio-golpe.mp3
exiftool -FileType -ImageSize -Software desafio/print-suporte.png

# %% Traduzindo com translate-shell (online, opcional)
# `trans` usa serviços de tradução na internet.
#   trans :pt    traduz para português (detecta o idioma de origem)
#   trans :fr    para francês (como no curso original)
#   -b           saída "breve": só a tradução
titulo "Tradução do OCR"
precisa tesseract tesseract-ocr
mkdir -p treino
tesseract desafio/print-suporte.png treino/print 2>/dev/null
if online; then
  precisa trans translate-shell
  trans -b :pt < treino/print.txt || alerta "O serviço de tradução não respondeu."
else
  alerta "offline: pulando a tradução. Texto original do OCR:"
  head -n 2 treino/print.txt
fi
rm -r treino
