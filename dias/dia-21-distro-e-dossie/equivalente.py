"""Dia 21 — distro, progresso e o selo, em Python puro (só biblioteca padrão).

Rode:  python3 equivalente.py

Ponte Linux -> Python:
    cat /etc/os-release   -> platform.freedesktop_os_release()
    uname -r / uname -m   -> platform.release() / platform.machine()
    command -v apt        -> shutil.which("apt")
    sha256sum             -> hashlib.sha256()
    find .progresso ...   -> Path.glob("*.flag")
"""
import hashlib
import platform
import shutil
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]


def main() -> None:
    try:
        info = platform.freedesktop_os_release()   # lê /etc/os-release
        print(f"Distro: {info.get('PRETTY_NAME', '?')}  ·  deriva de: {info.get('ID_LIKE', '-')}")
    except OSError:
        print("Distro: não é Linux (ou não tem /etc/os-release)")
    print(f"Kernel: {platform.release()}  ·  Arquitetura: {platform.machine()}")

    gerenciadores = [g for g in ("apt", "dnf", "pacman", "zypper", "apk") if shutil.which(g)]
    print("Gerenciadores de pacotes:", ", ".join(gerenciadores) or "nenhum conhecido")

    flags = sorted((RAIZ / ".progresso").glob("*.flag"))
    print(f"Pistas registradas: {len(flags)} de 20")

    # hash: uma vírgula muda tudo
    for texto in ("maré alta", "maré alta."):
        print(f"sha256({texto!r}) = {hashlib.sha256(texto.encode()).hexdigest()[:16]}…")

    # XOR: o mesmo gesto cifra e decifra
    chave, msg = b"coruja", b"pista secreta"
    xor = lambda dados: bytes(b ^ chave[i % len(chave)] for i, b in enumerate(dados))
    print("XOR ida e volta:", xor(xor(msg)).decode())


if __name__ == "__main__":
    main()
