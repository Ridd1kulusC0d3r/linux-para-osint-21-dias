# Dia 21 — O dossiê 🗂️

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-21.ipynb)
&nbsp;**Rank S** · ⏱️ ~45 min · 📖 Original: *Day 21. Which Linux distribution is better to use?* + *What to do next?* + *Application. Is it possible to do the same thing on Windows?* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> Sexta-feira, 18h40. A sala do Núcleo Coruja está vazia, exceto pela Mestra
> Iara, que pela primeira vez em três semanas está sentada esperando *você*.
> Na mesa dela, um envelope lacrado com cera azul.
>
> — Vinte pistas, recruta. Cada uma abriu a seguinte. Se todas estiverem
> certas, o lacre abre. Se uma estiver errada, ele continua fechado — e você
> sabe por onde recomeçar.
>
> Bento aparece na porta, de mochila.
> — E depois disso você escolhe a sua distro. Ninguém investiga de verdade em
> máquina emprestada.

**Sua tarefa:** reunir as 20 flags anteriores, abrir o selo com
`montar_dossie.sh` e entregar o dossiê. De quebra, escolher a distribuição
Linux que vai usar daqui pra frente.

## 🎯 Ao final de hoje você sabe

- [ ] Identificar a distro, a família e o kernel de qualquer máquina
- [ ] Explicar as diferenças entre as principais distros (e as feitas para OSINT)
- [ ] Entender, na prática, o que é um hash e uma cifra XOR
- [ ] Montar o seu dossiê e abrir o selo final
- [ ] Planejar os próximos passos depois do curso

## 📖 Conceito em 2 minutos

"Linux", a rigor, é só o **kernel** — o núcleo que conversa com o hardware.
Uma **distribuição** junta o kernel com programas, um gerenciador de pacotes,
configurações e uma filosofia. Por isso existem centenas de distros, mas elas
se agrupam em poucas **famílias**:

```text
Debian ──┬── Ubuntu ──┬── Linux Mint
         │            └── (Codespaces, WSL padrão, Colab)
         ├── Kali Linux
         ├── Parrot OS
         └── Tails
Fedora / RHEL ── Rocky, Alma
Arch ──┬── Manjaro
       └── BlackArch
```

Tudo o que você aprendeu nestes 21 dias funciona em qualquer uma delas. O que
muda é o comando de instalar programas (`apt`, `dnf`, `pacman`…) e o que vem
instalado de fábrica.

## ⌨️ Mão na massa

### 1. O RG da máquina

```bash
cat /etc/os-release        # nome, versão e de quem deriva (ID_LIKE)
uname -r                   # versão do kernel
uname -m                   # arquitetura (x86_64, aarch64…)
```

### 2. Descobrindo a família

```bash
for g in apt dnf pacman zypper; do command -v "$g" && echo "→ família do $g"; done
```

### 3. Quanto você instalou no curso

```bash
dpkg -l | tail -n +6 | wc -l   # pacotes .deb instalados
```

### 4. Hash e XOR — a mecânica do selo

```bash
printf '%s' "maré alta"  | sha256sum
printf '%s' "maré alta." | sha256sum    # um ponto muda tudo
```

O selo final foi cifrado com **XOR**, usando como chave o SHA-256 das 20
flags juntas. XOR tem uma propriedade bonita: aplicar a mesma chave duas
vezes devolve o original. O `comandos.sh` mostra isso com uma frase de brinquedo.

### 5. Abrindo o selo

```bash
bash montar_dossie.sh
```

Ele lê as flags guardadas pelos `checar.sh` de cada dia (em `.progresso/`),
confere todas e, se as 20 estiverem certas, abre o selo e grava
`dossie-final/DOSSIE.md`.

## 🐧 Qual distro escolher?

Não existe "a melhor" — existe a melhor **para o que você vai fazer**.

| Distro | Base | Para quem | Observação |
|---|---|---|---|
| **Ubuntu** (LTS) | Debian | Começar e trabalhar no dia a dia | É a distro dos exemplos deste curso, do Colab e do Codespaces |
| **Debian** | — | Quem quer estabilidade e simplicidade | Mãe de boa parte das distros desta lista |
| **Linux Mint** | Ubuntu | Quem vem do Windows | Interface familiar |
| **Kali Linux** | Debian | Pentest e segurança ofensiva | Centenas de ferramentas prontas; não é pensada para uso diário |
| **Parrot OS** | Debian | Segurança + privacidade | Tem edição "Home" mais leve |
| **Trace Labs OSINT VM** | Debian | OSINT, especialmente busca de pessoas desaparecidas | Máquina virtual pronta, mantida pela Trace Labs; a versão 2026.05 passou a ser construída sobre Debian |
| **Tails** | Debian | Anonimato forte (tudo via Tor, nada fica salvo) | Roda de pendrive e esquece tudo ao desligar |

