"""Gera um notebook Colab (.ipynb) para cada dia a partir do comandos.sh.

Uso (na raiz do repo):
    python3 ferramentas/gerar_notebooks.py          # gera/atualiza notebooks/
    python3 ferramentas/gerar_notebooks.py --checar # só confere se estão em dia (CI)

Como funciona:
    Cada bloco "# %% Título" do comandos.sh vira duas células:
      1. markdown  -> o título + as linhas de comentário logo abaixo dele
      2. código    -> %%bash, entrando na pasta do dia e carregando lib/comum.sh

Assim você edita só o comandos.sh e o notebook acompanha.
Só biblioteca padrão.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
REPO = "Ridd1kulusC0d3r/linux-para-osint-21-dias"
SAIDA = RAIZ / "notebooks"


def celula_md(texto: str) -> dict:
    linhas = texto.strip("\n").split("\n")
    return {"cell_type": "markdown", "metadata": {},
            "source": [l + "\n" for l in linhas[:-1]] + [linhas[-1]]}


def celula_code(texto: str) -> dict:
    linhas = texto.strip("\n").split("\n")
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": [l + "\n" for l in linhas[:-1]] + [linhas[-1]]}


def secoes(script: str) -> list[tuple[str, str, str]]:
    """Quebra o comandos.sh em (titulo, comentario_markdown, codigo)."""
    partes = re.split(r"^# %%[ \t]*(.*)$", script, flags=re.M)
    resultado = []
    # partes = [cabecalho, titulo1, corpo1, titulo2, corpo2, ...]
    for i in range(1, len(partes), 2):
        titulo, corpo = partes[i].strip(), partes[i + 1]
        linhas = corpo.strip("\n").split("\n")
        comentario = []
        while linhas and linhas[0].startswith("#"):
            comentario.append(re.sub(r"^# ?", "", linhas.pop(0)))
        resultado.append((titulo, "\n".join(comentario), "\n".join(linhas).strip("\n")))
    return resultado


def titulo_do_readme(pasta: Path) -> tuple[str, str]:
    readme = (pasta / "README.md").read_text(encoding="utf-8")
    titulo = readme.splitlines()[0].lstrip("# ").strip()
    m = re.search(r"## 🎬 Missão\s*\n(.*?)\n## ", readme, flags=re.S)
    missao = m.group(1).strip() if m else ""
    return titulo, missao


def montar(pasta: Path) -> dict:
    nn = pasta.name.split("-")[1]
    titulo, missao = titulo_do_readme(pasta)
    url_readme = f"https://github.com/{REPO}/tree/main/dias/{pasta.name}"
    celulas = [
        celula_md(
            f"# {titulo}\n\n"
            f"**Linux para OSINT — 21 dias** · baseado no curso de "
            f"[cipher387](https://github.com/cipher387/linux-for-OSINT-21-day) (MIT)\n\n"
            f"📘 Texto completo do dia: [{pasta.name}]({url_readme})\n\n"
            f"## 🎬 Missão\n\n{missao}"
        ),
        celula_md(
            "## ⚙️ Preparação\n\n"
            "Rode a célula abaixo **uma vez**. Ela baixa o repositório para dentro do Colab "
            "e define a variável `L4O_HOME`, que todas as outras células usam.\n\n"
            "> No Colab você é `root` e o `apt` funciona. Cada célula `%%bash` roda num "
            "processo separado: variáveis e `cd` não passam de uma célula para outra."
        ),
        celula_code(
            "import os, subprocess\n"
            "from pathlib import Path\n"
            "\n"
            "# Se já estamos dentro do repositório (Codespaces, máquina local), usa ele.\n"
            "aqui = Path.cwd()\n"
            "candidatos = [aqui, *aqui.parents]\n"
            "raiz = next((p for p in candidatos if (p / 'lib' / 'comum.sh').exists()), None)\n"
            "\n"
            "if raiz is None:  # Colab: clona o repositório\n"
            "    raiz = Path('/content/linux-para-osint-21-dias')\n"
            "    if not raiz.exists():\n"
            f"        subprocess.run(['git', 'clone', '--depth', '1', 'https://github.com/{REPO}', str(raiz)], check=True)\n"
            "\n"
            "os.environ['L4O_HOME'] = str(raiz)\n"
            "os.environ['L4O_CORES'] = '1'\n"
            "print('Repositório em', raiz)"
        ),
    ]
    for titulo_secao, comentario, codigo in secoes((pasta / "comandos.sh").read_text(encoding="utf-8")):
        md = f"### {titulo_secao}"
        if comentario.strip():
            md += "\n\n```text\n" + comentario.strip("\n") + "\n```"
        celulas.append(celula_md(md))
        celulas.append(celula_code(
            "%%bash\n"
            f'cd "$L4O_HOME/dias/{pasta.name}" && source "$L4O_HOME/lib/comum.sh"\n'
            f"{codigo}"
        ))
    if (pasta / "equivalente.py").exists():
        celulas += [
            celula_md("## 🐍 Ponte Python\n\nO mesmo resultado só com a biblioteca padrão do Python:"),
            celula_code(f'!cd "$L4O_HOME/dias/{pasta.name}" && python3 equivalente.py'),
        ]
    if (pasta / "checar.sh").exists():
        celulas += [
        celula_md(
            "## 🧩 Desafio\n\n"
            "Encontrou a flag? Troque o texto abaixo e rode a célula.\n\n"
            "Dicas e passo a passo estão no README do dia."
        ),
        celula_code(
            "flag = 'VAZANTE{troque_aqui}'  # ✏️ cole sua resposta\n"
            f'!cd "$L4O_HOME/dias/{pasta.name}" && bash checar.sh "{{flag}}"'
        ),
        ]
    celulas += [
        celula_md(
            "---\n\n"
            "📝 Anote o que aprendeu no `DIARIO.md` do repositório.\n\n"
            f"Feito por [Deivison Lourenço](https://github.com/Ridd1kulusC0d3r) · "
            f"curso original de [cipher387 / Cyber Detective](https://cybdetective.com)"
        ),
    ]
    return {
        "cells": celulas,
        "metadata": {
            "colab": {"name": f"dia-{nn}.ipynb", "provenance": []},
            "kernelspec": {"display_name": "Python 3", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 0,
    }


def main() -> int:
    checar = "--checar" in sys.argv
    SAIDA.mkdir(exist_ok=True)
    desatualizados = []
    for pasta in sorted((RAIZ / "dias").glob("dia-*")):
        if not (pasta / "comandos.sh").exists():
            continue
        nn = pasta.name.split("-")[1]
        destino = SAIDA / f"dia-{nn}.ipynb"
        conteudo = json.dumps(montar(pasta), ensure_ascii=False, indent=1) + "\n"
        if checar:
            if not destino.exists() or destino.read_text(encoding="utf-8") != conteudo:
                desatualizados.append(destino.name)
        else:
            destino.write_text(conteudo, encoding="utf-8")
            print("✔", destino.relative_to(RAIZ))
    if desatualizados:
        print("Notebooks desatualizados:", ", ".join(desatualizados))
        print("Rode: python3 ferramentas/gerar_notebooks.py")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
