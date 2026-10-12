# Dia 16 — Perguntando ao mundo 🔎

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-16.ipynb)
&nbsp;**Rank B** · ⏱️ ~50 min · 📖 Original: *Day 16. Web search automation tools* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> Segunda-feira, fim de tarde. Bento está com dezessete abas abertas no
> navegador, todas com buscas sobre a PixVelox.
>
> — Copiar e colar resultado de busca é o jeito mais caro de gastar a vida —
> resmunga a Mestra Iara, fechando o notebook dele. — O terminal pergunta ao
> mundo por você, e guarda a resposta num arquivo.
>
> Ela deixa dois arquivos na pasta do caso: uma busca do DuckDuckGo e uma
> exportação do **Netlas**, um buscador que não procura páginas, e sim
> **servidores**.
> — Um dos sites dessa busca não é vitrine. É bastidor. Ache, e veja o que
> ele expõe porta por porta.

**Sua tarefa:** processar os resultados salvos em `desafio/`, identificar o
host da infraestrutura escondida e montar a flag `VAZANTE{...}` a partir dos
títulos dos servidores dele.

## 🎯 Ao final de hoje você sabe

- [ ] Buscar no DuckDuckGo pelo terminal com `ddgr` (texto e `--json`)
- [ ] Extrair só os sites de uma lista de resultados (`grep -o '\[.*]'`)
- [ ] Usar operadores de busca (*dorks*): `site:`, `filetype:`, `intitle:`, `inurl:`
- [ ] Montar URLs de busca com **urlencode** (`jq @uri`) e automatizar várias buscas
- [ ] Entender buscadores de servidores (Netlas, Shodan, Censys)
- [ ] Processar JSON Lines do `netlas download` com `jq`

## 📖 Conceito em 2 minutos

Existem dois tipos de buscador que todo investigador usa:

| Tipo | O que indexa | Exemplos | Pergunta típica |
|---|---|---|---|
| **De páginas** | textos de sites, ligados por links | Google, Bing, DuckDuckGo | "quem fala de PixVelox?" |
| **De servidores** | cada IP e porta abertos na internet | Netlas, Shodan, Censys | "que máquinas respondem com 'PixVelox' no HTML?" |

Automatizar = **mesma pergunta, feita por um script, com o resultado salvo em
arquivo**. Daí em diante é o kit que você já tem: `grep`, `jq`, `sort`, `comm`.

Toda busca é, no fundo, uma **URL**. Espaços e símbolos viram códigos
(`%20`, `%22`…): isso é **urlencode**. Saber montar a URL é saber automatizar
qualquer buscador.

## ⌨️ Mão na massa

### 1. ddgr — DuckDuckGo no terminal

```bash
sudo apt install ddgr            # ou: pip install ddgr
ddgr -n 10 --np -C osint > busca_osint.txt   # --np: busca e sai; -C: sem cores
cat busca_osint.txt | grep -o '\[.*]'        # só os sites (entre colchetes)
ddgr -n 5 --json pixvelox > resultados.json  # resultado estruturado
jq -r '.[] | .url' resultados.json
ddgr --np -w social.example pixvelox         # -w = site:
```

### 2. Dorks

```text
"pixvelox" site:social.example       só naquele site
"pixvelox" filetype:pdf              só PDFs
intitle:"painel pxv"                 palavra no título
inurl:cashback "pix"                 palavra no endereço
```

### 3. URLs de busca com urlencode

```bash
while IFS= read -r dork; do
  q=$(jq -rn --arg q "$dork" '$q | @uri')
  echo "https://duckduckgo.com/html/?q=$q"
done < desafio/dorks.txt
```

### 4. Netlas (opcional, conta gratuita)

```bash
pip install netlas
netlas -h
netlas savekey SUA_CHAVE
netlas download -c 20 "http.body:*pixvelox*" > netlas_resultados.json
jq .data.http.title netlas_resultados.json > titulos.txt
```

Filtros úteis: `http.title:`, `domain:`, `port:`, `geo.city:`, `geo.country:`, `ip:`.

### 5. jq nos resultados e cruzamento

