# Dia 7 — Seguindo o dinheiro 💸

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-07.ipynb)
&nbsp;**Rank D** · ⏱️ ~50 min · 📖 Original: *Day 7. Sed and Awk* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> Chegou a resposta do ofício: um extrato com 240 transferências saindo das
> contas das vítimas em março, e uma lista de "apelidos" que o painel da
> PixVelox dava para as contas de destino.
>
> — A conta que mais aparece é a CT-0450 — você arrisca.
>
> Bento nem levanta a cabeça.
> — Aparecer muito não é receber muito. Some os valores. Por conta. E tira
> os estornos, que esse dinheiro voltou. Isso é **uma** linha de `awk`.
>
> Mestra Iara completa:
> — E quando achar a conta, limpe o apelido dela. Exportação de painel
> sempre vem suja.

**Sua tarefa:** descobrir qual conta de destino **recebeu mais dinheiro** em
PIX e limpar o apelido dela em `desafio/contas.txt`. A flag é
`VAZANTE{apelido_limpo}`.

## 🎯 Ao final de hoje você sabe

- [ ] Substituir texto com `sed 's/velho/novo/'` e `s///g`
- [ ] Imprimir linhas específicas e intervalos (`sed -n 7p`, `sed -n 5,9p`)
- [ ] Apagar linhas e editar uma cópia no lugar (`sed '/x/d'`, `sed -i`)
- [ ] Ler colunas com `awk -F,` e numerar linhas (`NR`, `$0`)
- [ ] Filtrar linhas (`/^v/`, `$3 > 1000`, `$5 == "PIX"`)
- [ ] **Somar por grupo** com arrays do `awk` (`soma[$3] += $4`)

## 📖 Conceito em 2 minutos

`sed` e `awk` leem um texto **linha a linha**, como uma esteira:

```text
               sed  → edita a linha     (trocar, apagar, imprimir)
linha ──► [ ]
               awk  → entende COLUNAS   (filtrar, calcular, resumir)
```

O `awk` corta cada linha em campos. Com `-F,` o corte é na vírgula:

```text
2026-03-01,vitima_386,CT-0588,904.75,ESTORNO
    $1         $2        $3     $4      $5          $0 = a linha inteira
```

Um programa `awk` é `padrão { ação }`: se a linha bate com o padrão, faz a
ação. O bloco especial `END { ... }` roda depois da última linha — é onde
você imprime os totais.

## ⌨️ Mão na massa

Tudo está em [`comandos.sh`](comandos.sh), comentado linha a linha.

### 1. sed: substituir

```bash
sed 's/Normal/SUSPEITO/' desafio/relatorio.txt      # 1ª ocorrência por linha
sed 's/[0-9]/#/g' desafio/digitos.txt               # todas (g = global)
sed '1,3 s/Normal/CONFERIDO/g' desafio/relatorio.txt   # só nas linhas 1 a 3
```

### 2. sed: escolher e apagar linhas

```bash
sed -n 7p desafio/relatorio.txt       # só a linha 7
sed -n 5,9p desafio/relatorio.txt     # da 5 à 9
sed '/^linha/d' desafio/relatorio.txt # apaga as que começam com "linha"
sed -i 's/a/b/g' copia.txt            # edita o arquivo (só em cópia!)
```

### 3. awk: linhas e colunas

```bash
awk '{print $0}' desafio/vitimas.csv          # tudo
awk '{print NR, $0}' desafio/vitimas.csv      # numerado
awk -F, '{print $1, $3}' desafio/vitimas.csv  # colunas 1 e 3
```

### 4. awk: filtros

```bash
awk '/^v/' desafio/vitimas.csv                          # começa com v
awk -F, 'NR > 1 && $3 > 1000' desafio/vitimas.csv       # pula o cabeçalho; valor > 1000
awk -F, '$5 == "ESTORNO"' desafio/extrato.csv           # compara texto
```

### 5. awk: somas

```bash
awk -F, 'NR > 1 {total += $3} END {print total}' desafio/vitimas.csv
awk -F, 'NR > 1 {soma[$2] += $3} END {for (c in soma) print soma[c], c}' desafio/vitimas.csv
```

## 🇧🇷 Versão brazuca

