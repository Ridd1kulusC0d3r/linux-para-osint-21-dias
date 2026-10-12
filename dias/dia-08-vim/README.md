# Dia 8 — A linha 4242 ✍️

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-08.ipynb)
&nbsp;**Rank C** · ⏱️ ~50 min · 📖 Original: *Day 8. Vim text editor* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> Às 18h a perícia entrega um presente envenenado: o log do servidor da
> PixVelox, **cinco mil linhas**, copiado de uma máquina que caiu antes de ser
> desligada. Você tenta abrir no bloco de notas do Colab; a aba engasga.
>
> A Mestra Iara deixa um bilhete na sua mesa e some de novo:
> *"Linha 4242. Ele troca todo `_` por `#MARE#`. Não salve no original."*
>
> Bento olha o arquivo por cima do seu ombro:
> — Vim. Abre, `:4242`, Enter. Só não me pergunte como sair.
> — Como eu saio?
> — Eu disse para não perguntar.

**Sua tarefa:** abrir `desafio/servidor-pixvelox.log` no Vim, ir até a linha
4242, desfazer o disfarce do maré_alta com uma substituição global e extrair
a flag `VAZANTE{...}`.

## 🎯 Ao final de hoje você sabe

- [ ] Entender os **modos** do Vim (normal, inserção, comando) e trocar entre eles
- [ ] **Sair** do Vim sem pânico (`:q`, `:q!`, `:wq`)
- [ ] Ir direto para uma linha (`:N`, `vim +N arquivo`)
- [ ] Buscar (`/texto`, `n`, `N`) e substituir em tudo (`:%s/velho/novo/g`)
- [ ] Apagar, copiar e colar linhas (`dd`, `yy`, `p`) e desfazer (`u`)
- [ ] Usar o Vim **sem interface** em scripts (`vim -es`, `ex`) — e o `vimtutor`

## 📖 Conceito em 2 minutos

O Vim é um editor de texto que roda **dentro do terminal**. Está em
praticamente todo servidor Linux do planeta — inclusive naquele servidor
suspeito onde você só tem SSH e nenhuma interface gráfica. Por isso vale
aprender o básico.

A grande diferença para um editor comum: o Vim tem **modos**.

```text
            i (inserir)                 : (dois pontos)
  ┌────────┐ ────────────► ┌──────────┐      ┌─────────────┐
  │ NORMAL │               │ INSERÇÃO │      │  COMANDO    │
  │ navegar│ ◄──────────── │ digitar  │      │ :w :q :%s   │
  └────────┘     Esc       └──────────┘      └─────────────┘
       ▲  └──────────────── : ──────────────────►  │
       └──────────────── Enter / Esc ──────────────┘
```

No modo **normal** as letras são comandos (`dd` apaga a linha, não digita
"dd"). Para escrever, aperte `i`. Para voltar, `Esc`. Para salvar, sair,
pular de linha ou substituir, `:` e o comando. Se perder o fio: **Esc, Esc,
`:q!`, Enter** — você sai sem estragar nada.

> **Colab x Vim:** o Colab não tem terminal interativo de verdade nas células,
> então o Vim trava a célula. No notebook nós mostramos o comando e rodamos a
> versão **não interativa** (`vim -es`). Para praticar com as mãos, use o
> GitHub Codespaces (terminal completo no navegador), uma VM ou o seu Linux.

## ⌨️ Mão na massa

O arquivo [`comandos.sh`](comandos.sh) tem tudo comentado; rode inteiro com
`bash comandos.sh`. Para abrir o Vim de verdade nas seções interativas:
`L4O_INTERATIVO=1 bash comandos.sh`.

### 1. Abrir, olhar e sair

```bash
vim desafio/servidor-pixvelox.log   # abre no modo normal
# dentro do Vim:
#   Ctrl+G   mostra nome do arquivo e número de linhas
#   :q       sai (se não alterou nada)
#   :q!      sai DESCARTANDO alterações
```

### 2. Pular para uma linha

```bash
vim +4242 desafio/servidor-pixvelox.log    # já abre na linha 4242
# dentro do Vim:  :4242 Enter   (ou 4242G no modo normal; gg = topo, G = fim)
```

### 3. Buscar

```bash
# dentro do Vim:
#   /mare_alta   procura para frente      n = próxima   N = anterior
#   ?mare_alta   procura para trás
#   :set number  mostra os números das linhas (:set nonumber esconde)
```

### 4. Substituir em todo o arquivo

```bash
cp desafio/servidor-pixvelox.log copia.log   # trabalhe SEMPRE numa cópia
vim copia.log
# dentro do Vim:
#   :%s/#MARE#/_/g    % = todas as linhas · s = substituir · g = todas na linha
#   :wq               salva e sai
```

### 5. Editar linhas: dd, yy, p, u

```bash
vim desafio/treino-vim.txt
# dd  apaga a linha    3dd apaga 3     yy copia a linha    p cola abaixo
# u   desfaz           Ctrl+R refaz    i   entra no modo inserção (Esc sai)
# :q!  sai sem salvar — é só treino
```

### 6. Vim sem interface (scripts e Colab)

