# Dia 3 — A caixa trancada 🔐

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-03.ipynb)
&nbsp;**Rank D** · ⏱️ ~35 min · 📖 Original: *Day 3. Install and run utilities* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> A polícia apreendeu o notebook de um "atendente" da PixVelox e mandou uma
> cópia para o Núcleo: dois arquivos, `inventario.zip` e `evidencia.zip`.
> O segundo pede senha.
>
> — O dono jura que não lembra a senha — diz a Mestra Iara, colocando o
> café na mesa. — Mas quem anota rotina em arquivo de texto também anota
> senha em algum lugar. Só não abra nada antes de saber o que tem dentro.
>
> Bento, sem tirar os olhos da tela:
> — E instala o `unzip` primeiro. Seu terminal ainda nem tem.

**Sua tarefa:** descobrir a senha da `desafio/evidencia.zip` e ler a flag
`VAZANTE{...}` que está no relatório lá dentro.

## 🎯 Ao final de hoje você sabe

- [ ] Ver o que está instalado (`dpkg -l`, `command -v`)
- [ ] Instalar e remover programas com `apt` (e o que é o `sudo`)
- [ ] Compactar arquivos e pastas (`zip`, `zip -r`)
- [ ] **Listar um zip sem extrair** (`zip -sf`, `unzip -l`)
- [ ] Extrair para uma pasta (`unzip -d`) e ler um arquivo direto (`unzip -p`)
- [ ] Lidar com zip protegido por senha (`zip -e`, `unzip -P`)

## 📖 Conceito em 2 minutos

No Linux você quase nunca baixa programa de site. Você pede ao **gerenciador
de pacotes**, que busca num repositório confiável, confere a assinatura e
instala tudo o que o programa precisa.

```text
você ──► apt install zip ──► repositório do Ubuntu ──► baixa zip.deb
                                                          │
                              dpkg instala e registra ◄───┘
```

- **`dpkg`** é o "almoxarifado": registra o que está instalado (`dpkg -l`).
- **`apt`** é o "comprador": busca, baixa, resolve dependências e chama o dpkg.
- **`sudo`** pede poder de administrador — instalar mexe no sistema todo.

E o **zip**? É uma caixa: vários arquivos num só, comprimidos. O detalhe que
vale ouro em investigação: **o índice da caixa (os nomes dos arquivos) fica
visível mesmo quando o conteúdo tem senha.**

## ⌨️ Mão na massa

Tudo está em [`comandos.sh`](comandos.sh), comentado linha a linha.

### 1. O que já tenho

```bash
dpkg -l | head            # lista os pacotes instalados (ii = instalado)
dpkg -l zip unzip         # só esses dois
command -v unzip          # onde está o programa (vazio = não existe)
dpkg -S "$(command -v ls)"   # de qual pacote veio o ls
```

### 2. Instalando

```bash
sudo apt update               # atualiza a lista do que existe para baixar
sudo apt install zip unzip    # instala
apt show zip                  # descrição e versão
sudo apt remove zip           # desinstala (não faça agora!)
```

### 3. Compactando

```bash
zip archive test1.txt test2.txt   # cria archive.zip
zip -r caso.zip pasta/            # pasta inteira, com subpastas
```

### 4. Espiando sem abrir

```bash
zip -sf archive.zip          # só os nomes
unzip -l archive.zip         # nomes, tamanhos e datas
unzip -t archive.zip         # testa se está íntegro
```

### 5. Extraindo

```bash
unzip archive.zip -d archive          # extrai dentro da pasta archive/
unzip -p archive.zip test1.txt        # imprime um arquivo, sem gravar nada
```

### 6. Senhas

```bash
zip -e secreto.zip arquivo.txt            # pede a senha (seguro)
unzip -P minhasenha secreto.zip -d saida  # senha na linha de comando
```

`-P` grava a senha no histórico do terminal (`~/.bash_history`). Use só em
treino; no dia a dia, deixe o `unzip` perguntar.

## 🇧🇷 Versão brazuca

