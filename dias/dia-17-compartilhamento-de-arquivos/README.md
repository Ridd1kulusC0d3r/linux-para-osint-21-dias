# Dia 17 — O torrent do kit 🧲

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-17.ipynb)
&nbsp;**Rank B** · ⏱️ ~50 min · 📖 Original: *Day 17. File sharing sites, torrents, FTP* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> Um informante de um fórum de golpes mandou ao Núcleo Coruja um arquivo de
> 1 KB: `kit_golpe_pixvelox.torrent`. Diz que é o "kit completo" que Os
> Vazantes vendem para afiliados: páginas falsas, roteiros de WhatsApp,
> listas de números.
>
> Bento já estava com o cliente de torrent aberto.
> — **Não.** — A Jurema fecha a tampa do notebook dele. — Baixar isso é
> compartilhar isso. Torrent sobe enquanto desce. Você vira distribuidor.
>
> A Mestra Iara sorri.
> — E nem precisa. O `.torrent` não é o kit: é a **ficha** do kit. Nome de
> cada arquivo, data, quem criou… e um bilhetinho de quem montou.

**Sua tarefa:** sem baixar nada, ler os metadados do `.torrent`, seguir a
instrução que maré_alta deixou para os afiliados e montar a flag
`VAZANTE{...}`. De bônus: descobrir, pelo hash, qual roteiro foi usado contra
a vítima 014.

## 🎯 Ao final de hoje você sabe

- [ ] Calcular e conferir **hashes** (`sha256sum`, `md5sum`, `sha256sum -c`)
- [ ] Identificar um arquivo só pela impressão digital
- [ ] Explicar o que há dentro de um `.torrent` (formato **bencode**)
- [ ] Ler metadados com `transmission-show` e `aria2c -S`
- [ ] Dissecar um **link magnet** (info hash, nome, trackers)
- [ ] Listar e baixar de servidores **FTP** com `curl`, `lftp` e `ftp`
- [ ] Conhecer clientes de terminal para sites de compartilhamento

## 📖 Conceito em 2 minutos

**Hash** é a impressão digital de um arquivo: um número enorme calculado a
partir de cada byte. Mesmo conteúdo → mesmo hash. Um espaço a mais → hash
completamente diferente. É assim que se prova que uma evidência não mudou
e que se reconhece o mesmo arquivo com nomes diferentes.

Um **torrent** divide os arquivos em pedaços e cada pessoa baixa pedaços de
outras pessoas (e envia ao mesmo tempo). O arquivo `.torrent` é só o
"cardápio":

```text
kit_golpe_pixvelox.torrent
├── announce / announce-list   → trackers (quem apresenta os participantes)
├── comment, created by, date  → metadados do autor  ← OSINT!
└── info
    ├── name, files[]          → nomes e tamanhos de tudo
    └── pieces                 → SHA-1 de cada pedaço
```

O **info hash** (SHA-1 do bloco `info`) identifica o torrent no mundo todo.
Um **magnet** é esse hash em forma de link. Tudo escrito em **bencode**:
`i42e` é o número 42, `4:spam` é um texto de 4 letras, `l…e` é lista e
`d…e` é dicionário.

**FTP** é o avô dos protocolos de arquivo (1971): sem criptografia, ainda
comum em órgãos públicos, câmeras e roteadores.

## ⌨️ Mão na massa

### 1. Hashes

```bash
sha256sum desafio/amostras/*.txt
md5sum desafio/amostras/roteiro_a.txt
sha256sum desafio/amostras/*.txt | grep 'f51dd5...'     # quem tem esse hash?
sha256sum ./*.txt > SHA256SUMS && sha256sum -c SHA256SUMS   # conferir depois
```

### 2. O torrent por dentro

```bash
head -c 400 desafio/kit_golpe_pixvelox.torrent     # bencode é quase legível
strings -n 8 desafio/kit_golpe_pixvelox.torrent | fold -w 100 | head
```

### 3. transmission-show e aria2c

```bash
sudo apt install transmission-cli aria2
transmission-show desafio/kit_golpe_pixvelox.torrent      # tudo
transmission-show -f desafio/kit_golpe_pixvelox.torrent   # só arquivos
transmission-show -m desafio/kit_golpe_pixvelox.torrent   # link magnet
aria2c -S desafio/kit_golpe_pixvelox.torrent              # -S só mostra, não baixa
```

### 4. Magnet

```bash
magnet=$(transmission-show -m desafio/kit_golpe_pixvelox.torrent)
echo "$magnet" | tr '?' '&' | tr '&' '\n'     # xt=urn:btih:<info hash>, dn=, tr=
```

### 5. Criando um torrent (para entender)

```bash
transmission-create -o teste.torrent -c "comentário" -t udp://tracker.example:6969/announce minha-pasta/
```

### 6. FTP

