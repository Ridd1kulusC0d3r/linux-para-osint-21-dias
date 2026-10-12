# Dia 10 — Dois grupos, um número 🔗

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-10.ipynb)
&nbsp;**Rank C** · ⏱️ ~45 min · 📖 Original: *Day 10. Text analyzing and editing utilities* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> Duas vítimas, sem se conhecerem, mandaram ao Núcleo a lista de membros dos
> grupos de "suporte" onde caíram: **Cashback VIP** e **Suporte Pix**. Uma
> exportou em CSV, a outra copiou de um jeito todo próprio — ponto e vírgula,
> colunas trocadas, apelidos em MAIÚSCULAS.
>
> Bento coloca as duas lado a lado na tela:
> — Golpista economiza chip. Se o mesmo número administra os dois grupos, é a
> nossa ponte.
>
> Jurema, da porta:
> — São telefones de gente. Cruza, acha o que importa e **não** espalha o resto.

**Sua tarefa:** encontrar o **único** telefone que aparece nos dois grupos e
montar a flag com o apelido dele em cada grupo, em minúsculas:
`VAZANTE{<apelido_no_grupo_A>_<apelido_no_grupo_B>}`.

## 🎯 Ao final de hoje você sabe

- [ ] Juntar arquivos com `cat` e medir com `wc`
- [ ] Recortar colunas e caracteres com `cut` (`-d`, `-f`, `-c`)
- [ ] Ordenar com `sort` (`-r`, `-n`, `-u`, `-t -k`) e lidar com repetidos com `uniq` (`-c`, `-d`)
- [ ] Montar rankings com `sort | uniq -c | sort -rn`
- [ ] Cruzar listas com `comm` e comparar versões com `diff`
- [ ] Padronizar texto com `tr` e colar colunas com `paste`

## 📖 Conceito em 2 minutos

Esses comandos são pequenos e fazem **uma coisa só**. A força vem de
encadeá-los com o cano `|` (pipe): a saída de um vira a entrada do outro.

```text
grupo-a.csv ─► tail -n +2 ─► cut -d, -f1 ─► sort -u ─┐
                (tira o       (só a coluna    (ordena e     ├─► comm -12 ─► número em comum
                cabeçalho)    de telefone)    tira repet.)  │
grupo-b.txt ─► tail -n +2 ─► cut -d';' -f2 ─► sort -u ─┘
```

Dois detalhes que derrubam iniciantes:

- `uniq` só remove repetidos **vizinhos**. Sempre `sort` antes.
- `comm` exige as duas listas **ordenadas**. Sem `sort`, ele erra calado (ou reclama).

## ⌨️ Mão na massa

O arquivo [`comandos.sh`](comandos.sh) tem tudo comentado; rode inteiro com
`bash comandos.sh`.

### 1. Juntar e contar

```bash
cat file1.txt file2.txt > file3.txt     # junta dois arquivos num novo
cat *.txt > alltext/file4.txt           # junta todos os .txt
wc -l desafio/*.csv                     # linhas de cada arquivo (+ total)
```

### 2. Recortar

```bash
cut -c 1 desafio/grupo-a-cashback-vip.csv        # 1º caractere de cada linha
cut -c 5-10 desafio/grupo-a-cashback-vip.csv     # caracteres 5 a 10
cut -d, -f1 desafio/grupo-a-cashback-vip.csv     # campo 1, separado por vírgula
cut -d';' -f2 desafio/grupo-b-suporte-pix.txt    # campo 2, separado por ;
tail -n +2 arquivo                               # tudo menos a 1ª linha (cabeçalho)
```

### 3. Ordenar e contar repetidos

```bash
sort arquivo        # alfabética          sort -r   invertida
sort -n arquivo     # numérica            sort -u   sem repetidos
sort -t, -k2 arq    # pela coluna 2, com vírgula como separador
sort arq | uniq     # remove repetidos    uniq -d   só os repetidos
sort arq | uniq -c | sort -rn | head     # ranking: quem aparece mais
```

### 4. Cruzar e comparar

```bash
comm -12 a.txt b.txt    # só o que está nos DOIS (listas ordenadas!)
comm -23 a.txt b.txt    # só no a
comm -13 a.txt b.txt    # só no b
diff ontem.csv hoje.csv       # < saiu   > entrou
diff -u ontem.csv hoje.csv    # formato do Git: - saiu   + entrou
```

### 5. Transformar e colar