```bash
jq -r '[.data.ip, .data.port, .data.host] | @tsv' desafio/netlas_resultados.json
grep -o '\[.*]' desafio/busca_pixvelox.txt | tr -d '[]' | sort -u > ddg.txt
jq -r '.data.host' desafio/netlas_resultados.json | sort -u > netlas.txt
comm -12 ddg.txt netlas.txt     # está nas duas buscas
```

## 🇧🇷 Versão brazuca

Diário oficial é uma das melhores fontes abertas do Brasil: nomeações,
contratos, licitações, sanções. O **Querido Diário** (Open Knowledge Brasil)
indexa diários de municípios e tem API pública sem chave:

```bash
termo="licitação pix"
q=$(jq -rn --arg q "$termo" '$q | @uri')
curl -s "https://api.queridodiario.ok.org.br/gazettes?querystring=$q&size=3" \
  | jq -r '.gazettes[] | "\(.date)  \(.territory_name)  \(.url)"'
```

Dorks que funcionam bem com fontes brasileiras:

```text
site:gov.br filetype:pdf "pregão eletrônico" "cashback"
site:jusbrasil.com.br "nome da empresa"
site:in.gov.br "portaria" "nome do órgão"
```

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) faz o mesmo processamento com `json`, `re`
e `urllib.parse`.

| Terminal | Python (stdlib) |
|---|---|
| `grep -o '\[.*]'` | `re.findall(r"\[(.*)\]", texto)` |
| `jq -r '.[] \| .url'` | `[r["url"] for r in json.load(f)]` |
| JSON Lines no `jq` | `json.loads(linha)` em cada linha |
| `jq @uri` | `urllib.parse.quote(q, safe="")` |
| `comm -12` | `set(a) & set(b)` |
| `sort -n` | `sorted(..., key=lambda s: s["port"])` |

## 🚀 Além do curso

- **`ddgs`** (`pip install ddgs`, antigo `duckduckgo-search`) — biblioteca
  Python que busca no DuckDuckGo (e outros buscadores) e devolve listas de
  dicionários — pronto para virar CSV ou JSON.
- **`shodan`** (`pip install shodan`) — CLI e biblioteca oficiais do Shodan:
  `shodan init CHAVE` e `shodan search 'http.title:"painel"'`.
- **Netlas Cookbook** (github.com/netlas-io/netlas-cookbook) — receitas
  prontas em Python para dezenas de tarefas de OSINT com a API do Netlas.

## 🧩 Desafio

1. Liste os sites da busca em `desafio/busca_pixvelox.txt`.
2. Descubra qual deles é infraestrutura (não é vitrine, notícia nem reclamação).
3. No `desafio/netlas_resultados.json`, filtre os servidores desse host.
4. Ordene pela **porta** e junte os pedaços entre colchetes dos títulos com `_`.
5. Confira: `bash checar.sh 'VAZANTE{...}'`

<details>
<summary>💡 Dica 1</summary>

Um dos sites tem "painel" no nome e uma página de login. No Netlas, ele
aparece em várias portas diferentes do mesmo IP.
</details>

<details>
<summary>💡 Dica 2</summary>

`jq -r 'select(.data.host == "HOST") | "\(.data.port) \(.data.http.title)"'`
e depois `sort -n | grep -o '\[[^]]*\]' | tr -d '[]' | paste -sd_`.
</details>

A solução comentada está em [`solucoes/dia-16.sh`](../../solucoes/dia-16.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- **Buscar é passivo; acessar é ativo.** Consultar o Netlas não toca no
  servidor do alvo. Abrir o painel encontrado, sim — e tentar logar nele é
  crime. Registre e passe para quem tem mandado.
- **Suas buscas te identificam.** Buscadores registram IP e termos. Em casos
  sensíveis, use uma máquina de investigação separada e nunca busque o nome
  do alvo logado na sua conta pessoal.
- **Automação com moderação:** `sleep` entre buscas, poucas por minuto.
  Buscadores bloqueiam robôs — e ferramentas de "raspagem do Google"
  violam os termos de uso deles; prefira APIs oficiais.
- **LGPD:** resultados de busca sobre pessoas físicas são dados pessoais.
  Guarde só o que tem finalidade clara na investigação.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 15](../dia-15-scraping/) · [Índice](../../README.md) · [Dia 17](../dia-17-compartilhamento-de-arquivos/) ➡️
