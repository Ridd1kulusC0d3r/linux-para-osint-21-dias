"""Fábrica de evidências do Dia 9 — gera desafio/crontab-robo.txt,
desafio/extrato-saques.txt e desafio/robo.sh.

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia09.py
Tudo é fictício. Só stdlib.

Como a pista funciona
---------------------
O "robô" d'Os Vazantes esvazia contas sempre no mesmo horário. O extrato
mostra os saques: todos às 03:17, todos num DOMINGO (a pessoa descobre com
`date -d AAAA-MM-DD +%A`). No crontab vazado há vários jobs com horários
parecidos (17:03 de domingo, 03:17 em dias úteis, 03:17 do dia 1º...). Só UM
roda às 03:17 de domingo. O valor do parâmetro --lote desse job é o miolo da
flag: VAZANTE{<lote>}.
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-09-screen-e-cron" / "desafio"

CRONTAB = """\
# crontab do usuário mare_alta — copiado do servidor 198.51.100.23 (vazamento de 2026-03)
# m   h    dom mon dow   comando
MAILTO=""
SHELL=/bin/bash

# --- manutenção ---
@reboot                 /home/mare_alta/robo.sh --lote ligar_tudo
*/5  *    *   *   *     /home/mare_alta/robo.sh --lote checar_painel
0    */6  *   *   *     /home/mare_alta/robo.sh --lote limpar_rastros

# --- disparos de mensagens falsas ---
30   9    *   *   1-5   /home/mare_alta/robo.sh --lote cashback_manha
0    12,18 *  *   *     /home/mare_alta/robo.sh --lote cashback_almoco_e_noite
45   20   *   *   6     /home/mare_alta/robo.sh --lote sabado_a_noite

# --- saques (o que interessa) ---
17   3    *   *   1-5   /home/mare_alta/robo.sh --lote saque_dia_util
3    17   *   *   0     /home/mare_alta/robo.sh --lote saque_fim_de_tarde
17   3    1   *   *     /home/mare_alta/robo.sh --lote saque_virada_do_mes
17   3    *   *   0     /home/mare_alta/robo.sh --lote robo_saca_domingo_madrugada
17   4    *   *   7     /home/mare_alta/robo.sh --lote saque_uma_hora_depois
0    3    *   *   sun   /home/mare_alta/robo.sh --lote saque_hora_cheia
"""

EXTRATO = """\
Extrato consolidado — contas de passagem (vítimas 014, 027, 031, 058)
data        hora   valor        destino
15/03/2026  03:17  R$ 4.870,00  conta de passagem 7
22/03/2026  03:17  R$ 2.115,50  conta de passagem 7
29/03/2026  03:17  R$ 6.300,00  conta de passagem 9
05/04/2026  03:17  R$ 1.980,00  conta de passagem 9
"""

ROBO = """\
#!/usr/bin/env bash
# Réplica INOFENSIVA do robô apreendido: só imprime o que faria.
# Uso: bash robo.sh --lote <nome>
echo "[robo] $(date '+%d/%m/%Y %H:%M:%S') executando lote: ${2:-nenhum}"
"""


def main() -> None:
    DESAFIO.mkdir(parents=True, exist_ok=True)
    (DESAFIO / "crontab-robo.txt").write_text(CRONTAB, encoding="utf-8")
    (DESAFIO / "extrato-saques.txt").write_text(EXTRATO, encoding="utf-8")
    (DESAFIO / "robo.sh").write_text(ROBO, encoding="utf-8")
    print(f"Evidências do Dia 9 criadas em {DESAFIO}")


if __name__ == "__main__":
    main()
