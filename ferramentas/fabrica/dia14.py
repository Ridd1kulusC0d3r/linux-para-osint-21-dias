"""Fábrica de evidências do Dia 14 — gera o export de um grupo de mensagens
(JSON), o sitemap do site falso (XML) e uma varredura de domínios (CSV).

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia14.py
Tudo é fictício. Só stdlib. Sempre gera os MESMOS arquivos (semente fixa).

Arquivos
--------
desafio/export-grupo.json   {"grupo": {...}, "membros": [...], "mensagens": [...]}
                            ~120 mensagens; algumas "apagadas" (apagada=true)
                            ainda trazem o campo texto_original.
desafio/sitemap.xml         sitemap padrão (com namespace) de pixvelox.example
desafio/dominios.csv        dominio,titulo,porta,registrado_em
desafio/cep-01001000.json   cópia salva de uma resposta pública da BrasilAPI (modo offline)

Como a pista funciona
---------------------
O maré_alta apagou mensagens no grupo, mas o export guardou o texto original.
Filtrando com jq — select(.apagada and .autor.handle == "mare_alta") — e
pegando .texto_original na ordem, saem os pedaços da flag:
VAZANTE{jq_select_acha_o_apagado}. Há mensagens apagadas de OUTROS autores
(iscas) e mensagens normais do maré_alta (sem texto_original).
"""
from pathlib import Path
from datetime import datetime, timedelta
import json
import random

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-14-json-xml-csv" / "desafio"

INICIO = datetime(2026, 3, 1, 8, 0)
PEDACOS = ["VAZANTE{", "jq_", "select_", "acha_", "o_apagado}"]
MEMBROS = [
    {"handle": "mare_alta", "nome_exibido": "Suporte PixVelox", "telefone": "(31) 90000-0042", "admin": True},
    {"handle": "lucas_suporte", "nome_exibido": "Lucas | Suporte", "telefone": "(31) 90000-7313", "admin": True},
    {"handle": "ana_cashback", "nome_exibido": "Ana Cashback", "telefone": "(31) 90000-2211", "admin": False},
    {"handle": "atendente_pix", "nome_exibido": "Atendimento Pix", "telefone": "(31) 90000-5150", "admin": False},
    {"handle": "vitima_014", "nome_exibido": "vítima 014", "telefone": None, "admin": False},
    {"handle": "vitima_027", "nome_exibido": "vítima 027", "telefone": None, "admin": False},
    {"handle": "vitima_031", "nome_exibido": "vítima 031", "telefone": None, "admin": False},
]
FALAS = {
    "mare_alta": ["bom dia equipe, meta de hoje: 40 códigos", "quem fechou o lote 7?",
                  "não usem o chip antigo", "planilha atualizada, aba de controle"],
    "lucas_suporte": ["cliente novo no privado", "mandei o print do contrato",
                      "ela passou o código", "pedindo comprovante"],
    "ana_cashback": ["link novo: pixvelox.example/cashback", "2 vítimas responderam",
                     "banco bloqueou a conta 11"],
    "atendente_pix": ["alguém tem o roteiro?", "cliente desconfiou", "trocando de número amanhã"],
    "vitima_014": ["oi, meu cashback não caiu", "passei o código, e agora?"],
    "vitima_027": ["assinei o contrato", "quando cai o 3%?"],
    "vitima_031": ["isso é golpe?", "vou na delegacia"],
}
ISCAS_APAGADAS = ["mensagem errada, ignora", "VAZANTE{nao_e_essa}", "foto sem querer",
                  "apagado por engano", "VAZANTE{quase_la}"]

SITEMAP_URLS = [
    ("https://pixvelox.example/", "2026-03-01", "1.0"),
    ("https://pixvelox.example/cashback", "2026-03-02", "0.9"),
    ("https://pixvelox.example/suporte", "2026-03-02", "0.8"),
    ("https://pixvelox.example/contrato-parceria", "2026-03-05", "0.5"),
    ("https://pixvelox.example/app/download", "2026-03-03", "0.7"),
    ("https://pixvelox.example/painel-operador-mare", "2026-03-09", "0.1"),
    ("https://suporte-pixvelox.example/chat", "2026-03-04", "0.6"),
]

