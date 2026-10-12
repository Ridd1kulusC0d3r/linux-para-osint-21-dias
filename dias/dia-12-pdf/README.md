# Dia 12 — O contrato 📄

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-12.ipynb)
&nbsp;**Rank C** · ⏱️ ~45 min · 📖 Original: *Day 12. Analyze PDF* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> A vítima 027 não perdeu só dinheiro: ela **assinou um contrato**. A PixVelox
> ofereceu 3% de "cashback" para usar a conta dela como passagem. É o famoso
> esquema de **conta laranja**, e o contrato veio em PDF, todo bonitinho.
>
> Jurema lê em voz alta, indignada:
> — "Cláusula 2ª: a parceira não deve comentar a parceria com o banco." Isso
> aqui é confissão com papel timbrado.
>
> Bento, sem tirar os olhos da tela:
> — O texto é o que eles **quiseram** escrever. Os metadados são o que eles
> **esqueceram** de apagar.

**Sua tarefa:** ler o texto de `desafio/contrato-pixvelox.pdf`, entender
como se forma o "código de verificação" do contrato e achar a peça que falta
nos metadados do PDF. Junte as duas coisas para formar a flag `VAZANTE{...}`.

## 🎯 Ao final de hoje você sabe

- [ ] Ler a ficha e os metadados de um PDF (`pdfinfo`, `exiftool`, `grep ^Producer`)
- [ ] Extrair o texto (`pdftotext`, com `-layout` e intervalo de páginas)
- [ ] Extrair as imagens embutidas (`pdfimages -list`, `-png`, `-all`)
- [ ] Reconhecer um PDF **escaneado** e aplicar OCR (`pdftoppm` + `tesseract`, `ocrmypdf`)
- [ ] Levantar metadados de vários PDFs de uma vez (`exiftool -T`)

## 📖 Conceito em 2 minutos

Um PDF não é uma "foto do documento". É um arquivo estruturado com:

```text
contrato.pdf
├── /Info (metadados)   Title, Author, Creator, Producer, Keywords, datas
├── página 1 ── texto (comandos de desenho de letras)  +  imagens (logo)
├── página 2 ── texto                                   +  imagens (rubrica)
└── (às vezes) XMP, anexos, formulários, JavaScript, histórico de versões
```

Três campos de metadados aparecem o tempo todo em investigações:

| Campo | O que costuma revelar |
|---|---|
| **Author** | o nome de usuário do computador de quem criou o documento |
| **Creator** | o programa usado para *escrever* (Word, Writer, Docs...) |
| **Producer** | o programa que *gerou o PDF* (exportador, impressora virtual, sistema) |

E um alerta: se a página é uma **imagem escaneada**, não existe texto para
extrair — só pixels. Aí entra o OCR, que você já conhece do Dia 11.

## ⌨️ Mão na massa

O arquivo [`comandos.sh`](comandos.sh) tem tudo comentado; rode inteiro com
`bash comandos.sh`.

### 1. Instalar

```bash
sudo apt install poppler-utils libimage-exiftool-perl tesseract-ocr ghostscript
pip install ocrmypdf          # opcional (ou: sudo apt install ocrmypdf)
```

### 2. Metadados

```bash
pdfinfo desafio/contrato-pixvelox.pdf
exiftool desafio/contrato-pixvelox.pdf
exiftool desafio/contrato-pixvelox.pdf | grep ^Producer     # ^ = começa com
```

### 3. Texto

```bash
pdftotext desafio/contrato-pixvelox.pdf contrato.txt       # para arquivo
pdftotext desafio/contrato-pixvelox.pdf -                  # na tela
pdftotext -layout -f 2 -l 2 desafio/contrato-pixvelox.pdf - # só a página 2, com layout
```

### 4. Imagens

```bash
pdfimages -list desafio/contrato-pixvelox.pdf               # o que tem lá dentro
pdfimages -png desafio/contrato-pixvelox.pdf extracted_images   # extrai como PNG
pdfimages -all desafio/contrato-pixvelox.pdf original       # mantém o formato original
```

### 5. PDF escaneado → OCR

