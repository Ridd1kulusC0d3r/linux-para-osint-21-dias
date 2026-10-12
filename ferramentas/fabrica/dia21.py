"""Fábrica do Dia 21 — sela a flag final com as 20 flags anteriores.

A flag final é cifrada com XOR usando como chave o SHA-256 das 20 flags
(uma por linha, na ordem dos dias). Só quem tem todas consegue abrir o selo.

Rode depois que todos os dias estiverem prontos:
    python3 ferramentas/fabrica/dia21.py
Só stdlib.
"""
import hashlib
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "dias" / "dia-21-distro-e-dossie" / "desafio" / "selo.hex"
FLAG_FINAL = "VAZANTE{mare_baixa_dossie_fechado}"


def flag_do_dia(n: int) -> str:
    sol = RAIZ / "solucoes" / f"dia-{n:02d}.sh"
    saida = subprocess.run(["bash", str(sol)], capture_output=True, text=True,
                           env={"L4O_OFFLINE": "1", "PATH": "/usr/local/bin:/usr/bin:/bin",
                                "HOME": str(Path.home()), "LANG": "C.UTF-8"}, check=True)
    return saida.stdout.strip().splitlines()[-1].strip()


def main() -> None:
    flags = [flag_do_dia(n) for n in range(1, 21)]
    chave = hashlib.sha256("\n".join(flags).encode()).digest()
    dados = FLAG_FINAL.encode()
    selo = bytes(b ^ chave[i % len(chave)] for i, b in enumerate(dados))
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(selo.hex() + "\n", encoding="utf-8")
    print("Selo gravado em", DESTINO.relative_to(RAIZ))
    print("sha256 da flag final:", hashlib.sha256(dados).hexdigest())


if __name__ == "__main__":
    main()
