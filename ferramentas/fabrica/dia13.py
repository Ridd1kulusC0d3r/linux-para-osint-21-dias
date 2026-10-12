"""Fábrica de evidências do Dia 13 — gera um .docx e um .xlsx "à mão".

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia13.py
Só stdlib (zipfile + XML escrito como texto). Tudo é fictício.

Por que à mão? Para mostrar o truque do dia: arquivos .docx/.xlsx/.pptx são
ZIPs cheios de XML. O Word e o Excel só "desenham" o que está lá dentro.

Arquivos
--------
desafio/roteiro-atendimento.docx  roteiro do falso suporte. Tem:
                                  - autor e "última modificação por" em docProps/core.xml
                                  - um COMENTÁRIO de revisão (word/comments.xml)
desafio/planilha-contas.xlsx      lista de contas de passagem. Tem:
                                  - aba "contas" (visível)
                                  - aba "controle" com state="hidden" (oculta)
desafio/pagina-salva.html         página simples para treinar pandoc offline

Como a pista funciona
---------------------
O comentário no roteiro diz que "o código fica na aba que ninguém vê". A aba
oculta "controle" da planilha guarda a flag em pedaços (uma linha por pedaço,
coluna "parte"). Quem lista o zip (unzip -l), lê xl/workbook.xml (state="hidden")
e abre xl/worksheets/sheet2.xml — ou converte todas as abas para CSV — junta
os pedaços: VAZANTE{aba_oculta_no_zip}.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import zipfile

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-13-arquivos-office" / "desafio"
DATA_ZIP = (2026, 3, 9, 23, 5, 0)          # datas fixas: arquivos sempre iguais

CORE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>{titulo}</dc:title><dc:creator>{autor}</dc:creator><cp:lastModifiedBy>{ultimo}</cp:lastModifiedBy>
<dcterms:created xsi:type="dcterms:W3CDTF">{criado}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{modificado}</dcterms:modified>
</cp:coreProperties>"""

APP = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>{app}</Application><Company>PixVelox</Company></Properties>"""

RELS_RAIZ = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="{principal}"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""

# ------------------------------------------------------------------ DOCX
PARAGRAFOS = [
    "ROTEIRO DE ATENDIMENTO - SUPORTE PIXVELOX",
    "1. Cumprimente pelo primeiro nome e diga que o cashback está bloqueado.",
    "2. Diga que, para liberar, o banco vai mandar um código por SMS.",
    "3. Peça o código com urgência: 'ele expira em 5 minutos'.",
    "4. Se a vítima hesitar, mande o print do 'contrato' (Dia 12).",
    "5. Nunca fale por ligação. Só texto.",
]
COMENTARIO = ("Lembrete pro time: o código desta semana NÃO vai no roteiro. "
              "Fica na planilha de contas, na aba que ninguém vê.")


def docx() -> dict[str, str]:
    ns = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    corpo = []
    for i, p in enumerate(PARAGRAFOS):
        if i == 3:   # o comentário fica preso ao passo 3
            corpo.append(f'<w:p><w:commentRangeStart w:id="0"/><w:r><w:t xml:space="preserve">{escape(p)}</w:t></w:r>'
                         f'<w:commentRangeEnd w:id="0"/><w:r><w:commentReference w:id="0"/></w:r></w:p>')
        else:
            corpo.append(f'<w:p><w:r><w:t xml:space="preserve">{escape(p)}</w:t></w:r></w:p>')
    return {
        "[Content_Types].xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/comments.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>""",
        "_rels/.rels": RELS_RAIZ.format(principal="word/document.xml"),
        "word/_rels/document.xml.rels": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments" Target="comments.xml"/>
