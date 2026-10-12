# Dia 20 — O script quebrado 🧰

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-20.ipynb)
&nbsp;**Rank A** · ⏱️ ~50 min · 📖 Original: *Day 20. Tools to make Linux easier to use* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> Na apreensão do notebook de um afiliado, a perícia achou dois arquivos
> d'Os Vazantes: um script chamado `selo.sh` e uma cópia do histórico do
> terminal de maré_alta. O histórico termina assim:
>
> ```text
> bash selo.sh
> bash selo.sh
> shellcheck selo.sh
> history -c
> ```
>
> — Rodou duas vezes, não funcionou, chamou o shellcheck e apagou o histórico
> — lê Bento. — Ele nunca conseguiu consertar.
>
> A Mestra Iara empurra a cadeira para você.
> — Recruta, vinte dias atrás você não sabia o que era `ls`. Hoje conserta o
> script do chefe da quadrilha. **Sem mexer no original.**

**Sua tarefa:** usar o `shellcheck` para achar os erros de
`desafio/script_quebrado.sh`, criar uma cópia corrigida, rodá-la e obter o
selo — a flag `VAZANTE{...}`.

## 🎯 Ao final de hoje você sabe

- [ ] Encontrar erros em scripts com **`shellcheck`** e entender os códigos `SCxxxx`
- [ ] Evitar os 3 erros clássicos: espaço no `=`, variável sem aspas, nome com espaço
- [ ] Depurar com `bash -x`
- [ ] Usar o **histórico**: `history`, `!!`, `!123`, **Ctrl+R**
- [ ] Criar **aliases** e torná-los permanentes no `~/.bashrc`
- [ ] Economizar digitação com **Tab** e consultar `tldr`, `fzf` e explainshell

## 📖 Conceito em 2 minutos

Você não precisa decorar o Linux: precisa saber **onde pedir ajuda** e
**como conferir** o que escreveu. Quatro tipos de ajudante:

| Ajudante | Pergunta que responde | Ferramenta |
|---|---|---|
| Revisor | "meu script tem erro?" | `shellcheck`, `bash -x` |
| Memória | "como era aquele comando?" | `history`, Ctrl+R, `fzf` |
| Atalho | "preciso digitar tudo isso?" | `alias`, Tab |
| Professor | "o que esse comando faz?" | `tldr`, `man`, explainshell, IA |

O erro mais comum de Bash é esquecer que o shell **divide tudo em espaços**.
`pedacos de selo` sem aspas vira três palavras: `pedacos`, `de`, `selo`.
A cura é uma só: **`"$variavel"` sempre entre aspas duplas**.

Assistentes de IA escrevem e explicam comandos muito bem — e também erram
com toda confiança. Use, mas **passe pelo `shellcheck`** e entenda antes de
rodar.

## ⌨️ Mão na massa

### 1. shellcheck

```bash
sudo apt install shellcheck
shellcheck desafio/script_quebrado.sh      # explicação completa
shellcheck -f gcc desafio/script_quebrado.sh   # uma linha por aviso
```

Cada código tem página própria: `https://www.shellcheck.net/wiki/SC2086`.
O exemplo clássico do curso original (`wrong_code.sh`) está no
[`comandos.sh`](comandos.sh): ele "roda sem erro" e mesmo assim está errado.

### 2. Os três erros clássicos

```bash
pasta = "x"            # ERRADO: roda o comando "pasta" com os argumentos = e x
pasta="pedacos de selo"
cat $pasta/a.txt       # ERRADO: vira cat pedacos de selo/a.txt (3 arquivos)
cat "$pasta"/a.txt     # certo
bash -x script.sh      # mostra cada comando, já expandido, antes de rodar
```

### 3. Histórico

```bash
history                 # tudo, numerado
history | grep git      # procurar
!!                      # repetir o último  (sudo !! = repetir com sudo)
!42                     # repetir o número 42
# Ctrl+R e digite um pedaço: busca reversa (Ctrl+R de novo = anterior)
history -r arquivo      # carrega um histórico salvo
```

### 4. Aliases

```bash
alias ll='ls -lah'
alias                                   # lista
echo "alias ll='ls -lah'" >> ~/.bashrc  # permanente
```

### 5. Teclas e ajudantes

```bash
# Tab completa (2x Tab mostra opções) · Ctrl+A/E início/fim · Ctrl+U apaga a linha · Alt+. último argumento
sudo apt install tldr fzf
tldr tar                                  # exemplos práticos (baixa páginas na 1ª vez)
find . -type f | fzf                      # filtra digitando pedaços (interativo)
find . -type f | fzf --filter='parte 03'  # versão para scripts
```

