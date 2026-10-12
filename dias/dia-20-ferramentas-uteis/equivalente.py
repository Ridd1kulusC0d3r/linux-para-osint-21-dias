"""Dia 20 — o mesmo do terminal, em Python puro (só biblioteca padrão).

Rode:  python3 equivalente.py

O grande bug do dia — nomes com espaço quebrados em pedaços — praticamente não
existe em Python: um caminho é UM objeto (Path), nunca uma lista de palavras.
Mas o Python tem o seu "shellcheck" na stdlib: compile() acha erros de sintaxe
sem executar nada, como `python3 -m py_compile arquivo.py`.

Ponte Linux -> Python:
    "$pasta"/*.txt              -> sorted(Path(pasta).glob("*.txt"))
    cat "$arquivo"              -> arquivo.read_text()
    tr 'A-Za-z' 'N-ZA-Mn-za-m'  -> codecs.decode(texto, "rot13")
    sed -i 's/a/b/'             -> texto.replace("a", "b")
    history | grep git          -> [l for l in linhas if " git " in f" {l} "]
    shellcheck (sintaxe)        -> compile(codigo, nome, "exec")
    explainshell / urlencode    -> urllib.parse.quote()
    "pasta com espaço" no bash  -> shlex.split() mostra como o shell divide palavras
"""
from pathlib import Path
from urllib.parse import quote
import codecs
import shlex

AQUI = Path(__file__).resolve().parent
DESAFIO = AQUI / "desafio"


def main() -> None:
    # 1. Como o Bash enxerga uma variável SEM aspas: o shlex simula a divisão
    pasta = "pedacos de selo"
    print("sem aspas, o shell vê:", shlex.split(f"cat {pasta}/parte 01.txt"))
    print("com aspas, o shell vê:", shlex.split(f'cat "{pasta}/parte 01.txt"'))
    print("para escrever com segurança:", "cat " + shlex.quote(f"{pasta}/parte 01.txt"))

    # 2. Em Python o caminho é um objeto só — espaços não atrapalham
    arquivos = sorted((DESAFIO / pasta).glob("*.txt"))
    print("\npedaços:", [a.name for a in arquivos])
    rot13 = "".join(a.read_text(encoding="utf-8") for a in arquivos)
    print("selo em ROT13:", rot13[:6] + "…")
    selo = codecs.decode(rot13, "rot13")             # o mesmo que o tr do script
    print("selo decodificado começa com:", selo[:8], "(o resto é com você no desafio)")

    # 3. "sed" em Python: corrigir uma cópia do script, em memória
    script = (DESAFIO / "script_quebrado.sh").read_text(encoding="utf-8")
    corrigido = (script.replace('pasta = "', 'pasta="')
                       .replace("in $pasta/*.txt", 'in "$pasta"/*.txt')
                       .replace("cat $arquivo", 'cat "$arquivo"'))
    mudancas = sum(1 for a, b in zip(script.splitlines(), corrigido.splitlines()) if a != b)
    print(f"\nlinhas corrigidas no script: {mudancas}")

    # 4. "shellcheck" do Python: compile() acha erro de sintaxe sem executar
    for codigo in ("pasta = 'pedacos de selo'", "pasta = = 'x'"):
        try:
            compile(codigo, "<teste>", "exec")
            print(f"  ok      {codigo}")
        except SyntaxError as e:
            print(f"  ERRO    {codigo}   -> {e.msg}")

    # 5. history | grep git
    historico = (DESAFIO / "historico_mare_alta.txt").read_text(encoding="utf-8").splitlines()
    print("\ncomandos git de maré_alta:")
    for n, linha in enumerate(historico, 1):
        if linha.startswith("git "):
            print(f"  {n:>4}  {linha}")

    # 6. Link do explainshell
    cmd = "find . -type f -name '*.txt' -exec sha256sum {} +"
    print("\nexplainshell:", "https://explainshell.com/explain?cmd=" + quote(cmd, safe=""))


if __name__ == "__main__":
    main()
