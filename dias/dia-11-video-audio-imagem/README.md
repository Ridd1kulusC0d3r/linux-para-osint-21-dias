# Dia 11 — O vídeo do golpe 🎞️

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-11.ipynb)
&nbsp;**Rank C** · ⏱️ ~60 min · 📖 Original: *Day 11. Video, audio and images* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> A vítima 014 encaminhou o vídeo que a convenceu: cinco segundos de
> propaganda da PixVelox, verde e otimista, "o Pix que devolve". Você assiste
> três vezes. Na terceira, jura ter visto alguma coisa piscar no meio.
>
> Bento nem olha:
> — Olho humano vê 24 quadros por segundo e não lembra de nenhum. O `ffmpeg`
> lembra de todos.
>
> A vítima mandou também um print da conversa com o "suporte" e um áudio.
> Mestra Iara, de passagem: — Antes de assistir, pergunte ao arquivo quem o fez.

**Sua tarefa:** ler os metadados de `desafio/video-golpe.mp4`, extrair os
quadros do vídeo e usar OCR para ler o código que aparece por um instante —
é a flag `VAZANTE{...}`.

## 🎯 Ao final de hoje você sabe

- [ ] Inspecionar vídeo e áudio com `ffprobe` e `exiftool`
- [ ] Extrair quadros de um vídeo (`ffmpeg -r 1`, `-vf fps=1`, `-ss`)
- [ ] Extrair o áudio e convertê-lo para WAV 16 kHz mono
- [ ] Transformar imagem em texto com OCR (`tesseract`, inclusive em português)
- [ ] Saber onde entram transcrição de fala (pocketsphinx, Whisper) e tradução (`trans`)

## 📖 Conceito em 2 minutos

Um arquivo de mídia é uma **caixa com várias coisas dentro**:

```text
video-golpe.mp4
├── metadados   título, autor, comentário, data de criação, software
├── faixa de vídeo  ── quadro 1, quadro 2, quadro 3 ... (imagens)
└── faixa de áudio  ── ondas sonoras (voz, música, bipe)
```

Para o investigador, cada parte é uma fonte:

- **metadados** → quem fez, quando, com que programa (`ffprobe`, `exiftool`);
- **quadros** → imagens que podem conter texto, rostos, placas, telas (`ffmpeg` + OCR);
- **áudio** → fala que pode ser transcrita e traduzida.

**OCR** (*Optical Character Recognition*) é o processo de "ler" letras numa
imagem. O `tesseract` é o OCR livre mais usado do mundo; ele funciona melhor
com texto nítido, grande e alto contraste.

## ⌨️ Mão na massa

O arquivo [`comandos.sh`](comandos.sh) tem tudo comentado; rode inteiro com
`bash comandos.sh`.

### 1. Instalar

```bash
sudo apt install ffmpeg tesseract-ocr libimage-exiftool-perl
sudo apt install tesseract-ocr-por      # opcional: OCR em português
```

### 2. Perguntar ao arquivo quem ele é

```bash
ffprobe -hide_banner desafio/video-golpe.mp4          # duração, codecs, metadados
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 desafio/video-golpe.mp4
exiftool desafio/video-golpe.mp4                      # tudo o que o exiftool reconhece
exiftool -Title -Artist -Comment desafio/video-golpe.mp4
```

### 3. Quadro a quadro

```bash
ffmpeg -i desafio/video-golpe.mp4 -r 1 frame%d.png          # 1 imagem por segundo (curso original)
ffmpeg -i desafio/video-golpe.mp4 -vf fps=1 quadro%d.png    # idem, sem quadros duplicados
ffmpeg -ss 2.5 -i desafio/video-golpe.mp4 -frames:v 1 um.png   # só o instante 2,5 s
```

### 4. Áudio

```bash
ffmpeg -i desafio/video-golpe.mp4 -q:a 0 -map a audio.mp3     # extrai o áudio
ffmpeg -i desafio/audio-golpe.mp3 -ar 16000 -ac 1 audio_16000.wav   # 16 kHz, mono
# transcrição offline do curso original (pesado, só inglês, opcional):
sudo apt install pocketsphinx pocketsphinx-en-us
pocketsphinx_continuous -infile audio_16000.wav 2> log.txt > fala.txt
```

### 5. OCR

