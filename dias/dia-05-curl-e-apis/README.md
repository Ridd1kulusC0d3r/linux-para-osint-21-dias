# Dia 5 — Bater na porta 🚪

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-05.ipynb)
&nbsp;**Rank D** · ⏱️ ~50 min · 📖 Original: *Day 5. Downloading files and working with APIs. Curl.* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> A vítima 014 encaminhou o SMS que recebeu: *"Seu CASHBACK de R$ 287,40
> expira HOJE! Resgate agora: encurta.example/x7Kp9"*.
>
> Você leva o mouse até o link. Jurema segura o seu pulso.
> — Clicar no link do golpista, do seu navegador, com seu IP, logado no seu
> e-mail? Não mesmo.
>
> Mestra Iara aponta o terminal.
> — Bata na porta sem entrar. O `curl` pergunta "para onde esse link vai?" e
> o servidor responde. Siga a resposta até o fim. **Até o fim.**

**Sua tarefa:** seguir a cadeia de redirecionamentos do link encurtado e
descobrir o que o último destino carrega. A flag `VAZANTE{...}` está lá,
disfarçada.

## 🎯 Ao final de hoje você sabe

- [ ] Pedir uma página pelo terminal (`curl`)
- [ ] Baixar arquivos com `-o` e `-O`, e em lote com `xargs`
- [ ] Ler só os **cabeçalhos** de uma resposta (`curl -I`)
- [ ] Seguir **redirecionamentos** sem abrir o navegador (`curl -sIL | grep -i ^location`)
- [ ] Consultar uma **API** que responde em JSON (BrasilAPI)
- [ ] Subir um servidor web local com `python3 -m http.server`

## 📖 Conceito em 2 minutos

Toda vez que você abre um site, o navegador faz um **pedido HTTP** e recebe
uma **resposta** em duas partes:

```text
PEDIDO                         RESPOSTA
GET /x7Kp9                     HTTP/1.1 302 Found          ← código de status
Host: encurta.example          Location: http://outro/...  ← cabeçalhos
                               Server: nginx
                               (linha em branco)
                               <html>...</html>            ← corpo
```

Os códigos que importam hoje: **200** (deu certo), **301/302** (mudou de
endereço — veja o `Location`) e **404** (não existe). Um link encurtado é só
um servidor que responde "302, vá para tal lugar". Golpistas encadeiam vários
saltos: rastreio de cliques, página promocional, cadastro…

O `curl` é um navegador sem janela: faz o pedido e mostra **exatamente** o
que voltou — sem rodar JavaScript, sem baixar imagens, sem cookies.

## ⌨️ Mão na massa

Tudo está em [`comandos.sh`](comandos.sh). Sem internet? Cada bloco usa uma
cópia salva em `desafio/salvos/`.

### 1. Pedir e baixar

```bash
curl https://example.com                                   # imprime a página
curl -sL https://www.rfc-editor.org/rfc/rfc2606.txt -o rfc2606.txt   # salva com o nome que você quer
curl -O https://www.rfc-editor.org/rfc/rfc2606.txt                   # salva com o nome da URL
xargs -n 1 curl -O < desafio/urls.txt                      # uma lista inteira
```

### 2. Só os cabeçalhos

```bash
curl -I https://example.com
curl -s -o /dev/null -w '%{http_code}\n' https://example.com   # só o código
```

### 3. Seguindo redirecionamentos

```bash
curl -sIL http://registro.br | grep -i ^location     # cada salto
curl -sL -o /dev/null -w '%{url_effective}\n' http://registro.br   # só o destino final
```

### 4. APIs

```bash
curl -s https://brasilapi.com.br/api/cep/v1/70150900 | jq .
curl -X 'GET' 'https://brasilapi.com.br/api/cnpj/v1/00000000000191' \
     -H 'accept: application/json' > resultado.json
```

`-X` escolhe o método (GET lê, POST envia), `-H` acrescenta um cabeçalho e
`>` guarda a resposta num arquivo.

### 5. Seu próprio servidor

```bash
python3 -m http.server 8086 --directory desafio/salvos   # serve a pasta na porta 8086
curl http://127.0.0.1:8086/rfc2606-resumo.txt              # em outro terminal
```

E para o desafio: `desafio/encurtador.py` reproduz o encurtador do golpe na
sua máquina, usando a cadeia salva em `cabecalhos-link-golpe.txt`:

```bash
python3 desafio/encurtador.py 8085 &          # sobe o servidor falso
curl -sIL --noproxy '*' --connect-to ::127.0.0.1:8085 http://encurta.example/x7Kp9
kill %1                                       # derruba o servidor
```

