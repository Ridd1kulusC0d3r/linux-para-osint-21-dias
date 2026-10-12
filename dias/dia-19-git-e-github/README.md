# Dia 19 — O commit apagado 🌿

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-19.ipynb)
&nbsp;**Rank B** · ⏱️ ~60 min · 📖 Original: *Day 19. Git and Github* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> Bento entra correndo na sala, notebook aberto.
> — Achei! O site da PixVelox estava num repositório público. Seis commits.
> O cara subiu um `config.env` e apagou catorze minutos depois. Já era,
> sumiu.
>
> A Mestra Iara nem tira os olhos do café.
> — Bento, o git é um diário que **não aceita borracha**. Apagar um arquivo
> é só escrever mais uma página dizendo "apaguei". As páginas de antes
> continuam lá.
>
> Antes que o repositório saísse do ar, a equipe salvou tudo num arquivo:
> `desafio/vazantes.bundle`.

**Sua tarefa:** clonar o repositório a partir do bundle, encontrar o arquivo
que maré_alta apagou e recuperar a `PAINEL_CHAVE` — a flag `VAZANTE{...}`.
De quebra, descobrir que e-mail pessoal escapou num dos commits.

## 🎯 Ao final de hoje você sabe

- [ ] Instalar o git e **clonar** um repositório (`git clone`)
- [ ] Ler a linha do tempo com `git log` (e formatos como `%an <%ae>`)
- [ ] Ver o que cada commit mudou: `git show`, `git log -p`, `git diff`
- [ ] Fazer o ciclo `git add` → `git commit` → `git push` e checar com `git status`
- [ ] Encontrar arquivos **apagados** e recuperá-los do histórico
- [ ] Extrair **e-mails de autores** de commits (OSINT clássico)

## 📖 Conceito em 2 minutos

Um repositório git é uma pasta com uma pasta oculta `.git/` dentro. Nela
mora **todo** o histórico: cada **commit** é uma fotografia completa dos
arquivos, com autor, e-mail, data e mensagem.

```text
f825acf ── aa1bfb9 ── 856ddca ── 647d7b6 ── 242c143 ── befd85d  ← HEAD (agora)
primeiro   cashback   +config    -config    roteiro    readme
                      .env       .env
                        ▲
                        └── o conteúdo continua aqui para sempre
```

Clonar = baixar **a pasta `.git` inteira**. Por isso, quem clona recebe
todas as versões de todos os arquivos — inclusive senhas que o autor
"apagou". Para remover de verdade é preciso reescrever o histórico (e, se
já foi publicado, é tarde: alguém pode ter clonado).

E todo commit carrega `nome <e-mail>` de quem fez. Basta uma máquina mal
configurada para um e-mail pessoal vazar.

## ⌨️ Mão na massa

### 1. Instalar e clonar

```bash
sudo apt install git
git clone desafio/vazantes.bundle pxv-site     # de um bundle (offline)
git clone https://github.com/USUARIO/REPO      # do GitHub
cd pxv-site && ls -la && cat README.md
```

### 2. Linha do tempo e autores

```bash
git log --oneline
git log --stat
git log --format='%an <%ae>' | sort | uniq -c        # quem commitou, com e-mail
git log --format='%ad %s' --date=format:'%d/%m %H:%M'  # horários (hábitos!)
```

### 3. O que mudou

```bash
git show HEAD                 # último commit, com a diferença
git show HEAD~2               # dois commits atrás
git diff HASH1 HASH2          # compara duas versões
git log -p -- config.env      # todas as mudanças de um arquivo
```

### 4. O que foi apagado

```bash
git log --diff-filter=D --name-only    # commits que apagaram arquivos
git show HASH^:config.env              # o arquivo como era ANTES do commit HASH
git log -S 'PAINEL_' --oneline         # commits que puseram/tiraram esse texto
```

### 5. Seu próprio commit

