"""Fábrica de evidências do Dia 16 — resultados de busca salvos (ddgr e netlas).

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia16.py
Tudo é fictício (domínios .example, IPs da faixa de documentação 203.0.113.0/24
e 198.51.100.0/24, reservadas pela RFC 5737). Só stdlib.

A trilha da flag:
  1. busca_pixvelox.txt (saída do ddgr) -> `grep -o '\\[.*]'` lista os sites;
     um deles é um domínio de infraestrutura: painel.pxv-tunel.example
  2. netlas_resultados.json (saída do netlas download, uma linha JSON por
     servidor) -> jq filtra só esse host, ordena por porta e os pedaços entre
     colchetes dos títulos formam a flag.
"""
from pathlib import Path
import json

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-16-automacao-de-busca" / "desafio"

HOST = "painel.pxv-tunel.example"
PEDACOS = ["dork", "certa", "acha", "o", "painel"]   # -> VAZANTE{dork_certa_acha_o_painel}

# ---------------------------------------------------------------------------
# Resultados "do DuckDuckGo" para: pixvelox cashback
# (título, site, url, resumo)
# ---------------------------------------------------------------------------
RESULTADOS_DDG = [
    ("PixVelox — Cashback em todo Pix", "pixvelox.example", "https://pixvelox.example/",
     "Ganhe até 15% de volta em TODO Pix. Mais de 40 mil brasileiros já recebem."),
    ("PixVelox é golpe? Veja 312 reclamações", "reclamacoes.example",
     "https://reclamacoes.example/empresa/pixvelox",
     "Consumidores relatam que o suporte pediu o código de verificação e a conta foi esvaziada."),
    ("Alerta: falso app de cashback via Pix circula no WhatsApp", "noticias-mg.example",
     "https://noticias-mg.example/2026/09/alerta-falso-cashback-pix",
     "Polícia Civil orienta: nenhum banco pede código por mensagem."),
    ("Login — Painel PXV", HOST, f"https://{HOST}/login",
     "Acesso restrito. Usuário e senha da equipe PXV."),
    ("Como funciona o cashback no Pix? Guia completo", "blog-financas.example",
     "https://blog-financas.example/cashback-pix-guia",
     "Cashback é parte do valor devolvido. Desconfie de promessas acima de 5%."),
    ("pixvelox_oficial (@pixvelox_oficial) — perfil", "social.example",
     "https://social.example/@pixvelox_oficial",
     "Cashback em todo Pix 💸 Suporte 24h no WhatsApp."),
    ("Fórum: alguém recebeu o cashback da PixVelox?", "forum-consumidor.example",
     "https://forum-consumidor.example/t/pixvelox/4471",
     "Recebi R$ 0,00 e perdi R$ 1.200. O atendente sumiu depois do código."),
]

# ---------------------------------------------------------------------------
# Resultados "do Netlas" para: http.body:*pixvelox*
# ---------------------------------------------------------------------------
def registros_netlas() -> list[dict]:
    regs = []

    def add(ip, host, porta, titulo, status=200, server="nginx/1.24.0"):
        regs.append({
            "data": {
                "ip": ip,
                "host": host,
                "port": porta,
                "protocol": "http" if porta in (80, 8080) else "https",
                "domain": [host],
                "http": {"title": titulo, "status_code": status,
                         "headers": {"server": [server]}},
                "geo": {"country": "BR", "city": "Belo Horizonte"},
                "last_updated": "2026-10-05T03:14:00Z",
            }
        })

    # Ruído: outros servidores que mencionam pixvelox
    add("203.0.113.10", "pixvelox.example", 443, "PixVelox — Cashback em todo Pix")
    add("203.0.113.10", "pixvelox.example", 80, "301 Moved Permanently", status=301)
    add("198.51.100.7", "reclamacoes.example", 443, "PixVelox é golpe? [reclamações]")
    add("198.51.100.23", "espelho-pxv.example", 443, "Espelho PixVelox [beta]")
    add("198.51.100.23", "espelho-pxv.example", 8443, "Espelho PixVelox [teste]")
    # A infraestrutura escondida: portas fora de ordem para obrigar o sort
    portas = [9004, 9001, 9005, 9003, 9002]
    ordem = sorted(portas)
    for porta in portas:
        pedaco = PEDACOS[ordem.index(porta)]
        add("203.0.113.66", HOST, porta, f"Painel PXV — módulo [{pedaco}]",
            server="Werkzeug/3.0.1 Python/3.12.3")
    add("198.51.100.99", "blog-financas.example", 443, "Cashback no Pix: guia [2026]")
    add("203.0.113.66", HOST, 22, "", status=0, server="")
    return regs


def main() -> None:
    DESAFIO.mkdir(parents=True, exist_ok=True)

    # Saída de texto do ddgr (formato parecido com o real)
    linhas = []
    for i, (titulo, site, _url, resumo) in enumerate(RESULTADOS_DDG, 1):
        linhas.append(f" {i}.  {titulo} [{site}]")
        linhas.append(f"     {resumo}")
        linhas.append("")
    (DESAFIO / "busca_pixvelox.txt").write_text("\n" + "\n".join(linhas), encoding="utf-8")

    # Saída JSON do ddgr (ddgr --json): lista de {abstract, title, url}
    em_json = [{"abstract": r, "title": t, "url": u} for t, _s, u, r in RESULTADOS_DDG]
    (DESAFIO / "busca_pixvelox.json").write_text(
        json.dumps(em_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Saída do netlas download: um objeto JSON por linha (JSON Lines)
    with open(DESAFIO / "netlas_resultados.json", "w", encoding="utf-8") as f:
        for reg in registros_netlas():
            f.write(json.dumps(reg, ensure_ascii=False) + "\n")

    # Lista de dorks para o exercício de automação
    (DESAFIO / "dorks.txt").write_text(
        '"pixvelox"\n'
        '"pixvelox" site:social.example\n'
        '"pixvelox" filetype:pdf\n'
        'intitle:"painel pxv"\n'
        'inurl:cashback "pix" "código de verificação"\n',
        encoding="utf-8")
    print(f"Resultados de busca do Dia 16 criados em {DESAFIO}")


if __name__ == "__main__":
    main()
