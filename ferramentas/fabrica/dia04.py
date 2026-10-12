"""Fábrica de evidências do Dia 4 — gera 200 conversas exportadas em
desafio/conversas/<data>/conversa-NNN.txt e a lista desafio/selecionadas.txt.

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia04.py
Tudo é fictício. Só stdlib. Sempre gera os MESMOS arquivos (semente fixa).

Como a pista funciona
---------------------
Em 5 das 200 conversas o operador "mare_alta" escorrega e cola um pedaço de
texto ("guarda isso: ..."). Quem acha os arquivos que contêm "mare_alta"
(find + xargs grep -l), ordena pelo nome e junta os pedaços, monta a flag.
"""
from pathlib import Path
import random
import shutil

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-04-processamento-em-lote" / "desafio"
CONVERSAS = DESAFIO / "conversas"

# número da conversa -> pedaço (em ordem crescente = ordem da flag)
PEDACOS = {17: "duzentas_", 58: "conversas_", 103: "um_", 144: "so_", 191: "operador"}

ATENDENTES = ["lucas_suporte", "ana_cashback", "atendente_pix", "suporte_oficial"]
FALAS_VITIMA = [
    "oi, meu cashback não caiu",
    "vocês são da PixVelox mesmo?",
    "recebi um código por SMS, é esse?",
    "não estou conseguindo entrar no app",
    "quanto tempo demora para liberar?",
    "meu filho disse que isso é golpe",
    "já mandei o código, e agora?",
    "o saldo da minha conta sumiu!!",
]
FALAS_GOLPISTA = [
    "Olá! Suporte PixVelox, como posso ajudar?",
    "Para liberar o cashback preciso do código de 6 dígitos.",
    "Fique tranquilo(a), é um procedimento padrão.",
    "Pode me enviar o código que chegou por SMS?",
    "Pronto, em até 24h o valor aparece na sua conta.",
    "Acesse pixvelox.example/cashback e confirme seus dados.",
]


def conversa(n: int, rng: random.Random) -> str:
    atendente = rng.choice(ATENDENTES)
    vitima = f"vitima_{n:03d}"
    dia = 1 + (n - 1) // 20                      # 20 conversas por dia
    linhas = []
    hora, minuto = 9 + rng.randint(0, 9), rng.randint(0, 50)
    for i in range(rng.randint(3, 6)):
        quem, fala = (vitima, rng.choice(FALAS_VITIMA)) if i % 2 == 0 else (atendente, rng.choice(FALAS_GOLPISTA))
        linhas.append(f"2026-03-{dia:02d} {hora:02d}:{minuto + i:02d} | {quem} | {fala}")
    if n in PEDACOS:
        # o deslize do operador, no meio da conversa
        pos = rng.randint(1, len(linhas) - 1)
        linhas.insert(pos, f"2026-03-{dia:02d} {hora:02d}:{minuto + pos:02d} | mare_alta | guarda isso: {PEDACOS[n]}")
    elif n % 37 == 0:
        # pista falsa: cita a "maré" mas não é o operador
        linhas.append(f"2026-03-{dia:02d} {hora:02d}:59 | {vitima} | a maré tá alta hoje na praia kkk")
    return "\n".join(linhas) + "\n"


def main() -> None:
    rng = random.Random(404)
    if CONVERSAS.exists():
        shutil.rmtree(CONVERSAS)
    for n in range(1, 201):
        dia = 1 + (n - 1) // 20
        alvo = CONVERSAS / f"2026-03-{dia:02d}" / f"conversa-{n:03d}.txt"
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_text(conversa(n, rng), encoding="utf-8")
    # lista usada no exemplo de "xargs -I" (zipar só algumas conversas)
    (DESAFIO / "selecionadas.txt").write_text(
        "2026-03-01/conversa-001.txt\n2026-03-01/conversa-002.txt\n2026-03-02/conversa-021.txt\n",
        encoding="utf-8",
    )
    print(f"Evidências do Dia 4 criadas em {DESAFIO}")


if __name__ == "__main__":
    main()