**Sugestão prática:** use **Ubuntu ou Debian** numa máquina virtual para
estudar e trabalhar, instale as ferramentas que precisar (você já sabe), e
mantenha uma VM separada, descartável, para investigações reais. Distros
"cheias de ferramentas" são ótimas para conhecer o que existe, mas aprender a
montar o próprio ambiente vale mais.

## 🪟 E no Windows?

Dá para fazer quase tudo deste curso sem sair do Windows:

- **WSL** (`wsl --install` no PowerShell como administrador) instala um Ubuntu
  de verdade dentro do Windows. É o caminho mais simples.
- **Máquina virtual** (VirtualBox, VMware, Hyper-V) para isolamento total.
- **Codespaces** ou **Colab**, quando não puder instalar nada.

## 🇧🇷 Versão brazuca

Seu dossiê vai precisar circular. Antes de mandar para alguém, pense em:

```bash
sha256sum dossie-final/DOSSIE.md > dossie-final/DOSSIE.md.sha256   # integridade
date '+%d/%m/%Y %H:%M:%S %Z' >> dossie-final/registro.txt          # quando foi gerado
```

Registrar o hash do arquivo e a data de geração é o começo de uma **cadeia de
custódia** — o que dá valor de prova ao que você coletou (no Brasil, os arts.
158-A a 158-F do Código de Processo Penal tratam disso).

## 🐍 Ponte Python

| Terminal | Python (stdlib) |
|---|---|
| `cat /etc/os-release` | `platform.freedesktop_os_release()` |
| `uname -r` / `uname -m` | `platform.release()` / `platform.machine()` |
| `command -v apt` | `shutil.which("apt")` |
| `sha256sum` | `hashlib.sha256()` |
| XOR byte a byte | `bytes(a ^ b for a, b in ...)` |

## 🚀 Além do curso

- **Curso irmão:** [Python for OSINT. 21-day course for beginners](https://github.com/cipher387/python-for-OSINT-21-days), do mesmo autor. A seção 🐍 de cada dia já te deixou no meio do caminho.
- **`distrobox`** roda outras distros em contêiner dentro da sua: teste Kali ou Arch sem formatar nada (`apt install distrobox`).
- **Ansible** ou um simples `instalar_tudo.sh` versionado no seu GitHub: reconstruir sua máquina de investigação em minutos é OPSEC.

## 🧭 E agora?

1. **Refaça o curso digitando** em vez de rodar `comandos.sh`. A memória está nos dedos.
2. **Automatize uma tarefa real** sua com Bash: renomear prints, baixar uma lista de URLs, extrair e-mails de um PDF.
3. **Siga quem produz conteúdo:** o autor original publica ferramentas de OSINT o tempo todo em [cybdetective.com](https://cybdetective.com).
4. **Contribua aqui:** uma fonte brasileira, um desafio novo, uma explicação melhor — veja o [CONTRIBUTING.md](../../CONTRIBUTING.md).

## 🧩 Desafio

1. Garanta que os 20 dias anteriores estão com a flag registrada (`bash checar.sh 'VAZANTE{...}'` em cada um).
2. Rode `bash montar_dossie.sh`.
3. A última linha é a flag final. Confira: `bash checar.sh 'VAZANTE{...}'`.

<details>
<summary>💡 Dica 1</summary>

O script diz exatamente quais dias estão faltando. Volte neles.
</details>

<details>
<summary>💡 Dica 2</summary>

Estudou no Colab e a máquina foi apagada? O progresso some junto. Basta rodar
de novo o `checar.sh` de cada dia com as flags que você anotou no `DIARIO.md`.
</details>

A solução comentada está em [`solucoes/dia-21.sh`](../../solucoes/dia-21.sh).

## 🛡️ Ética e OPSEC

- Um dossiê real contém dados pessoais. **LGPD vale para você também**:
  colete só o necessário, guarde com segurança e saiba por que está guardando.
- Separe identidades: a máquina (ou VM) de investigação não é a mesma do seu
  e-mail pessoal e redes sociais.
- OSINT é sobre informação **aberta**. Invadir, enganar ou "dar um jeitinho"
  para acessar o que não é público deixa de ser OSINT — e pode ser crime.

## 📝 Diário de bordo

Feche o [`DIARIO.md`](../../DIARIO.md) com três linhas: o dia mais difícil, o
comando que mais vai usar, e a distro que escolheu.

---

⬅️ [Dia 20](../dia-20-ferramentas-uteis/) · [Índice](../../README.md) · [História](../../historia/README.md) 🦉
