# Dia 9 — O relógio do robô ⏰

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-09.ipynb)
&nbsp;**Rank C** · ⏱️ ~45 min · 📖 Original: *Day 9. Screen and Crone* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> Jurema chega com um extrato na mão e cara de quem não dormiu.
> — Quatro vítimas, quatro saques. Todos às **03:17**. Nenhum humano acorda
> nesse horário para roubar com tanta pontualidade.
>
> Bento já sabe:
> — Robô. E robô em Linux tem relógio: **cron**.
>
> Na pasta da perícia, um arquivo copiado do servidor d'Os Vazantes:
> `crontab-robo.txt`. Uma dúzia de tarefas agendadas, todas chamando o mesmo
> `robo.sh` com um `--lote` diferente. Várias parecem certas. Só uma é.

**Sua tarefa:** descobrir em que dia da semana caem os saques do
`desafio/extrato-saques.txt`, achar no `desafio/crontab-robo.txt` o **único**
job que roda exatamente naquele dia e horário, e montar a flag
`VAZANTE{<valor do --lote>}`.

## 🎯 Ao final de hoje você sabe

- [ ] Criar sessões `screen` que sobrevivem à queda da conexão (`-S`, `-ls`, `-r`)
- [ ] Destacar (`Ctrl+A D`), rodar destacado (`-dmS`) e encerrar (`-XS nome quit`)
- [ ] Ler os **cinco campos** de uma linha do cron e os atalhos `*`, `*/5`, `1-5`, `@reboot`
- [ ] Listar e editar o seu agendamento (`crontab -l`, `crontab -e`)
- [ ] Descobrir o dia da semana de uma data com `date -d`

## 📖 Conceito em 2 minutos

Duas dores comuns de quem faz coleta OSINT:

1. **"Minha coleta leva 6 horas e a conexão caiu no meio."** → `screen`.
   Ele cria um terminal que vive no servidor, não na sua janela. Você sai,
   volta depois e está tudo lá.
2. **"Quero coletar todo dia às 7h sem lembrar."** → `cron`. Um serviço que
   acorda a cada minuto, lê as tabelas de agendamento (crontabs) e roda o que
   estiver na hora.

Uma linha de crontab tem **cinco campos de tempo** e o comando:

```text
┌───────────── minuto        0-59
│  ┌────────── hora          0-23
│  │ ┌──────── dia do mês    1-31
│  │ │ ┌────── mês           1-12
│  │ │ │ ┌──── dia da semana 0-7  (0 e 7 = domingo; também sun, mon...)
│  │ │ │ │
17 3 * * 0   /home/mare_alta/robo.sh   →  03:17 de todo domingo
```

`*` = qualquer valor · `*/5` = a cada 5 · `1-5` = de 1 a 5 · `12,18` = 12 e 18
· `@reboot` = ao ligar a máquina. Todos os campos precisam bater ao mesmo tempo.

> **Colab:** não há serviço cron ativo nem terminal interativo, então lá você
> pratica a **leitura** de crontabs e o `screen -dmS` (que não precisa de
> terminal). Para ver um agendamento disparar de verdade, use Codespaces, uma
> VM ou o seu Linux.

## ⌨️ Mão na massa

O arquivo [`comandos.sh`](comandos.sh) tem tudo comentado; rode inteiro com
`bash comandos.sh`.

### 1. screen: sessões que não morrem

```bash
sudo apt install screen
screen -S coleta-vazante      # cria e entra na sessão
# ... rode algo demorado ...
# Ctrl+A, solte, D            -> destaca (a sessão continua rodando)
screen -ls                    # lista sessões
screen -r coleta-vazante      # volta para ela
screen -XS coleta-vazante quit   # encerra de fora
```

### 2. Rodando algo destacado, por script

```bash
screen -dmS robo-demo bash -c 'bash desafio/robo.sh --lote teste > saida.log'
screen -ls
cat saida.log
```

`-d -m` cria a sessão já destacada — ideal para disparar coletas longas de
dentro de outro script (ou de uma célula do Colab).

### 3. Lendo um crontab

```bash
cat desafio/crontab-robo.txt
grep -Ev '^(#|$|[A-Z]+=)' desafio/crontab-robo.txt \
  | awk '{ print "min="$1, "hora="$2, "dia="$3, "mes="$4, "semana="$5, "->", $NF }'
```

### 4. Que dia da semana foi?

```bash
date -d 2026-03-15 +%A     # nome do dia
date -d 2026-03-15 +%u     # 1 = segunda ... 7 = domingo
```

