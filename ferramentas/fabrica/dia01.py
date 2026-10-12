"""Fábrica de evidências do Dia 1 — gera a pasta desafio/caso/.

Rode a partir da raiz do repo:  python3 ferramentas/fabrica/dia01.py
Tudo é fictício. Só stdlib.
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CASO = RAIZ / "dias" / "dia-01-arquivos-e-pastas" / "desafio" / "caso"

ARQUIVOS = {
    "LEIA-ME.txt": (
        "Pendrive entregue pela Mestra Iara.\n"
        "Bilhete colado: 'comece pelo que ninguém vê'.\n"
    ),
    "vitimas/lista-preliminar.txt": (
        "Relatos recebidos (resumo):\n"
        "- vítima 001, Belo Horizonte: perdeu R$ 1.200 após 'suporte' no WhatsApp\n"
        "- vítima 002, Contagem: recebeu link pixvelox.example/cashback\n"
        "- vítima 003, Belo Horizonte: passou o código de 6 dígitos por SMS\n"
    ),
    "vitimas/belo-horizonte/relato-001.txt": (
        "Relato 001 — atendente se apresentou como 'Lucas do suporte PixVelox'.\n"
        "Pediu o código para 'liberar o cashback'.\n"
    ),
    "vitimas/belo-horizonte/relato-003.txt": (
        "Relato 003 — mesma conversa, mesmo roteiro, outro nome de atendente.\n"
    ),
    "vitimas/belo-horizonte/.nota_iara.txt": (
        "Muito bem, recruta. Arquivos que começam com ponto ficam ocultos.\n"
        "Golpistas também escondem coisas assim. Anote a flag:\n"
        "\n"
        "VAZANTE{o_que_ninguem_ve}\n"
    ),
    "vitimas/contagem/relato-002.txt": (
        "Relato 002 — link recebido: pixvelox.example/cashback\n"
    ),
    "suspeitos/pixvelox.txt": (
        "PixVelox — 'fintech' sem CNPJ localizado até agora.\n"
        "Domínio citado pelas vítimas: pixvelox.example\n"
    ),
    "suspeitos/.cache/lixo.tmp": "arquivo temporário sem importância\n",
    "rascunhos/.nao_e_aqui.txt": "Quase! Esta nota é uma pista falsa. Procure perto das vítimas.\n",
}


def main() -> None:
    for caminho, conteudo in ARQUIVOS.items():
        alvo = CASO / caminho
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_text(conteudo, encoding="utf-8")
    print(f"Evidências do Dia 1 criadas em {CASO}")


if __name__ == "__main__":
    main()
