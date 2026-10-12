"""Dia 15 — o mesmo do terminal, em Python puro (só biblioteca padrão).

Rode:  python3 equivalente.py

Ponte Linux -> Python:
    python3 -m http.server       -> http.server.ThreadingHTTPServer (numa thread)
    curl URL                     -> urllib.request.urlopen(URL).read()
    curl -w '%{http_code}'       -> resposta.status / urllib.error.HTTPError.code
    grep -o 'href="[^"]*"'       -> re.findall(r'href="([^"]*)"', html)
    grep -o '<!--.*-->'          -> re.findall(r"<!--(.*?)-->", html)
    html2text                    -> html.parser.HTMLParser (+ entidades viram texto)
    mini-crawler (fila)          -> collections.deque + set de visitadas
"""
from collections import deque
from functools import partial
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urljoin
from urllib.request import urlopen
import re
import threading

AQUI = Path(__file__).resolve().parent
SITE = AQUI / "desafio" / "site"


class Silencioso(SimpleHTTPRequestHandler):
    """Servidor de arquivos que não imprime uma linha por requisição."""

    def log_message(self, *args):  # noqa: D401 - só silencia o log
        pass


class ParaTexto(HTMLParser):
    """Um html2text de bolso: guarda só o texto, ignorando as tags.

    Com convert_charrefs=True (padrão), entidades como &#86; já chegam
    convertidas em handle_data — é por isso que a flag aparece.
    """

    def __init__(self):
        super().__init__()
        self.partes: list[str] = []

    def handle_data(self, data):
        if data.strip():
            self.partes.append(data.strip())


def baixar(url: str) -> tuple[int, str]:
    """Equivale a `curl -s -w '%{http_code}' URL`: devolve (código, html)."""
    try:
        with urlopen(url, timeout=5) as resp:
            return resp.status, resp.read().decode("utf-8")
    except HTTPError as e:
        return e.code, ""


def html2text(html: str) -> str:
    leitor = ParaTexto()
    leitor.feed(html)
    return "\n".join(leitor.partes)


def main() -> None:
    # 1. Liga o servidor numa porta livre (porta 0 = o sistema escolhe)
    servidor = ThreadingHTTPServer(("127.0.0.1", 0), partial(Silencioso, directory=str(SITE)))
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{servidor.server_address[1]}"
    print("servidor local em", base)

    try:
        # 2. Links, e-mails e comentários das páginas públicas
        tudo = "".join(baixar(f"{base}/{p}")[1] for p in
                       ("index.html", "cashback.html", "sobre.html", "contato.html"))
        print("\nlinks:", sorted(set(re.findall(r'href="([^"]*)"', tudo))))
        print("e-mails:", sorted(set(re.findall(r"[\w.-]+@[\w.-]+\.example", tudo))))
        print("comentários:")
        for c in sorted(set(re.findall(r"<!--(.*?)-->", tudo))):
            print("   ", c.strip())

        # 3. robots.txt
        _, robots = baixar(f"{base}/robots.txt")
        proibidos = [linha.split()[1] for linha in robots.splitlines() if linha.startswith("Disallow")]
        print("\nrobots.txt proíbe:", proibidos)

        # 4. Mini-crawler a partir do primeiro caminho proibido
        fila, visitadas = deque([urljoin(base, proibidos[0])]), set()
        textos = []
        while fila:
            url = fila.popleft()
            if url in visitadas:
                continue
            visitadas.add(url)
            codigo, html = baixar(url)
            print(f"  {codigo}  {url.replace(base, '')}")
            if codigo != 200:
                continue
            textos.append(html2text(html))
            for link in re.findall(r'href="([^"]*)"', html):
                if not link.startswith(("http", "mailto:", "/")):
                    fila.append(urljoin(url, link))

        # 5. "html2text" em tudo que o crawler achou, procurando a flag
        achados = re.findall(r"VAZANTE\{[^}]*\}", "\n".join(textos))
        print("\nflag encontrada?", "sim" if achados else "não")
    finally:
        servidor.shutdown()        # sempre desligue o servidor (como o kill no Bash)
        servidor.server_close()


if __name__ == "__main__":
    main()
