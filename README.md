<div align="center">

# 🦉 Linux para OSINT — 21 dias

### *Terminal no Jutsu* · Operação Vazante

**Aprenda o terminal Linux investigando um golpe fictício, um comando de cada vez.**
Tudo em português, com história, desafios com flag, notebooks Colab e a ponte para Python.

[![Baseado em cipher387/linux-for-OSINT-21-day](https://img.shields.io/badge/baseado%20em-cipher387%2Flinux--for--OSINT--21--day-blue?logo=github)](https://github.com/cipher387/linux-for-OSINT-21-day)
[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-green)](LICENSE)
[![Testes](https://github.com/Ridd1kulusC0d3r/linux-para-osint-21-dias/actions/workflows/testes.yml/badge.svg)](https://github.com/Ridd1kulusC0d3r/linux-para-osint-21-dias/actions/workflows/testes.yml)
[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-01.ipynb)
[![Abrir no Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Ridd1kulusC0d3r/linux-para-osint-21-dias)

[**🌐 Site com progresso e checador de flags**](https://ridd1kulusc0d3r.github.io/linux-para-osint-21-dias/) · [**▶️ Comece aqui**](COMECE-AQUI.md) · [**📜 A história**](historia/README.md) · [**🧾 Cheatsheet**](CHEATSHEET.md)

</div>

---

> [!NOTE]
> Este repositório é o meu **diário de estudos** do excelente curso
> [**Linux for OSINT. 21-day course for beginners**](https://github.com/cipher387/linux-for-OSINT-21-day),
> de **[cipher387 / Cyber Detective](https://cybdetective.com)**. A sequência de temas e os
> comandos de cada dia vêm de lá; textos, história, desafios e ferramentas são novos.
> Leia o [PDF original](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf)
> e **dê uma estrela no repositório do autor**. Detalhes em [CREDITOS.md](CREDITOS.md).

## 🌊 A premissa

Uma falsa fintech chamada **PixVelox** promete cashback em todo Pix. Quando a
vítima pede ajuda, o "suporte" no WhatsApp pede o código de verificação — e a
conta esvazia. Você é recruta do **Núcleo Coruja** e tem 21 dias para aprender
Linux e montar o dossiê d'**Os Vazantes**. Cada ferramenta nova abre uma pista;
cada pista termina numa flag `VAZANTE{...}`.

*Tudo é ficção: domínios `.example`, telefones e pessoas inventados.*

## 🗺️ Os 21 dias

| Dia | Capítulo | Tema | Rank | Colab |
|---:|---|---|:---:|:---:|
| 0 | [O pendrive](dias/dia-00-preparacao/) | Preparar o ambiente | D | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-00.ipynb) |
| 1 | [O que ninguém vê](dias/dia-01-arquivos-e-pastas/) | Arquivos, pastas e ocultos | D | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-01.ipynb) |
| 2 | [O script do Bento](dias/dia-02-bash-script/) | Bash: variáveis, condições, laços, funções | D | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-02.ipynb) |
| 3 | [A caixa trancada](dias/dia-03-instalar-programas/) | Instalar programas, zip | D | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-03.ipynb) |
| 4 | [Duzentas conversas](dias/dia-04-processamento-em-lote/) | Processamento em lote: `find`, `xargs` | D | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-04.ipynb) |
| 5 | [Bater na porta](dias/dia-05-curl-e-apis/) | `curl`, cabeçalhos e APIs | D | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-05.ipynb) |
| 6 | [Agulha no vazamento](dias/dia-06-grep/) | `grep` e regex | D | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-06.ipynb) |
| 7 | [Seguindo o dinheiro](dias/dia-07-sed-e-awk/) | `sed` e `awk` | D | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-07.ipynb) |
| 8 | [A linha 4242](dias/dia-08-vim/) | Vim | C | 🖥️ Codespaces |
| 9 | [O relógio do robô](dias/dia-09-screen-e-cron/) | `screen` e `cron` | C | 🖥️ Codespaces |
| 10 | [Dois grupos, um número](dias/dia-10-utilitarios-de-texto/) | `sort`, `uniq`, `cut`, `comm` | C | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-10.ipynb) |
| 11 | [O vídeo do golpe](dias/dia-11-video-audio-imagem/) | `ffmpeg`, OCR, metadados | C | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-11.ipynb) |
| 12 | [O contrato](dias/dia-12-pdf/) | PDF por dentro | C | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-12.ipynb) |
| 13 | [A planilha esquecida](dias/dia-13-arquivos-office/) | Arquivos Office | C | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-13.ipynb) |
| 14 | [O export do grupo](dias/dia-14-json-xml-csv/) | JSON, XML, CSV | C | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-14.ipynb) |
| 15 | [O site clone](dias/dia-15-scraping/) | Scraping | B | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-15.ipynb) |
| 16 | [Perguntando ao mundo](dias/dia-16-automacao-de-busca/) | Automação de buscas | B | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-16.ipynb) |
| 17 | [O torrent do kit](dias/dia-17-compartilhamento-de-arquivos/) | Torrents, FTP, hashes | B | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-17.ipynb) |
| 18 | [Quem registrou?](dias/dia-18-investigacao-de-dominio/) | `whois`, `dig` | B | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-18.ipynb) |
| 19 | [O commit apagado](dias/dia-19-git-e-github/) | Git e GitHub | B | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-19.ipynb) |
| 20 | [O script quebrado](dias/dia-20-ferramentas-uteis/) | `shellcheck`, `history`, atalhos | A | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-20.ipynb) |
| 21 | [O dossiê](dias/dia-21-distro-e-dossie/) | Distros e fechamento do caso | S | [▶️](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-21.ipynb) |

