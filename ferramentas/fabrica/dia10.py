"""Fábrica de evidências do Dia 10 — gera as listas de membros de dois grupos
de "suporte" d'Os Vazantes.

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia10.py
Tudo é fictício (telefones no formato (31) 90000-XXXX). Só stdlib.
Sempre gera os MESMOS arquivos (semente fixa).

Arquivos
--------
desafio/grupo-a-cashback-vip.csv   telefone,apelido,entrou_em   (com linhas repetidas)
desafio/grupo-a-ontem.csv          o mesmo grupo um dia antes (para treinar diff)
desafio/grupo-b-suporte-pix.txt    APELIDO;TELEFONE              (outra ordem, outro separador,
                                                                apelidos em MAIÚSCULAS)

Como a pista funciona
---------------------
Só UM telefone está nos dois grupos. Quem extrai a coluna de telefone de cada
lista (cut), ordena sem repetição (sort -u) e cruza (comm -12) acha o número.
O apelido desse número no grupo A e no grupo B (este em minúsculas, via tr),
juntos com "_", formam a flag:  VAZANTE{<apelido_A>_<apelido_B>}.
"""
from pathlib import Path
import random

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-10-utilitarios-de-texto" / "desafio"

COMUM = "(31) 90000-7313"
APELIDO_A = "um_chip"
APELIDO_B = "dois_grupos"

PREFIXOS = ["ana", "bia", "caio", "duda", "edu", "fabi", "gui", "helo", "igor", "ju",
            "leo", "malu", "nina", "otto", "pri", "rafa", "say", "tito", "vivi", "zeca"]
SUFIXOS = ["cashback", "pix", "promo", "vip", "bh", "contagem", "betim", "suporte", "app", "ofertas"]


def telefone(n: int) -> str:
    return f"(31) 90000-{n:04d}"


def main() -> None:
    rng = random.Random(10)
    DESAFIO.mkdir(parents=True, exist_ok=True)

    numeros = rng.sample(range(1000, 9999), 120)
    numeros = [n for n in numeros if telefone(n) != COMUM]
    nums_a, nums_b = numeros[:55], numeros[55:110]

    apelidos = [f"{p}_{s}" for p in PREFIXOS for s in SUFIXOS]
    rng.shuffle(apelidos)

    # ---------- grupo A ----------
    linhas_a = []
    for i, n in enumerate(nums_a):
        dia = rng.randint(1, 28)
        linhas_a.append(f"{telefone(n)},{apelidos[i]},{dia:02d}/02/2026")
    linhas_a.insert(31, f"{COMUM},{APELIDO_A},14/02/2026")
    # Exportações bagunçadas: algumas linhas saíram duplicadas, e grudadas
    for _ in range(6):
        pos = rng.randrange(len(linhas_a))
        linhas_a.insert(pos + 1, linhas_a[pos])
    ontem = list(linhas_a)
    # Hoje: algumas pessoas saíram e 2 entraram desde ontem
    for _ in range(3):
        pos = rng.randrange(len(linhas_a))
        if not linhas_a[pos].startswith(COMUM):
            linhas_a.pop(pos)
    linhas_a.append(f"{telefone(numeros[110])},novo_membro_1,01/03/2026")
    linhas_a.append(f"{telefone(numeros[111])},novo_membro_2,01/03/2026")
    cab = "telefone,apelido,entrou_em"
    (DESAFIO / "grupo-a-cashback-vip.csv").write_text(cab + "\n" + "\n".join(linhas_a) + "\n", encoding="utf-8")
    (DESAFIO / "grupo-a-ontem.csv").write_text(cab + "\n" + "\n".join(ontem) + "\n", encoding="utf-8")

    # ---------- grupo B ----------
    linhas_b = [f"{apelidos[60 + i].upper()};{telefone(n)}" for i, n in enumerate(nums_b)]
    linhas_b.insert(17, f"{APELIDO_B.upper()};{COMUM}")
    rng.shuffle(linhas_b)
    (DESAFIO / "grupo-b-suporte-pix.txt").write_text(
        "APELIDO;TELEFONE\n" + "\n".join(linhas_b) + "\n", encoding="utf-8")

    # sanidade: exatamente um número em comum
    tel_a = {l.split(",")[0] for l in linhas_a}
    tel_b = {l.split(";")[1] for l in linhas_b}
    assert tel_a & tel_b == {COMUM}, tel_a & tel_b
    print(f"Evidências do Dia 10 criadas em {DESAFIO}")


if __name__ == "__main__":
    main()