```bash
ls > test.txt
git status                     # ?? test.txt  (não rastreado)
git add test.txt
git commit -m "minha mensagem" # sem -m, abre um editor
git push                       # envia ao remoto (GitHub pede login/token)
git status
```

## 🇧🇷 Versão brazuca

Muitos dados públicos brasileiros vivem no GitHub, e o histórico mostra
**quando** e **como** cada coisa mudou:

```bash
# Querido Diário (Open Knowledge Brasil): raspadores de diários oficiais
git clone https://github.com/okfn-brasil/querido-diario
cd querido-diario
git log --format='%ad %an %s' --date=short | head      # quem mexeu, quando
```

Para ver de onde veio um e-mail em projetos públicos, a própria interface do
GitHub ajuda: acrescente **`.patch`** ao endereço de um commit
(`https://github.com/USUARIO/REPO/commit/HASH.patch`) e a primeira linha
`From:` mostra nome e e-mail do autor.

## 🐍 Ponte Python

A stdlib não tem módulo git; [`equivalente.py`](equivalente.py) chama o
programa `git` com `subprocess` e mostra como o git **dá nome aos arquivos**:
o SHA-1 de `blob <tamanho>\0<conteúdo>`.

| Terminal | Python (stdlib) |
|---|---|
| `git clone X pasta` | `subprocess.run(["git", "clone", X, pasta])` |
| `git log --format=...` | `subprocess.run(..., capture_output=True).stdout` |
| `sort \| uniq -c` | `collections.Counter` |
| `git hash-object arquivo` | `hashlib.sha1(b"blob %d\0" % len(c) + c)` |
| pasta temporária | `tempfile.TemporaryDirectory()` |

## 🚀 Além do curso

- **gitleaks** (github.com/gitleaks/gitleaks) — varre todo o histórico atrás
  de chaves, tokens e senhas: `gitleaks git pxv-site`. Defensores usam para
  limpar; investigadores, para achar.
- **trufflehog** (github.com/trufflesecurity/trufflehog) — mesma ideia, e
  ainda **testa** se a credencial encontrada está ativa (não faça isso em
  sistemas de terceiros: é acesso indevido).
- **GitHub CLI** (`apt install gh`) — busca código e repositórios pelo
  terminal: `gh search code "pixvelox" --limit 20`.

## 🧩 Desafio

1. Clone `desafio/vazantes.bundle` para uma pasta de trabalho.
2. Descubra qual commit **apagou** um arquivo.
3. Recupere o conteúdo desse arquivo do commit **anterior**.
4. Copie o valor de `PAINEL_CHAVE`.
5. Confira: `bash checar.sh 'VAZANTE{...}'`
6. Bônus: qual e-mail pessoal de maré_alta aparece nos autores?

<details>
<summary>💡 Dica 1</summary>

`git log --diff-filter=D --name-only` mostra o commit que apagou e o nome do
arquivo.
</details>

<details>
<summary>💡 Dica 2</summary>

`git show HASH^:config.env` (o `^` significa "o commit anterior a HASH"). Ou
simplesmente `git log -p -- config.env`.
</details>

A solução comentada está em [`solucoes/dia-19.sh`](../../solucoes/dia-19.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- **Achar não é usar.** Encontrar uma senha num repositório público é OSINT;
  **testá-la** para entrar no painel é acesso não autorizado (Lei 12.737/2012).
  Documente e encaminhe.
- **O seu e-mail também vaza.** Antes de commitar em repositórios públicos,
  configure `git config --global user.email` com o e-mail *noreply* que o
  GitHub oferece. Investigador também deixa rastro.
- **Nunca commite segredos** nos seus projetos. Use `.gitignore` *antes* do
  primeiro commit — depois, já está no histórico.
- **LGPD:** e-mails de commits são dados pessoais de quem os escreveu. Use só
  na finalidade da investigação.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 18](../dia-18-investigacao-de-dominio/) · [Índice](../../README.md) · [Dia 20](../dia-20-ferramentas-uteis/) ➡️
