"""Fábrica de evidências do Dia 17 — o torrent do "kit golpe" e as amostras.

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia17.py
Tudo é fictício. Só stdlib — inclusive o bencode, escrito à mão abaixo.

Gera em dias/dia-17-compartilhamento-de-arquivos/desafio/:
  kit_golpe_pixvelox.torrent  torrent válido (bencode) com comentário,
                              "created by", data, trackers .example e lista de
                              arquivos. Os arquivos de config/ trazem, na ordem,
                              as palavras da flag.
  amostras/                   6 roteiros de golpe; um deles tem o SHA-256 que
                              a vítima 014 informou (exercício de hash).
  denuncia_vitima014.txt      a denúncia com o hash conhecido.
  ftp_listagem.txt            cópia salva de uma listagem FTP (modo offline).
"""
from pathlib import Path
import hashlib
import shutil

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-17-compartilhamento-de-arquivos" / "desafio"

PALAVRAS = ["torrent", "tambem", "deixa", "rastro"]   # VAZANTE{torrent_tambem_deixa_rastro}
TAM_PEDACO = 16 * 1024                                # 16 KiB por pedaço


# --------------------------------------------------------------------------
# bencode: o formato dos .torrent
#   inteiro  -> i42e
#   texto    -> 4:spam      (tamanho, dois-pontos, bytes)
#   lista    -> l ... e
#   dicionário -> d chave valor ... e   (chaves em ordem alfabética)
# --------------------------------------------------------------------------
def bencode(valor) -> bytes:
    if isinstance(valor, int):
        return b"i%de" % valor
    if isinstance(valor, str):
        valor = valor.encode("utf-8")
    if isinstance(valor, bytes):
        return b"%d:%s" % (len(valor), valor)
    if isinstance(valor, list):
        return b"l" + b"".join(bencode(v) for v in valor) + b"e"
    if isinstance(valor, dict):
        partes = []
        for chave in sorted(valor, key=lambda k: k.encode() if isinstance(k, str) else k):
            partes.append(bencode(chave) + bencode(valor[chave]))
        return b"d" + b"".join(partes) + b"e"
    raise TypeError(type(valor))


def conteudo_falso(nome: str, tamanho: int) -> bytes:
    """Bytes determinísticos (sempre iguais) para um arquivo do kit."""
    semente = hashlib.sha256(nome.encode()).digest()
    bloco = (b"# kit PixVelox - " + nome.encode() + b"\n") + semente
    return (bloco * (tamanho // len(bloco) + 1))[:tamanho]


def gerar_torrent() -> None:
    arquivos = [
        ("LEIA-ME.txt", 900),
        ("paginas/index.html", 6_200),
        ("paginas/cashback.html", 4_800),
        ("paginas/img/logo_pixvelox.png", 21_000),
        ("roteiros/suporte_whatsapp_v3.txt", 3_100),
        ("roteiros/respostas_prontas.txt", 2_400),
        ("listas/numeros_alvo_lote07.csv", 12_000),
    ]
    # As palavras da flag viram nomes dos arquivos de configuração, numerados
    for i, palavra in enumerate(PALAVRAS, 1):
        arquivos.append((f"config/{i:02d}_{palavra}.cfg", 300 + 37 * i))
    arquivos.append(("config/00_LEIA_PRIMEIRO.cfg", 420))

    # Concatena todo o conteúdo e calcula o SHA-1 de cada pedaço (é assim que
    # um torrent garante que cada parte baixada não foi adulterada)
    tudo = b"".join(conteudo_falso(n, t) for n, t in arquivos)
    pedacos = b"".join(hashlib.sha1(tudo[i:i + TAM_PEDACO]).digest()
                       for i in range(0, len(tudo), TAM_PEDACO))

    info = {
        "name": "kit_golpe_pixvelox_v7",
        "piece length": TAM_PEDACO,
        "pieces": pedacos,
        "files": [{"length": t, "path": n.split("/")} for n, t in arquivos],
    }
    torrent = {
        "announce": "udp://tracker.vazantes.example:6969/announce",
        "announce-list": [["udp://tracker.vazantes.example:6969/announce"],
                          ["http://tracker2.pxv-tunel.example:8080/announce"]],
        "comment": "kit completo v7. config/: ler na ordem dos numeros, pular o 00. "
                   "duvidas no grupo. -- mare_alta",
        "created by": "mktorrent 1.1 (maquina: MAREALTA-NOTE)",
        "creation date": 1788249600,   # 2026-09-01 08:00 UTC
        "info": info,
    }
    (DESAFIO / "kit_golpe_pixvelox.torrent").write_bytes(bencode(torrent))


ROTEIROS = {
    "roteiro_a.txt": "Olá! Aqui é do suporte PixVelox. Seu cashback está pronto.\n",
    "roteiro_b.txt": "Olá! Aqui é do suporte PixVelox. Seu cashback está pronto!\n",
    "roteiro_c.txt": ("Olá! Aqui é do suporte PixVelox. Para liberar seu cashback de "
                      "R$ 150,00, me envie o código de 6 dígitos que chegou por SMS.\n"),
    "roteiro_d.txt": "Olá, aqui é do suporte PixVelox. Seu cashback está pronto.\n",
    "roteiro_e.txt": "Bom dia! Suporte PixVelox. Confirme seu nome completo, por favor.\n",
    "roteiro_f.txt": "Olá! Aqui é do suporte PixVelox. Seu cashback está pronto. \n",
}
ROTEIRO_DA_VITIMA = "roteiro_c.txt"


def gerar_amostras() -> None:
    pasta = DESAFIO / "amostras"
    pasta.mkdir(parents=True, exist_ok=True)
    for nome, texto in ROTEIROS.items():
        (pasta / nome).write_text(texto, encoding="utf-8")
    h = hashlib.sha256(ROTEIROS[ROTEIRO_DA_VITIMA].encode("utf-8")).hexdigest()
    (DESAFIO / "denuncia_vitima014.txt").write_text(
        "Denúncia — vítima 014 (Betim/MG), 18/09/2026\n"
        "A vítima salvou a mensagem do 'suporte' como arquivo e o perito do\n"
        "plantão calculou a impressão digital (SHA-256) dela:\n"
        "\n"
        f"  sha256: {h}\n"
        "\n"
        "Qual roteiro do kit foi usado contra ela?\n",
        encoding="utf-8")


def gerar_ftp() -> None:
    (DESAFIO / "ftp_listagem.txt").write_text(
        "drwxr-xr-x   2 ftp      ftp          4096 Sep 01  2026 kits\n"
        "-rw-r--r--   1 ftp      ftp           512 Sep 01  2026 LEIA-ME.txt\n"
        "-rw-r--r--   1 ftp      ftp          1136 Sep 01  2026 kit_golpe_pixvelox.torrent\n"
        "drwxr-xr-x   2 ftp      ftp          4096 Sep 03  2026 listas\n",
        encoding="utf-8")


def main() -> None:
    if DESAFIO.exists():
        shutil.rmtree(DESAFIO)
    DESAFIO.mkdir(parents=True)
    gerar_torrent()
    gerar_amostras()
    gerar_ftp()
    print(f"Evidências do Dia 17 criadas em {DESAFIO}")


if __name__ == "__main__":
    main()