```bash
pdftotext desafio/termo-escaneado.pdf - | wc -c     # ~0 caracteres: é imagem
pdftoppm -r 150 -png desafio/termo-escaneado.pdf pagina   # vira pagina-1.png
tesseract pagina-1.png -                              # OCR manual
ocrmypdf desafio/termo-escaneado.pdf result.pdf      # PDF novo, pesquisável
ocrmypdf --force-ocr entrada.pdf result.pdf          # refaz OCR mesmo se já houver texto
pdftotext result.pdf result.txt
```

### 6. Em lote

```bash
exiftool -T -FileName -Author -Producer -CreateDate *.pdf     # tabela
exiftool -csv -Author -Producer *.pdf > metadados.csv         # planilha
```

## 🇧🇷 Versão brazuca

Editais, contratos e atas de órgãos públicos são publicados em PDF — e
carregam metadados. Um exercício legítimo e revelador: baixe PDFs de
licitações no **Portal Nacional de Contratações Públicas** (<https://pncp.gov.br>)
ou no **Diário Oficial da União** (<https://www.in.gov.br>) e compare quem
produziu os documentos.

```bash
exiftool -T -FileName -Author -Creator -Producer -CreateDate *.pdf | sort -t$'\t' -k2
```

Se a proposta de duas empresas "concorrentes" tem o **mesmo Author** ou foi
criada no mesmo minuto, isso é um indício clássico de conluio em licitação,
apontado em auditorias do TCU e das controladorias. Indício — não prova:
investigue o resto.

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) abre o PDF como **bytes** e encontra o
dicionário `/Info`, as strings de texto e os JPEGs embutidos com regex. Isso
funciona no nosso contrato (não comprimido); PDFs reais comprimem o conteúdo
e pedem `zlib` ou uma biblioteca.

| Terminal | Python (stdlib) |
|---|---|
| `pdfinfo` / `exiftool` | `re` no dicionário `/Info` |
| `grep ^Producer` | `info.get("Producer")` |
| `pdftotext` | `re.findall(rb"\((.*?)\) Tj", ...)` dentro de `BT ... ET` |
| `pdfimages -all` | recortar os bytes entre `stream` e `endstream` dos `/DCTDecode` |
| (stream comprimido) | `zlib.decompress(dados)` |

## 🚀 Além do curso

- **pypdf** (`pip install pypdf`): a biblioteca Python pura mais simples para
  PDF — `PdfReader("contrato.pdf").metadata` e `page.extract_text()`.
- **pdfplumber** (`pip install pdfplumber`): extrai **tabelas** de PDFs (ótimo
  para extratos, notas de empenho e relatórios oficiais) com coordenadas de
  cada palavra.
- **qpdf** (`apt install qpdf`): `qpdf --qdf --object-streams=disable in.pdf out.pdf`
  descomprime o PDF para você ler a estrutura num editor de texto; e
  `qpdf --show-npages` conta páginas. Para o lado oposto (limpar metadados
  antes de publicar), veja `mat2` (`apt install mat2`).

## 🧩 Desafio

1. Leia o texto do contrato: a cláusula 9ª explica o código de verificação.
2. Descubra em qual campo de metadados está a "palavra-chave".
3. Monte a flag e confira: `bash checar.sh 'VAZANTE{...}'`

<details>
<summary>💡 Dica 1</summary>

`pdftotext desafio/contrato-pixvelox.pdf - | grep -A1 verificação`
</details>

<details>
<summary>💡 Dica 2</summary>

"Palavra-chave" em inglês é *keyword*. `pdfinfo` mostra uma linha `Keywords:`.
</details>

A solução comentada está em [`solucoes/dia-12.sh`](../../solucoes/dia-12.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- **Os seus PDFs também falam.** Antes de entregar um relatório, rode
  `exiftool relatorio.pdf`: o Author pode ser o seu login, e o Producer, o
  seu sistema. Limpe com `exiftool -all:all= relatorio.pdf` (e confira; em
  PDF, o exiftool só "esconde" os dados antigos — use `qpdf` para reescrever
  o arquivo) ou exporte já sem metadados.
- Contratos de vítimas trazem dados pessoais e bancários. Guarde o original
  com hash (`sha256sum`) e trabalhe numa cópia.
- PDF pode conter **JavaScript e links maliciosos**. Abra evidências
  suspeitas com as ferramentas de linha de comando (que não executam nada),
  não no leitor padrão.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 11](../dia-11-video-audio-imagem/) · [Índice](../../README.md) · [Dia 13](../dia-13-arquivos-office/) ➡️
