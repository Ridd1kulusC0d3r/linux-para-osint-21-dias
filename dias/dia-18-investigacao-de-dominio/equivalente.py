"""Dia 18 — o mesmo do terminal, em Python puro (só biblioteca padrão).

Rode:  python3 equivalente.py

Ponte Linux -> Python:
    whois dominio            -> socket: conectar em whois.registro.br:43 e enviar o nome
    grep '^created:'         -> linhas que começam com "created:"
    dig +short dominio A     -> socket.gethostbyname(dominio)
    dig -x IP                -> socket.gethostbyaddr(IP)
    awk '$4 == "TXT"'        -> linha.split("\\t")[3] == "TXT"
    sort | uniq -d           -> collections.Counter(...) com contagem > 1
(A stdlib não consulta MX/NS/TXT; para isso existe o pacote dnspython.)
"""
from collections import Counter, defaultdict
from pathlib import Path
import socket

AQUI = Path(__file__).resolve().parent
DESAFIO = AQUI / "desafio"


def whois_online(dominio: str, servidor: str = "whois.registro.br") -> str:
    """O protocolo whois é simples: abre TCP na porta 43, manda o nome, lê tudo."""
    with socket.create_connection((servidor, 43), timeout=10) as s:
        s.sendall(dominio.encode() + b"\r\n")
        partes = []
        while dado := s.recv(4096):
            partes.append(dado)
    return b"".join(partes).decode("utf-8", "replace")


def campos_whois(texto: str) -> list[tuple[str, str]]:
    """Transforma 'chave:   valor' em pares (ignora comentários com %)."""
    pares = []
    for linha in texto.splitlines():
        if ":" in linha and not linha.startswith("%"):
            chave, valor = linha.split(":", 1)
            pares.append((chave.strip(), valor.strip()))
    return pares


def main() -> None:
    socket.setdefaulttimeout(5)                # não fica pendurado sem internet
    # 1. whois (online de verdade se der; senão, as cópias salvas)
    try:
        real = whois_online("registro.br")
        print("whois registro.br (online) ->", [v for k, v in campos_whois(real) if k == "created"][:1])
    except OSError:
        print("whois online indisponível: usando as cópias salvas")

    # 2. dig +short (A) com o resolvedor do sistema
    try:
        print("example.com ->", socket.gethostbyname("example.com"))
    except OSError:
        print("DNS online indisponível")

    # 3. Correlação dos whois salvos
    valores = defaultdict(set)                 # (campo, valor) -> domínios
    for arq in sorted((DESAFIO / "whois").glob("*.txt")):
        dominio = arq.stem
        for chave, valor in campos_whois(arq.read_text(encoding="utf-8")):
            if chave in ("tech-c", "nserver", "e-mail"):
                valores[(chave, valor)].add(dominio)
    print("\nem mais de um domínio:")
    for (chave, valor), doms in sorted(valores.items()):
        if len(doms) > 1:
            print(f"  {chave}: {valor}  <- {sorted(doms)}")

    # 4. Quantas vezes cada tech-c aparece (sort | uniq -c)
    tech = Counter(v for (k, v), d in valores.items() if k == "tech-c" for _ in d)
    print("\ntech-c:", dict(tech))

    # 5. Registros DNS salvos, separados por tipo (awk '$4 == "TXT"')
    print("\nregistros TXT por domínio:")
    for arq in sorted((DESAFIO / "dns").glob("*.txt")):
        txts = [l.split("\t")[4] for l in arq.read_text(encoding="utf-8").splitlines()
                if l.split("\t")[3] == "TXT"]
        print(f"  {arq.stem}: {len(txts)} registros TXT")


if __name__ == "__main__":
    main()
