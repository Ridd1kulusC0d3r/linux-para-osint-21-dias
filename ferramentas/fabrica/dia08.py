"""Fábrica de evidências do Dia 8 — gera desafio/servidor-pixvelox.log (5 000 linhas)
e desafio/bilhete-iara.txt.

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia08.py
Tudo é fictício. Só stdlib. Sempre gera os MESMOS arquivos (semente fixa).

Como a pista funciona
---------------------
O log do servidor da PixVelox tem 5 000 linhas. O operador "mare_alta" colou
rascunhos de "códigos" no meio do log, mas trocou todo sublinhado por #MARE#
para atrapalhar quem procura com grep. Há 25 códigos falsos (iscas) espalhados.
O verdadeiro está na LINHA 4242, como diz o bilhete da Mestra Iara.

No Vim:  :4242   (pula para a linha)   e   :%s/#MARE#/_/g   (desfaz a troca)
"""
from pathlib import Path
import random

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-08-vim" / "desafio"

TOTAL = 5000
LINHA_CERTA = 4242
SEGREDO = "VAZANTE{esc_dois_pontos_wq}".replace("_", "#MARE#")

ROTAS = ["/api/login", "/api/cashback", "/api/pix/enviar", "/api/suporte/chat",
         "/static/app.js", "/api/codigo/validar", "/promo/cashback10", "/healthz"]
NIVEIS = ["INFO"] * 8 + ["WARN"] * 2 + ["ERROR"]
ISCAS = ["isca", "quase", "nao_e_essa", "pista_falsa", "tente_de_novo", "mare_baixa"]


def linha_comum(rng: random.Random, n: int) -> str:
    """Uma linha de log 'normal', parecida com a de um servidor web."""
    hora = f"{(n // 400) + 2:02d}/03 {(n // 17) % 24:02d}:{n % 60:02d}:{(n * 7) % 60:02d}"
    ip = f"203.0.113.{rng.randint(1, 254)}"        # faixa reservada p/ documentação
    nivel = rng.choice(NIVEIS)
    rota = rng.choice(ROTAS)
    status = 200 if nivel == "INFO" else (429 if nivel == "WARN" else 500)
    return f"{hora} {nivel:<5} {ip} {rota} {status}"


def main() -> None:
    rng = random.Random(8)
    DESAFIO.mkdir(parents=True, exist_ok=True)
    posicoes_iscas = set(rng.sample(range(50, TOTAL), 25)) - {LINHA_CERTA}
    linhas = []
    for n in range(1, TOTAL + 1):
        base = linha_comum(rng, n)
        if n == LINHA_CERTA:
            base += f" DEBUG mare_alta rascunho={SEGREDO}"
        elif n in posicoes_iscas:
            falso = f"VAZANTE{{{rng.choice(ISCAS)}_{n:04d}}}".replace("_", "#MARE#")
            base += f" DEBUG mare_alta rascunho={falso}"
        linhas.append(base)
    (DESAFIO / "servidor-pixvelox.log").write_text("\n".join(linhas) + "\n", encoding="utf-8")

    (DESAFIO / "bilhete-iara.txt").write_text(
        "Recruta,\n"
        "o maré_alta esconde rascunhos no log do servidor e troca todo '_' por '#MARE#'.\n"
        "Tem dezenas de códigos ali — quase todos são isca.\n"
        "O que interessa está na linha 4242. Abra no Vim, vá até ela e desfaça a troca.\n"
        "E não salve nada no original: saia com :q!\n"
        "— I.\n",
        encoding="utf-8",
    )
    # Arquivo pequeno para treinar dd / yy / p sem medo
    (DESAFIO / "treino-vim.txt").write_text(
        "linha 1: esta linha é para copiar (yy) e colar (p)\n"
        "linha 2: esta linha é para apagar (dd)\n"
        "linha 3: aqui o maré_alta escreveu PixVelox errado: PixVeloz\n"
        "linha 4: corrija o nome no arquivo inteiro com uma substituição global (:%s)\n"
        "linha 5: PixVeloz, PixVeloz, PixVeloz\n",
        encoding="utf-8",
    )
    print(f"Evidências do Dia 8 criadas em {DESAFIO}")


if __name__ == "__main__":
    main()
