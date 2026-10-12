"""Fábrica de evidências do Dia 20 — o script quebrado de maré_alta.

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia20.py
Tudo é fictício. Só stdlib.

Gera em dias/dia-20-ferramentas-uteis/desafio/:
  script_quebrado.sh     script com 3 bugs clássicos de Bash (o shellcheck
                         aponta todos). Do jeito que está, NÃO monta a flag.
  pedacos de selo/       pasta COM ESPAÇOS no nome, com 5 arquivos também com
                         espaços ("parte 01.txt"...). Cada um guarda um pedaço
                         da flag em ROT13 (troca cada letra pela 13ª seguinte),
                         que o script desfaz com `tr`.
  historico_mare_alta.txt  um ~/.bash_history "esquecido" (exercício de history).

Os bugs:
  1. `pasta = "pedacos de selo"`  -> espaços em volta do = (vira um comando)
  2. `for arquivo in $pasta/*.txt` -> variável sem aspas quebra nos espaços
  3. `cat $arquivo`               -> idem, o nome "parte 01.txt" vira 2 arquivos
"""
from pathlib import Path
import codecs
import shutil

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-20-ferramentas-uteis" / "desafio"

PEDACOS = ["VAZANTE{", "aspas_", "salvam_", "o_", "script}"]   # VAZANTE{aspas_salvam_o_script}

SCRIPT = r'''#!/usr/bin/env bash
# selo.sh — monta o "selo" de acesso do painel a partir dos pedaços.
# Escrito às pressas por mare_alta. "Funcionava na minha máquina."
cd "$(dirname "$0")" || exit 1

pasta = "pedacos de selo"

selo=""
for arquivo in $pasta/*.txt; do
  pedaco=$(cat $arquivo 2>/dev/null)
  selo="$selo$pedaco"
done

if [ -z "$selo" ]; then
  echo "Selo vazio. Alguma coisa deu errado..." >&2
  exit 1
fi

# os pedaços estão em ROT13; tr desfaz
echo "$selo" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
'''

HISTORICO = """cd ~/pxv-site
ls -la
nano config.env
git add config.env
git commit -m "config do painel"
git push
git rm config.env
git commit -m "remove config (ops)"
git push
ssh admin@painel.pxv-tunel.example
bash selo.sh
bash selo.sh
shellcheck selo.sh
history -c
"""


def main() -> None:
    if DESAFIO.exists():
        shutil.rmtree(DESAFIO)
    pasta = DESAFIO / "pedacos de selo"
    pasta.mkdir(parents=True)
    for i, pedaco in enumerate(PEDACOS, 1):
        (pasta / f"parte {i:02d}.txt").write_text(codecs.encode(pedaco, "rot13"), encoding="utf-8")
    script = DESAFIO / "script_quebrado.sh"
    script.write_text(SCRIPT, encoding="utf-8")
    script.chmod(0o755)
    (DESAFIO / "historico_mare_alta.txt").write_text(HISTORICO, encoding="utf-8")
    print(f"Evidências do Dia 20 criadas em {DESAFIO}")


if __name__ == "__main__":
    main()
