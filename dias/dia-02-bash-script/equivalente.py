"""Dia 2 — o mesmo do terminal, em Python puro (só biblioteca padrão).

Rode:  python3 equivalente.py

Ponte Linux -> Python:
    nome="x"; echo "$nome"     -> nome = "x"; print(nome)
    $(( a * b ))               -> a * b
    if (( x > 10 )); then      -> if x > 10:
    case "$x" in *abc*)        -> match / if "abc" in x
    for x in "${lista[@]}"     -> for x in lista:
    for i in {1..5}            -> for i in range(1, 6):
    while [ $x -le 5 ]         -> while x <= 5:
    until [ $x -lt 10 ]        -> while not (x < 10):
    funcao() { ...; }          -> def funcao(): ...
    while IFS=';' read -r a b  -> for linha in arquivo: a, b = linha.split(";")
    rev                        -> texto[::-1]
"""
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DESAFIO = AQUI / "desafio"


def saudar(nome: str) -> None:
    """Equivale à função `saudar` do comandos.sh."""
    print(f"Bem-vindo ao Núcleo Coruja, {nome}!")


def decodificar_numeros(dado: str) -> str:
    """'17-21-5-0' -> 'que_'  (0 vira _, N vira a N-ésima letra)."""
    alfabeto = "abcdefghijklmnopqrstuvwxyz"
    return "".join("_" if n == "0" else alfabeto[int(n) - 1] for n in dado.split("-"))


def main() -> None:
    # Variáveis e contas
    alvo, dominio = "PixVelox", "pixvelox.example"
    print(f"Alvo: {alvo} ({dominio}) — {len(alvo)} letras — {alvo.upper()}")
    vitimas, prejuizo_medio = 412, 850
    print(f"Prejuízo estimado: R$ {vitimas * prejuizo_medio}")

    # if / elif / else
    valor = 1200
    print("prejuízo ALTO" if valor > 1000 else "prejuízo baixo")

    # for com lista e com sequência
    for nome in ["lucas_suporte", "mare_alta", "atendente_pix", "bot_cashback"]:
        print("Verificando:", nome)
    for i in range(1, 4):
        print("Rodada", i)

    # while e until
    x = 1
    while x <= 5:
        x += 1
    x = 15
    while not x < 10:          # until [ $x -lt 10 ]
        x -= 1
    print("until terminou em", x)

    # ler arquivo linha a linha (while read)
    for n, linha in enumerate((DESAFIO / "vitimas.txt").read_text(encoding="utf-8").splitlines(), 1):
        print(f"{n}: {linha}")

    saudar("recruta")

    # O decodificador do Bento, completo, em Python
    pedacos = []
    for linha in (DESAFIO / "pistas.txt").read_text(encoding="utf-8").splitlines():
        if not linha or linha.startswith("#"):
            continue
        ordem, metodo, dado = linha.split(";")
        if metodo == "ruido":
            continue
        texto = dado[::-1] if metodo == "inverte" else decodificar_numeros(dado)
        pedacos.append((int(ordem), texto))
    resposta = "".join(texto for _, texto in sorted(pedacos))
    print(f"Pedaços decodificados: {len(pedacos)} (a flag fica para você montar!)")
    print("Primeiro pedaço:", resposta[:2] + "...")


if __name__ == "__main__":
    main()
