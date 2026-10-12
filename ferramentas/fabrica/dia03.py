"""Fábrica de evidências do Dia 3 — gera desafio/inventario.zip (aberto),
desafio/evidencia.zip (protegido por senha) e os arquivinhos de treino.

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia03.py
Precisa do programa `zip` (apt install zip): a biblioteca padrão do Python
lê zips com senha, mas não sabe CRIAR.

Como a pista funciona
---------------------
A senha da evidencia.zip não está DENTRO de nenhum arquivo: está no NOME de
um arquivo do inventario.zip. Quem lista o zip sem extrair (zip -sf ou
unzip -l) vê a senha. Quem extrai tudo e só lê os textos, não vê nada.
"""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-03-instalar-programas" / "desafio"

SENHA = "preamar2026"
FLAG = "VAZANTE{a_senha_estava_no_nome}"
DATA_FIXA = 1772366400  # 2026-03-01 12:00 UTC — datas fixas = zip reproduzível

INVENTARIO = {
    "inventario/LEIA-ME.txt": "Inventário do notebook apreendido com o 'suporte' PixVelox.\nNada de útil nos textos. Só fotos de tela e anotações de rotina.\n",
    "inventario/anotacoes/rotina-segunda.txt": "abrir 3 chips, responder fila, pedir codigo, repassar\n",
    "inventario/anotacoes/rotina-terca.txt": "mesma rotina. mare_alta cobrou meta de 40 contas\n",
    "inventario/anotacoes/roteiro-atendimento.txt": "Ola! Sou do suporte PixVelox. Para liberar seu cashback preciso do codigo de 6 digitos.\n",
    "inventario/fotos/print-001.txt": "(foto de tela: conversa com vítima 014)\n",
    "inventario/fotos/print-002.txt": "(foto de tela: conversa com vítima 022)\n",
    "inventario/fotos/print-003.txt": "(foto de tela: painel de saques)\n",
    # A pista: o conteúdo é inútil, o NOME do arquivo é que importa.
    f"inventario/fotos/.lembrete/cofre_senha={SENHA}.txt": "(vazio)\n",
    "inventario/planilhas/metas-marco.txt": "semana 1: 38 contas | semana 2: 41 contas\n",
}

EVIDENCIA = {
    "evidencia/relatorio-saque.txt": (
        "Relatório interno — saques de março/2026\n"
        "Responsável: mare_alta\n"
        "Contas usadas: ver extrato do banco (pasta financeiro)\n"
        "\n"
        f"Assinatura do lote: {FLAG}\n"
    ),
    "evidencia/contatos-laranjas.txt": "laranja 01 — (31) 90000-0101\nlaranja 02 — (31) 90000-0102\n",
}

TREINO = {
    "test1.txt": "arquivo de teste 1 — evidência fictícia\n",
    "test2.txt": "arquivo de teste 2 — evidência fictícia\n",
}


def escrever(base: Path, arquivos: dict[str, str]) -> None:
    for caminho, conteudo in arquivos.items():
        alvo = base / caminho
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_text(conteudo, encoding="utf-8")
        os.utime(alvo, (DATA_FIXA, DATA_FIXA))


def main() -> None:
    if shutil.which("zip") is None:
        raise SystemExit("Instale o zip primeiro: sudo apt install zip")
    DESAFIO.mkdir(parents=True, exist_ok=True)
    escrever(DESAFIO, TREINO)
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        escrever(base, INVENTARIO)
        escrever(base, EVIDENCIA)
        for pasta in base.rglob("*"):
            if pasta.is_dir():
                os.utime(pasta, (DATA_FIXA, DATA_FIXA))
        for nome in ("inventario.zip", "evidencia.zip"):
            (DESAFIO / nome).unlink(missing_ok=True)
        # -r recursivo, -X sem atributos extras, -q silencioso
        subprocess.run(["zip", "-rqX", str(DESAFIO / "inventario.zip"), "inventario"], cwd=base, check=True)
        # -P define a senha (criptografia ZipCrypto, a "clássica")
        subprocess.run(["zip", "-rqX", "-P", SENHA, str(DESAFIO / "evidencia.zip"), "evidencia"], cwd=base, check=True)
    print(f"Evidências do Dia 3 criadas em {DESAFIO}")


if __name__ == "__main__":
    main()