### 5. O seu agendamento

```bash
crontab -l     # lista
crontab -e     # edita (na 1ª vez pergunta qual editor: escolha nano se não curtiu o Vim)
# exemplo de linha: coleta todo domingo às 03:17, guardando a saída
# 17 3 * * 0  /home/voce/coleta.sh >> /home/voce/coleta.log 2>&1
crontab -r     # APAGA tudo, sem perguntar. Cuidado.
```

Dicas que evitam 90% das dores: caminhos **absolutos**, saída redirecionada
para log (`>> arq.log 2>&1`) e lembrar que o cron roda com um `PATH` mínimo.

## 🇧🇷 Versão brazuca

Monitorar publicações oficiais é um uso clássico de cron. Exemplo: guardar
todo dia útil às 7h05 o JSON de feriados nacionais da **BrasilAPI** (fonte
pública), e uma vez por mês a lista de bancos — se algo mudar, o `diff`
(Dia 10) avisa:

```bash
# m  h  dom mon dow  comando
5    7  *   *   1-5  curl -s https://brasilapi.com.br/api/feriados/v1/2026 > ~/coletas/feriados-$(date +\%F).json
0    6  1   *   *    curl -s https://brasilapi.com.br/api/banks/v1 > ~/coletas/bancos-$(date +\%Y\%m).json
```

Repare no `\%`: dentro do crontab o `%` vira quebra de linha, então precisa
ser escapado. O mesmo vale para acompanhar o **Diário Oficial da União**
(<https://www.in.gov.br>) ou o Querido Diário em busca de um CNPJ de interesse.

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) reimplementa o "cérebro" do cron: para cada
linha, testa se os cinco campos batem com uma data.

| Terminal | Python (stdlib) |
|---|---|
| `date -d 2026-03-15 +%A` | `datetime.date(2026, 3, 15).strftime("%A")` |
| `date +%u` | `date.isoweekday()` |
| `awk '{print $1, $2}'` num crontab | `linha.split()` |
| `screen -dmS nome cmd` | `subprocess.Popen([...])` |
| `while true; do ...; sleep 60; done` | `while True: ...; time.sleep(60)` |

## 🚀 Além do curso

- **tmux** (`apt install tmux`): o sucessor moderno do screen. `tmux new -s coleta`,
  `Ctrl+B D` para destacar, `tmux attach -t coleta` para voltar.
- **systemd timers** (`systemctl list-timers`): o agendador moderno do Linux,
  com logs no `journalctl` e "recuperação" de execuções perdidas com a máquina
  desligada.
- **APScheduler** (`pip install apscheduler`): agenda tarefas *dentro* de um
  programa Python com sintaxe de cron (`CronTrigger.from_crontab("17 3 * * 0")`).
  E o site **crontab.guru** traduz qualquer expressão para português... quer
  dizer, para inglês legível.

## 🧩 Desafio

1. Leia `desafio/extrato-saques.txt`: que horário se repete?
2. Descubra o **dia da semana** de cada data.
3. No `desafio/crontab-robo.txt`, ache o job cujos **cinco campos** batem.
4. Monte `VAZANTE{<valor do --lote>}` e confira: `bash checar.sh 'VAZANTE{...}'`

<details>
<summary>💡 Dica 1</summary>

`date -d 2026-03-15 +%A`. E no cron, domingo pode ser `0`, `7` ou `sun`.
</details>

<details>
<summary>💡 Dica 2</summary>

Cuidado com as iscas: `3 17` é 17:03 (minuto vem primeiro!), `1-5` é segunda a
sexta, e um `1` no terceiro campo significa "dia 1º do mês".
</details>

A solução comentada está em [`solucoes/dia-09.sh`](../../solucoes/dia-09.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- Coleta automática **multiplica** o impacto: um robô mal configurado pode
  sobrecarregar um site pequeno. Use intervalos generosos e respeite termos de
  uso e `robots.txt`.
- O que o cron coleta fica guardado. Se for dado pessoal, a LGPD exige
  finalidade, necessidade e prazo: programe também a **limpeza** (um job que
  apaga coletas antigas).
- Sessões `screen` esquecidas num servidor continuam rodando — e mostram seus
  comandos para quem tiver acesso à máquina. Encerre o que não usa
  (`screen -XS nome quit`).

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 8](../dia-08-vim/) · [Índice](../../README.md) · [Dia 10](../dia-10-utilitarios-de-texto/) ➡️
