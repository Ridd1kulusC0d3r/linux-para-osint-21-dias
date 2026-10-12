"""Dia 19 — o mesmo do terminal, em Python (só biblioteca padrão + o programa git).

Rode:  python3 equivalente.py

A stdlib não tem um "módulo git", então chamamos o próprio git com subprocess
(é o que bibliotecas como GitPython fazem por baixo). O interessante aqui é
entender COMO o git guarda as coisas: cada arquivo vira um "blob" cujo nome é
o SHA-1 de  b"blob <tamanho>\\0" + conteúdo. Calculamos isso com hashlib.

Ponte Linux -> Python:
    git clone X pasta            -> subprocess.run(["git", "clone", X, pasta])
    git log --format=...         -> saída do subprocess, .splitlines()
    sort | uniq -c               -> collections.Counter
    git hash-object arquivo      -> hashlib.sha1(b"blob %d\\0" % len(c) + c)
    git log --diff-filter=D      -> idem, filtrando commits que apagaram
    git show HASH^:arquivo       -> idem, lendo a versão antiga
"""
from collections import Counter
from pathlib import Path
import hashlib
import subprocess
import tempfile

AQUI = Path(__file__).resolve().parent
BUNDLE = AQUI / "desafio" / "vazantes.bundle"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True).stdout


def hash_blob(conteudo: bytes) -> str:
    """Equivale a `git hash-object`: como o git dá nome a um arquivo."""
    return hashlib.sha1(b"blob %d\0" % len(conteudo) + conteudo).hexdigest()


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "pxv-site"
        subprocess.run(["git", "clone", "-q", str(BUNDLE), str(repo)], check=True)

        # git log --oneline
        print("histórico:")
        for linha in git(repo, "log", "--format=%h %ad %s", "--date=short").splitlines():
            print("  ", linha)

        # Autores e e-mails (OSINT clássico)
        autores = Counter(git(repo, "log", "--format=%an <%ae>").splitlines())
        print("\nautores:", dict(autores))

        # O nome de um arquivo no git é o SHA-1 do conteúdo
        readme = (repo / "README.md").read_bytes()
        print("\nhash do README calculado em Python:", hash_blob(readme))
        print("hash do README segundo o git:      ", git(repo, "rev-parse", "HEAD:README.md").strip())

        # Commits que apagaram arquivos
        apagados = git(repo, "log", "--diff-filter=D", "--name-only", "--format=%h").split()
        commit, arquivos = apagados[0], apagados[1:]
        print(f"\ncommit {commit} apagou: {arquivos}")

        # A versão anterior ao apagamento continua lá
        antigo = git(repo, "show", f"{commit}^:{arquivos[0]}")
        chaves = [l.split("=")[0] for l in antigo.splitlines()]
        print(f"{arquivos[0]} recuperado do histórico — variáveis: {chaves}")
        print("(o valor de PAINEL_CHAVE fica para você no desafio)")


if __name__ == "__main__":
    main()
