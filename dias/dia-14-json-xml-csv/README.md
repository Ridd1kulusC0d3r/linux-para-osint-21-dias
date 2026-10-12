# Dia 14 — O export do grupo 🧬

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-14.ipynb)
&nbsp;**Rank C** · ⏱️ ~55 min · 📖 Original: *Day 14. JSON, XML, CSV* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> O colaborador arrependido do Dia 13 fez mais uma: exportou o grupo **interno**
> da equipe da PixVelox antes de ser removido. Um `export-grupo.json` de 26 KB,
> com membros, 120 mensagens e uma surpresa.
>
> — O maré_alta apaga tudo o que escreve de importante — avisa o colaborador.
>
> Bento rola o arquivo e para numa linha:
> — `"apagada": true`... e logo embaixo, `"texto_original"`. O app escondeu da
> tela, mas o export levou junto. Clássico.
>
> No mesmo pacote vieram o `sitemap.xml` do site falso e um CSV de domínios
> parecidos com o da PixVelox.

**Sua tarefa:** usar o `jq` para filtrar, entre as 120 mensagens, as que
foram **apagadas pelo maré_alta**, recuperar o texto original delas na ordem
e montar a flag `VAZANTE{...}`.

## 🎯 Ao final de hoje você sabe

- [ ] Navegar em JSON com `jq`: `.chave`, `.lista[0]`, `.lista[].campo`, `length`
- [ ] Filtrar com `select(...)` e transformar com `map(...)`, `group_by`, `@csv`
- [ ] Consultar XML com `xmlstarlet sel` e XPath (inclusive com namespace)
- [ ] Manipular CSV de verdade com csvkit: `csvlook`, `csvcut`, `csvgrep`, `in2csv`, `csvstat`
- [ ] Encadear `curl | jq` com uma API pública

## 📖 Conceito em 2 minutos

Os três formatos guardam a mesma coisa — dados — de jeitos diferentes:

```text
JSON  {"membros": [{"handle": "mare_alta", "admin": true}, ...]}   ← APIs, exports de apps
XML   <urlset><url><loc>https://...</loc></url></urlset>            ← sitemaps, RSS, Office
CSV   dominio,titulo,porta                                         ← planilhas, dados abertos
      pixvelox.example,"PixVelox - o Pix que devolve",443
```

O JSON é uma **árvore**: objetos `{ }` com chaves e listas `[ ]` com itens.
O `jq` anda por essa árvore com um "caminho":

```text
.mensagens            → a lista de mensagens
.mensagens[0]         → a primeira (índice começa em 0)
.mensagens[]          → cada uma, separadamente
.mensagens[].autor.handle   → o handle do autor de cada mensagem
.mensagens[] | select(.apagada)   → só as que têm apagada = true
```

## ⌨️ Mão na massa

O arquivo [`comandos.sh`](comandos.sh) tem tudo comentado; rode inteiro com
`bash comandos.sh`.

### 1. Instalar

```bash
sudo apt install jq xmlstarlet
pip install csvkit            # ou: sudo apt install csvkit
```

### 2. jq: chaves e listas

```bash
jq '.' desafio/export-grupo.json | head          # bonito e colorido
jq '.grupo.criado_por' desafio/export-grupo.json
jq '.membros[0].handle' desafio/export-grupo.json        # o primeiro
jq -r '.membros[].handle' desafio/export-grupo.json      # todos, sem aspas (-r)
jq '.mensagens | length' desafio/export-grupo.json       # quantos
```

### 3. jq: select, map e companhia

```bash
jq -r '.membros[] | select(.admin) | .handle' desafio/export-grupo.json
jq -r '.mensagens[] | select(.autor.handle == "lucas_suporte") | .texto' desafio/export-grupo.json
jq -c '.mensagens[:5] | map(.id)' desafio/export-grupo.json
jq '[.mensagens[] | select(.apagada)] | length' desafio/export-grupo.json
jq -r '.membros[] | [.handle, .nome_exibido] | @csv' desafio/export-grupo.json   # JSON -> CSV
```

Dentro de `select` dá para combinar condições com `and`, `or` e `not`, e
comparar textos com `==`, `test("regex")` ou `contains("trecho")`.

### 4. xmlstarlet

```bash
xmlstarlet sel -t -m "//TITLE" -v . -n xml_sample.xml      # XML simples (curso original)
# sitemaps têm namespace (xmlns=...): use o prefixo _:
xmlstarlet sel -t -m "//_:url" -v "_:loc" -n desafio/sitemap.xml
xmlstarlet sel -t -m "//_:url[_:priority < 0.5]" -v "_:loc" -n desafio/sitemap.xml
```

`-t` abre o template, `-m` (*match*) escolhe os elementos com XPath, `-v`
imprime um valor, `-o` imprime um texto fixo e `-n` quebra a linha.

### 5. csvkit

