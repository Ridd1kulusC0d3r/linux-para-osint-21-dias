# ▶️ Comece aqui

Bem-vindo(a) ao Núcleo Coruja, recruta. Três passos e você está dentro.

## 1. Escolha onde estudar

| Se você... | Use |
|---|---|
| só tem navegador e quer começar já | **Google Colab** — botão ▶️ em cada dia |
| quer um terminal de verdade sem instalar nada | **GitHub Codespaces** — [abrir](https://codespaces.new/Ridd1kulusC0d3r/linux-para-osint-21-dias) |
| tem Ubuntu, Debian, WSL ou uma VM | **clone o repositório** (abaixo) |

Os dias 8 (Vim) e 9 (`screen`/`cron`) precisam de terminal interativo: use
Codespaces ou sua máquina.

## 2. Baixe e teste

```bash
git clone https://github.com/Ridd1kulusC0d3r/linux-para-osint-21-dias.git
cd linux-para-osint-21-dias
bash ferramentas/verificar_ambiente.sh
```

Quer instalar tudo de uma vez (opcional)?

```bash
bash ferramentas/instalar_tudo.sh            # básico
bash ferramentas/instalar_tudo.sh completo   # + vídeo, OCR, PDF, Office
```

## 3. Siga o ritmo de um dia

1. Leia o `README.md` do dia — começa pela **🎬 Missão**.
2. Rode os comandos: `bash comandos.sh` (ou digite um por um, que fixa melhor).
3. Compare com o `equivalente.py`.
4. Resolva o **🧩 Desafio** e confira: `bash checar.sh 'VAZANTE{...}'`.
5. Anote no [`DIARIO.md`](DIARIO.md).

Travou? As dicas ficam em blocos recolhidos no README. A solução completa
está em `solucoes/` — abra só depois de tentar.

## Atalhos úteis

| Variável | Efeito |
|---|---|
| `L4O_OFFLINE=1 bash comandos.sh` | força o modo offline (usa as cópias salvas) |
| `L4O_INTERATIVO=1 bash comandos.sh` | executa de verdade os comandos interativos (vim, screen, man) |

Seu progresso fica em `.progresso/` (ignorado pelo git). No site do curso
você também marca os dias concluídos e confere flags no navegador.

Boa caçada. 🦉
