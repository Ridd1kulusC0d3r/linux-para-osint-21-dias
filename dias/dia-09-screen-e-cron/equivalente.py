"""Dia 9 — ler um crontab e descobrir "quem roda quando", em Python puro.

Rode:  python3 equivalente.py

O cron é só um laço que, a cada minuto, pergunta para cada linha:
"os 5 campos batem com AGORA?". Vamos escrever esse teste à mão.

Ponte Linux -> Python:
    date -d 2026-03-15 +%A  -> datetime.date(2026, 3, 15).strftime("%A")
    date +%u (1=seg..7=dom) -> date.isoweekday()
    campos do crontab       -> linha.split(maxsplit=5)
    screen -dmS (fundo)     -> subprocess.Popen(...)   (processo que segue sozinho)
    while true; sleep 60    -> while True: time.sleep(60)
"""
from datetime import datetime
from pathlib import Path
import subprocess
import sys

AQUI = Path(__file__).resolve().parent
CRONTAB = AQUI / "desafio" / "crontab-robo.txt"
NOMES_DIAS = {"sun": 0, "mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6}


def bate(campo: str, valor: int, semana: bool = False) -> bool:
    """Diz se um campo do cron (ex.: '*', '*/5', '1-5', '12,18', 'sun') aceita o valor."""
    for parte in campo.split(","):
        parte = str(NOMES_DIAS.get(parte.lower(), parte))
        passo = 1
        if "/" in parte:
            parte, p = parte.split("/")
            passo = int(p)
        if parte == "*":
            inicio, fim = 0, 59
        elif "-" in parte:
            inicio, fim = map(int, parte.split("-"))
        else:
            inicio = fim = int(parte)
        candidatos = set(range(inicio, fim + 1, passo))
        if semana and 7 in candidatos:      # no cron, 0 e 7 são domingo
            candidatos.add(0)
        if valor in candidatos:
            return True
    return False


def roda_em(linha: str, quando: datetime) -> bool:
    m, h, dia, mes, sem = linha.split()[:5]
    dia_semana = quando.isoweekday() % 7          # 0 = domingo, como no cron
    # (simplificação: o cron real trata dia-do-mês e dia-da-semana com "OU"
    #  quando os dois são restritos; aqui nenhum job do caso faz isso)
    return (bate(m, quando.minute) and bate(h, quando.hour) and bate(dia, quando.day)
            and bate(mes, quando.month) and bate(sem, dia_semana, semana=True))


def main() -> None:
    jobs = [l for l in CRONTAB.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith(("#", "@")) and "=" not in l.split()[0]]
    print(f"{len(jobs)} jobs com horário no crontab")

    saque = datetime(2026, 3, 15, 3, 17)
    print(f"{saque:%d/%m/%Y} foi {saque.strftime('%A')} (isoweekday={saque.isoweekday()})")
    for job in jobs:
        if roda_em(job, saque):
            lote = job.split()[-1]
            print("roda às 03:17 de domingo ->", lote)
            print("flag -> VAZANTE{" + lote + "}")

    # screen -dmS: um processo que segue sem prender o terminal
    proc = subprocess.Popen([sys.executable, "-c", "print('[robo] rodando em segundo plano')"])
    proc.wait()


if __name__ == "__main__":
    main()
