"""Fábrica de evidências do Dia 5 — gera:

  desafio/sms-golpe.txt              o SMS com o link encurtado
  desafio/cabecalhos-link-golpe.txt  saída salva de `curl -sIL` no link (a cadeia)
  desafio/encurtador.py              servidor local (só stdlib) que REPRODUZ a cadeia
  desafio/salvos/...                 cópias offline das respostas de APIs/sites reais
  desafio/urls-locais.txt            lista para o exemplo de download em lote

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia05.py
Tudo é fictício (domínios .example). Só stdlib.

Como a pista funciona
---------------------
O link encurtado passa por 4 redirecionamentos. Só o ÚLTIMO destino tem o
parâmetro `protocolo=`, codificado em Base64. Quem segue a cadeia até o fim
(curl -sIL ... | grep -i ^location | tail -n 1) e decodifica, acha a flag.
"""
from pathlib import Path
import base64
import json

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-05-curl-e-apis" / "desafio"

FLAG = "VAZANTE{siga_a_cadeia_ate_o_fim}"
LINK_CURTO = "http://encurta.example/x7Kp9"
DATA = "Tue, 03 Mar 2026 14:22:{:02d} GMT"


PAGINA = b"<html><body><h1>Cadastro recebido!</h1><p>Aguarde o contato do suporte PixVelox pelo WhatsApp.</p></body></html>\n"


def cadeia() -> str:
    protocolo = base64.b64encode(FLAG.encode()).decode()
    saltos = [
        ("301 Moved Permanently", "http://rastreio.encurta.example/clique?id=x7Kp9&canal=sms", "encurta"),
        ("302 Found", "http://promo.pixvelox.example/cashback?origem=sms&cupom=PIXDOBRO", "encurta"),
        ("302 Found", "http://pixvelox.example/cadastro?cupom=PIXDOBRO&indicacao=mare_alta", "nginx"),
        ("302 Found", f"http://suporte-pixvelox.example/obrigado?protocolo={protocolo}", "nginx"),
    ]
    blocos = []
    for i, (status, destino, servidor) in enumerate(saltos):
        blocos.append(
            f"HTTP/1.1 {status}\r\n"
            f"Server: {servidor}\r\n"
            f"Date: {DATA.format(i)}\r\n"
            "Content-Length: 0\r\n"
            f"Location: {destino}\r\n"
            "\r\n"
        )
    blocos.append(
        "HTTP/1.1 200 OK\r\n"
        "Server: nginx\r\n"
        f"Date: {DATA.format(len(saltos))}\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(PAGINA)}\r\n"
        "X-Powered-By: PixVelox-Painel/0.9\r\n"
        "\r\n"
    )
    return "".join(blocos)


ENCURTADOR = r'''#!/usr/bin/env python3
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
'''

SMS = (
    "De: +55 31 90000-4477  —  03/03/2026 14:21\n"
    "PixVelox: Seu CASHBACK de R$ 287,40 expira HOJE! Resgate agora: "
    f"{LINK_CURTO}\n"
)

# --- Cópias offline de respostas REAIS e públicas (reduzidas para o curso) ---
# Palácio do Planalto (CEP 70150-900) e Banco do Brasil (CNPJ 00.000.000/0001-91),
# ambos órgão/empresa pública. Campos simplificados; consulte a API para a versão atual.
CEP = {
    "cep": "70150900",
    "state": "DF",
    "city": "Brasília",
    "neighborhood": "Zona Cívico-Administrativa",
    "street": "Praça dos Três Poderes",
    "service": "copia-salva-para-o-curso",
}
CNPJ = {
    "cnpj": "00000000000191",
    "razao_social": "BANCO DO BRASIL SA",
    "nome_fantasia": "DIRECAO GERAL",
    "uf": "DF",
    "municipio": "BRASILIA",
    "natureza_juridica": "Sociedade de Economia Mista",
    "descricao_situacao_cadastral": "ATIVA",
    "data_inicio_atividade": "1966-08-01",
    "cnae_fiscal_descricao": "Bancos múltiplos, com carteira comercial",
    "_aviso": "cópia reduzida salva para uso offline no curso",
}
EXAMPLE_HEAD = (
    "HTTP/2 200 \r\n"
    "content-type: text/html\r\n"
    "etag: \"84238dfc8092e5d9c0dac8ef93371a07:1736799080.121134\"\r\n"
    "last-modified: Mon, 13 Jan 2025 20:11:20 GMT\r\n"
    "cache-control: max-age=3022\r\n"
    "date: Tue, 03 Mar 2026 14:00:00 GMT\r\n"
    "\r\n"
)
DOCS = {
    "rfc2606-resumo.txt": (
        "RFC 2606 — Reserved Top Level DNS Names (resumo do curso)\n"
        "Reserva .test, .example, .invalid e .localhost para testes e documentação.\n"
        "É por isso que a PixVelox usa pixvelox.example: esse domínio nunca vai existir.\n"
    ),
    "rfc9110-resumo.txt": (
        "RFC 9110 — HTTP Semantics (resumo do curso)\n"
        "301 = mudou de endereço para sempre; 302 = mudou temporariamente;\n"
        "o novo endereço vem no cabeçalho Location.\n"
    ),
}


def main() -> None:
    salvos = DESAFIO / "salvos"
    salvos.mkdir(parents=True, exist_ok=True)
    (DESAFIO / "sms-golpe.txt").write_text(SMS, encoding="utf-8")
    (DESAFIO / "cabecalhos-link-golpe.txt").write_text(cadeia(), encoding="utf-8", newline="")
    (DESAFIO / "encurtador.py").write_text(ENCURTADOR, encoding="utf-8")
    (salvos / "cep-70150900.json").write_text(json.dumps(CEP, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (salvos / "cnpj-00000000000191.json").write_text(json.dumps(CNPJ, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (salvos / "cabecalhos-example.com.txt").write_text(EXAMPLE_HEAD, encoding="utf-8", newline="")
    for nome, texto in DOCS.items():
        (salvos / nome).write_text(texto, encoding="utf-8")
    (DESAFIO / "urls-locais.txt").write_text(
        "".join(f"http://127.0.0.1:8086/{nome}\n" for nome in DOCS), encoding="utf-8")
    (DESAFIO / "urls.txt").write_text(
        "https://www.rfc-editor.org/rfc/rfc2606.txt\n"
        "https://www.rfc-editor.org/rfc/rfc6761.txt\n",
        encoding="utf-8",
    )
    print(f"Evidências do Dia 5 criadas em {DESAFIO}")


if __name__ == "__main__":
    main()