</Relationships>""",
        "word/document.xml": f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:document {ns}><w:body>{"".join(corpo)}</w:body></w:document>',
        "word/comments.xml": f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:comments {ns}>'
                             f'<w:comment w:id="0" w:author="mare_alta" w:date="2026-03-09T23:01:00Z" w:initials="MA">'
                             f'<w:p><w:r><w:t xml:space="preserve">{escape(COMENTARIO)}</w:t></w:r></w:p></w:comment></w:comments>',
        "docProps/core.xml": CORE.format(titulo="Roteiro de atendimento", autor="mare_alta",
                                         ultimo="suporte_lucas", criado="2026-03-02T21:40:00Z",
                                         modificado="2026-03-09T23:05:00Z"),
        "docProps/app.xml": APP.format(app="Microsoft Office Word"),
    }


# ------------------------------------------------------------------ XLSX
CONTAS = [
    ["conta", "banco", "titular", "status"],
    ["passagem 7", "Banco Exemplo", "vítima 027 (laranja)", "ativa"],
    ["passagem 9", "Banco Exemplo", "vítima 031 (laranja)", "ativa"],
    ["passagem 11", "Banco Fictício", "vítima 044 (laranja)", "bloqueada"],
    ["passagem 12", "Banco Fictício", "vítima 058 (laranja)", "ativa"],
]
CONTROLE = [
    ["ordem", "parte", "obs"],
    [1, "VAZANTE{", "não apagar"],
    [2, "aba_", ""],
    [3, "oculta_", ""],
    [4, "no_zip}", "trocar toda segunda"],
]


def coluna(i: int) -> str:
    return "ABCDEFGHIJ"[i]


def planilha(linhas: list[list]) -> str:
    xml = []
    for r, linha in enumerate(linhas, 1):
        cels = []
        for c, valor in enumerate(linha):
            ref = f"{coluna(c)}{r}"
            if isinstance(valor, int):
                cels.append(f'<c r="{ref}"><v>{valor}</v></c>')
            elif valor != "":
                cels.append(f'<c r="{ref}" t="inlineStr"><is><t>{escape(valor)}</t></is></c>')
        xml.append(f'<row r="{r}">{"".join(cels)}</row>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            f'<sheetData>{"".join(xml)}</sheetData></worksheet>')


def xlsx() -> dict[str, str]:
    return {
        "[Content_Types].xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>""",
        "_rels/.rels": RELS_RAIZ.format(principal="xl/workbook.xml"),
        "xl/_rels/workbook.xml.rels": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
</Relationships>""",
        "xl/workbook.xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="contas" sheetId="1" r:id="rId1"/><sheet name="controle" sheetId="2" state="hidden" r:id="rId2"/></sheets>
</workbook>""",
        "xl/worksheets/sheet1.xml": planilha(CONTAS),
        "xl/worksheets/sheet2.xml": planilha(CONTROLE),
        "docProps/core.xml": CORE.format(titulo="Contas de passagem", autor="mare_alta",
                                         ultimo="mare_alta", criado="2026-02-20T02:10:00Z",
                                         modificado="2026-03-09T23:04:00Z"),
        "docProps/app.xml": APP.format(app="Microsoft Excel"),
    }


HTML = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>PixVelox - Cashback</title></head>
<body>
<h1>PixVelox: o Pix que devolve</h1>
<p>Ganhe <strong>10% de cashback</strong> em todo Pix. Fale com o suporte!</p>
<ul><li>Sem taxas</li><li>Sem burocracia</li><li>Suporte 24h: suporte@pixvelox.example</li></ul>
</body></html>
"""


def gravar_zip(destino: Path, arquivos: dict[str, str]) -> None:
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for nome, conteudo in arquivos.items():
            info = zipfile.ZipInfo(nome, date_time=DATA_ZIP)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, conteudo.encode("utf-8"))


def main() -> None:
    DESAFIO.mkdir(parents=True, exist_ok=True)
    gravar_zip(DESAFIO / "roteiro-atendimento.docx", docx())
    gravar_zip(DESAFIO / "planilha-contas.xlsx", xlsx())
    (DESAFIO / "pagina-salva.html").write_text(HTML, encoding="utf-8")
    print(f"Evidências do Dia 13 criadas em {DESAFIO}")


if __name__ == "__main__":
    main()
