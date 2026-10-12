"""Fábrica de evidências do Dia 7 — gera desafio/extrato.csv (transações
fictícias), desafio/contas.txt (apelidos das contas) e os arquivinhos de treino.

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia07.py
Tudo é fictício. Só stdlib. Semente fixa = sempre igual.

Como a pista funciona
---------------------
O extrato tem PIX saindo das vítimas para várias contas de destino. Somando
os valores por conta de destino (awk), a conta que mais recebeu é a CT-0377.
O apelido dela em contas.txt está "sujo" (sublinhados trocados por "~", com
espaços e lixo de exportação); um sed de limpeza revela o texto, e a flag é
VAZANTE{apelido_limpo}.
"""
from pathlib import Path
import random

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-07-sed-e-awk" / "desafio"

CONTAS = {
    "CT-0102": "conta~da~padaria",
    "CT-0219": "reserva~de~emergencia",
    "CT-0377": "o~dinheiro~deixa~rastro",
    "CT-0450": "aluguel~marco",
    "CT-0588": "laranja~de~reserva",
    "CT-0613": "poupanca~ferias",
}
# peso de cada conta no sorteio e faixa de valores (em centavos)
PERFIL = {
    "CT-0102": (3, 2000, 40000),
    "CT-0219": (2, 5000, 90000),
    "CT-0377": (4, 30000, 150000),   # recebe menos vezes que algumas, mas valores maiores
    "CT-0450": (6, 1000, 25000),     # a que MAIS aparece (pista falsa para quem só conta)
    "CT-0588": (2, 20000, 120000),
    "CT-0613": (3, 3000, 60000),
}


def extrato() -> str:
    rng = random.Random(777)
    contas = list(PERFIL)
    pesos = [PERFIL[c][0] for c in contas]
    linhas = ["data,origem,destino,valor,tipo"]
    for i in range(240):
        destino = rng.choices(contas, weights=pesos)[0]
        _, minimo, maximo = PERFIL[destino]
        centavos = rng.randint(minimo, maximo)
        dia = 1 + i // 8
        origem = f"vitima_{rng.randint(1, 412):03d}"
        tipo = "ESTORNO" if rng.random() < 0.05 else "PIX"
        linhas.append(f"2026-03-{dia:02d},{origem},{destino},{centavos / 100:.2f},{tipo}")
    return "\n".join(linhas) + "\n"


def contas_txt() -> str:
    linhas = ["# exportado do painel em 2026-03-31 -- formato: CONTA ; apelido"]
    for conta, apelido in CONTAS.items():
        linhas.append(f"{conta} ;   {apelido}   ##fim")
    return "\n".join(linhas) + "\n"


TREINO_SED = "\n".join(
    ["Relatório do dia: tudo Normal"] * 3
    + ["Atendimento Normal no turno da tarde", "Saque Normal às 23h", "Fim do relatório"]
    + [f"linha {n}: Normal" for n in range(7, 15)]
) + "\n"
TREINO_DIGITOS = "454545 contas\n236464 contas\n2364745 contas\n87907980 contas\n"
TREINO_AWK = (
    "Nome,Cidade,Prejuizo\n"
    "vítima 014,Belo Horizonte,1200\n"
    "vítima 022,Contagem,850\n"
    "vítima 031,Betim,430\n"
    "vítima 047,Belo Horizonte,2100\n"
)


def main() -> None:
    DESAFIO.mkdir(parents=True, exist_ok=True)
    (DESAFIO / "extrato.csv").write_text(extrato(), encoding="utf-8")
    (DESAFIO / "contas.txt").write_text(contas_txt(), encoding="utf-8")
    (DESAFIO / "relatorio.txt").write_text(TREINO_SED, encoding="utf-8")
    (DESAFIO / "digitos.txt").write_text(TREINO_DIGITOS, encoding="utf-8")
    (DESAFIO / "vitimas.csv").write_text(TREINO_AWK, encoding="utf-8")
    print(f"Evidências do Dia 7 criadas em {DESAFIO}")


if __name__ == "__main__":
    main()