DOMINIOS = [
    ("pixvelox.example", "PixVelox - o Pix que devolve", 443, "2026-02-14"),
    ("suporte-pixvelox.example", "Suporte PixVelox 24h", 443, "2026-02-15"),
    ("pixvelox-cashback.example", "Cashback PixVelox", 80, "2026-02-20"),
    ("cashback-pix.example", "Cashback Pix oficial", 80, "2026-02-21"),
    ("banco-exemplo.example", "Banco Exemplo - Internet Banking", 443, "2015-06-01"),
    ("loja-ficticia.example", "Loja Fictícia", 443, "2019-09-10"),
    ("pixvel0x.example", "PixVelox - o Pix que devolve", 80, "2026-03-01"),
    ("noticias.example", "Notícias do Brasil", 443, "2012-01-20"),
    ("app-pixvelox.example", "Baixe o app PixVelox", 8080, "2026-03-02"),
]


def mensagens(rng: random.Random) -> list[dict]:
    lista = []
    autores = list(FALAS)
    pos_pedacos = sorted(rng.sample(range(10, 115), len(PEDACOS)))
    pos_iscas = set(rng.sample([i for i in range(5, 118) if i not in pos_pedacos], len(ISCAS_APAGADAS)))
    iscas = iter(ISCAS_APAGADAS)
    pedacos = iter(PEDACOS)
    for i in range(120):
        quando = INICIO + timedelta(minutes=97 * i + rng.randint(0, 40))   # sempre crescente
        dia = quando.day
        msg = {"id": 1000 + i, "data": quando.strftime("%Y-%m-%dT%H:%M:00-03:00")}
        if i in pos_pedacos:
            autor = "mare_alta"
            msg.update(autor={"handle": autor}, texto=None, apagada=True,
                       texto_original=next(pedacos))
        elif i in pos_iscas:
            autor = rng.choice([a for a in autores if a != "mare_alta"])
            msg.update(autor={"handle": autor}, texto=None, apagada=True,
                       texto_original=next(iscas))
        else:
            autor = rng.choice(autores)
            msg.update(autor={"handle": autor}, texto=rng.choice(FALAS[autor]), apagada=False)
        if rng.random() < 0.08:
            msg["anexos"] = [{"tipo": "imagem", "arquivo": f"IMG-202603{dia:02d}-{i:04d}.jpg"}]
        lista.append(msg)
    return lista


def sitemap() -> str:
    linhas = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, data, prioridade in SITEMAP_URLS:
        linhas += ["  <url>", f"    <loc>{loc}</loc>", f"    <lastmod>{data}</lastmod>",
                   f"    <priority>{prioridade}</priority>", "  </url>"]
    linhas.append("</urlset>")
    return "\n".join(linhas) + "\n"


def main() -> None:
    rng = random.Random(14)
    DESAFIO.mkdir(parents=True, exist_ok=True)
    export = {
        "grupo": {"nome": "Suporte PixVelox (equipe)", "criado_em": "2026-02-28T22:00:00-03:00",
                  "criado_por": "mare_alta", "exportado_em": "2026-03-10T09:00:00-03:00"},
        "membros": MEMBROS,
        "mensagens": mensagens(rng),
    }
    (DESAFIO / "export-grupo.json").write_text(
        json.dumps(export, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DESAFIO / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    csv_txt = "dominio,titulo,porta,registrado_em\n" + "".join(
        f'{d},"{t}",{p},{r}\n' for d, t, p, r in DOMINIOS)
    (DESAFIO / "dominios.csv").write_text(csv_txt, encoding="utf-8")
    # cópia salva da resposta pública da BrasilAPI (para o modo offline)
    cep = {"cep": "01001000", "state": "SP", "city": "São Paulo", "neighborhood": "Sé",
           "street": "Praça da Sé", "service": "copia-salva"}
    (DESAFIO / "cep-01001000.json").write_text(json.dumps(cep, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Evidências do Dia 14 criadas em {DESAFIO}")


if __name__ == "__main__":
    main()