## 🧱 O que tem em cada dia

```text
dias/dia-NN-tema/
├── README.md        🎬 missão · 🎯 objetivos · 📖 conceito · ⌨️ comandos · 🇧🇷 versão brazuca
│                    🐍 ponte Python · 🚀 além do curso · 🧩 desafio · 🛡️ ética e OPSEC
├── comandos.sh      todos os comandos do dia, comentados linha a linha
├── equivalente.py   o mesmo resultado em Python puro (só biblioteca padrão)
├── checar.sh        confere a sua flag sem revelar a resposta
└── desafio/         evidências fictícias da Operação Vazante
```

| Diferencial | Como funciona |
|---|---|
| 🎬 **História contínua** | Os 21 dias são capítulos de um mesmo caso. A pista de hoje usa o que você aprendeu ontem. |
| 🧩 **Desafio com flag** | Cada dia esconde uma flag `VAZANTE{...}`. O `checar.sh` compara só o hash SHA-256 — sem spoiler no repositório. |
| ☁️ **Colab e Codespaces** | Um notebook por dia, gerado do `comandos.sh`. Dias 8 e 9 (Vim, `screen`, `cron`) pedem terminal real → Codespaces já configurado. |
| 📴 **Funciona offline** | Toda seção que usa internet tem cópia salva da resposta. Dá para estudar no avião. |
| 🐍 **Ponte para Python** | Cada dia mostra o equivalente em Python stdlib — prepara para o curso irmão *Python for OSINT*. |
| 🇧🇷 **Versão brazuca** | BrasilAPI, registro.br, dados.gov.br, Diário Oficial: aplicação local de cada técnica. |
| 🛡️ **Ética e OPSEC** | LGPD, cadeia de custódia e os rastros que **você** deixa. |
| ✅ **Testado automaticamente** | O GitHub Actions roda todos os dias, todas as soluções e o lint a cada mudança — e toda segunda-feira. |

## ▶️ Começar em 1 minuto

**No navegador, sem instalar nada:** clique em [▶️ Colab do Dia 1](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-01.ipynb).

**Terminal de verdade, sem instalar nada:** [Abrir no Codespaces](https://codespaces.new/Ridd1kulusC0d3r/linux-para-osint-21-dias).

**Na sua máquina (Ubuntu, Debian, WSL ou VM):**

```bash
git clone https://github.com/Ridd1kulusC0d3r/linux-para-osint-21-dias.git
cd linux-para-osint-21-dias
bash dias/dia-01-arquivos-e-pastas/comandos.sh   # roda o Dia 1
bash dias/dia-01-arquivos-e-pastas/checar.sh 'VAZANTE{...}'   # confere a flag
```

Mais detalhes no [**COMECE-AQUI.md**](COMECE-AQUI.md).

## 🧰 Para quem mantém

```bash
python3 ferramentas/gerar_notebooks.py   # regenera os notebooks a partir dos comandos.sh
bash ferramentas/testar_tudo.sh          # testa todos os dias (ou: testar_tudo.sh 05)
python3 ferramentas/fabrica/dia05.py     # recria as evidências de um dia
```

Quer ajudar? Leia o [CONTRIBUTING.md](CONTRIBUTING.md).

## 🙏 Créditos

- Curso original: **[cipher387 / Cyber Detective](https://github.com/cipher387)** — [linux-for-OSINT-21-day](https://github.com/cipher387/linux-for-OSINT-21-day) (MIT)
- Adaptação, história e ferramentas: **[Deivison Lourenço](https://www.linkedin.com/in/deivisonlourencos)** ([@Ridd1kulusC0d3r](https://github.com/Ridd1kulusC0d3r))

Licença MIT — veja [LICENSE](LICENSE) e [LICENSE-ORIGINAL](LICENSE-ORIGINAL).