```bash
tesseract desafio/print-suporte.png saida     # cria saida.txt (o .txt é automático)
tesseract desafio/print-suporte.png -         # imprime na tela
tesseract imagem.png - -l por                 # português (precisa do tesseract-ocr-por)
for q in quadro*.png; do tesseract "$q" - 2>/dev/null; done   # OCR em todos os quadros
```

### 6. Traduzir (online, opcional)

```bash
sudo apt install translate-shell
trans -b :pt < saida.txt     # para português
trans :fr < saida.txt        # para francês, como no original
```

## 🇧🇷 Versão brazuca

Golpes brasileiros circulam como **vídeo curto com texto na tela** (Reels,
Shorts, Kwai, status de WhatsApp). Com o modelo português do tesseract, o
mesmo método vira uma triagem: extraia um quadro por segundo e procure
palavras-chave típicas do golpe.

```bash
sudo apt install tesseract-ocr-por
ffmpeg -loglevel error -i video-suspeito.mp4 -vf fps=1 q%03d.png
for q in q*.png; do
  echo "== $q"; tesseract "$q" - -l por 2>/dev/null
done | grep -iE '==|pix|cashback|chave|resgate|código|whatsapp'
```

Para conferir se um banco citado no vídeo existe de verdade, consulte a lista
de instituições autorizadas no **Banco Central** (<https://www.bcb.gov.br/estabilidadefinanceira/encontreinstituicao>)
ou a **BrasilAPI**: `curl -s https://brasilapi.com.br/api/banks/v1 | jq '.[] | .name' | head`.

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) lê os metadados **abrindo os bytes** do
MP4, do MP3 e do PNG (sem bibliotecas!), cria um WAV 16 kHz com o módulo
`wave` e, se `ffmpeg` e `tesseract` existirem, chama os dois com `subprocess`.

| Terminal | Python (stdlib) |
|---|---|
| `exiftool video.mp4` | `struct` percorrendo as caixas (atoms) do MP4 |
| `exiftool audio.mp3` | ler a etiqueta ID3v2 do começo do arquivo |
| `exiftool -ImageSize img.png` | `struct.unpack(">II", dados[16:24])` |
| `ffmpeg -ar 16000 -ac 1 x.wav` | `wave.open(..., "wb")` com `setframerate(16000)` |
| `ffmpeg` / `tesseract` | `subprocess.run([...])` |

## 🚀 Além do curso

- **Whisper** (`pip install openai-whisper`, ou o mais rápido
  `pip install faster-whisper`): transcrição de fala local, offline, que
  entende português muito bem. `whisper audio.mp3 --language pt --model small`.
  Funciona bem no Colab com GPU.
- **pytesseract** (`pip install pytesseract`): chama o tesseract de dentro do
  Python em uma linha — `pytesseract.image_to_string(Image.open("q4.png"), lang="por")`.
- **yt-dlp** (`pip install yt-dlp`): baixa vídeos de centenas de sites para
  análise local (com `--write-info-json` guarda também os metadados da
  plataforma). Respeite os termos de uso de cada site.

## 🧩 Desafio

1. Leia os metadados do vídeo: há um comentário revelador.
2. Extraia os quadros, um por segundo.
3. Passe OCR em cada quadro.
4. Confira: `bash checar.sh 'VAZANTE{...}'`

<details>
<summary>💡 Dica 1</summary>

`exiftool -Comment desafio/video-golpe.mp4` diz qual quadro olhar.
</details>

<details>
<summary>💡 Dica 2</summary>

`ffmpeg -i desafio/video-golpe.mp4 -vf fps=1 q%d.png` e depois
`tesseract q4.png -`.
</details>

A solução comentada está em [`solucoes/dia-11.sh`](../../solucoes/dia-11.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- **Metadados funcionam nos dois sentidos.** Antes de publicar qualquer
  imagem ou vídeo do seu relatório, limpe os seus: `exiftool -all= arquivo`
  (ele guarda uma cópia `_original`).
- Vídeos e áudios de vítimas podem conter **voz e rosto**, que são dados
  pessoais (e a biometria é dado sensível, LGPD art. 5º, II). Use só o
  necessário e borre o que não for relevante.
- OCR e transcrição **erram**. Sempre confira o trecho importante olhando a
  imagem ou ouvindo o áudio original antes de pôr num relatório.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 10](../dia-10-utilitarios-de-texto/) · [Índice](../../README.md) · [Dia 12](../dia-12-pdf/) ➡️
