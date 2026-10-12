"""Dia 5 — o mesmo do terminal, em Python puro (só biblioteca padrão).

Rode:  python3 equivalente.py           (tenta a internet; sem rede usa cópias salvas)
       L4O_OFFLINE=1 python3 equivalente.py   (força o modo offline)

Ponte Linux -> Python:
    curl URL                     -> urllib.request.urlopen(URL).read()
    curl URL -o arquivo          -> urllib.request.urlretrieve(URL, arquivo)
    xargs -n 1 curl -O < urls    -> for url in urls: urlretrieve(url, nome_do_fim_da_url)
    curl -I URL                  -> Request(URL, method="HEAD") / resposta.headers
    curl -sIL ... | grep location-> http.client + seguir o cabeçalho Location num laço
    curl -H 'accept: ...'        -> Request(URL, headers={...})
    jq .                         -> json.loads() + json.dumps(indent=2)
    python3 -m http.server       -> http.server.ThreadingHTTPServer
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import http.client
import importlib.util
import json
import os
import sys
import tempfile
import threading
import urllib.request

AQUI = Path(__file__).resolve().parent
DESAFIO = AQUI / "desafio"
SALVOS = DESAFIO / "salvos"


class Silencioso(SimpleHTTPRequestHandler):
    """O mesmo de `python3 -m http.server`, sem imprimir cada acesso."""
    def log_message(self, *args) -> None:
        pass


def online() -> bool:
    if os.environ.get("L4O_OFFLINE"):
        return False
    try:
        urllib.request.urlopen("https://example.com", timeout=5)
        return True
    except Exception:
        return False


def api_json(url: str, copia: Path) -> dict:
    """curl -H 'accept: application/json' URL  (ou a cópia salva, offline)."""
    if ONLINE:
        pedido = urllib.request.Request(url, headers={"accept": "application/json",
                                                      "User-Agent": "curso-linux-osint"})
        with urllib.request.urlopen(pedido, timeout=15) as resp:
            return json.load(resp)
    return json.loads(copia.read_text(encoding="utf-8"))


def cadeia_local(url: str, porta: int) -> list[tuple[int, str]]:
    """Equivale a `curl -sIL --connect-to ::127.0.0.1:porta URL`: pede só os
    cabeçalhos (HEAD) e segue o Location até não haver mais redirecionamento."""
    saltos = []
    for _ in range(10):                                    # limite de segurança
        partes = urlsplit(url)
        conexao = http.client.HTTPConnection("127.0.0.1", porta, timeout=5)
        caminho = partes.path + ("?" + partes.query if partes.query else "")
        conexao.request("HEAD", caminho, headers={"Host": partes.hostname})
        resp = conexao.getresponse()
        destino = resp.getheader("Location")
        saltos.append((resp.status, destino or url))
        conexao.close()
        if not destino:
            break
        url = destino
    return saltos


def main() -> None:
    # 1. curl -I: cabeçalhos
    if ONLINE:
        with urllib.request.urlopen(urllib.request.Request("https://example.com", method="HEAD"), timeout=10) as r:
            print("curl -I example.com ->", r.status, dict(r.headers))
    else:
        print("offline: cabeçalhos salvos de example.com:")
        print((SALVOS / "cabecalhos-example.com.txt").read_text(encoding="utf-8").strip())

    # 2. Download em lote de um servidor local (python3 -m http.server)
    servidor = ThreadingHTTPServer(("127.0.0.1", 0), partial(Silencioso, directory=str(SALVOS)))
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    porta = servidor.server_address[1]
    sem_proxy = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with tempfile.TemporaryDirectory() as tmp:
        for nome in ("rfc2606-resumo.txt", "rfc9110-resumo.txt"):
            url = f"http://127.0.0.1:{porta}/{nome}"
            destino = Path(tmp) / url.rsplit("/", 1)[-1]          # curl -O
            destino.write_bytes(sem_proxy.open(url, timeout=5).read())
        print("\nbaixados (servidor local):", sorted(p.name for p in Path(tmp).iterdir()))
    servidor.shutdown()

    # 3. Cadeia de redirecionamentos do golpe, num encurtador local
    sys.dont_write_bytecode = True                         # não deixa __pycache__ no repo
    spec = importlib.util.spec_from_file_location("encurtador", DESAFIO / "encurtador.py")
    encurtador = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(encurtador)
    falso = ThreadingHTTPServer(("127.0.0.1", 0), encurtador.Encurtador)
    threading.Thread(target=falso.serve_forever, daemon=True).start()
    print("\ncurl -sIL http://encurta.example/x7Kp9 (local):")
    for status, destino in cadeia_local("http://encurta.example/x7Kp9", falso.server_address[1]):
        print(f"  {status}  {destino[:70]}")
    falso.shutdown()
    print("  (decodificar o último destino fica para você!)")

    # 4. APIs da BrasilAPI (ou cópias salvas)
    cep = api_json("https://brasilapi.com.br/api/cep/v1/70150900", SALVOS / "cep-70150900.json")
    print("\nCEP 70150-900 ->", cep.get("street"), "-", cep.get("city"), "/", cep.get("state"))
    cnpj = api_json("https://brasilapi.com.br/api/cnpj/v1/00000000000191", SALVOS / "cnpj-00000000000191.json")
    print("CNPJ 00.000.000/0001-91 ->", json.dumps(
        {k: cnpj.get(k) for k in ("razao_social", "uf", "descricao_situacao_cadastral")}, ensure_ascii=False))


ONLINE = online()

if __name__ == "__main__":
    main()
