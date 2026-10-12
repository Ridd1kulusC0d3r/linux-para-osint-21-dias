"""Fábrica de evidências do Dia 19 — o repositório git d'Os Vazantes (bundle).

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia19.py
Precisa do programa `git`. Tudo é fictício.

Gera dias/dia-19-git-e-github/desafio/vazantes.bundle: um repositório inteiro
num arquivo só (git bundle). Histórico:
  1. README inicial
  2. página de cashback
  3. config.env com a "chave do painel" (a FLAG)      <- o erro de OPSEC
  4. remove config.env e adiciona .gitignore          <- "apagou"... só no presente
  5. roteiro do suporte (commit com e-mail pessoal vazado: OSINT clássico)
  6. ajuste no README
As datas são fixas, então o bundle sai igual toda vez.
"""
from pathlib import Path
import os
import subprocess
import tempfile

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-19-git-e-github" / "desafio"

FLAG = "VAZANTE{o_git_nunca_esquece}"
AUTOR = ("mare_alta", "mare_alta@pixvelox.example")

COMMITS = [
    ("2026-08-20T22:14:00-03:00", AUTOR, "primeiro commit", {
        "README.md": "# pxv-site\n\nSite da PixVelox. Não compartilhar.\n",
    }, []),
    ("2026-08-21T01:02:00-03:00", AUTOR, "pagina de cashback", {
        "site/cashback.html": "<h1>Ative seu cashback</h1>\n<form action=\"/c.php\"></form>\n",
    }, []),
    ("2026-08-23T03:41:00-03:00", AUTOR, "config do painel", {
        "config.env": ("PAINEL_URL=https://painel.pxv-tunel.example\n"
                       "PAINEL_USER=admin\n"
                       f"PAINEL_CHAVE={FLAG}\n"
                       "SMS_GATEWAY=gw.sms-barato.example\n"),
    }, []),
    ("2026-08-23T03:55:00-03:00", AUTOR, "remove config (ops)", {
        ".gitignore": "config.env\n*.log\n",
    }, ["config.env"]),
    ("2026-08-25T19:30:00-03:00", ("Mare Alta", "mare.alta.dev@protonmail.example"),
     "roteiro do suporte v3", {
        "roteiros/suporte_v3.txt": ("Olá! Aqui é do suporte PixVelox.\n"
                                    "Para liberar seu cashback, me envie o código de 6 dígitos.\n"),
    }, []),
    ("2026-08-26T10:05:00-03:00", AUTOR, "readme", {
        "README.md": "# pxv-site\n\nSite da PixVelox. Não compartilhar.\n\n- site/\n- roteiros/\n",
    }, []),
]


def git(pasta: Path, *args: str, env: dict | None = None) -> None:
    subprocess.run(["git", "-C", str(pasta), *args], check=True,
                   stdout=subprocess.DEVNULL, env=env)


def main() -> None:
    DESAFIO.mkdir(parents=True, exist_ok=True)
    base_env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    base_env.update({"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"})
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "pxv-site"
        repo.mkdir()
        git(repo, "init", "-q", "-b", "main", env=base_env)
        git(repo, "config", "commit.gpgsign", "false", env=base_env)
        for data, (nome, email), msg, arquivos, remover in COMMITS:
            for caminho, conteudo in arquivos.items():
                alvo = repo / caminho
                alvo.parent.mkdir(parents=True, exist_ok=True)
                alvo.write_text(conteudo, encoding="utf-8")
                git(repo, "add", caminho, env=base_env)
            for caminho in remover:
                git(repo, "rm", "-q", caminho, env=base_env)
            env = dict(base_env,
                       GIT_AUTHOR_NAME=nome, GIT_AUTHOR_EMAIL=email, GIT_AUTHOR_DATE=data,
                       GIT_COMMITTER_NAME=nome, GIT_COMMITTER_EMAIL=email, GIT_COMMITTER_DATE=data)
            git(repo, "commit", "-q", "-m", msg, env=env)
        destino = DESAFIO / "vazantes.bundle"
        destino.unlink(missing_ok=True)
        git(repo, "bundle", "create", str(destino), "--all", env=base_env)
    print(f"Repositório do Dia 19 empacotado em {destino}")


if __name__ == "__main__":
    main()
