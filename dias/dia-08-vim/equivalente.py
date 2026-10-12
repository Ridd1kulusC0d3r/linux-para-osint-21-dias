"""Dia 8 — o que fizemos no Vim, em Python puro (só biblioteca padrão).

Rode:  python3 equivalente.py

Um editor de texto é, no fundo, uma LISTA DE LINHAS. Por isso tudo o que o
Vim faz vira operação de lista em Python.

Ponte Vim -> Python:
    :4242            -> linhas[4241]            (listas começam em 0!)
    /mare_alta       -> [n for n, l in enumerate(linhas, 1) if "mare_alta" in l]
    :%s/velho/novo/g -> [l.replace("velho", "novo") for l in linhas]
    dd               -> del linhas[i]
    yy + p           -> linhas.insert(i + 1, linhas[i])
    :w / :wq         -> Path.write_text("\\n".join(linhas))
    :q!              -> simplesmente não gravar
"""
from pathlib import Path
import re
import tempfile

AQUI = Path(__file__).resolve().parent
LOG = AQUI / "desafio" / "servidor-pixvelox.log"
TREINO = AQUI / "desafio" / "treino-vim.txt"


def main() -> None:
    linhas = LOG.read_text(encoding="utf-8").splitlines()
    print(f"wc -l -> {len(linhas)} linhas")

    # /mare_alta  (como :g/mare_alta/#)
    achados = [n for n, l in enumerate(linhas, 1) if "mare_alta" in l]
    print(f"/mare_alta -> {len(achados)} ocorrências; primeiras: {achados[:5]}")

    # :%s/#MARE#/_/g  e depois  :4242
    corrigidas = [l.replace("#MARE#", "_") for l in linhas]
    alvo = corrigidas[4242 - 1]
    print(":4242 ->", alvo)
    m = re.search(r"VAZANTE\{[^}]*\}", alvo)
    print("flag ->", m.group(0) if m else "não encontrada")

    # dd, yy, p e :wq num arquivo temporário (o original fica intacto)
    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp) / "treino-vim.txt"
        texto = TREINO.read_text(encoding="utf-8").splitlines()
        texto.append(texto[0])                          # 1G yy G p
        del texto[1]                                    # 2G dd
        texto = [l.replace("PixVeloz", "PixVelox") for l in texto]   # :%s///g
        copia.write_text("\n".join(texto) + "\n", encoding="utf-8")  # :wq
        print("\ntreino-vim.txt depois de yy/p/dd/:%s:")
        print(copia.read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()
