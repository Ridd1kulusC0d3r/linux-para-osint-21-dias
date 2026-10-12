# Dia 18 — Quem registrou? 🌐

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-18.ipynb)
&nbsp;**Rank B** · ⏱️ ~50 min · 📖 Original: *Day 18. Domain investigation* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> A Jurema chega com uma pasta de papel (sim, papel).
> — Ofício respondido pelo registro. Três domínios aparecem nas denúncias:
> `pixvelox.example`, `suporte-pixvelox.example` e `cashback-pix-oficial.example`.
> Cada um em nome de uma pessoa diferente.
>
> — Laranjas — resume Bento. — Nome de dono não vale nada.
>
> A Mestra Iara folheia as saídas de `whois` e `dig` que a equipe salvou.
> — Dono se troca. Encanamento, não. Quem configura o DNS, quem é o contato
> técnico, qual e-mail recebe os avisos… isso o golpista reaproveita. Descubra
> quais domínios são **da mesma mão** — e o que eles deixaram escrito no DNS.

**Sua tarefa:** correlacionar os whois e os registros DNS salvos em
`desafio/`, descobrir quais domínios pertencem ao mesmo operador e montar a
flag `VAZANTE{...}` com os registros TXT deles.

## 🎯 Ao final de hoje você sabe

- [ ] Consultar `whois` e filtrar datas e contatos com `grep`
- [ ] Ler um whois no formato do **registro.br** (owner, owner-c, tech-c, nserver)
- [ ] Consultar o DNS com `dig`, `dig +short`, `host` e `nslookup`
- [ ] Pedir tipos específicos de registro: **A, MX, NS, TXT** e reverso (`-x`)
- [ ] **Correlacionar** domínios por infraestrutura compartilhada
- [ ] Usar **RDAP** (o whois em JSON) e saber para que serve o `netlas host`

## 📖 Conceito em 2 minutos

Dois bancos de dados públicos contam a vida de um domínio:

| Fonte | Pergunta | Ferramenta | Exemplos de campo |
|---|---|---|---|
| **Registro** (whois/RDAP) | *quem* registrou e *quando* | `whois` | owner, tech-c, created, expires |
| **DNS** | *para onde* ele aponta | `dig`, `host` | A (IP), MX (e-mail), NS, TXT |

No `.br`, o whois do registro.br mostra **contatos** por um código
(`nic-hdl-br`, ex.: `MAALT12`). Se dois domínios têm o **mesmo tech-c**, a
mesma pessoa cuida dos dois — mesmo que o "dono" seja diferente.

Os registros **TXT** são texto livre: servem para SPF (quem pode mandar
e-mail pelo domínio) e para provar posse a serviços (`google-site-verification=…`).
Um código de verificação repetido em dois domínios é uma ligação fortíssima.

## ⌨️ Mão na massa

### 1. whois

```bash
sudo apt install whois
whois registro.br
whois example.com | grep 'Creation'              # .com: "Creation Date"
grep -E '^(created|expires):' desafio/whois/pixvelox.example.txt   # .br: "created"
```

### 2. dig

```bash
sudo apt install dnsutils
dig example.com                  # completo: veja a ANSWER SECTION
dig +short example.com A         # só o IP
dig +short registro.br MX        # servidor de e-mail
dig +short registro.br NS        # servidores de nome
dig +short registro.br TXT       # textos (SPF, verificações)
dig +short -x 8.8.8.8            # reverso: IP -> nome
```

### 3. host e nslookup

```bash
host example.com
host -t MX registro.br
nslookup -type=NS registro.br
```

### 4. Correlação

```bash
for arq in desafio/whois/*.txt; do
  d=$(basename "$arq" .txt)
  grep -E '^(tech-c|nserver|e-mail):' "$arq" | sed "s|^|$d  |"
done | awk '{print $2, $3}' | sort | uniq -c | awk '$1 > 1'   # o que se repete
```

### 5. Netlas (opcional)

```bash
pip install netlas
netlas savekey SUA_CHAVE
netlas host registro.br         # whois + DNS + servidores de uma vez
```