Bases públicas brasileiras chegam quase sempre em **zip gigante**: os
[Dados Abertos do CNPJ](https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj)
da Receita Federal, os [resultados eleitorais do TSE](https://dadosabertos.tse.jus.br/)
e boa parte do [Portal da Transparência](https://portaldatransparencia.gov.br/download-de-dados).
Alguns têm vários gigabytes descompactados. Antes de encher o disco, olhe o
índice:

```bash
# depois de baixar um desses zips (Dia 5 ensina a baixar com curl):
unzip -l arquivo.zip                    # o que tem e quanto ocupa
unzip -l arquivo.zip | tail -n 1        # total descompactado
unzip -p arquivo.zip um_arquivo.csv | head -n 5   # amostra sem extrair
```

Ver as 5 primeiras linhas de um CSV de 3 GB sem extraí-lo economiza minutos
e espaço — e já mostra se aquele arquivo serve para a sua investigação.

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) usa o módulo `zipfile` da biblioteca
padrão. Ele lê zips com senha, mas não cria.

| Terminal | Python (stdlib) |
|---|---|
| `command -v zip` | `shutil.which("zip")` |
| `pip list` | `importlib.metadata.distributions()` |
| `zip archive a b` | `ZipFile("archive.zip", "w").write(...)` |
| `zip -sf` / `unzip -l` | `ZipFile.namelist()` / `infolist()` |
| `unzip -d pasta` | `ZipFile.extractall("pasta")` |
| `unzip -p a.zip x` | `ZipFile.read("x")` |
| `unzip -P senha` | `ZipFile.read(nome, pwd=b"senha")` |
| `unzip -t` | `ZipFile.testzip()` |

## 🚀 Além do curso

- **`7z`** (no Ubuntu 24.04, pacote `7zip`; em versões antigas, `p7zip-full`) abre quase tudo: `.7z`, `.rar`, `.tar.gz`, `.iso`. `7z l arquivo` lista sem extrair, igual ao `unzip -l`.
- **[pipx](https://pipx.pypa.io/)** (`sudo apt install pipx`) instala ferramentas Python de OSINT, cada uma no seu cantinho, sem quebrar o sistema: `pipx install holehe`, `pipx install maigret`.
- **`zip2john`** + **John the Ripper** (`apt install john`) testam senhas de zip por força bruta. Só com **autorização** e em material que você tem direito de abrir — veja abaixo.

## 🧩 Desafio

1. Entre em `desafio/`.
2. Tente abrir `evidencia.zip` — vai pedir senha.
3. Investigue `inventario.zip` **sem extrair**. Os textos lá dentro são
   inúteis; preste atenção em outra coisa.
4. Abra a evidência com a senha e encontre a flag.
5. Confira: `bash checar.sh 'VAZANTE{...}'`

<details>
<summary>💡 Dica 1</summary>

Quem extrai tudo e roda `cat` em cada arquivo não acha nada. A pista está no
**índice** do zip. `zip -sf inventario.zip` ou `unzip -l inventario.zip`.
</details>

<details>
<summary>💡 Dica 2</summary>

Repare no nome do arquivo dentro de `fotos/.lembrete/`. Depois:
`unzip -p -P SENHA evidencia.zip evidencia/relatorio-saque.txt`.
</details>

A solução comentada está em [`solucoes/dia-03.sh`](../../solucoes/dia-03.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- **Arquivo de evidência pode ter malware.** Liste antes de extrair
  (`unzip -l`) e desconfie de `.exe`, `.js`, `.lnk` e de nomes como
  `../../.bashrc`, que tentam escrever fora da pasta. Extraia sempre com `-d`
  numa pasta isolada — de preferência numa máquina virtual.
- Jurema avisa: **quebrar a senha de um arquivo que não é seu, sem
  autorização, pode ser crime** (Lei 12.737/2012, a "Lei Carolina
  Dieckmann", e art. 154-A do Código Penal). Em investigação oficial, isso
  exige ordem judicial ou consentimento do dono.
- Instale programas só de fontes confiáveis (`apt`, PyPI oficial, GitHub do
  autor). Um "OSINT tool" pirata é o jeito mais rápido de virar vítima.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 2](../dia-02-bash-script/) · [Índice](../../README.md) · [Dia 4](../dia-04-processamento-em-lote/) ➡️