E para entender um comando copiado: cole em **https://explainshell.com**.

## 🇧🇷 Versão brazuca

Monte um `~/.bashrc` de investigador brasileiro com aliases para as APIs
públicas que você usou no curso:

```bash
cat >> ~/.bashrc <<'FIM'
# --- Núcleo Coruja ---
cep()  { curl -s "https://brasilapi.com.br/api/cep/v1/$1" | jq; }
cnpj() { curl -s "https://brasilapi.com.br/api/cnpj/v1/$1" | jq '{razao_social, situacao_cadastral, municipio}'; }
ddd()  { curl -s "https://brasilapi.com.br/api/ddd/v1/$1" | jq; }
rdap() { curl -s "https://rdap.registro.br/domain/$1" | jq '{ldhName, events}'; }
alias hashes='sha256sum'
FIM
source ~/.bashrc
cep 30130010       # um CEP do centro de Belo Horizonte
ddd 31
```

(Funções em vez de alias quando o atalho precisa de argumento no meio do
comando.)

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) mostra que o bug do dia quase não existe
em Python (um `Path` nunca vira várias palavras) e usa `shlex` para **simular
como o shell divide** uma linha.

| Terminal | Python (stdlib) |
|---|---|
| `"$pasta"/*.txt` | `sorted(Path(pasta).glob("*.txt"))` |
| como o shell divide palavras | `shlex.split(linha)` |
| escapar com segurança | `shlex.quote(caminho)` |
| `tr 'A-Za-z' 'N-ZA-Mn-za-m'` | `codecs.decode(texto, "rot13")` |
| `shellcheck` (sintaxe) | `compile(codigo, nome, "exec")` / `python3 -m py_compile` |
| `history \| grep git` | `[l for l in linhas if l.startswith("git ")]` |

## 🚀 Além do curso

- **`shfmt`** (`apt install shfmt`) — formata scripts Bash automaticamente
  (indentação, espaços): `shfmt -i 2 -w script.sh`. O par perfeito do shellcheck.
- **Atuin** (atuin.sh) — substitui o Ctrl+R por um histórico com busca,
  data, pasta e duração de cada comando, guardado em SQLite.
- **`tldr`** em Python (`pip install tldr`) — o mesmo cliente de hoje, mais
  atualizado que o do apt; `tldr --update` baixa as páginas para uso offline.

## 🧩 Desafio

1. Rode `shellcheck desafio/script_quebrado.sh` e leia os avisos.
2. Crie uma **cópia** do script (ex.: `cp` ou `sed ... > copia.sh`) na mesma pasta.
3. Corrija a cópia até o `shellcheck` não reclamar mais.
4. Rode a cópia: ela imprime o selo. Apague a cópia.
5. Confira: `bash checar.sh 'VAZANTE{...}'`

<details>
<summary>💡 Dica 1</summary>

São três correções: tirar os espaços em volta do `=`, e pôr aspas em
`$pasta` (no `for`) e em `$arquivo` (no `cat`).
</details>

<details>
<summary>💡 Dica 2</summary>

`sed -e 's/^pasta = /pasta=/' -e 's|in \$pasta/|in "$pasta"/|' -e 's|cat \$arquivo|cat "$arquivo"|' script_quebrado.sh > corrigido.sh`
</details>

A solução comentada está em [`solucoes/dia-20.sh`](../../solucoes/dia-20.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- **Seu histórico é um relatório da sua investigação** — inclusive de
  senhas digitadas por engano e dos alvos que você pesquisou. Em máquina
  compartilhada, cuide do `~/.bash_history` (e lembre: `history -c` só limpa
  a memória; o arquivo pode já estar salvo, como maré_alta descobriu).
- Comandos começados com **espaço** não vão para o histórico se
  `HISTCONTROL=ignorespace` (padrão no Ubuntu). Útil para chaves de API.
- **Nunca rode o que você não entende**, venha de fórum, de IA ou de um
  "script de OSINT milagroso". explainshell e shellcheck antes; máquina de
  testes depois.
- Evidência apreendida é **intocável**: trabalhe sempre numa cópia e registre
  o `sha256sum` do original.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 19](../dia-19-git-e-github/) · [Índice](../../README.md) · [Dia 21](../dia-21-distro-e-dossie/) ➡️
