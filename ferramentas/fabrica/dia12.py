"""Fábrica de evidências do Dia 12 — gera dois PDFs da PixVelox.

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia12.py
Precisa de: Pillow (PIL). O PDF é escrito "à mão" (só bytes), para você ver
que um PDF é, no fundo, um arquivo de texto com objetos numerados.

Arquivos
--------
desafio/contrato-pixvelox.pdf   2 páginas de texto + 2 imagens (logo e rubrica).
                                Metadados (Info): Author, Creator, Producer,
                                Keywords, datas.
desafio/termo-escaneado.pdf     "digitalização": só uma imagem, sem texto
                                (para treinar OCR com ocrmypdf ou tesseract).

Como a pista funciona
---------------------
O texto do contrato (pdftotext) diz que o código de verificação é a
"palavra-chave interna do documento" entre VAZANTE{ e }. A palavra-chave está
no metadado Keywords (pdfinfo / exiftool). Juntando os dois:
VAZANTE{laranja_assina_tudo}. O Producer/Author entregam o maré_alta, e a
imagem da rubrica (pdfimages) confirma.
"""
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-12-pdf" / "desafio"
FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONTE_LIVRE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAGINA_1 = [
    (16, "CONTRATO DE PARCERIA COMERCIAL"),
    (11, ""),
    (11, "CONTRATADA: PixVelox Pagamentos Digitais (pixvelox.example)"),
    (11, "CONTRATANTE: vítima 027, doravante chamada PARCEIRA"),
    (11, ""),
    (11, "Cláusula 1ª - A PARCEIRA cede o uso de sua conta bancária para"),
    (11, "\"recebimento de cashback\" em troca de 3% dos valores movimentados."),
    (11, "Cláusula 2ª - A PARCEIRA não deve comentar a parceria com o banco."),
    (11, "Cláusula 3ª - Códigos recebidos por SMS devem ser repassados ao"),
    (11, "suporte em até 5 minutos."),
    (11, ""),
    (11, "Contato do suporte: suporte@pixvelox.example / (31) 90000-0042"),
]
PAGINA_2 = [
    (11, "Cláusula 9ª - Validade e verificação"),
    (11, ""),
    (11, "O código de verificação deste contrato é formado pela"),
    (11, "palavra-chave interna do documento, escrita entre VAZANTE{ e }."),
    (11, ""),
    (11, "Belo Horizonte, 05 de março de 2026."),
    (11, ""),
    (11, "Assinatura da CONTRATADA (rubrica abaixo):"),
]
INFO = {
    "Title": "Contrato de Parceria - PixVelox",
    "Author": "mare_alta",
    "Subject": "parceria cashback - modelo laranja",
    "Keywords": "laranja_assina_tudo",
    "Creator": "Writer (rascunho de mare_alta)",
    "Producer": "PixVelox DocGen 0.3 - operador mare_alta",
    "CreationDate": "D:20260305221700-03'00'",
    "ModDate": "D:20260306031700-03'00'",
}


def jpeg(img: Image.Image) -> bytes:
    buf = BytesIO()
    img.save(buf, "JPEG", quality=70)
    return buf.getvalue()


def logo() -> Image.Image:
    img = Image.new("RGB", (240, 80), "#0b3d2e")
    d = ImageDraw.Draw(img)
    d.text((18, 18), "PixVelox", fill="white", font=ImageFont.truetype(FONTE, 34))
    return img


def rubrica() -> Image.Image:
    img = Image.new("RGB", (300, 90), "white")
    d = ImageDraw.Draw(img)
    d.line([(10, 60), (60, 20), (90, 70), (140, 25), (170, 65)], fill="navy", width=3)
    d.text((180, 30), "mare_alta", fill="navy", font=ImageFont.truetype(FONTE_LIVRE, 22))
    return img


def esc(texto: str) -> bytes:
    """Escapa parênteses e barras para strings de PDF; codifica em Latin-1."""
    t = texto.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    return t.encode("latin-1")


