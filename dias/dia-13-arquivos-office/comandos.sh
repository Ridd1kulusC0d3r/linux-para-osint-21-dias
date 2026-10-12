#!/usr/bin/env bash
# =============================================================================
#  Dia 13 — A planilha esquecida: arquivos Office por dentro
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
#  Pacotes: unzip, libimage-exiftool-perl, pandoc, libreoffice-nogui
#  (o LibreOffice é grande: ~300 MB. Ele só é instalado nas seções que o usam.)
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% O truque do dia: .docx e .xlsx são ZIP
# Desde 2007, os formatos do Office (docx, xlsx, pptx) e do LibreOffice (odt,
# ods) são arquivos ZIP com XML dentro. O comando `file` confirma, e o
# `unzip -l` lista o conteúdo SEM extrair nada.
titulo "O que é um .xlsx de verdade?"
precisa unzip
file desafio/planilha-contas.xlsx desafio/roteiro-atendimento.docx
echo "---"
unzip -l desafio/planilha-contas.xlsx

# %% Metadados: quem escreveu e quem mexeu por último
# Em docProps/core.xml ficam o autor (dc:creator), quem salvou por último
# (cp:lastModifiedBy) e as datas. `unzip -p` imprime um arquivo de dentro do
# zip na tela, sem extrair para o disco.
titulo "docProps/core.xml do roteiro"
precisa unzip
unzip -p desafio/roteiro-atendimento.docx docProps/core.xml | grep -o '<dc:creator>[^<]*\|<cp:lastModifiedBy>[^<]*\|<dcterms:[a-z]*[^>]*>[^<]*' | sed 's/<[^>]*>/ /g'
titulo "O mesmo com exiftool"
precisa exiftool libimage-exiftool-perl
exiftool -Creator -LastModifiedBy -CreateDate -ModifyDate -Application -Company desafio/roteiro-atendimento.docx

# %% Comentários de revisão: word/comments.xml
# Quem revisa um documento no Word deixa comentários na margem. Mesmo
# "escondidos" na visualização, eles continuam dentro do arquivo.
titulo "Comentários escondidos no roteiro"
precisa unzip
unzip -l desafio/roteiro-atendimento.docx | grep -i comment
unzip -p desafio/roteiro-atendimento.docx word/comments.xml | sed 's/<w:comment /\n&/g; s/<[^>]*>//g'
echo

# %% Abas da planilha: visíveis e ocultas
# A lista de abas fica em xl/workbook.xml. Uma aba escondida no Excel tem
# state="hidden" (ou "veryHidden", que nem aparece no menu "Reexibir").
titulo "Abas da planilha"
precisa unzip
unzip -p desafio/planilha-contas.xlsx xl/workbook.xml | grep -o '<sheet [^>]*>'
dica "Tem aba com state=\"hidden\"? O conteúdo dela está em xl/worksheets/sheetN.xml."

# %% Lendo o XML de uma aba
# Cada aba é um XML com linhas (<row>) e células (<c>). Tirando as tags com
# sed, sobra o texto. Aqui olhamos a aba VISÍVEL (sheet1.xml).
titulo "Aba 1 (visível), sem as tags"
precisa unzip
unzip -p desafio/planilha-contas.xlsx xl/worksheets/sheet1.xml | sed 's/<row/\n&/g' | sed 's/<[^>]*>/ /g; s/  */ /g'
echo

# %% Extraindo tudo para olhar com calma
# `unzip -d pasta` extrai para uma pasta. `find` (Dia 1) mostra a árvore.
titulo "Extraindo o docx"
precisa unzip
mkdir -p treino
unzip -q -o desafio/roteiro-atendimento.docx -d treino/roteiro
find treino/roteiro -type f | sort
rm -r treino

# %% LibreOffice sem janela: convertendo documentos
# `libreoffice --headless` roda sem interface gráfica — perfeito para scripts.
#   --convert-to txt      documento -> texto
#   --convert-to csv      planilha  -> CSV (SÓ a primeira aba!)
#   --outdir pasta        onde salvar
# `libreoffice -h` mostra todas as opções.
titulo "docx -> txt e xlsx -> csv"
precisa libreoffice libreoffice-nogui
libreoffice -h 2>/dev/null | head -n 5
mkdir -p treino
libreoffice --headless --convert-to 'txt:Text (encoded):UTF8' --outdir treino desafio/roteiro-atendimento.docx >/dev/null 2>&1
libreoffice --headless --convert-to csv --outdir treino desafio/planilha-contas.xlsx >/dev/null 2>&1
ls treino
cat treino/roteiro-atendimento.txt
cat treino/planilha-contas.csv
rm -r treino

# %% Todas as abas de uma vez (LibreOffice 7.2 ou mais novo)
# O filtro de CSV aceita opções; a última (-1) significa "exporte TODAS as abas",
# cada uma num arquivo <nome>-<aba>.csv. Abas ocultas também saem!
titulo "Uma aba por arquivo CSV"
precisa libreoffice libreoffice-nogui
mkdir -p treino
libreoffice --headless \
  --convert-to 'csv:Text - txt - csv (StarCalc):44,34,76,1,,0,false,true,false,false,false,-1' \
  --outdir treino desafio/planilha-contas.xlsx >/dev/null 2>&1
ls treino
dica "Abra cada CSV com cat. Algum nome de aba chamou a sua atenção?"
rm -r treino

# %% pandoc: o conversor universal de documentos
# pandoc converte entre dezenas de formatos (md, html, docx, odt, txt, epub...).
#   echo "texto" | pandoc -o result.docx     cria um docx a partir de texto
#   pandoc -f html -t docx pagina.html -o x.docx   página web -> Word
#   pandoc arquivo.docx -t plain             Word -> texto puro
#   --track-changes=all                      inclui comentários e revisões
titulo "pandoc"
precisa pandoc
mkdir -p treino
echo "Relatório preliminar — Operação Vazante" | pandoc -o treino/result.docx
pandoc -f html -t docx desafio/pagina-salva.html -o treino/website.docx
ls -l treino
pandoc desafio/pagina-salva.html -t plain
echo "--- roteiro, com comentários:"
pandoc --track-changes=all desafio/roteiro-atendimento.docx -t plain
rm -r treino

# %% pandoc direto de um site (online)
# O curso original converte uma página da web para docx direto da URL.
titulo "Página web -> docx"
precisa pandoc
mkdir -p treino
if online; then
  pandoc -f html -t docx https://example.com -o treino/website.docx \
    && pandoc treino/website.docx -t plain | head -n 5
else
  alerta "offline: usando cópia salva"
  pandoc -f html -t docx desafio/pagina-salva.html -o treino/website.docx
  pandoc treino/website.docx -t plain | head -n 3
fi
rm -r treino
