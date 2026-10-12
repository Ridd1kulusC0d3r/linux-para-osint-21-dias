#!/usr/bin/env bash
# =============================================================================
#  Dia 9 — O relógio do robô: screen (sessões que não morrem) e cron (agenda)
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
#  `screen -S` sem -d e `crontab -e` são interativos: aparecem via `interativo`.
#  No Colab o cron NÃO roda (não há serviço de agendamento ativo); lá você
#  aprende a LER e ESCREVER crontabs. Para ver o cron funcionando, use
#  Codespaces, VM ou o seu Linux.
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% Instalando o screen
# `screen` cria terminais "virtuais" que continuam vivos mesmo se você fechar
# a janela ou cair a conexão SSH. Perfeito para coletas que levam horas.
titulo "screen instalado?"
precisa screen
screen --version

# %% Criando e entrando numa sessão (modo interativo)
#   screen -S nome      cria uma sessão chamada "nome" e entra nela
#   Ctrl+A e depois D   "destaca" (detach): sai da sessão SEM matá-la
#   screen -ls          lista as sessões
#   screen -r nome      volta (reattach) para a sessão
#   exit                dentro da sessão: encerra a sessão de vez
titulo "Sessão interativa"
interativo screen -S coleta-vazante
dica "Lá dentro: rode algo demorado, aperte Ctrl+A e depois D, e veja com screen -ls."

# %% Rodando algo destacado (sem prender o terminal)
# `screen -dmS nome comando` cria a sessão JÁ destacada e roda o comando
# lá dentro. É assim que se dispara uma coleta longa por script.
#   -d -m   cria destacada (detached), sem precisar de terminal
#   -S      dá um nome à sessão
# O robô aqui é uma réplica inofensiva: só escreve uma linha num arquivo.
titulo "screen -dmS: o robô trabalhando em segundo plano"
precisa screen
mkdir -p treino
screen -dmS robo-demo bash -c 'bash desafio/robo.sh --lote demonstracao > treino/saida.log; sleep 60'
# espera o robô escrever (no máximo ~5 s)
for _ in 1 2 3 4 5 6 7 8 9 10; do [ -s treino/saida.log ] && break; sleep 0.5; done
screen -ls || true          # screen -ls devolve código 1 quando há sessões; tudo bem
cat treino/saida.log

# %% Voltando e encerrando uma sessão
#   screen -r nome          entra de novo (interativo)
#   screen -XS nome quit    manda o comando "quit" para a sessão: ela morre
# -X envia um comando para a sessão; -S escolhe qual.
titulo "Encerrando a sessão do robô"
precisa screen
interativo screen -r robo-demo
if screen -XS robo-demo quit 2>/dev/null; then
  ok "Sessão robo-demo encerrada."
else
  alerta "Nenhuma sessão robo-demo ativa (rode a seção anterior antes)."
fi
screen -ls || true
rm -rf treino

# %% A sintaxe do cron: cinco campos e um comando
# Cada linha de um crontab diz QUANDO e O QUE rodar:
#
#   ┌──────── minuto        (0-59)
#   │  ┌───── hora          (0-23)
#   │  │ ┌─── dia do mês    (1-31)
#   │  │ │ ┌─ mês           (1-12)
#   │  │ │ │ ┌ dia da semana (0-7; 0 e 7 = domingo; ou sun, mon...)
#   17 3 * * 0  comando     ->  às 03:17 de todo domingo
#
#   *     qualquer valor         */5   a cada 5         1-5   de 1 a 5 (seg a sex)
#   12,18 às 12 e às 18          @reboot  ao ligar a máquina
titulo "O crontab vazado do robô"
cat desafio/crontab-robo.txt

# %% Lendo o crontab como tabela
# Linhas que começam com # são comentários. Linhas com = são variáveis.
# O awk (Dia 7) separa os campos e mostra cada job de forma legível.
titulo "Jobs em colunas"
grep -Ev '^(#|$|[A-Z]+=)' desafio/crontab-robo.txt \
  | awk '$1 ~ /^@/ { printf "%-8s %-28s\n", $1, $NF; next }
         { printf "min=%-4s hora=%-6s dia=%-3s mes=%-3s semana=%-4s -> %s\n", $1, $2, $3, $4, $5, $NF }'

# %% Que dia da semana foi?
# O extrato mostra os saques. Para casar com o cron, precisamos do dia da
# semana de cada data. `date -d AAAA-MM-DD +%A` responde; +%u dá o número
# (1 = segunda ... 7 = domingo).
titulo "Datas dos saques"
cat desafio/extrato-saques.txt
for d in 2026-03-15 2026-03-22; do
  echo "$d -> $(date -d "$d" +%A) (número $(date -d "$d" +%u))"
done
dica "Todos os saques têm a MESMA hora. Compare com os campos do crontab."

# %% Filtrando jobs por horário
# Exemplo: quais jobs rodam às 3 da manhã (campo hora = 3)?
# Repare que vários jobs "parecem" certos. Cada campo precisa bater.
titulo "Jobs com hora = 3"
grep -Ev '^(#|$|[A-Z]+=|@)' desafio/crontab-robo.txt | awk '$2 == "3"'

# %% O seu próprio crontab
#   crontab -l   lista o seu crontab
#   crontab -e   edita (abre um editor — interativo)
#   crontab -r   APAGA o seu crontab inteiro (cuidado: sem confirmação!)
# Os logs do cron ficam no journal:  journalctl -u cron  (ou /var/log/syslog)
titulo "Meu crontab"
precisa crontab cron
crontab -l 2>/dev/null || dica "Você ainda não tem crontab (normal na primeira vez)."
interativo crontab -e
mostrar "17 3 * * 0  /caminho/coleta.sh >> /caminho/coleta.log 2>&1"
dica "Sempre use caminhos absolutos e redirecione a saída para um log."

# %% Ainda dá para agendar no Colab?
# Não há cron ativo no Colab. Para algo "de tempos em tempos" numa sessão,
# um laço com sleep resolve (rodando em screen ou com nohup ... &).
# Aqui, 3 voltas rápidas de 1 segundo para ver a ideia.
titulo "Agendador de pobre: laço + sleep"
for volta in 1 2 3; do
  bash desafio/robo.sh --lote "volta_$volta"
  sleep 1
done
