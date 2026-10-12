"""Dia 13 — abrindo .docx e .xlsx por dentro, em Python puro (só stdlib).

Rode:  python3 equivalente.py

Como .docx e .xlsx são ZIPs com XML, o Python lê tudo com dois módulos da
biblioteca padrão: zipfile (abre o pacote) e xml.etree.ElementTree (entende
o XML). Nada de Office instalado.

Ponte Linux -> Python:
    file arquivo.xlsx           -> zipfile.is_zipfile()
    unzip -l arquivo.xlsx       -> ZipFile.namelist() / infolist()
    unzip -p arq docProps/core.xml -> ZipFile.read("docProps/core.xml")
    grep state="hidden"         -> ElementTree: sheet.get("state")
    libreoffice --convert-to csv (todas as abas) -> ler cada sheetN.xml e csv.writer
    pandoc --track-changes=all  -> ler word/comments.xml
"""
from pathlib import Path
import csv
import io
import xml.etree.ElementTree as ET
import zipfile

AQUI = Path(__file__).resolve().parent
DOCX = AQUI / "desafio" / "roteiro-atendimento.docx"
XLSX = AQUI / "desafio" / "planilha-contas.xlsx"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
}


def metadados(z: zipfile.ZipFile) -> dict:
    raiz = ET.fromstring(z.read("docProps/core.xml"))
    return {"autor": raiz.findtext("dc:creator", namespaces=NS),
            "ultimo": raiz.findtext("cp:lastModifiedBy", namespaces=NS)}


def comentarios(z: zipfile.ZipFile) -> list[tuple[str, str]]:
    if "word/comments.xml" not in z.namelist():
        return []
    raiz = ET.fromstring(z.read("word/comments.xml"))
    return [(c.get(f"{{{NS['w']}}}author"), "".join(t.text or "" for t in c.iter(f"{{{NS['w']}}}t")))
            for c in raiz.findall("w:comment", NS)]


def abas(z: zipfile.ZipFile) -> list[tuple[str, str, str]]:
    """(nome, estado, arquivo XML) de cada aba, na ordem do workbook.

    Simplificação: supomos aba N -> sheetN.xml. O jeito "oficial" é seguir o
    r:id de cada aba em xl/_rels/workbook.xml.rels.
    """
    raiz = ET.fromstring(z.read("xl/workbook.xml"))
    saida = []
    for i, aba in enumerate(raiz.find("s:sheets", NS), 1):
        saida.append((aba.get("name"), aba.get("state", "visible"), f"xl/worksheets/sheet{i}.xml"))
    return saida


def linhas_da_aba(z: zipfile.ZipFile, caminho: str) -> list[list[str]]:
    raiz = ET.fromstring(z.read(caminho))
    linhas = []
    for row in raiz.iter(f"{{{NS['s']}}}row"):
        celulas = []
        for c in row.findall("s:c", NS):
            texto = c.findtext("s:is/s:t", namespaces=NS) or c.findtext("s:v", namespaces=NS) or ""
            celulas.append(texto)
        linhas.append(celulas)
    return linhas


def main() -> None:
    print("file ->", DOCX.name, "é zip?", zipfile.is_zipfile(DOCX))

    with zipfile.ZipFile(XLSX) as z:
        print("\nunzip -l planilha-contas.xlsx")
        for info in z.infolist():
            print(f"  {info.file_size:>6}  {info.filename}")

    with zipfile.ZipFile(DOCX) as z:
        print("\ndocProps/core.xml ->", metadados(z))
        for autor, texto in comentarios(z):
            print(f"comentário de {autor}: {texto}")

    with zipfile.ZipFile(XLSX) as z:
        print("\nabas ->")
        partes = []
        for nome, estado, caminho in abas(z):
            print(f"  {nome:<10} {estado:<8} {caminho}")
            # "libreoffice --convert-to csv" de cada aba, em memória
            buf = io.StringIO()
            csv.writer(buf, lineterminator="\n").writerows(linhas_da_aba(z, caminho))
            print("   ", buf.getvalue().replace("\n", "\n    ").rstrip())
            if estado == "hidden":
                partes = [l[1] for l in linhas_da_aba(z, caminho)[1:]]
        print("\nflag ->", "".join(partes))


if __name__ == "__main__":
    main()
