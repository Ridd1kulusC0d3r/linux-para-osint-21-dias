# Dia 4 — Duzentas conversas 💬

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-04.ipynb)
&nbsp;**Rank D** · ⏱️ ~45 min · 📖 Original: *Day 4. Batch file processing* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> As vítimas começaram a mandar as conversas exportadas do WhatsApp. Não
> uma, nem dez: **duzentas**, organizadas por dia em `desafio/conversas/`.
>
> — Lê tudo e me fala se o tal do mare_alta aparece — pede a Mestra Iara.
>
> Você abre a primeira. Depois a segunda. Na sétima, Bento cruza os braços:
> — Vai abrir as duzentas no bloco de notas? Eu faço em uma linha. Você
> também vai fazer.

**Sua tarefa:** descobrir em quais conversas o operador `mare_alta`
escorregou e montar a flag `VAZANTE{...}` com o que ele mandou "guardar",
na ordem em que as conversas aconteceram.

## 🎯 Ao final de hoje você sabe

- [ ] Achar arquivos por nome, tipo, tamanho e pasta (`find`)
- [ ] Rodar um comando para **cada** arquivo com laços (`for`, `while read`)
- [ ] Transformar uma lista em argumentos com `xargs` (`-0`, `-I`, `-n`, `-P`)
- [ ] Converter arquivos em massa (`.txt` → `.csv`)
- [ ] Apagar e compactar em lote — com segurança
- [ ] Usar `find -exec` como alternativa ao `xargs`

## 📖 Conceito em 2 minutos

Processamento em lote é sempre a mesma receita em três passos:

```text
  1. LISTAR           2. FILTRAR / AGIR             3. JUNTAR
  find ... ─────────► xargs comando / for ... ─────► sort, wc, zip...
  "quais arquivos?"   "o que fazer com cada um?"    "qual o resultado?"
```

O `find` responde "quais arquivos?". O `xargs` (ou um laço) responde "faça
isto com cada um". E o resto do pipe resume tudo.

Por que `xargs` e não só `for`? Porque o `xargs` agrupa vários arquivos numa
única chamada do comando (muito mais rápido) e ainda roda em paralelo com
`-P`. Já o `for` é mais fácil de ler quando você precisa fazer várias coisas
com cada arquivo.

## ⌨️ Mão na massa

Tudo está em [`comandos.sh`](comandos.sh), comentado linha a linha.

### 1. Medir o lote

```bash
find desafio/conversas -name "*.txt" -type f | wc -l   # quantos arquivos
du -sh desafio/conversas                                # quanto espaço
find desafio/conversas -type f -size +400c | wc -l      # quantos com mais de 400 bytes
```

### 2. Um laço para cada arquivo

```bash
# jeito do curso original (quebra com nomes que têm espaço):
for i in $(find desafio/conversas -name "*.txt" -type f); do echo "$i"; done

# jeito seguro:
find desafio/conversas -name "*.txt" -print0 |
  while IFS= read -r -d '' arquivo; do echo "$arquivo"; done
```

### 3. Conversão em massa

```bash
for arquivo in copia/*.txt; do
  sed 's/ | /;/g' "$arquivo" > "${arquivo%.txt}.csv"   # troca o separador
done
```

`${arquivo%.txt}` corta o `.txt` do fim do nome. Trabalhe sempre numa
**cópia**: conversão em massa errada em evidência original não tem volta.

### 4. xargs

```bash
find desafio/conversas -name '*.txt' -print0 | xargs -0 wc -l      # todos de uma vez
find desafio/conversas -name '*.txt' -print0 | xargs -0 grep -l cashback   # quais citam
find pasta -name "*.zip" -type f | xargs rm -f                   # apagar em lote
xargs -I nome zip selecionadas desafio/conversas/nome < desafio/selecionadas.txt
find ... -print0 | xargs -0 -n 20 -P 4 comando                   # 4 em paralelo
```

### 5. find -exec

```bash
find desafio/conversas -name 'conversa-00[1-3].txt' -exec wc -l {} +
```

## 🇧🇷 Versão brazuca