`--connect-to ::127.0.0.1:8085` diz ao curl: "qualquer domínio, conecte na
minha máquina". Assim você treina com os nomes reais do golpe sem tocar no
servidor dos golpistas.

## 🇧🇷 Versão brazuca

A [BrasilAPI](https://brasilapi.com.br/docs) junta várias fontes públicas
num lugar só, sem cadastro. Com `curl` + `jq` você faz uma ficha rápida de
**empresa pública**:

```bash
CNPJ=00000000000191      # Banco do Brasil
curl -s "https://brasilapi.com.br/api/cnpj/v1/$CNPJ" \
  | jq '{razao_social, natureza_juridica, uf, municipio, data_inicio_atividade}'

curl -s https://brasilapi.com.br/api/banks/v1/1 | jq .        # código bancário 001
curl -s https://brasilapi.com.br/api/ddd/v1/31 | jq '.cities | length'   # cidades do DDD 31
curl -s https://brasilapi.com.br/api/feriados/v1/2026 | jq -r '.[].name'
```

E a pergunta "esse domínio `.br` existe?" o próprio
[registro.br](https://registro.br/) responde (Dia 18 aprofunda com `whois`):
`curl -sI https://registro.br` mostra os cabeçalhos do serviço.

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) faz tudo com `urllib`, `http.client`,
`http.server` e `json` — e segue a cadeia do golpe num servidor local.

| Terminal | Python (stdlib) |
|---|---|
| `curl URL` | `urllib.request.urlopen(URL).read()` |
| `curl -o arquivo URL` | `urllib.request.urlretrieve(URL, arquivo)` |
| `curl -I URL` | `Request(URL, method="HEAD")` → `.headers` |
| `curl -H 'k: v'` | `Request(URL, headers={"k": "v"})` |
| `curl -sIL \| grep location` | `http.client` + laço seguindo `Location` |
| `jq .` | `json.loads()` / `json.dumps(indent=2)` |
| `python3 -m http.server` | `http.server.ThreadingHTTPServer` |

## 🚀 Além do curso

- **[HTTPie](https://httpie.io/)** (`apt install httpie`, comando `http`) é um curl feito para humanos, com JSON colorido: `http brasilapi.com.br/api/cep/v1/70150900`.
- **[httpx](https://www.python-httpx.org/)** (`pip install httpx`) é a biblioteca Python moderna para HTTP, com suporte a HTTP/2 e requisições assíncronas — ótima para consultar centenas de URLs. Tem também um modo linha de comando (`pip install 'httpx[cli]'`).
- **[urlscan.io](https://urlscan.io/)** abre um link suspeito num navegador *deles* e mostra toda a cadeia de redirecionamentos, capturas de tela e domínios contatados. Ideal para não expor a sua máquina.

## 🧩 Desafio

1. Leia `desafio/sms-golpe.txt`.
2. Siga a cadeia do link até o último destino: pelo arquivo salvo
   `desafio/cabecalhos-link-golpe.txt` **ou** subindo `desafio/encurtador.py`
   e usando `curl -sIL`.
3. O último endereço carrega um parâmetro estranho. Decodifique-o.
4. Confira: `bash checar.sh 'VAZANTE{...}'`

<details>
<summary>💡 Dica 1</summary>

`grep -i '^location' desafio/cabecalhos-link-golpe.txt | tail -n 1` mostra só
o último salto. Os saltos anteriores têm pistas (como quem indicou o
cadastro), mas a flag está no final.
</details>

<details>
<summary>💡 Dica 2</summary>

Texto que só tem letras, números e termina com `=` costuma ser **Base64**.
`echo 'TEXTO' | base64 -d` decodifica.
</details>

A solução comentada está em [`solucoes/dia-05.sh`](../../solucoes/dia-05.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- **Cada `curl` deixa seu IP no log do servidor.** Bater na porta do
  golpista avisa que alguém está investigando. Em caso real, use um
  serviço intermediário (urlscan.io), uma VPN ou Tor (`curl -x
  socks5h://127.0.0.1:9050 ...`) — e combine isso com a sua equipe.
- O `curl` se apresenta como `curl/8.x` no cabeçalho `User-Agent`. Alguns
  golpistas mostram uma página inocente para robôs. Trocar com `-A` ajuda,
  mas lembre: você continua se identificando pelo IP.
- Respeite as APIs públicas: leia os limites de uso, ponha `sleep` em laços
  e não use dados de pessoas físicas sem base legal (LGPD).
- Nunca use `curl ... | bash` com URL de terceiros: isso executa o que o
  servidor mandar, sem você ver.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 4](../dia-04-processamento-em-lote/) · [Índice](../../README.md) · [Dia 6](../dia-06-grep/) ➡️
