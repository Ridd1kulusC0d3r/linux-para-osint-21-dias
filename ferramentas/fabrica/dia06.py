"""Fábrica de evidências do Dia 6 — caixa de denúncias e log do falso suporte.

Gera, de forma reproduzível (semente fixa):
  desafio/denuncias.txt      ~1.500 linhas de denúncias recebidas pelo Núcleo
  desafio/log-suporte.txt    ~1.500 linhas do log do "suporte" da PixVelox
  desafio/anotacoes/*.txt    três notas curtas (para grep -r)

Tudo fictício: só domínios .example, sem senhas, sem documentos.
Rode na raiz:  python3 ferramentas/fabrica/dia06.py
"""
import random
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-06-grep" / "desafio"

PROVEDORES = ["correio.example", "mailbr.example", "caixa-postal.example", "webmail.example"]
CIDADES = ["Belo Horizonte", "Contagem", "Betim", "Nova Lima", "Sabará", "Ribeirão das Neves"]
ASSUNTOS = [
    "recebi link de cashback", "pediram código por SMS", "conta zerada depois do suporte",
    "perfil falso no Instagram", "atendente disse que era da PixVelox", "boleto estranho",
    "app pediu acesso à tela", "mensagem com erro de português", "ligaram dizendo ser do banco",
]
ATENDENTES = ["lucas", "camila", "rafa", "bia", "joao.pedro", "marina"]


def main() -> None:
    rnd = random.Random(2026)
    DESAFIO.mkdir(parents=True, exist_ok=True)

    # 1. denúncias: e-mails de vítimas em provedores fictícios
    linhas = []
    for i in range(1, 1501):
        vit = f"vitima{rnd.randint(1, 480):03d}"
        prov = rnd.choice(PROVEDORES)
        cidade = rnd.choice(CIDADES)
        assunto = rnd.choice(ASSUNTOS)
        dia, hora = rnd.randint(1, 30), rnd.randint(0, 23)
        linhas.append(f"2026-09-{dia:02d} {hora:02d}h | {cidade} | {vit}@{prov} | {assunto}")
    # algumas linhas citam o domínio do golpe, em maiúsculas e minúsculas
    for pos in rnd.sample(range(len(linhas)), 40):
        linhas[pos] += rnd.choice([" | link: pixvelox.example/cashback",
                                   " | link: PixVelox.example/bonus",
                                   " | remetente: suporte@pixvelox.example"])
    (DESAFIO / "denuncias.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")

    # 2. log do falso suporte: endereços do próprio golpe
    log = []
    for i in range(1, 1501):
        at = rnd.choice(ATENDENTES)
        vit = f"vitima{rnd.randint(1, 480):03d}@{rnd.choice(PROVEDORES)}"
        acao = rnd.choice(["abriu atendimento", "enviou link", "pediu código", "encerrou", "transferiu"])
        log.append(f"[{i:05d}] {at}@pixvelox.example -> {vit} :: {acao}")
    # iscas: subdomínios parecidos, mas não o certo
    log[311] = "[00312] cofre@pixvelox.example -> sistema@pixvelox.example :: backup agendado"
    log[777] = "[00778] mare_alta@cofre-pixvelox.example -> painel@pixvelox.example :: login"
    # a agulha: o único endereço no subdomínio cofre.pixvelox.example
    log[1203] = ("[01204] painel@pixvelox.example -> "
                 "agulha_achada_no_palheiro@cofre.pixvelox.example :: copia oculta do relatorio")
    (DESAFIO / "log-suporte.txt").write_text("\n".join(log) + "\n", encoding="utf-8")

    # 3. anotações espalhadas, para praticar grep -r e grep em vários arquivos
    notas = DESAFIO / "anotacoes"
    notas.mkdir(exist_ok=True)
    (notas / "bento.txt").write_text(
        "Bento: o log do suporte tem mais de mil linhas. Não leia, filtre.\n"
        "Bento: e-mail tem formato. Formato vira regex.\n", encoding="utf-8")
    (notas / "iara.txt").write_text(
        "Iara: golpista gosta de subdomínio. Repare no que vem antes de pixvelox.example.\n",
        encoding="utf-8")
    (notas / "jurema.txt").write_text(
        "Jurema: as denúncias têm e-mail de vítima. Isso é dado pessoal — LGPD.\n"
        "Jurema: use só para a investigação e não compartilhe a lista.\n", encoding="utf-8")
    print(f"Evidências do Dia 6 criadas em {DESAFIO}")


if __name__ == "__main__":
    main()