Os **Diários Oficiais** (da União, dos estados e dos municípios) são o
melhor exemplo de lote: um PDF por dia, anos de edições. O projeto
[Querido Diário](https://queridodiario.ok.org.br/), da Open Knowledge Brasil,
coleta diários de centenas de municípios e oferece uma
[API pública](https://queridodiario.ok.org.br/api/docs). Com os PDFs
baixados (Dia 5 ensina a baixar; Dia 12 a extrair texto de PDF), a busca em
lote fica assim:

```bash
# quais edições citam a empresa investigada?
find diarios/ -name '*.txt' -print0 | xargs -0 grep -il 'nome da empresa' | sort

# quantas citações por ano?
find diarios/ -name '*.txt' -print0 | xargs -0 grep -il 'nome da empresa' \
  | cut -d/ -f2 | sort | uniq -c
```

Contratos, nomeações e licitações aparecem ali, com data. É OSINT em lote
com fonte 100% pública.

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) refaz o dia com `pathlib`, `zipfile`,
`collections` e `concurrent.futures`.

| Terminal | Python (stdlib) |
|---|---|
| `find -name '*.txt' -type f` | `Path(...).rglob("*.txt")` |
| `find -size +400c` | `p.stat().st_size > 400` |
| `for a in ...; do ... done` | `for p in sorted(...):` |
| `"${a%.txt}.csv"` | `p.with_suffix(".csv")` |
| `xargs grep -l palavra` | `[p for p in arqs if "palavra" in p.read_text()]` |
| `xargs rm -f` | `p.unlink(missing_ok=True)` |
| `xargs -P 4` | `ThreadPoolExecutor(4)` |
| `sort \| uniq -c \| sort -rn` | `Counter(...).most_common()` |

## 🚀 Além do curso

- **GNU `parallel`** (`apt install parallel`) é o `xargs -P` turbinado: barra de progresso, retomada de tarefas e log de cada execução. Ex.: `find . -name '*.pdf' | parallel pdftotext {}`.
- **`fd`** (pacote `fd-find`, comando `fdfind`) é um `find` moderno com execução embutida: `fdfind -e txt -x wc -l` roda `wc -l` em cada `.txt`, em paralelo.
- **[ripgrep](https://github.com/BurntSushi/ripgrep)** (`apt install ripgrep`, comando `rg`) busca em milhares de arquivos muito mais rápido que `find | xargs grep`: `rg -l mare_alta desafio/conversas`.

## 🧩 Desafio

1. Liste todas as conversas em `desafio/conversas/`.
2. Filtre só as que citam o operador `mare_alta` (sem abrir uma por uma!).
3. Ordene pelo caminho do arquivo (data + número = ordem em que aconteceram).
4. Em cada uma, pegue o que vem depois de `guarda isso:` e junte tudo.
5. Confira: `bash checar.sh 'VAZANTE{...}'`

<details>
<summary>💡 Dica 1</summary>

`find desafio/conversas -name '*.txt' -print0 | xargs -0 grep -l 'mare_alta' | sort`
dá a lista de arquivos, já em ordem. Cuidado: a vítima que comenta que "a
maré tá alta" na praia não é o operador.
</details>

<details>
<summary>💡 Dica 2</summary>

Mande a lista para `xargs grep -h '| mare_alta |'`, corte o começo da linha
com `sed 's/.*guarda isso: //'` e cole os pedaços com `tr -d '\n'`.
</details>

A solução comentada está em [`solucoes/dia-04.sh`](../../solucoes/dia-04.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- **`xargs rm` não perdoa.** Sempre rode o `find` sozinho primeiro, leia a
  lista e só depois acrescente `| xargs rm`. Um asterisco no lugar errado
  apaga o caso inteiro.
- Conversas de vítimas são **dados pessoais** — às vezes sensíveis (saúde,
  finanças, família). Jurema lembra: guarde só o necessário, em pasta
  protegida, e use números ("vítima 017") em vez de nomes nos relatórios.
- Processar em lote acelera também o erro: confira uma amostra à mão antes
  de confiar no resultado de 200 arquivos.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 3](../dia-03-instalar-programas/) · [Índice](../../README.md) · [Dia 5](../dia-05-curl-e-apis/) ➡️
