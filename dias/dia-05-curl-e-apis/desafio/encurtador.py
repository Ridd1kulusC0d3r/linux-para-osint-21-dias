#!/usr/bin/env python3
"""Servidor local que REPRODUZ a cadeia de redirecionamentos salva em
cabecalhos-link-golpe.txt. Serve para treinar `curl -I` e `curl -L` sem
internet e sem tocar no site de verdade dos golpistas.

Uso:  python3 encurtador.py [porta]        (padrão: 8085)
Teste noutro terminal:
  curl -sIL --noproxy '*' --connect-to ::127.0.0.1:8085 http://encurta.example/x7Kp9

O --connect-to faz o curl mandar TODOS os nomes (encurta.example,
pixvelox.example...) para 127.0.0.1:8085, mantendo o nome no cabeçalho Host.
Só biblioteca padrão. Pare com Ctrl+C.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import sys

AQUI = Path(__file__).resolve().parent
PRIMEIRO = "http://encurta.example/x7Kp9"


def carregar_cadeia() -> dict:
    """Lê o arquivo de cabeçalhos e monta {(host, caminho): (status, cabeçalhos)}."""
    texto = (AQUI / "cabecalhos-link-golpe.txt").read_text(encoding="utf-8")
    blocos = [b for b in texto.replace("\r\n", "\n").split("\n\n") if b.strip()]
    rotas, url = {}, PRIMEIRO
    for bloco in blocos:
        linhas = bloco.splitlines()
        status = int(linhas[0].split()[1])
        cabecalhos = [tuple(x.strip() for x in l.split(":", 1)) for l in linhas[1:]]
        partes = urlsplit(url)
        caminho = partes.path + ("?" + partes.query if partes.query else "")
        rotas[(partes.hostname, caminho)] = (status, cabecalhos)
        url = dict((k.lower(), v) for k, v in cabecalhos).get("location", url)
    return rotas


ROTAS = carregar_cadeia()
PAGINA = b"<html><body><h1>Cadastro recebido!</h1><p>Aguarde o contato do suporte PixVelox pelo WhatsApp.</p></body></html>\n"


class Encurtador(BaseHTTPRequestHandler):
    def responder(self, com_corpo: bool) -> None:
        host = (self.headers.get("Host") or "").split(":")[0]
        status, cabecalhos = ROTAS.get((host, self.path), (404, [("Content-Length", "0")]))
        self.send_response(status)
        for nome, valor in cabecalhos:
            if nome.lower() not in ("server", "date"):      # o http.server já manda esses
                self.send_header(nome, valor)
        self.end_headers()
        if com_corpo and status == 200:
            self.wfile.write(PAGINA)

    def do_HEAD(self) -> None:
        self.responder(False)

    def do_GET(self) -> None:
        self.responder(True)

    def log_message(self, *args) -> None:   # silencioso
        pass


if __name__ == "__main__":
    porta = int(sys.argv[1]) if len(sys.argv) > 1 else 8085
    print(f"Encurtador falso ouvindo em http://127.0.0.1:{porta} (Ctrl+C para parar)")
    ThreadingHTTPServer(("127.0.0.1", porta), Encurtador).serve_forever()
