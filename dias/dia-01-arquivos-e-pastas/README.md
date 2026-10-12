# Dia 1 — O que ninguém vê 🗂️

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-01.ipynb)
&nbsp;**Rank D** · ⏱️ ~40 min · 📖 Original: *Day 1. Basic skills of working with files and directories in command line* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> O pendrive tem uma pasta `caso/` e nada mais parece interessante. Relatos de
> vítimas, um arquivo sobre a PixVelox, uns rascunhos. Você abre tudo no
> explorador de arquivos e não acha nada. Lembra do bilhete: *"comece pelo que
> ninguém vê"*.
>
> Bento passa atrás da sua cadeira, olha a tela e ri:
> — Explorador de arquivos esconde coisa, recruta. O terminal não.

**Sua tarefa:** encontrar a nota que a Mestra Iara escondeu dentro de
`desafio/caso/` e extrair a flag `VAZANTE{...}`.

## 🎯 Ao final de hoje você sabe

- [ ] Descobrir onde está (`pwd`) e o que tem na pasta (`ls`)
- [ ] Navegar entre pastas (`cd`) com caminhos relativos e absolutos
- [ ] Ver arquivos **ocultos** (`ls -a`) e procurar arquivos (`find`)
- [ ] Ler arquivos (`cat`, `head`, `tail`)
- [ ] Criar, copiar, mover e apagar (`mkdir`, `touch`, `cp`, `mv`, `rm`)
- [ ] Ler datas de um arquivo (`stat`) e pedir ajuda (`--help`, `man`)

## 📖 Conceito em 2 minutos

O Linux organiza tudo numa **árvore** que começa em `/` (a raiz). Cada pasta
pode ter arquivos e outras pastas. Você está sempre "parado" em alguma pasta —
o **diretório atual**. Os comandos agem a partir dali.

```text
/                      ← raiz
└── home/
    └── você/          ← ~  (sua pasta pessoal)
        └── linux-para-osint-21-dias/
            └── dias/dia-01-arquivos-e-pastas/   ← você está aqui
                └── desafio/caso/
```

Dois atalhos que você vai usar o tempo todo: `.` é "a pasta atual" e `..` é
"a pasta de cima". E uma regra que vale ouro em OSINT: **arquivo cujo nome
começa com ponto é oculto**. Configurações, caches, históricos… e às vezes,
pistas.

## ⌨️ Mão na massa

Abra o terminal na pasta do Dia 1 (ou o notebook no Colab) e siga junto. O
arquivo [`comandos.sh`](comandos.sh) tem tudo comentado linha a linha; rode
inteiro com `bash comandos.sh`.

### 1. Onde estou e o que tem aqui

```bash
pwd          # mostra a pasta atual
ls           # lista o conteúdo
ls -lh       # formato longo, com tamanhos legíveis
```

### 2. Navegando

```bash
cd desafio/caso      # entra (caminho relativo)
cd ..                # sobe um nível
cd -                 # volta para onde estava
cd ~                 # vai para a sua pasta pessoal
```

### 3. Vendo o invisível

```bash
ls -la               # -a mostra os ocultos
ls -laR              # -R desce por todas as subpastas
find . -type f -name '.*'   # só arquivos ocultos, em qualquer profundidade
```

### 4. Lendo

```bash
cat LEIA-ME.txt                  # tudo
head -n 3 vitimas/lista-preliminar.txt   # só o começo
tail -n 2 vitimas/lista-preliminar.txt   # só o final
```

### 5. Organizando o seu caso

```bash
mkdir -p meu-caso/{evidencias,notas,relatorio}   # cria 3 pastas de uma vez
echo "Dia 1 — recebi o pendrive" >  meu-caso/notas/diario.txt   # cria/sobrescreve
echo "Dia 1 — achei os ocultos"  >> meu-caso/notas/diario.txt   # acrescenta
cp -rp desafio/caso/vitimas meu-caso/evidencias/   # copia preservando datas
mv meu-caso/notas/rascunho.txt meu-caso/notas/hipoteses.txt    # renomeia
rm -r meu-caso        # apaga SEM lixeira — cuidado!
```

### 6. Datas e ajuda

```bash
stat desafio/caso/vitimas/belo-horizonte/relato-001.txt   # datas de acesso/modificação
ls --help | head       # ajuda rápida
man ls                 # manual completo (sai com q)
```

## 🇧🇷 Versão brazuca

Monte agora a estrutura que você vai usar em **todas** as investigações reais.
Ela segue a lógica de cadeia de custódia (original intocado, trabalho em cópia):

```bash
CASO="caso-$(date +%Y%m%d)-pixvelox"
mkdir -p "$CASO"/{00-original,01-copias,02-notas,03-relatorio}
echo "Aberto em $(date '+%d/%m/%Y %H:%M') por $(whoami)" > "$CASO/02-notas/abertura.txt"
ls -R "$CASO"
```

Prefixos numéricos (`00-`, `01-`…) mantêm as pastas na ordem certa no `ls`.
A data no formato `AAAAMMDD` faz os casos aparecerem em ordem cronológica.

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) faz tudo isso só com a biblioteca padrão
(`pathlib`, `shutil`). Repare numa diferença importante: **o Python mostra
arquivos ocultos por padrão**, o `ls` não.

| Terminal | Python (stdlib) |
|---|---|
| `pwd` | `Path.cwd()` |
| `ls -la` | `Path.iterdir()` |
| `find . -name '.*'` | `Path.rglob(".*")` |
| `cat` | `Path.read_text()` |
| `mkdir -p` | `Path.mkdir(parents=True, exist_ok=True)` |
| `cp -r` | `shutil.copytree()` |
| `stat` | `Path.stat()` |

## 🚀 Além do curso

- **`tree`** desenha a árvore de pastas: `tree -a desafio/caso` (o `-a` inclui ocultos). Instale com `apt install tree`.
- **`fd`** é um `find` moderno e muito mais rápido, com sintaxe simples:
  `fd -H . desafio/caso` (o `-H` inclui ocultos). No Ubuntu o pacote é `fd-find` e o comando se chama `fdfind`.
- Em Python, `os.scandir()` é a forma mais rápida de listar pastas enormes (milhões de arquivos de um vazamento, por exemplo).

## 🧩 Desafio

1. Entre em `desafio/caso/`.
2. Encontre **todos** os arquivos ocultos.
3. Um deles é pista falsa. O outro tem a flag.
4. Confira: `bash checar.sh 'VAZANTE{...}'`

<details>
<summary>💡 Dica 1</summary>

`ls` sozinho não mostra arquivos que começam com ponto.
</details>

<details>
<summary>💡 Dica 2</summary>

`find . -type f -name '.*'` lista todos os ocultos de uma vez. Depois é só `cat`.
</details>

A solução comentada está em [`solucoes/dia-01.sh`](../../solucoes/dia-01.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- **Nunca altere a evidência original.** Copie com `cp -p` e trabalhe na cópia.
- `rm` não tem lixeira. Em pasta de evidência, prefira `rm -i` ou simplesmente não apague.
- Ao baixar arquivos de um alvo, lembre que **você** também deixa rastros:
  pastas ocultas como `~/.bash_history` registram o que você digitou.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 0](../dia-00-preparacao/) · [Índice](../../README.md) · [Dia 2](../dia-02-bash-script/) ➡️
