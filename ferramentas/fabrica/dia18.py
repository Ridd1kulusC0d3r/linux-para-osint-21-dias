"""Fábrica de evidências do Dia 18 — whois e DNS salvos de domínios fictícios.

Rode a partir de qualquer pasta:  python3 ferramentas/fabrica/dia18.py
Tudo é fictício (sufixo .example; IPs da faixa de documentação 203.0.113.0/24
e 198.51.100.0/24). O whois imita o formato do whois do registro.br. Só stdlib.

Os nomes de pessoas são de "laranjas" claramente fictícios (Fulana de Tal...).

A trilha da flag:
  - pixvelox.example e suporte-pixvelox.example têm "donos" (owner) diferentes,
    mas o MESMO contato técnico (tech-c), o mesmo e-mail e os mesmos servidores
    de nome (nserver). Um terceiro domínio, cashback-pix-oficial.example, é uma
    isca: parece parente pelo nome, mas não compartilha nada.
  - Os registros TXT "pxv-verif=NN-palavra" de cada domínio guardam pedaços.
    Juntando, em ordem, só os pedaços dos domínios LIGADOS, sai a flag.
"""
from pathlib import Path
import shutil

RAIZ = Path(__file__).resolve().parents[2]
DESAFIO = RAIZ / "dias" / "dia-18-investigacao-de-dominio" / "desafio"

CABECALHO = """% Copyright (c) Nic.br
%  The use of the data below is only permitted as described in
%  full by the Use and Privacy Policy at https://registro.br/upp ,
%  being prohibited its distribution, commercialization or
%  reproduction, in particular, to use it for advertising or
%  any similar purpose.
%  2026-10-05T10:12:44-03:00 - IP: 198.51.100.200
"""

CONTATOS = {
    "MAALT12": ("Ciclano Mare de Tal", "mare.alta.dev@protonmail.example", "20250811"),
    "JOSIL88": ("Fulana de Tal", "fulana.det@email.example", "20240302"),
    "RTPER45": ("Beltrana de Tal", "beltrana.det@provedor.example", "20260714"),
    "CBOFC01": ("Central Cashback", "contato@cashback-pix-oficial.example", "20230120"),
    "HOSTB09": ("Hospedagem Barata Ltda", "abuse@hospedagembarata.example", "20190505"),
}

DOMINIOS = {
    "pixvelox.example": {
        "owner": "Fulana de Tal", "owner-c": "JOSIL88", "tech-c": "MAALT12",
        "ns": ["ns1.marecheia-dns.example", "ns2.marecheia-dns.example"],
        "created": "20260818", "changed": "20260902", "expires": "20270818",
        "a": ["203.0.113.10"], "mx": "10 mx.mailpxv.example.",
        "txt": ["v=spf1 include:_spf.mailpxv.example ~all",
                "pxv-verif=01-dois", "pxv-verif=03-um", "pxv-verif=05-dono"],
    },
    "suporte-pixvelox.example": {
        "owner": "Beltrana de Tal", "owner-c": "RTPER45", "tech-c": "MAALT12",
        "ns": ["ns1.marecheia-dns.example", "ns2.marecheia-dns.example"],
        "created": "20260821", "changed": "20260821", "expires": "20270821",
        "a": ["203.0.113.66"], "mx": "10 mx.mailpxv.example.",
        "txt": ["v=spf1 include:_spf.mailpxv.example ~all",
                "pxv-verif=02-dominios", "pxv-verif=04-so"],
    },
    "cashback-pix-oficial.example": {
        "owner": "Central Cashback", "owner-c": "CBOFC01", "tech-c": "HOSTB09",
        "ns": ["ns1.hospedagembarata.example", "ns2.hospedagembarata.example"],
        "created": "20230120", "changed": "20260110", "expires": "20270120",
        "a": ["198.51.100.40"], "mx": "10 mail.hospedagembarata.example.",
        "txt": ["v=spf1 a mx ~all",
                "pxv-verif=02-golpes", "pxv-verif=04-diferentes"],
    },
}


def whois(dominio: str, d: dict) -> str:
    linhas = [CABECALHO, f"domain:      {dominio}", f"owner:       {d['owner']}",
              f"owner-c:     {d['owner-c']}", f"tech-c:      {d['tech-c']}"]
    for ns in d["ns"]:
        linhas += [f"nserver:     {ns}", "nsstat:      20261005 AA", "nslastaa:    20261005"]
    linhas += [f"created:     {d['created']}", f"changed:     {d['changed']}",
               f"expires:     {d['expires']}", "status:      published", ""]
    for handle in sorted({d["owner-c"], d["tech-c"]}):
        nome, email, criado = CONTATOS[handle]
        linhas += [f"nic-hdl-br:  {handle}", f"person:      {nome}",
                   f"e-mail:      {email}", "country:     BR",
                   f"created:     {criado}", f"changed:     {criado}", ""]
    linhas.append("% Security and mail abuse issues should also be addressed to")
    linhas.append("% cert.br, http://www.cert.br/ , respectivelly to cert@cert.br")
    linhas.append("% and mail-abuse@cert.br")
    linhas.append("%")
    linhas.append("% whois.registro.br accepts only direct match queries. Types")
    linhas.append("% of queries are: domain (.br), registrant (tax ID), ticket,")
    linhas.append("% provider, CIDR block, IP and ASN.")
    return "\n".join(linhas) + "\n"


def registros(dominio: str, d: dict) -> list[str]:
    """Registros DNS no formato de `dig +noall +answer` (nome TTL classe tipo valor)."""
    r = [f"{dominio}.\t300\tIN\tA\t{ip}" for ip in d["a"]]
    r += [f"{dominio}.\t3600\tIN\tNS\t{ns}." for ns in d["ns"]]
    r.append(f"{dominio}.\t3600\tIN\tMX\t{d['mx']}")
    r += [f'{dominio}.\t300\tIN\tTXT\t"{t}"' for t in d["txt"]]
    return r


def dig_completo(dominio: str, d: dict) -> str:
    """Saída de `dig pixvelox.example` (consulta A), no formato real do dig."""
    a = d["a"][0]
    return f"""
; <<>> DiG 9.18.39-0ubuntu0.24.04.7-Ubuntu <<>> {dominio}
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 41872
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;{dominio}.		IN	A

;; ANSWER SECTION:
{dominio}.	300	IN	A	{a}

;; Query time: 23 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Mon Oct 05 10:12:44 -03 2026
;; MSG SIZE  rcvd: 61
"""


def main() -> None:
    if DESAFIO.exists():
        shutil.rmtree(DESAFIO)
    (DESAFIO / "whois").mkdir(parents=True)
    (DESAFIO / "dns").mkdir()
    for dominio, d in DOMINIOS.items():
        (DESAFIO / "whois" / f"{dominio}.txt").write_text(whois(dominio, d), encoding="utf-8")
        (DESAFIO / "dns" / f"{dominio}.txt").write_text(
            "\n".join(registros(dominio, d)) + "\n", encoding="utf-8")
    (DESAFIO / "dig_pixvelox.example.txt").write_text(
        dig_completo("pixvelox.example", DOMINIOS["pixvelox.example"]), encoding="utf-8")
    print(f"Evidências do Dia 18 criadas em {DESAFIO}")


if __name__ == "__main__":
    main()
