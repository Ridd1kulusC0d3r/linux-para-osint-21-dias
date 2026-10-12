"""Fábrica de evidências do Dia 15 — gera o site clone da PixVelox em desafio/site/.

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia15.py
Tudo é fictício (domínios .example, telefones (31) 90000-XXXX). Só stdlib.

A flag fica numa página que NÃO é linkada pela home: só se chega nela lendo o
robots.txt e seguindo os links do "painel interno". Lá, o texto está escrito
com entidades HTML (&#86;&#65;...), então um grep cru não acha — é preciso
converter o HTML em texto (html2text) para ler.
"""
from pathlib import Path
import shutil

RAIZ = Path(__file__).resolve().parents[2]
DIA = RAIZ / "dias" / "dia-15-scraping"
SITE = DIA / "desafio" / "site"

FLAG = "VAZANTE{robots_txt_aponta_o_esconderijo}"


def entidades(texto: str) -> str:
    """Escreve cada caractere como entidade numérica HTML (&#NN;)."""
    return "".join(f"&#{ord(c)};" for c in texto)


def pagina(titulo: str, corpo: str, extra_head: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{titulo}</title>
<meta name="description" content="PixVelox: cashback em todo Pix. Rápido, fácil, seguro.">
<meta name="generator" content="ClonaSite Pro 3.2">
{extra_head}</head>
<body>
<nav>
  <a href="index.html">Início</a> |
  <a href="cashback.html">Cashback</a> |
  <a href="sobre.html">Quem somos</a> |
  <a href="contato.html">Fale conosco</a>
</nav>
{corpo}
<footer>
  <p>&copy; 2026 PixVelox Pagamentos &mdash; todos os direitos reservados.</p>
  <!-- rodape copiado do site bancoamigo.example; trocar o CNPJ depois -->
</footer>
</body>
</html>
"""


ARQUIVOS = {
    "index.html": pagina(
        "PixVelox — Cashback em todo Pix",
        """<h1>Ganhe até 15% de volta em TODO Pix!</h1>
<p>Mais de 40 mil brasileiros já recebem cashback com a PixVelox.</p>
<p><a href="cashback.html">Quero meu cashback agora</a></p>
<p>Dúvidas? Fale com o
<a href="https://chat.suporte-pixvelox.example/atendimento?origem=site">suporte no WhatsApp</a>.</p>
<!-- TODO: tirar o link do painel antes de publicar. ass: mare_alta -->
<script src="https://cdn.pixvelox.example/js/rastreio.js" data-conta="PXV-2026-0042"></script>
""",
    ),
    "cashback.html": pagina(
        "Ative seu cashback — PixVelox",
        """<h1>Ative seu cashback</h1>
<p>Informe seus dados. Em seguida, nosso suporte vai pedir um
<strong>código de verificação</strong> para liberar o seu saldo.</p>
<form action="https://coleta.suporte-pixvelox.example/c.php" method="post">
  <input name="nome" placeholder="Nome completo">
  <input name="celular" placeholder="(31) 9XXXX-XXXX">
  <input name="banco" placeholder="Seu banco">
  <button>Liberar cashback</button>
</form>
<!-- formulario envia pro servidor de coleta; nao mudar o action -->
""",
    ),
    "sobre.html": pagina(
        "Quem somos — PixVelox",
        """<h1>Quem somos</h1>
<p>Somos uma fintech mineira apaixonada por devolver dinheiro para você.</p>
<ul>
  <li>Diretoria: <a href="mailto:diretoria@pixvelox.example">diretoria@pixvelox.example</a></li>
  <li>Imprensa: <a href="mailto:imprensa@pixvelox.example">imprensa@pixvelox.example</a></li>
</ul>
<p>Siga a gente: <a href="https://social.example/@pixvelox_oficial">@pixvelox_oficial</a></p>
<!-- foto da equipe e banco de imagens, nao e a gente kkk -->
""",
    ),
    "contato.html": pagina(
        "Fale conosco — PixVelox",
        """<h1>Fale conosco</h1>
<p>Atendimento 24h pelo WhatsApp: (31) 90000-0042</p>
<p>E-mail do suporte: <a href="mailto:suporte@pixvelox.example">suporte@pixvelox.example</a></p>
<p>Financeiro: financeiro@pixvelox.example</p>
<!-- copia oculta das reclamacoes vai para mare_alta@suporte-pixvelox.example -->
""",
    ),
    "robots.txt": (
        "# robots.txt da PixVelox\n"
        "User-agent: *\n"
        "Disallow: /painel-interno/\n"
        "Disallow: /backup-2026/\n"
        "\n"
        "Sitemap: https://pixvelox.example/sitemap.xml\n"
    ),
    "painel-interno/index.html": pagina(
        "Painel interno — NÃO INDEXAR",
        """<h1>Painel interno</h1>
<p>Acesso restrito à equipe. Se você chegou aqui sem querer, feche esta página.</p>
<ul>
  <li><a href="metas-semana.html">Metas da semana</a></li>
  <li><a href="rascunho-campanha-v2.html">Rascunho da campanha v2</a></li>
</ul>
<!-- painel sem senha por enquanto, ninguem acha mesmo. ass: mare_alta -->
""",
        '<meta name="robots" content="noindex, nofollow">\n',
    ),
    "painel-interno/metas-semana.html": pagina(
        "Metas da semana",
        """<h1>Metas da semana</h1>
<ol>
  <li>Disparar 5 mil mensagens de "cashback liberado".</li>
  <li>Trocar o número do suporte se for denunciado.</li>
  <li>Nada de assinar mensagem com o apelido. (Sim, mare_alta, é com você.)</li>
</ol>
""",
    ),
    "painel-interno/rascunho-campanha-v2.html": pagina(
        "Rascunho — campanha v2",
        f"""<h1>Campanha v2 — rascunho</h1>
<p>Texto do disparo: &quot;Seu cashback de R&#36; 150,00 expira hoje!&quot;</p>
<p>Código interno da campanha: <span class="cod">{entidades(FLAG)}</span></p>
<!-- escrevi o codigo em entidades HTML pra ninguem achar com grep. ass: mare_alta -->
""",
    ),
}


# Cópia de example.com (página pública feita para exemplos) para o modo offline
EXAMPLE_COM = """<!doctype html>
<html>
<head>
    <title>Example Domain</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
</head>
<body>
<div>
    <h1>Example Domain</h1>
    <p>This domain is for use in documentation examples without needing permission. Avoid use in operations.</p>
    <p><a href="https://iana.org/domains/example">Learn more</a></p>
</div>
</body>
</html>
"""

# Template do nuclei que extrai e-mails .example das páginas
TEMPLATE_NUCLEI = r"""id: extrair-emails-example

info:
  name: Extrai e-mails de dominios .example (Dia 15)
  author: nucleo-coruja
  severity: info

http:
  - method: GET
    path:
      - "{{BaseURL}}"
    extractors:
      - type: regex
        regex:
          - '[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.example'
"""


def main() -> None:
    (DIA / "desafio").mkdir(parents=True, exist_ok=True)
    (DIA / "desafio" / "example.com.html").write_text(EXAMPLE_COM, encoding="utf-8")
    (DIA / "desafio" / "extrair-emails.yaml").write_text(TEMPLATE_NUCLEI, encoding="utf-8")
    if SITE.exists():
        shutil.rmtree(SITE)
    for caminho, conteudo in ARQUIVOS.items():
        alvo = SITE / caminho
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_text(conteudo, encoding="utf-8")
    print(f"Site clone do Dia 15 criado em {SITE}")


if __name__ == "__main__":
    main()
