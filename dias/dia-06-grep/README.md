# Dia 6 — Agulha no vazamento 🔍

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-06.ipynb)
&nbsp;**Rank D** · ⏱️ ~45 min · 📖 Original: *Day 6. Search in files. Grep* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> Chegaram dois arquivos de uma vez: a caixa de denúncias do Núcleo, com mil e
> quinhentas mensagens de vítimas, e — presente de uma fonte anônima — o log do
> "suporte" da PixVelox, com outras mil e quinhentas linhas.
>
> — Não leia — diz Bento, sem tirar o fone. — Filtra.
>
> Num post-it, a Mestra Iara deixou só uma frase: *"Golpista gosta de
> subdomínio."*

**Sua tarefa:** extrair os e-mails do log do falso suporte e encontrar o único
endereço que vive num subdomínio escondido de `pixvelox.example`. A parte
antes do `@` é a flag: `VAZANTE{...}`.

## 🎯 Ao final de hoje você sabe

- [ ] Procurar texto em arquivos (`grep`, `grep -F`)
- [ ] Ignorar maiúsculas (`-i`), numerar (`-n`), contar (`-c`), inverter (`-v`)
- [ ] Buscar em vários arquivos e pastas (`*.txt`, `-r`, `-l`)
- [ ] Usar classes de caracteres (`[0-9]`) e regex estendida (`-E`)
- [ ] Extrair só o pedaço que interessa (`-o`) — por exemplo, e-mails

## 📖 Conceito em 2 minutos

`grep` lê um texto linha por linha e devolve só as linhas que combinam com
um **padrão**. O padrão pode ser um texto fixo (`gmail`) ou uma **expressão
regular** — uma pequena linguagem para descrever formatos:

| Regex | Significa | Combina com |
|---|---|---|
| `[0-9]` | um dígito | `7` |
| `[a-z]+` | uma ou mais letras minúsculas | `suporte` |
| `.` | qualquer caractere | `x`, `@`, `3` |
| `\.` | um ponto de verdade | `.` |
| `{2,}` | 2 ou mais vezes | `br`, `com`, `example` |
| `^` / `$` | começo / fim da linha | |

Em OSINT, isso é ouro: e-mails, telefones, URLs, chaves PIX e hashes têm
**formato**. Formato vira regex, regex vira filtro, e um arquivo gigante vira
uma lista curta.

## ⌨️ Mão na massa

### 1. Busca simples

```bash
grep -F pixvelox desafio/denuncias.txt          # texto fixo
grep -cF pixvelox desafio/denuncias.txt         # só a contagem
grep -ciF pixvelox desafio/denuncias.txt        # ignorando maiúsculas
grep -n "remetente: suporte@" desafio/denuncias.txt   # com número da linha
```

### 2. Padrões e vários arquivos

```bash
grep '[0-9]' desafio/anotacoes/*.txt            # linhas com algum dígito
grep -n "LGPD" desafio/anotacoes/*.txt          # em todos os .txt da pasta
grep -rl "subdomínio" desafio/                  # -r recursivo, -l só nomes
ls -R desafio | grep ".txt"                     # filtrando a saída de outro comando
```

### 3. Tirando o ruído

```bash
grep -v "abriu atendimento" desafio/log-suporte.txt | grep -v "encerrou"
```

### 4. Extraindo e-mails

```bash
grep -Eo "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}" desafio/log-suporte.txt
```

> ⚠️ **Pegadinha:** muitas regex de e-mail (inclusive a do curso original) terminam em `{2,6}`.
> Terminações com mais de 6 letras, como `.example` ou `.technology`, ficam **cortadas**.
> Use `{2,}`. O `comandos.sh` mostra a diferença lado a lado.

### 5. Só os domínios, contados

```bash
grep -Eo "@[A-Za-z0-9.-]+\.[A-Za-z]{2,}" desafio/log-suporte.txt | sort | uniq -c | sort -rn
```

## 🇧🇷 Versão brazuca

Os mesmos truques valem para os formatos que mais aparecem em golpes no Brasil:

```bash
# telefones no formato (31) 90000-0000
grep -Eo '\([0-9]{2}\) 9?[0-9]{4}-[0-9]{4}' arquivo.txt

# CEP (00000-000)
grep -Eo '\b[0-9]{5}-[0-9]{3}\b' arquivo.txt

# links de Pix copia-e-cola começam com 000201
grep -Eo '000201[0-9A-Za-z.]{20,}' arquivo.txt
```

Achou um CEP? No Dia 5 você aprendeu a consultá-lo na BrasilAPI.

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) usa o módulo `re` e `collections.Counter`.

| Terminal | Python (stdlib) |
|---|---|
| `grep -F texto` | `"texto" in linha` |
| `grep -i` | `linha.lower()` |
| `grep -n` | `enumerate(linhas, start=1)` |
| `grep -v` | `"texto" not in linha` |
| `grep -Eo regex` | `re.findall(regex, texto)` |
| `grep -r` | `Path.rglob("*")` |
| `sort \| uniq -c` | `Counter(...)` |

## 🚀 Além do curso

- **`ripgrep` (`rg`)** é um grep moderno e muito mais rápido em pastas enormes; respeita o `.gitignore` e já busca recursivamente. No Ubuntu: `apt install ripgrep`.
- **`ugrep`** busca dentro de arquivos compactados (`zip`, `gz`) e PDFs sem extrair — útil em pacotes de vazamento. `apt install ugrep`.
- Em Python, a biblioteca **`regex`** (`pip install regex`) estende o `re` com classes Unicode como `\p{L}` (qualquer letra, com acento) — ótimo para nomes em português.

## 🧩 Desafio

1. Extraia todos os e-mails de `desafio/log-suporte.txt`.
2. Liste os domínios e repare nos que se parecem com `pixvelox.example`.
3. Um endereço vive num subdomínio que aparece **uma vez só**. Cuidado com as duas iscas.
4. A parte antes do `@` é a flag. Confira: `bash checar.sh 'VAZANTE{...}'`

<details>
<summary>💡 Dica 1</summary>

O último bloco do `comandos.sh` mostra cada domínio com sua contagem. Procure o que tem contagem 1.
</details>

<details>
<summary>💡 Dica 2</summary>

`cofre@pixvelox.example` e `cofre-pixvelox.example` não são a mesma coisa que `alguem@cofre.pixvelox.example`.
Use `grep -F '@cofre.pixvelox.example'` e depois `cut -d@ -f1`.
</details>

A solução comentada está em [`solucoes/dia-06.sh`](../../solucoes/dia-06.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- A caixa de denúncias tem e-mails de **vítimas**: é dado pessoal protegido pela LGPD. Use só para a investigação e nunca publique a lista.
- Arquivos de vazamento reais podem conter dados de milhões de pessoas. Ter acesso não autoriza divulgar — e em muitos casos nem guardar.
- Trabalhe em cópias e anote de onde veio cada arquivo (cadeia de custódia, Dia 1).

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) a regex que você mais vai usar e para quê.

---

⬅️ [Dia 5](../dia-05-curl-e-apis/) · [Índice](../../README.md) · [Dia 7](../dia-07-sed-e-awk/) ➡️