```bash
vim -es +4242p -cq desafio/servidor-pixvelox.log    # imprime a linha 4242
ex -s +'4242p' +'q!' desafio/servidor-pixvelox.log  # o mesmo, via "ex"
vim -es -c 'g/mare_alta/#' -c 'q!' desafio/servidor-pixvelox.log   # tipo grep -n
vim -es -c '%s/#MARE#/_/g' -c 'wq' copia.log        # substitui e salva
sed -n '4242p' desafio/servidor-pixvelox.log        # o primo do Dia 7
```

`-e` liga o modo ex, `-s` deixa silencioso, `+cmd` e `-c cmd` executam
comandos de dois pontos em sequência.

### 7. Guia de sobrevivência (cole na parede)

| Tecla | O que faz |
|---|---|
| `Esc` | volta ao modo normal (na dúvida, aperte duas vezes) |
| `i` / `a` / `o` | insere antes do cursor / depois / numa linha nova |
| `:w` · `:q` · `:wq` · `:q!` | salva · sai · salva e sai · sai sem salvar |
| `:N` · `gg` · `G` | vai para a linha N · topo · fim |
| `/texto` · `n` · `N` | busca · próxima · anterior |
| `dd` · `yy` · `p` · `u` | apaga · copia · cola · desfaz |
| `:%s/a/b/g` | troca todos os `a` por `b` |

Aviso de **swap file** (`.swp`)? O Vim achou uma sessão anterior aberta ou
interrompida. Leia a mensagem, escolha `(R)ecover` ou `(D)elete it`.

### 8. vimtutor

```bash
vimtutor        # tutorial interativo de ~30 min (em pt se o sistema estiver em pt_BR)
vimtutor pt     # força o português
```

## 🇧🇷 Versão brazuca

Os Diários Oficiais publicam edições inteiras em texto, e um arquivo de
dezenas de milhares de linhas é comum. O **Querido Diário** (Open Knowledge
Brasil) disponibiliza diários oficiais municipais em texto puro em
<https://queridodiario.ok.org.br>. Baixe uma edição em `.txt` e treine:

```bash
vim +/PREGÃO diario.txt                 # abre já na primeira ocorrência
# :g/CONTRATO/#                         # lista todas as linhas com CONTRATO
# :%s/\s\+$//g                          # remove espaços sobrando no fim das linhas
# :w notas-pregao.txt                   # salva o resultado com outro nome
```

Para o nosso caso, monte um **arquivo de notas** do dia no Vim: `vim notas-dia08.txt`,
`i`, escreva o que achou na linha 4242, `Esc`, `:wq`.

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) mostra que um editor é, no fundo, uma
**lista de linhas** — e cada comando do Vim vira uma operação de lista.

| Vim | Python (stdlib) |
|---|---|
| `:4242` | `linhas[4241]` (lista começa em 0) |
| `/mare_alta` | `[n for n, l in enumerate(linhas, 1) if "mare_alta" in l]` |
| `:%s/a/b/g` | `[l.replace("a", "b") for l in linhas]` |
| `dd` | `del linhas[i]` |
| `yy` + `p` | `linhas.insert(i + 1, linhas[i])` |
| `:wq` | `Path.write_text("\n".join(linhas))` |

## 🚀 Além do curso

- **Neovim** (`apt install neovim`, comando `nvim`): o Vim modernizado, com
  as mesmas teclas, configuração em Lua e plugins. `nvim --headless` também
  roda sem interface.
- **micro** (`apt install micro`): editor de terminal com atalhos "normais"
  (Ctrl+S salva, Ctrl+Q sai). Ótimo quando você não quer modos.
- **`less +4242 arquivo`** ou **`less +/mare_alta arquivo`**: só leitura, abre
  arquivos gigantes instantaneamente e nunca altera a evidência. Em Python,
  `linecache.getline("arquivo", 4242)` (stdlib) lê uma linha específica.

## 🧩 Desafio

1. Faça uma **cópia** de `desafio/servidor-pixvelox.log`.
2. Abra a cópia no Vim e vá para a linha indicada pelo bilhete da Iara.
3. Desfaça o disfarce do maré_alta em **todo** o arquivo.
4. Confira: `bash checar.sh 'VAZANTE{...}'`

<details>
<summary>💡 Dica 1</summary>

`:4242` pula para a linha. Existem mais de 20 "rascunhos" no log; só o da linha
certa vale.
</details>

<details>
<summary>💡 Dica 2</summary>

`:%s/#MARE#/_/g` troca todas as ocorrências. Sem interface:
`vim -es -c '%s/#MARE#/_/g' -c 'wq' copia.log` e depois `vim -es +4242p -cq copia.log`.
</details>

A solução comentada está em [`solucoes/dia-08.sh`](../../solucoes/dia-08.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- **Editor muda arquivo.** Abrir evidência no Vim e dar `:w` sem querer altera
  a data de modificação e o hash. Trabalhe numa cópia ou use `vim -R`
  (somente leitura) / `view arquivo`.
- O Vim cria `.swp` e pode gravar `~/.viminfo` com o histórico das suas buscas
  e comandos — inclusive termos sensíveis da investigação. Em máquina
  compartilhada, rode `vim -i NONE` ou limpe o `~/.viminfo`.
- Logs de servidor trazem IPs e, às vezes, dados pessoais (LGPD, art. 5º).
  Guarde só o necessário para o caso e não publique trechos sem anonimizar.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 7](../dia-07-sed-e-awk/) · [Índice](../../README.md) · [Dia 9](../dia-09-screen-e-cron/) ➡️