O [Portal da Transparência](https://portaldatransparencia.gov.br/download-de-dados)
publica em CSV as despesas do governo federal, os cartões de pagamento e as
transferências a estados e municípios. Esses arquivos usam **ponto e
vírgula** como separador e **vírgula decimal** (`1.234,56`). Com `sed` e
`awk` você ajusta e soma:

```bash
# depois de baixar e extrair (Dias 3 e 5):
# 1) sed tira o ponto de milhar e troca a vírgula decimal por ponto
# 2) awk soma a coluna de valor (aqui a 8ª, confira no cabeçalho!) por favorecido (5ª)
sed -e 's/\.//g' -e 's/,/./g' arquivo.csv \
  | awk -F';' 'NR > 1 {soma[$5] += $8} END {for (f in soma) printf "%.2f;%s\n", soma[f], f}' \
  | sort -t';' -k1 -rn | head
```

Antes de somar, olhe o cabeçalho com `head -n 1 arquivo.csv | tr ';' '\n' | nl`
para saber o número de cada coluna. E repare nas aspas: se um campo tiver
`;` dentro de aspas, o `awk` simples se perde — aí use `csvkit` (Dia 14).

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) usa `re`, `csv` e `collections`.

| Terminal | Python (stdlib) |
|---|---|
| `sed 's/a/b/'` | `linha.replace("a", "b", 1)` |
| `sed 's/[0-9]/#/g'` | `re.sub(r"[0-9]", "#", linha)` |
| `sed -n 5,9p` | `linhas[4:9]` |
| `sed '/x/d'` | `[l for l in linhas if "x" not in l]` |
| `awk '{print NR, $0}'` | `enumerate(linhas, 1)` |
| `awk -F, '{print $1}'` | `csv.reader(f)` → `campos[0]` |
| `soma[$3] += $4` | `defaultdict(float)` |
| `n[$3]++` | `Counter(...)` |

## 🚀 Além do curso

- **[Miller](https://miller.readthedocs.io/)** (`apt install miller`, comando `mlr`) é um "awk que entende CSV de verdade" — aspas, cabeçalhos e JSON: `mlr --icsv --opprint stats1 -a sum -f valor -g destino desafio/extrato.csv`.
- **[DuckDB](https://duckdb.org/)** (`pip install duckdb`) roda SQL direto em CSVs gigantes, sem importar nada: `SELECT destino, sum(valor) FROM 'extrato.csv' GROUP BY 1`. Também tem linha de comando própria.
- **`sd`** (pacote `sd` no Debian/Ubuntu recentes) é um `sed` moderno para substituições, com regex mais simples de escrever: `sd '~' '_' arquivo`.

## 🧩 Desafio

1. Olhe o `desafio/extrato.csv` (`head`) e identifique as colunas.
2. Some a coluna `valor` por conta de `destino`, **só nas linhas PIX**.
3. Ache a conta que recebeu mais dinheiro.
4. Encontre o apelido dela em `desafio/contas.txt` e limpe com `sed`: sem a
   conta, sem espaços, sem `##fim`, e com `~` trocado por `_`.
5. Confira: `bash checar.sh 'VAZANTE{apelido_limpo}'`

<details>
<summary>💡 Dica 1</summary>

`awk -F, 'NR > 1 && $5 == "PIX" {soma[$3] += $4} END {for (c in soma) print soma[c], c}' desafio/extrato.csv | sort -rn`
</details>

<details>
<summary>💡 Dica 2</summary>

`grep '^CT-XXXX ' desafio/contas.txt | sed -e 's/^[^;]*;[[:space:]]*//' -e 's/[[:space:]]*##fim$//' -e 's/~/_/g'`
</details>

A solução comentada está em [`solucoes/dia-07.sh`](../../solucoes/dia-07.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- **Dados bancários são protegidos por sigilo** (Lei Complementar 105/2001).
  Extrato de terceiro só chega a uma investigação por ordem judicial ou
  pelo próprio titular. Jurema não abre mão disso.
- Somar errado acusa a pessoa errada. Confira o separador, o cabeçalho, os
  estornos e uma amostra das linhas à mão antes de concluir.
- "Conta de destino" muitas vezes é de um **laranja** — alguém que também
  pode ser vítima. No relatório, escreva "conta que recebeu", não "golpista".
- `sed -i` sobrescreve o arquivo. Em evidência, trabalhe sempre numa cópia.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 6](../dia-06-grep/) · [Índice](../../README.md) · [Dia 8](../dia-08-vim/) ➡️