```bash
csvlook desafio/dominios.csv                       # tabela legível
csvcut -c dominio,porta desafio/dominios.csv > cut_csv.csv   # colunas por nome
csvgrep -d ',' -c 2 -m 'PixVelox' desafio/dominios.csv       # coluna 2 contém...
csvgrep -c porta -r '^80$' desafio/dominios.csv              # com regex
in2csv -k membros desafio/export-grupo.json > membros.csv    # JSON -> CSV
csvstat -c porta desafio/dominios.csv                        # estatísticas
```

## 🇧🇷 Versão brazuca

A **BrasilAPI** (<https://brasilapi.com.br>) devolve JSON de fontes públicas
brasileiras — CEP, CNPJ, bancos, feriados, DDD. É o playground perfeito para
o `jq`:

```bash
curl -s https://brasilapi.com.br/api/cep/v1/01001000 | jq '{cep, city, street}'
curl -s https://brasilapi.com.br/api/ddd/v1/31 | jq -r '.cities[]' | head
curl -s https://brasilapi.com.br/api/banks/v1 | jq -r '.[] | select(.name != null) | select(.name | test("PAGAMENTO"; "i")) | "\(.code)\t\(.name)"'
# dados cadastrais PÚBLICOS de uma empresa (aqui, o próprio Banco do Brasil):
curl -s https://brasilapi.com.br/api/cnpj/v1/00000000000191 | jq '{razao_social, municipio, data_inicio_atividade}'
```

E para qualquer site, o sitemap é um mapa pronto do que existe lá. Descubra o
endereço dele no `robots.txt` (linha `Sitemap:`) e liste as páginas:
`curl -s https://SITE/sitemap.xml | xmlstarlet sel -t -m "//_:loc" -v . -n | head`.

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) usa só `json`, `xml.etree.ElementTree` e
`csv`. Os filtros do `jq` viram **compreensões de lista**.

| Terminal | Python (stdlib) |
|---|---|
| `jq '.membros[0].handle'` | `dados["membros"][0]["handle"]` |
| `jq '.membros[].handle'` | `[m["handle"] for m in dados["membros"]]` |
| `jq 'select(.admin)'` | `[m for m in membros if m["admin"]]` |
| `jq 'map(.id)'` | `[m["id"] for m in mensagens]` |
| `jq '... \| @csv'` / `in2csv` | `csv.writer` / `csv.DictWriter` |
| `xmlstarlet sel -m //loc -v .` | `ET.parse(...).getroot().iter("{ns}loc")` |
| `csvcut` / `csvgrep` | `csv.DictReader` + `if` |

## 🚀 Além do curso

- **gron** (`apt install gron`): "achata" um JSON em linhas `json.membros[0].handle = "mare_alta";`
  — aí dá para usar `grep` direto e descobrir o caminho de qualquer campo.
- **jless** (<https://jless.io>): visualizador interativo de JSON no terminal,
  com dobra de níveis e busca — ótimo para explorar um export grande antes de
  escrever o filtro.
- **DuckDB** (`pip install duckdb`): SQL direto em arquivos —
  `duckdb -c "SELECT * FROM 'dominios.csv' WHERE porta = 80"` ou
  `SELECT ... FROM read_json_auto('export-grupo.json')`. Para CSVs de
  gigabytes, é muito mais rápido que planilha.

## 🧩 Desafio

1. Olhe a estrutura de uma mensagem apagada no `export-grupo.json`.
2. Filtre com `jq` só as apagadas **do maré_alta**.
3. Pegue o `texto_original` de cada uma, na ordem, e junte.
4. Confira: `bash checar.sh 'VAZANTE{...}'`

<details>
<summary>💡 Dica 1</summary>

`jq -c '.mensagens[] | select(.apagada)' desafio/export-grupo.json` mostra as
apagadas. Há iscas de outros autores.
</details>

<details>
<summary>💡 Dica 2</summary>

`select(.apagada and .autor.handle == "mare_alta") | .texto_original` com `-r`,
e depois `tr -d '\n'` para juntar tudo numa linha.
</details>

A solução comentada está em [`solucoes/dia-14.sh`](../../solucoes/dia-14.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- Exports de grupos têm **dados de terceiros** (telefones, nomes, mensagens de
  vítimas). Use `jq` para extrair só o necessário e não redistribua o export
  inteiro (LGPD: minimização).
- Um export pode ser editado antes de chegar a você. Registre o `sha256sum`
  do arquivo recebido e de quem ele veio; quando possível, peça o export
  direto ao detentor do celular, com testemunha.
- APIs públicas têm limites de uso. Não dispare milhares de consultas em
  sequência: use `sleep` entre chamadas e guarde as respostas em disco.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 13](../dia-13-arquivos-office/) · [Índice](../../README.md) · [Dia 15](../dia-15-scraping/) ➡️