```bash
tr '[:upper:]' '[:lower:]'    # MAIÚSCULAS -> minúsculas (também com acentos)
tr ';' ','                    # troca separador
tr -d '() -'                  # apaga parênteses, espaços e hífens: (31) 90000-1234 -> 31900001234
paste -d, tel.txt nomes.txt   # cola dois arquivos lado a lado
paste -sd+ numeros.txt        # 3+5+8 (todas as linhas numa só)
```

## 🇧🇷 Versão brazuca

Cruzar listas é o pão com manteiga de quem investiga dinheiro público. O
**Portal da Transparência** (<https://portaldatransparencia.gov.br/download-de-dados>)
oferece CSVs de servidores, sanções (CEIS/CNEP) e pagamentos. Um exercício
clássico: quais empresas sancionadas no CEIS aparecem também numa lista de
fornecedores?

```bash
# os CSVs do portal usam ; e vêm em Latin-1: converta antes
iconv -f latin1 -t utf-8 CEIS.csv > ceis.csv
cut -d';' -f4 ceis.csv | tr -d '"./-' | sort -u > cnpj-sancionados.txt
cut -d';' -f2 fornecedores.csv | tr -d '"./-' | sort -u > cnpj-fornecedores.txt
comm -12 cnpj-sancionados.txt cnpj-fornecedores.txt
```

(Os números de coluna variam conforme o arquivo; confira com `head -n 1`.)
O `tr -d` que tira pontuação é o truque que faz `12.345.678/0001-90` e
`12345678000190` virarem a mesma coisa.

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) faz o cruzamento com **conjuntos**: em
Python, `comm -12` é simplesmente `set(a) & set(b)`.

| Terminal | Python (stdlib) |
|---|---|
| `cut -d, -f1` | `linha.split(",")[0]` ou `csv.DictReader` |
| `cut -c 5-10` | `linha[4:10]` |
| `sort -u` | `sorted(set(x))` |
| `sort \| uniq -c \| sort -rn` | `collections.Counter(x).most_common()` |
| `comm -12 a b` | `set(a) & set(b)` |
| `diff -u a b` | `difflib.unified_diff(a, b)` |
| `tr '[:upper:]' '[:lower:]'` | `texto.lower()` |
| `paste -d, a b` | `",".join(par) for par in zip(a, b)` |

## 🚀 Além do curso

- **Miller** (`apt install miller`, comando `mlr`): `cut`/`sort`/`uniq` que
  entendem cabeçalho de CSV e JSON. Ex.: `mlr --icsv --opprint count-distinct -f telefone grupo-a.csv`.
- **phonenumbers** (`pip install phonenumbers`): biblioteca Python (port da
  libphonenumber do Google) que valida e padroniza telefones brasileiros para
  o formato E.164 (`+5531...`) — essencial antes de cruzar listas reais.
- **`datamash`** (`apt install datamash`): estatísticas e agrupamentos no
  terminal (`datamash -t, -s -g 1 count 1`).

## 🧩 Desafio

1. Extraia só os telefones de cada grupo (cuidado: separadores e colunas diferentes).
2. Ordene sem repetidos e cruze as listas.
3. Ache o apelido do número em comum em cada grupo, em minúsculas.
4. Confira: `bash checar.sh 'VAZANTE{apelidoA_apelidoB}'`

<details>
<summary>💡 Dica 1</summary>

No grupo A o telefone é o campo 1 (`cut -d, -f1`); no grupo B é o campo 2
(`cut -d';' -f2`). Não esqueça do `tail -n +2` para tirar o cabeçalho.
</details>

<details>
<summary>💡 Dica 2</summary>

`comm -12 <(... | sort -u) <(... | sort -u)` — o `<( )` faz a saída de um
comando parecer um arquivo. Depois, `grep -F 'número'` em cada lista e
`tr '[:upper:]' '[:lower:]'`.
</details>

A solução comentada está em [`solucoes/dia-10.sh`](../../solucoes/dia-10.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- Listas de membros de grupos são **dados pessoais** (LGPD, art. 5º, I). Cruze
  para achar o suspeito, mas não redistribua a lista inteira nem exponha
  vítimas que só estavam no grupo.
- Um número em comum é **indício**, não prova: chips são emprestados,
  clonados e reciclados pelas operadoras. Corrobore com outras fontes.
- Ao pedir listas a vítimas, registre de quem veio cada arquivo e quando
  (cadeia de custódia) — e guarde o original intocado.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 9](../dia-09-screen-e-cron/) · [Índice](../../README.md) · [Dia 11](../dia-11-video-audio-imagem/) ➡️
