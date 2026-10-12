# Dia 15 — O site clone 🕸️

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-15.ipynb)
&nbsp;**Rank B** · ⏱️ ~60 min · 📖 Original: *Day 15. Scraping* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> O site da PixVelox saiu do ar ontem à noite. Por sorte, a Jurema pediu
> preservação de prova e a equipe salvou uma cópia completa antes: está em
> `desafio/site/`.
>
> — Clicar página por página é coisa de turista — diz Bento, girando a cadeira.
> — A gente **sobe o clone num servidor local** e raspa tudo: links, e-mails,
> comentários. Programador de golpe adora deixar recado no código.
>
> A Mestra Iara passa e deixa só um bilhete na mesa: *"o que o dono pede para
> os robôs não verem é exatamente o que você precisa ver"*.

**Sua tarefa:** servir o clone em `127.0.0.1`, descobrir a área que a PixVelox
escondeu dos buscadores, navegar por ela e extrair o código interno da
campanha — a flag `VAZANTE{...}`.

## 🎯 Ao final de hoje você sabe

- [ ] Servir uma pasta como site local com `python3 -m http.server` (e desligar depois!)
- [ ] Rodar um processo em **segundo plano** (`&`, `$!`, `kill`)
- [ ] Baixar páginas com `curl` e extrair links, e-mails e comentários com `grep -o` + `sed`
- [ ] Ler o `robots.txt` e testar se os caminhos existem (código HTTP)
- [ ] Entender o que é um **crawler** e escrever um de bolso em Bash
- [ ] Transformar HTML em texto com `html2text` (inclusive entidades `&#86;`)
- [ ] Saber para que servem `katana`, `nuclei` e `wget -r`

## 📖 Conceito em 2 minutos

**Raspagem (scraping)** é baixar páginas automaticamente e tirar delas os
dados que interessam. São sempre dois passos:

```text
  baixar  ─────────────►  extrair
  curl, wget, katana      grep -o, sed, html2text, nuclei
```

Uma página web é só um **arquivo de texto** (HTML). O navegador esconde muita
coisa que está lá dentro: **comentários** (`<!-- ... -->`), endereços para onde
formulários enviam dados (`action="..."`), scripts de rastreio, e-mails em
`mailto:`. O terminal mostra tudo.

E existe um arquivo que quase todo site tem: o **`robots.txt`**. Ele pede
(educadamente) para robôs de busca não visitarem certas pastas. Não tranca
nada — e ainda funciona como um mapa do que o dono acha "sensível".

Um **crawler** (rastreador) é o robô que abre uma página, coleta os links,
visita esses links, coleta os novos… até acabar. `katana` é um crawler
profissional; hoje você também escreve um de 15 linhas.

## ⌨️ Mão na massa

Rode `bash comandos.sh` na pasta do dia. Cada seção liga o servidor, faz o
trabalho e **desliga** o servidor no final.

### 1. Subindo o clone num servidor local

```bash
python3 -m http.server 8015 --bind 127.0.0.1 --directory desafio/site &  # & = segundo plano
SERVIDOR=$!                     # $! = PID do último processo em segundo plano
curl -sI http://127.0.0.1:8015/ # -I = só cabeçalhos
kill "$SERVIDOR"                # desliga (sempre!)
```

### 2. Links, e-mails e comentários

```bash
curl -s http://127.0.0.1:8015/index.html -o index.html
grep -o 'href="[^"]*"' index.html | sed 's/^href="//; s/"$//'   # links
grep -oE '[[:alnum:]._-]+@[[:alnum:].-]+\.example' index.html    # e-mails
grep -o '<!--.*-->' index.html                                   # comentários
grep -o 'action="[^"]*"' cashback.html                           # para onde vai o formulário
```

### 3. robots.txt

```bash
curl -s http://127.0.0.1:8015/robots.txt | grep '^Disallow' | awk '{print $2}'
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8015/painel-interno/   # 200 existe, 404 não
```

### 4. Mini-crawler

```bash
fila=("/painel-interno/index.html"); visitadas=()
while [ "${#fila[@]}" -gt 0 ]; do
  atual="${fila[0]}"; fila=("${fila[@]:1}")
  # ... baixa, guarda em visitadas, extrai os href e põe os internos na fila
done
```

(versão completa e comentada no [`comandos.sh`](comandos.sh))

### 5. html2text

```bash
sudo apt install html2text
html2text -utf8 -nobs desafio/site/sobre.html    # só o texto, sem tags
```

O `html2text` traduz **entidades HTML**: `&#86;&#65;&#90;` vira `VAZ`. Um
`grep VAZANTE` no HTML cru não encontra texto escrito assim.

### 6. wget recursivo

```bash
wget -r -l 2 -nH -P espelho http://127.0.0.1:8015/index.html   # baixa o site seguindo links
```

O `wget` respeita o `robots.txt` por padrão (`-e robots=off` desliga — só com autorização).