```bash
curl --list-only ftp://ftp.ibge.gov.br/          # lista uma pasta
curl -O ftp://servidor.example/pasta/arquivo.csv  # baixa
lftp -e 'ls; bye' ftp://ftp.ibge.gov.br           # cliente completo
ftp ftp.ibge.gov.br                               # clássico, interativo (login: anonymous)
awk '$1 !~ /^d/ {print $5, $NF}' desafio/ftp_listagem.txt   # tamanho e nome
```

### 7. Sites de compartilhamento

| Serviço | Cliente de terminal |
|---|---|
| Google Drive | `gdrive` (glotlabs/gdrive) |
| Dropbox | `dbxcli` |
| Mega | `MEGAcmd` (`mega-get`) |
| Vídeos (YouTube e muitos outros) | `yt-dlp` |
| Link direto | `curl -O` / `wget` |

## 🇧🇷 Versão brazuca

Muitos dados públicos brasileiros ainda moram em FTP ou em links diretos de
download — e é justamente aí que o hash faz diferença:

```bash
# FTP do IBGE: malhas territoriais, censos, PNAD
curl --list-only ftp://ftp.ibge.gov.br/

# Dados abertos da Receita Federal (CNPJ) são arquivos .zip grandes,
# listados em dados.gov.br. Depois de baixar, registre o hash:
sha256sum Empresas0.zip >> SHA256SUMS
```

O **Portal Brasileiro de Dados Abertos** (`dados.gov.br`) tem API que devolve
os links de download de cada conjunto. Guardar o `sha256sum` do arquivo do
dia em que você baixou permite provar, meses depois, exatamente qual versão
embasou a sua análise.

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) tem um **decodificador de bencode em 25
linhas** — dá para ler qualquer `.torrent` sem instalar nada.

| Terminal | Python (stdlib) |
|---|---|
| `sha256sum arq` | `hashlib.sha256(Path(arq).read_bytes()).hexdigest()` |
| `md5sum arq` | `hashlib.md5(...).hexdigest()` |
| `transmission-show` | `bdecode()` (função própria) |
| info hash | `hashlib.sha1(bencode(info)).hexdigest()` |
| decodificar magnet | `urllib.parse.parse_qs(urlparse(m).query)` |
| `curl ftp://` | `ftplib.FTP("servidor").nlst()` |

## 🚀 Além do curso

- **`torf`** (`pip install torf`) — biblioteca Python para ler, criar e
  validar torrents; o `torf-cli` (`pip install torf-cli`) mostra tudo com
  `torf arquivo.torrent`.
- **`yt-dlp`** (`pip install yt-dlp`) — baixa vídeos de centenas de sites;
  com `--skip-download --write-info-json` guarda só os metadados (data de
  upload, canal, descrição) — muito útil em OSINT.
- **`ssdeep`** (`apt install ssdeep`) — "hash difuso": diz se dois arquivos
  são **parecidos** (ex.: roteiros com uma vírgula de diferença), coisa que o
  SHA-256 não faz.

## 🧩 Desafio

1. Abra `desafio/kit_golpe_pixvelox.torrent` com `transmission-show` (ou o `equivalente.py`).
2. Leia o comentário: maré_alta deixou uma instrução para os afiliados.
3. Siga a instrução na lista de arquivos e junte as palavras com `_`.
4. Confira: `bash checar.sh 'VAZANTE{...}'`
5. Bônus: qual roteiro de `desafio/amostras/` tem o hash da `denuncia_vitima014.txt`?

<details>
<summary>💡 Dica 1</summary>

O comentário fala da pasta `config/` e de uma ordem. Os nomes dos arquivos
lá têm um número e uma palavra.
</details>

<details>
<summary>💡 Dica 2</summary>

`transmission-show -f arquivo.torrent | grep -o 'config/[0-9][0-9]_[a-z]*' | grep -v /00_ | sort`
e depois tire o prefixo com `sed` e junte com `paste -sd_`.
</details>

A solução comentada está em [`solucoes/dia-17.sh`](../../solucoes/dia-17.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- **Torrent sobe enquanto desce.** Baixar material ilícito via BitTorrent é
  também **distribuí-lo** — e seu IP fica visível para todos os participantes
  do enxame. Inspecione o `.torrent`; não baixe.
- **Vazamentos de dados:** baixar, guardar ou repassar bases vazadas com dados
  pessoais pode configurar crime e viola a LGPD. Em investigação oficial, isso
  passa por autorização e cadeia de custódia.
- **Clientes não oficiais** (Drive, Mega, redes sociais) podem bloquear a conta
  usada. Nunca use sua conta pessoal.
- **Hash sempre.** Tudo que você coletar: `sha256sum` na hora, anotado com data
  e origem. É isso que torna a evidência confiável.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 16](../dia-16-automacao-de-busca/) · [Índice](../../README.md) · [Dia 18](../dia-18-investigacao-de-dominio/) ➡️
