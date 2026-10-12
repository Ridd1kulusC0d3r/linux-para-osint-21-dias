# Dia 13 — A planilha esquecida 📊

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-13.ipynb)
&nbsp;**Rank C** · ⏱️ ~45 min · 📖 Original: *Day 13. MS Office files* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> Um ex-"atendente" da PixVelox resolveu colaborar. Arrependido, entregou dois
> arquivos que circulavam no grupo interno: o **roteiro de atendimento** que
> os golpistas seguem, em Word, e uma **planilha de contas** de passagem, em
> Excel.
>
> Você abre a planilha: uma aba só, quatro contas laranja. Nada de novo.
>
> Mestra Iara aparece com o café:
> — Recruta, você sabe o que é um `.xlsx`?
> — Uma planilha?
> — É um **zip**. Abra o zip.

**Sua tarefa:** descobrir o que o roteiro esconde além do texto, achar a
parte da planilha que o Excel não mostra e montar a flag `VAZANTE{...}`.

## 🎯 Ao final de hoje você sabe

- [ ] Explicar por que `.docx`, `.xlsx` e `.pptx` são arquivos **ZIP com XML**
- [ ] Listar e ler partes internas com `unzip -l` e `unzip -p`
- [ ] Achar autor, último editor e datas em `docProps/core.xml` (e com `exiftool`)
- [ ] Encontrar **comentários de revisão** e **abas ocultas**
- [ ] Converter documentos sem interface: `libreoffice --headless --convert-to`
- [ ] Converter entre formatos com `pandoc`

## 📖 Conceito em 2 minutos

Desde 2007, os documentos do Office seguem o padrão **Office Open XML**: o
arquivo é um ZIP, e cada parte do documento é um XML lá dentro.

```text
planilha-contas.xlsx  (= um .zip)
├── [Content_Types].xml        o "índice" de tipos
├── docProps/
│   ├── core.xml               autor, último a salvar, datas  ◄── OSINT
│   └── app.xml                programa, empresa
└── xl/
    ├── workbook.xml           lista de abas (e se estão ocultas!)  ◄── OSINT
    └── worksheets/
        ├── sheet1.xml         aba 1
        └── sheet2.xml         aba 2

roteiro-atendimento.docx
└── word/
    ├── document.xml           o texto
    └── comments.xml           comentários de revisão  ◄── OSINT
```

O Word e o Excel **escolhem** o que mostrar. Uma aba oculta, um comentário
resolvido, o nome de quem salvou por último: tudo continua no arquivo. Os
formatos do LibreOffice (`.odt`, `.ods`) seguem a mesma ideia — também são
ZIPs, com `meta.xml` e `content.xml`.

## ⌨️ Mão na massa

O arquivo [`comandos.sh`](comandos.sh) tem tudo comentado; rode inteiro com
`bash comandos.sh`.

### 1. Abrindo o zip

```bash
file desafio/planilha-contas.xlsx           # "Microsoft Excel 2007+"
unzip -l desafio/planilha-contas.xlsx        # lista sem extrair
unzip -p desafio/planilha-contas.xlsx xl/workbook.xml   # imprime uma parte
unzip -q desafio/roteiro-atendimento.docx -d roteiro/   # extrai tudo
```

### 2. Metadados

```bash
unzip -p desafio/roteiro-atendimento.docx docProps/core.xml
exiftool -Creator -LastModifiedBy -CreateDate -ModifyDate desafio/roteiro-atendimento.docx
```

### 3. Comentários e abas ocultas

```bash
unzip -p desafio/roteiro-atendimento.docx word/comments.xml | sed 's/<[^>]*>//g'
unzip -p desafio/planilha-contas.xlsx xl/workbook.xml | grep -o '<sheet [^>]*>'
# state="hidden" ou state="veryHidden" = aba escondida
```

### 4. LibreOffice sem janela

```bash
sudo apt install libreoffice-nogui        # ~300 MB; no desktop, "libreoffice" completo
libreoffice -h
libreoffice --headless --convert-to txt desafio/roteiro-atendimento.docx
libreoffice --headless --convert-to csv desafio/planilha-contas.xlsx    # só a 1ª aba!
libreoffice --headless --convert-to csv antigo.xls                      # .xls antigo também
# todas as abas, uma por arquivo (LibreOffice 7.2+):
libreoffice --headless --convert-to 'csv:Text - txt - csv (StarCalc):44,34,76,1,,0,false,true,false,false,false,-1' desafio/planilha-contas.xlsx
```

