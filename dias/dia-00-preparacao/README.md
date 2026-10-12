# Dia 0 — O pendrive 💾

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-00.ipynb)
&nbsp;**Rank D** · ⏱️ ~20 min · 📖 Original: *Day 0. Getting ready to work* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> A Mestra Iara já saiu da sala. O pendrive está na sua mão, mas seu
> computador é Windows e você nunca abriu um terminal. Bento, sem tirar os
> olhos da tela dele, avisa:
> — Você não precisa instalar nada hoje. Abre um navegador. O Linux vem até você.

**Sua tarefa:** escolher onde vai estudar, abrir um terminal Linux e rodar o
verificador de ambiente.

## 🎯 Ao final de hoje você sabe

- [ ] Escolher entre Colab, Codespaces, máquina virtual ou Linux instalado
- [ ] Abrir um terminal e baixar este repositório
- [ ] Rodar seu primeiro script com `bash`

## 📖 Conceito em 2 minutos

O **terminal** (ou *shell*, ou *linha de comando*) é um programa onde você
digita ordens em texto e o computador responde em texto. O shell padrão do
Ubuntu é o **Bash**. Tudo o que você fizer nos próximos 21 dias acontece aqui.

Você não precisa de um computador com Linux. Escolha um destes ambientes:

| Ambiente | Precisa instalar? | Melhor para | Limitações |
|---|---|---|---|
| **Google Colab** | Não, só navegador | Seguir os notebooks, dias 1–7 e 10–21 | Sem Vim/`screen`/`cron` interativos (dias 8 e 9); a máquina é apagada quando fecha |
| **GitHub Codespaces** | Não, só conta GitHub | O curso inteiro, com terminal de verdade | Cota mensal gratuita de horas |
| **Máquina virtual** (VirtualBox + Ubuntu) | Sim | Quem quer aprender "pra valer" | Ocupa disco e RAM |
| **WSL** (Windows) | Sim, `wsl --install` | Quem usa Windows no dia a dia | Pequenas diferenças de rede e sistema de arquivos |
| **Linux instalado** | — | Quem já usa | Nenhuma |

> 💡 O autor do curso original indicava o Gitpod, que deixou de ser gratuito.
> Hoje ele mesmo recomenda o GitHub Codespaces — e este repositório já vem
> com a configuração pronta (`.devcontainer/`).

## ⌨️ Mão na massa

### Opção A — Colab (zero instalação)

Clique no botão **Abrir no Colab** no topo de qualquer dia e rode a primeira
célula. Ela baixa o repositório sozinha.

### Opção B — Codespaces (recomendado)

1. Abra a página do repositório no GitHub, logado.
2. **Code → Codespaces → Create codespace on main**.
3. Espere o terminal aparecer embaixo. As ferramentas básicas já são instaladas automaticamente.

### Opção C — No seu Linux, VM ou WSL

```bash
git clone https://github.com/Ridd1kulusC0d3r/linux-para-osint-21-dias.git
cd linux-para-osint-21-dias
bash ferramentas/instalar_tudo.sh          # opcional: deixa tudo pronto
```

### Primeiros comandos

```bash
cd dias/dia-00-preparacao
bash comandos.sh        # roda todos os exemplos de hoje
```

Ou digite um por um:

```bash
whoami                  # quem sou eu?
pwd                     # onde estou?
cat /etc/os-release     # que sistema é este?
df -h .                 # quanto espaço tenho?
bash ../../ferramentas/verificar_ambiente.sh   # o que já está instalado?
```

## 🗺️ Como cada dia funciona

Toda pasta `dias/dia-NN-.../` tem a mesma estrutura:

```text
dia-05-curl-e-apis/
├── README.md        ← a aula: missão, conceito, comandos, desafio
├── comandos.sh      ← todos os comandos do dia, comentados — rode com bash
├── equivalente.py   ← o mesmo resultado em Python puro (biblioteca padrão)
├── checar.sh        ← confere a sua flag sem dar spoiler
└── desafio/         ← as evidências fictícias da Operação Vazante
```

E na raiz do repositório:

- `notebooks/` — um notebook Colab por dia, gerado a partir do `comandos.sh`
- `solucoes/` — soluções comentadas (só depois de tentar!)
- `DIARIO.md` — o seu diário de bordo
- `CHEATSHEET.md` — todos os comandos do curso numa página

## 🧩 Desafio

Hoje não tem flag. Rode o verificador e veja o que já está instalado:

```bash
bash ferramentas/verificar_ambiente.sh
```

Se a última linha disser **Tudo pronto!** ou mostrar quantas ferramentas
faltam, você está no jogo.

## 🛡️ Ética e OPSEC

- Ambientes na nuvem (Colab, Codespaces) pertencem a outra empresa. **Não
  coloque dados reais de investigação** neles — use só o material fictício do curso.
- Para casos reais, prefira uma máquina virtual sua, isolada, que você pode
  apagar e recriar.

## 📝 Diário de bordo

Abra o [`DIARIO.md`](../../DIARIO.md) e escreva: em qual ambiente vai estudar
e por quê.

---

[Índice](../../README.md) · [Dia 1](../dia-01-arquivos-e-pastas/) ➡️