## 🇧🇷 Versão brazuca

O **registro.br** tem um serviço RDAP público, em JSON:

```bash
curl -s https://rdap.registro.br/domain/registro.br | jq '.events'
curl -s https://rdap.registro.br/domain/registro.br | jq -r '.nameservers[].ldhName'
```

Para domínios `.br` de empresas, o whois traz um **CNPJ** no campo
`ownerid`. Com ele você cruza com a base aberta da Receita, por exemplo pela
**BrasilAPI**:

```bash
curl -s https://brasilapi.com.br/api/cnpj/v1/00000000000191 | jq '{razao_social, municipio, data_inicio_atividade}'
```

(O exemplo usa o CNPJ público do Banco do Brasil.) Domínio criado na semana
do golpe e empresa aberta há 20 anos não combinam — desconfie.

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) fala o protocolo whois direto por socket
(é só abrir a porta 43 e mandar o nome!) e faz a correlação com `Counter`.

| Terminal | Python (stdlib) |
|---|---|
| `whois dominio` | `socket.create_connection(("whois.registro.br", 43))` |
| `dig +short dominio A` | `socket.gethostbyname(dominio)` |
| `dig -x IP` | `socket.gethostbyaddr(IP)` |
| `grep '^tech-c:'` | `linha.startswith("tech-c:")` |
| `sort \| uniq -c` | `collections.Counter` |
| `dig MX/NS/TXT` | não tem na stdlib → `pip install dnspython` |

## 🚀 Além do curso

- **`dnspython`** (`pip install dnspython`) — consultas DNS completas em Python:
  `dns.resolver.resolve("registro.br", "MX")`.
- **`python-whois`** (`pip install python-whois`) — whois já "parseado" em
  dicionário: `whois.whois("example.com").creation_date`.
- **`dnstwist`** (`pip install dnstwist`) — gera variações de um domínio
  (typosquatting) e verifica quais estão registradas: ótimo para achar clones
  como `pixve1ox`, `pix-velox`… do jeito defensivo.

## 🧩 Desafio

1. Compare os três arquivos em `desafio/whois/`.
2. Descubra quais domínios compartilham o mesmo **tech-c** (e e-mail, e DNS).
3. Nos arquivos de `desafio/dns/` **só desses domínios**, pegue os registros
   TXT `pxv-verif=NN-palavra`.
4. Ordene pelo número e junte as palavras com `_`.
5. Confira: `bash checar.sh 'VAZANTE{...}'`

<details>
<summary>💡 Dica 1</summary>

`grep -h '^tech-c:' desafio/whois/*.txt | sort | uniq -c` mostra qual handle se
repete. O domínio "cashback-pix-oficial" parece parente pelo nome… mas é?
</details>

<details>
<summary>💡 Dica 2</summary>

`awk -F'\t' '$4 == "TXT" {print $5}'` nos dois arquivos de DNS certos, depois
`grep -o 'pxv-verif=[0-9]*-[a-z]*' | cut -d= -f2 | sort -n | cut -d- -f2 | paste -sd_`.
</details>

A solução comentada está em [`solucoes/dia-18.sh`](../../solucoes/dia-18.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- **whois e DNS são públicos e passivos** — consultá-los não toca no servidor
  do alvo (o DNS responde por cache ou pelo provedor). Já um `nmap` no IP é
  ativo: fora do escopo de OSINT sem autorização.
- **Nome no whois não é culpa.** Laranjas e vítimas de roubo de identidade
  aparecem como "donos". Correlação aponta caminho; não acusa ninguém.
- **LGPD:** o registro.br oculta dados de pessoas físicas justamente por
  privacidade. Dados de contato obtidos por ofício só podem ser usados na
  finalidade da investigação.
- O próprio whois avisa: os dados **não podem ser redistribuídos** nem usados
  para publicidade. Cite a fonte e a data no relatório, não republique a base.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 17](../dia-17-compartilhamento-de-arquivos/) · [Índice](../../README.md) · [Dia 19](../dia-19-git-e-github/) ➡️