### 5. pandoc

```bash
sudo apt install pandoc
echo "Some text" | pandoc -o result.docx                  # texto -> Word
pandoc -f html -t docx https://example.com -o website.docx  # site -> Word (online)
pandoc desafio/roteiro-atendimento.docx -t plain          # Word -> texto
pandoc --track-changes=all desafio/roteiro-atendimento.docx -t plain   # com comentários
```

## 🇧🇷 Versão brazuca

Órgãos públicos publicam planilhas e documentos o tempo todo — e eles saem
com metadados. No **dados.gov.br** (<https://dados.gov.br>) e nos portais de
transparência de estados e prefeituras há milhares de `.xlsx` e `.docx`.
Um levantamento rápido de "quem produz o quê" num lote de arquivos baixados:

```bash
for f in *.xlsx *.docx; do
  autor=$(unzip -p "$f" docProps/core.xml 2>/dev/null | grep -o '<dc:creator>[^<]*' | cut -d'>' -f2)
  ultimo=$(unzip -p "$f" docProps/core.xml 2>/dev/null | grep -o '<cp:lastModifiedBy>[^<]*' | cut -d'>' -f2)
  echo "$f | autor: $autor | último: $ultimo"
done
```

E confira abas ocultas em planilhas oficiais: às vezes elas guardam tabelas de
apoio, fórmulas e versões anteriores dos dados — informação pública, mas que
ninguém viu.

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) abre os dois arquivos só com `zipfile` e
`xml.etree.ElementTree` — sem Office, sem LibreOffice.

| Terminal | Python (stdlib) |
|---|---|
| `file arquivo.xlsx` | `zipfile.is_zipfile()` |
| `unzip -l` | `ZipFile.infolist()` |
| `unzip -p arq parte.xml` | `ZipFile.read("parte.xml")` |
| `grep state="hidden"` | `aba.get("state")` com ElementTree |
| `libreoffice --convert-to csv` | ler `sheetN.xml` e gravar com `csv.writer` |
| `pandoc --track-changes=all` | ler `word/comments.xml` |

## 🚀 Além do curso

- **openpyxl** (`pip install openpyxl`): lê e escreve `.xlsx` em Python;
  `wb.worksheets` traz todas as abas e `ws.sheet_state` diz se estão ocultas.
- **python-docx** (`pip install python-docx`): lê parágrafos, tabelas e
  `doc.core_properties.author` de arquivos Word.
- **oletools** (`pip install oletools`): analisa documentos Office em busca de
  **macros** maliciosas (`olevba arquivo.docm`) — essencial antes de abrir
  anexos suspeitos de golpistas.

## 🧩 Desafio

1. Leia o roteiro **por dentro**: existe uma parte que o texto não mostra.
2. Siga a pista até a planilha e encontre o que o Excel esconde.
3. Junte os pedaços na ordem certa e confira: `bash checar.sh 'VAZANTE{...}'`

<details>
<summary>💡 Dica 1</summary>

`unzip -l desafio/roteiro-atendimento.docx` — tem um `comments.xml` lá.
</details>

<details>
<summary>💡 Dica 2</summary>

`unzip -p desafio/planilha-contas.xlsx xl/workbook.xml` mostra qual aba está
`hidden`; o conteúdo dela está em `xl/worksheets/sheet2.xml` (ou exporte todas
as abas para CSV com o LibreOffice).
</details>

A solução comentada está em [`solucoes/dia-13.sh`](../../solucoes/dia-13.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- **O seu relatório também é um zip.** Antes de mandar um `.docx`, confira
  `docProps/core.xml`: o seu nome de usuário, o da empresa e comentários de
  revisão podem ir junto. No Word: *Arquivo → Informações → Inspecionar
  documento*. No LibreOffice: *Ferramentas → Opções → Segurança → Remover
  informações pessoais ao salvar*.
- Documentos de golpistas podem ter **macros**. Analise com `unzip`,
  `exiftool` e `olevba` — ferramentas que leem sem executar.
- Planilhas de "contas laranja" listam pessoas que muitas vezes também são
  vítimas. Trate esses dados com o cuidado da LGPD: acesso restrito, uso só
  para a investigação.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 12](../dia-12-pdf/) · [Índice](../../README.md) · [Dia 14](../dia-14-json-xml-csv/) ➡️
