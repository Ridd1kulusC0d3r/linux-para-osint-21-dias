#!/usr/bin/env bash
# =============================================================================
#  Dia 12 — O contrato: texto, imagens e metadados de PDF
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
#  Pacotes: poppler-utils (pdftotext, pdfimages, pdfinfo, pdftoppm),
#           libimage-exiftool-perl, tesseract-ocr; opcional: ocrmypdf
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% Instalando o kit de PDF
# O pacote poppler-utils traz vários comandos pequenos, um para cada tarefa:
#   pdfinfo    informações e metadados       pdftotext   extrai o texto
#   pdfimages  extrai as imagens              pdftoppm    "fotografa" cada página
titulo "Ferramentas de PDF"
precisa pdftotext poppler-utils
precisa exiftool libimage-exiftool-perl
pdftotext -v 2>&1 | head -n 1
ls -lh desafio/

# %% Um PDF é texto? Espiando por dentro
# Abra um PDF com `head` e você verá que ele começa com %PDF-1.x e tem
# "objetos" numerados (1 0 obj ... endobj). `strings` mostra o que é legível.
# Às vezes os metadados aparecem até aqui, sem ferramenta nenhuma.
titulo "Os primeiros bytes e as strings do contrato"
precisa strings binutils
head -c 8 desafio/contrato-pixvelox.pdf; echo
strings desafio/contrato-pixvelox.pdf | grep -E '^<< /Type /(Catalog|Page) ' | head -n 3

# %% pdfinfo: a ficha do documento
# Título, autor, programa que criou, datas, número de páginas, tamanho.
titulo "pdfinfo"
precisa pdfinfo poppler-utils
pdfinfo desafio/contrato-pixvelox.pdf

# %% exiftool: metadados com lupa
# O exiftool lê os mesmos campos (e às vezes mais: XMP, histórico de edição).
# `grep ^Producer` filtra só a linha que COMEÇA com Producer (o ^ é "início").
titulo "exiftool"
precisa exiftool libimage-exiftool-perl
exiftool desafio/contrato-pixvelox.pdf
echo "---"
exiftool desafio/contrato-pixvelox.pdf | grep ^Producer

# %% pdftotext: o texto do contrato
#   pdftotext arquivo.pdf saida.txt   grava num arquivo
#   pdftotext arquivo.pdf -           imprime na tela
#   -layout                           tenta manter colunas e espaçamento
#   -f 2 -l 2                         só da página 2 até a 2
titulo "Texto completo"
precisa pdftotext poppler-utils
mkdir -p treino
pdftotext desafio/contrato-pixvelox.pdf treino/contrato.txt
cat treino/contrato.txt
echo "--- só a página 2, mantendo o layout:"
pdftotext -layout -f 2 -l 2 desafio/contrato-pixvelox.pdf - | head -n 8
rm -r treino

# %% pdfimages: as imagens embutidas
#   -list         só lista (página, tamanho, tipo)
#   -png          extrai convertendo para PNG
#   -all          extrai no formato original (JPEG continua JPEG)
#   prefixo       nome base dos arquivos gerados (prefixo-000.png ...)
titulo "Imagens dentro do contrato"
precisa pdfimages poppler-utils
pdfimages -list desafio/contrato-pixvelox.pdf
mkdir -p treino
pdfimages -png desafio/contrato-pixvelox.pdf treino/extracted_images
ls -l treino
rm -r treino

# %% PDF escaneado: quando não há texto
# O termo da vítima 031 é uma "digitalização": a página inteira é uma foto.
# pdftotext não acha nada (só uma quebra de página). Precisamos de OCR.
titulo "pdftotext num PDF escaneado"
precisa pdftotext poppler-utils
pdftotext desafio/termo-escaneado.pdf - | wc -c
dica "Quase zero caracteres: não existe camada de texto. Hora do OCR."

# %% OCR manual: pdftoppm + tesseract
# Sem instalar nada novo: "fotografamos" a página (pdftoppm) e lemos com o
# tesseract (Dia 11).
#   -r 150   resolução em DPI (mais DPI = OCR melhor, arquivo maior)
titulo "OCR página a página"
precisa pdftoppm poppler-utils
precisa tesseract tesseract-ocr
mkdir -p treino
pdftoppm -r 150 -png desafio/termo-escaneado.pdf treino/pagina
tesseract treino/pagina-1.png - 2>/dev/null
rm -r treino

# %% ocrmypdf: PDF pesquisável com uma linha
# O ocrmypdf faz o OCR e devolve um NOVO PDF com camada de texto invisível
# (aí o pdftotext e o Ctrl+F funcionam). O curso original instala via pip;
# no Ubuntu também existe o pacote apt "ocrmypdf" (depende de tesseract e
# ghostscript). Ele é pesado, então só instalamos quando há internet.
#   --force-ocr   refaz o OCR mesmo se a página já tiver texto (são DOIS hífens)
titulo "ocrmypdf (opcional)"
mkdir -p treino
if command -v ocrmypdf >/dev/null 2>&1 || { online && precisa ocrmypdf; }; then
  ocrmypdf -q desafio/termo-escaneado.pdf treino/result.pdf \
    || ocrmypdf -q --force-ocr desafio/termo-escaneado.pdf treino/result.pdf
  pdftotext treino/result.pdf - | head -n 5
else
  alerta "offline e sem ocrmypdf: veja o OCR manual da seção anterior."
  mostrar "ocrmypdf desafio/termo-escaneado.pdf result.pdf"
  mostrar "ocrmypdf --force-ocr desafio/termo-escaneado.pdf result.pdf"
fi
rm -r treino

# %% Metadados em lote
# Com vários PDFs, o exiftool monta uma tabela de uma vez:
#   -T              saída em colunas separadas por TAB
#   -csv            saída CSV (ótimo para planilha)
titulo "Autor e programa de todos os PDFs da pasta"
precisa exiftool libimage-exiftool-perl
exiftool -T -FileName -Author -Producer -CreateDate desafio/*.pdf
