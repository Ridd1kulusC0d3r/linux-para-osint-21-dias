"""Dia 17 — o mesmo do terminal, em Python puro (só biblioteca padrão).

Rode:  python3 equivalente.py

Ponte Linux -> Python:
    sha256sum arquivo        -> hashlib.sha256(Path(arquivo).read_bytes()).hexdigest()
    md5sum arquivo           -> hashlib.md5(...).hexdigest()
    sha256sum ... | grep H   -> comparar hexdigest() com o hash procurado
    transmission-show        -> decodificar o bencode (função abaixo, ~25 linhas)
    transmission-show -m     -> "magnet:?xt=urn:btih:" + sha1(bencode(info))
    urldecode                -> urllib.parse.unquote / parse_qs
"""
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse
import hashlib

AQUI = Path(__file__).resolve().parent
DESAFIO = AQUI / "desafio"


# ---------------------------------------------------------------------------
# Decodificador de bencode
#   i42e -> 42   |   4:spam -> b"spam"   |   l...e -> lista   |   d...e -> dict
# Devolve (valor, posição onde parou).
# ---------------------------------------------------------------------------
def bdecode(dados: bytes, i: int = 0):
    c = dados[i:i + 1]
    if c == b"i":                                   # inteiro: i<número>e
        fim = dados.index(b"e", i)
        return int(dados[i + 1:fim]), fim + 1
    if c == b"l":                                   # lista: l<itens>e
        i, lista = i + 1, []
        while dados[i:i + 1] != b"e":
            item, i = bdecode(dados, i)
            lista.append(item)
        return lista, i + 1
    if c == b"d":                                   # dicionário: d<chave><valor>...e
        i, dic = i + 1, {}
        while dados[i:i + 1] != b"e":
            chave, i = bdecode(dados, i)
            valor, i = bdecode(dados, i)
            dic[chave.decode()] = valor
        return dic, i + 1
    dois_pontos = dados.index(b":", i)              # texto: <tamanho>:<bytes>
    tamanho = int(dados[i:dois_pontos])
    inicio = dois_pontos + 1
    return dados[inicio:inicio + tamanho], inicio + tamanho


def bencode(v) -> bytes:
    """O inverso (precisamos dele para recalcular o info hash)."""
    if isinstance(v, int):
        return b"i%de" % v
    if isinstance(v, bytes):
        return b"%d:%s" % (len(v), v)
    if isinstance(v, list):
        return b"l" + b"".join(bencode(x) for x in v) + b"e"
    return b"d" + b"".join(bencode(k.encode()) + bencode(v[k]) for k in sorted(v)) + b"e"


def main() -> None:
    # 1. Hashes das amostras e busca pelo hash da denúncia
    print("sha256sum das amostras:")
    hashes = {}
    for arq in sorted((DESAFIO / "amostras").glob("*.txt")):
        h = hashlib.sha256(arq.read_bytes()).hexdigest()
        hashes[h] = arq.name
        print(f"  {h[:16]}…  {arq.name}")
    denuncia = (DESAFIO / "denuncia_vitima014.txt").read_text(encoding="utf-8")
    alvo = denuncia.split("sha256:")[1].split()[0]
    print("roteiro usado contra a vítima 014:", hashes.get(alvo, "não encontrado"))

    # 2. Decodificando o .torrent
    torrent, _ = bdecode((DESAFIO / "kit_golpe_pixvelox.torrent").read_bytes())
    info = torrent["info"]
    criado = datetime.fromtimestamp(torrent["creation date"], tz=timezone.utc)
    print("\nnome:      ", info["name"].decode())
    print("criado por:", torrent["created by"].decode())
    print("criado em: ", f"{criado:%d/%m/%Y %H:%M} UTC")
    print("comentário:", torrent["comment"].decode())
    print("trackers:  ", [t[0].decode() for t in torrent["announce-list"]])
    print("arquivos:")
    for f in info["files"]:
        caminho = "/".join(p.decode() for p in f["path"])
        print(f"  {f['length']:>7}  {caminho}")

    # 3. Info hash e link magnet (SHA-1 do dicionário "info" em bencode)
    info_hash = hashlib.sha1(bencode(info)).hexdigest()
    magnet = (f"magnet:?xt=urn:btih:{info_hash}&dn={quote(info['name'].decode())}"
              + "".join(f"&tr={quote(t[0].decode(), safe='')}" for t in torrent["announce-list"]))
    print("\nmagnet:", magnet)
    campos = parse_qs(urlparse(magnet).query)          # urldecode automático
    print("trackers decodificados do magnet:", campos["tr"])


if __name__ == "__main__":
    main()