### 7. katana e nuclei (opcional, precisa de internet e Go)

```bash
go install github.com/projectdiscovery/katana/cmd/katana@latest
katana -u https://example.com -d 2 -silent          # crawler
katana -list dominios.txt -o resultados.txt

go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
git clone https://github.com/cipher387/juicyinfo-nuclei-templates
nuclei -t juicyinfo-nuclei-templates/juicy_info/title.yaml -l resultados.txt
nuclei -t desafio/extrair-emails.yaml -l urls.txt   # template nosso, com regex de e-mail
```

O binário vai para `$(go env GOPATH)/bin` — coloque essa pasta no `PATH`.
Os templates do `nuclei` são YAML: troque a regex do `extractors` e você
extrai telefones, carteiras de cripto, links de redes sociais…

## 🇧🇷 Versão brazuca

Muitos sites públicos brasileiros também têm `robots.txt` e páginas cheias de
links para PDFs (editais, diários, relatórios). O mesmo kit funciona:

```bash
# O robots.txt do portal gov.br
curl -s https://www.gov.br/robots.txt | head -n 20

# Links da página inicial do registro.br (onde se registram os domínios .br)
curl -s https://registro.br/ | grep -o 'href="[^"]*"' | sed 's/^href="//; s/"$//' | sort -u | head
```

Para diários oficiais municipais, antes de raspar, veja se já existe uma API:
o projeto **Querido Diário** (Open Knowledge Brasil) raspou centenas de
municípios e oferece busca em `https://api.queridodiario.ok.org.br/gazettes?querystring=...`.
Raspar o que já tem API é desperdício — e mais carga no servidor dos outros.

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) sobe o servidor numa *thread*, faz o
crawler com uma fila (`deque`) e transforma HTML em texto com `HTMLParser`.

| Terminal | Python (stdlib) |
|---|---|
| `python3 -m http.server &` | `ThreadingHTTPServer` + `threading.Thread` |
| `kill $SERVIDOR` | `servidor.shutdown()` |
| `curl URL` | `urllib.request.urlopen(URL).read()` |
| `curl -w '%{http_code}'` | `resp.status` / `HTTPError.code` |
| `grep -o 'href="[^"]*"'` | `re.findall(r'href="([^"]*)"', html)` |
| `html2text` | `html.parser.HTMLParser` (`handle_data`) |
| fila do crawler | `collections.deque` + `set()` |

## 🚀 Além do curso

- **`trafilatura`** (`pip install trafilatura`) extrai o texto principal de uma
  página, sem menus e rodapés: `trafilatura -u https://example.com`. Ótimo para
  arquivar notícias.
- **`beautifulsoup4`** (`pip install beautifulsoup4`) é a biblioteca Python
  clássica de raspagem: `soup.find_all("a")` em vez de regex.
- **Playwright** (`pip install playwright` + `playwright install chromium`)
  abre um navegador de verdade, sem janela, para páginas que só mostram o
  conteúdo depois de rodar JavaScript.

## 🧩 Desafio

1. Suba `desafio/site/` em `http://127.0.0.1:8015` (em segundo plano).
2. Leia o `robots.txt` e descubra qual pasta escondida **existe** de verdade.
3. Siga os links dentro dela até a página da campanha.
4. Extraia o código interno da campanha. Desligue o servidor.
5. Confira: `bash checar.sh 'VAZANTE{...}'`

<details>
<summary>💡 Dica 1</summary>

Uma das pastas do `robots.txt` responde 404. A outra responde 200 — e tem um
`index.html` com links.
</details>

<details>
<summary>💡 Dica 2</summary>

`grep VAZANTE` no HTML não acha nada porque o código está em entidades HTML
(`&#86;&#65;…`). Passe a página pelo `html2text -utf8` antes do `grep`.
</details>

A solução comentada está em [`solucoes/dia-15.sh`](../../solucoes/dia-15.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- **Raspar não é invadir, mas tem limites.** `robots.txt` não é tranca, mas
  ignorá-lo em massa pode violar termos de uso. Área com senha é outra
  história: contornar autenticação é crime (Lei 12.737/2012).
- **Seja gentil com o servidor:** use `sleep` entre requisições e limite a
  profundidade. Robô agressivo derruba site pequeno — e chama atenção.
- **Você deixa rastro.** Cada requisição registra seu IP e o `User-Agent`
  (`curl/8.x` denuncia um robô) no log do alvo. Em site de golpista, isso
  pode alertá-lo. Prefira cópias (Wayback Machine, `archive.today`) e uma
  máquina de investigação isolada.
- **LGPD:** e-mails e telefones raspados são dados pessoais. Colete só o
  necessário para a investigação e guarde com controle de acesso.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 14](../dia-14-json-xml-csv/) · [Índice](../../README.md) · [Dia 16](../dia-16-automacao-de-busca/) ➡️