def stream_texto(linhas, y_inicial=780) -> bytes:
    partes = [b"BT"]
    y = y_inicial
    for tam, linha in linhas:
        partes.append(b"/F1 %d Tf 1 0 0 1 60 %d Tm (%s) Tj" % (tam, y, esc(linha)))
        y -= tam + 9
    partes.append(b"ET")
    return b"\n".join(partes)


def montar_pdf(objetos: list[bytes]) -> bytes:
    """Recebe a lista de objetos (o 1º é o catálogo) e calcula a tabela xref."""
    saida = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    posicoes = []
    for i, obj in enumerate(objetos, 1):
        posicoes.append(len(saida))
        saida += b"%d 0 obj\n" % i + obj + b"\nendobj\n"
    xref = len(saida)
    saida += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objetos) + 1)
    for p in posicoes:
        saida += b"%010d 00000 n \n" % p
    return bytes(saida), xref


def obj_stream(dados: bytes, extra: bytes = b"") -> bytes:
    return b"<< /Length %d %s>>\nstream\n" % (len(dados), extra) + dados + b"\nendstream"


def obj_imagem(img: Image.Image) -> bytes:
    return obj_stream(jpeg(img), b"/Type /XObject /Subtype /Image /Width %d /Height %d "
                      b"/ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode " % img.size)


def finalizar(objetos: list[bytes], info_num: int | None) -> bytes:
    corpo, xref = montar_pdf(objetos)
    trailer = b"trailer\n<< /Size %d /Root 1 0 R" % (len(objetos) + 1)
    if info_num:
        trailer += b" /Info %d 0 R" % info_num
    return corpo + trailer + b" >>\nstartxref\n%d\n%%%%EOF\n" % xref


def contrato() -> bytes:
    # 1 catálogo · 2 páginas · 3 fonte · 4 pág1 · 5 conteúdo1 · 6 pág2 · 7 conteúdo2
    # 8 logo · 9 rubrica · 10 info
    cont1 = b"q 160 0 0 53 60 800 cm /Logo Do Q\n" + stream_texto(PAGINA_1, 760)
    cont2 = stream_texto(PAGINA_2, 780) + b"\nq 200 0 0 60 60 560 cm /Rubrica Do Q"
    recursos = b"/Resources << /Font << /F1 3 0 R >> /XObject << /Logo 8 0 R /Rubrica 9 0 R >> >>"
    info = b"<< " + b" ".join(b"/%s (%s)" % (k.encode(), esc(v)) for k, v in INFO.items()) + b" >>"
    objetos = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [4 0 R 6 0 R] /Count 2 >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 5 0 R " + recursos + b" >>",
        obj_stream(cont1),
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 7 0 R " + recursos + b" >>",
        obj_stream(cont2),
        obj_imagem(logo()),
        obj_imagem(rubrica()),
        info,
    ]
    return finalizar(objetos, 10)


def escaneado() -> bytes:
    """Uma 'digitalização': página inteira é uma imagem, sem camada de texto."""
    img = Image.new("RGB", (1240, 700), "#f4f1ea")
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONTE_LIVRE, 40)
    linhas = ["TERMO DE ADESAO - PIXVELOX", "", "I agree to share my SMS codes",
              "with PixVelox support.", "", "Signed: victim 031"]
    for i, l in enumerate(linhas):
        d.text((80, 80 + i * 90), l, fill="black", font=f)
    conteudo = b"q 595 0 0 336 0 400 cm /Scan Do Q"
    objetos = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R "
        b"/Resources << /XObject << /Scan 5 0 R >> >> >>",
        obj_stream(conteudo),
        obj_imagem(img),
        b"<< /Producer (Scanner XYZ 2.1) /CreationDate (D:20260307101500-03'00') >>",
    ]
    return finalizar(objetos, 6)


def main() -> None:
    DESAFIO.mkdir(parents=True, exist_ok=True)
    (DESAFIO / "contrato-pixvelox.pdf").write_bytes(contrato())
    (DESAFIO / "termo-escaneado.pdf").write_bytes(escaneado())
    print(f"Evidências do Dia 12 criadas em {DESAFIO}")


if __name__ == "__main__":
    main()
