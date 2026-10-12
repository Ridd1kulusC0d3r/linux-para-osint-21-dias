# Dia 2 — O script do Bento 📜

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/linux-para-osint-21-dias/blob/main/notebooks/dia-02.ipynb)
&nbsp;**Rank D** · ⏱️ ~50 min · 📖 Original: *Day 2. Basic bash script syntax* ([PDF do cipher387](https://github.com/cipher387/linux-for-OSINT-21-day/blob/main/Linux%20for%20OSINT.pdf))

---

## 🎬 Missão

> Bento chega atrasado, com o notebook debaixo do braço e um copo de café frio.
> — Recruta, as vítimas mandaram umas mensagens em código que o "suporte" da
> PixVelox usou. Eu anotei tudo em `pistas.txt` e comecei um script para
> decodificar… mas aí me chamaram para outra reunião.
>
> Ele abre o `decodificador.sh`: metade funciona, metade é `TODO`.
> — Uma parte está de trás para frente, outra virou número. E eu colei uns
> lixos no meio, foi mal. Ninguém decodifica isso na mão. **Laço resolve.**

**Sua tarefa:** completar o script do Bento para processar
`desafio/pistas.txt` e montar a flag `VAZANTE{...}` a partir dos pedaços na
ordem certa.

## 🎯 Ao final de hoje você sabe

- [ ] Criar e executar um script (`bash script.sh`, `chmod +x`, shebang)
- [ ] Guardar valores em **variáveis** e fazer contas com `$(( ))`
- [ ] Tomar decisões com `if`, `elif`, `else` e `case`
- [ ] Repetir tarefas com `for`, `while` e `until`
- [ ] Agrupar comandos em **funções** com argumentos (`$1`, `$2`)
- [ ] Ler um arquivo linha por linha, separando campos com `IFS`

## 📖 Conceito em 2 minutos

Um **script** é uma receita: comandos que você digitaria um a um, guardados
num arquivo para rodar de novo quando quiser. É isso que transforma uma busca
manual de 2 horas numa tarefa de 2 segundos.

Quatro peças montam qualquer script:

```text
variável   →  guarda um valor          alvo="pixvelox.example"
condição   →  escolhe um caminho       if [ -f arquivo ]; then ... fi
laço       →  repete                   for x in lista; do ... done
função     →  dá nome a um bloco       consultar() { ... }
```

Duas pegadinhas que derrubam todo iniciante:
**não ponha espaço ao redor do `=`** (`x=1`, nunca `x = 1`) e **sempre use
aspas ao ler variáveis** (`"$x"`), senão nomes com espaço se partem em pedaços.

## ⌨️ Mão na massa

Tudo está em [`comandos.sh`](comandos.sh), comentado linha a linha. Rode com
`bash comandos.sh`.

### 1. O primeiro script

```bash
cat > ola.sh <<'FIM'
#!/usr/bin/env bash
echo "Olá, recruta. Hoje é $(date +%d/%m/%Y)."
FIM
bash ola.sh        # roda pedindo ao bash
chmod +x ola.sh    # dá permissão de execução
./ola.sh           # roda direto (o shebang diz quem executa)
```

### 2. Variáveis e contas

```bash
alvo="PixVelox"
hoje=$(date +%Y-%m-%d)            # saída de comando vira variável
echo "Alvo: $alvo — $hoje"
echo "Tamanho: ${#alvo}"          # quantas letras
echo "Prejuízo: $(( 412 * 850 ))" # contas com inteiros
```

### 3. Decisões

```bash
read -r -p "Valor do prejuízo: " valor     # o usuário digita
if (( valor > 1000 )); then echo "ALTO"; else echo "baixo"; fi

case "$link" in
  *pixvelox.example*) echo "Link do golpe!" ;;
  *)                  echo "Desconhecido" ;;
esac
```

### 4. Laços

```bash
declare -a suspeitos=("lucas_suporte" "mare_alta")
for nome in "${suspeitos[@]}"; do echo "$nome"; done

for pasta in primeira segunda terceira; do mkdir -p "$pasta"; done

x=1;  while [ "$x" -le 5 ];  do echo "$x"; x=$(( x + 1 )); done
x=15; until [ "$x" -lt 10 ]; do echo "$x"; x=$(( x - 1 )); done

while read -r linha; do echo "→ $linha"; done < desafio/vitimas.txt
```

### 5. Funções

```bash
saudar() {
  local nome="$1"            # primeiro argumento
  echo "Bem-vindo, $nome!"
}
saudar "recruta"
saudar "Jurema"
```

### 6. Campos separados (a chave do desafio)

```bash
while IFS=';' read -r ordem metodo dado; do
  echo "ordem=$ordem metodo=$metodo dado=$dado"
done < desafio/pistas.txt
```

## 🇧🇷 Versão brazuca

Um laço + uma função = consulta em lote numa API pública brasileira. A
[BrasilAPI](https://brasilapi.com.br/docs) responde CEPs de graça. Aqui
consultamos endereços de **órgãos públicos** (Palácio do Planalto e
Congresso Nacional):

```bash
consultar_cep() {
  local cep="$1"
  echo "== CEP $cep"
  curl -s "https://brasilapi.com.br/api/cep/v1/$cep"
  echo
  sleep 1        # educação: não martele a API
}

for cep in 70150900 70160900; do
  consultar_cep "$cep"
done
```

Amanhã de manhã, troque a lista por um arquivo com 50 CEPs citados pelas
vítimas e use `while read -r cep; do consultar_cep "$cep"; done < ceps.txt`.
O mesmo esqueleto serve para feriados (`/api/feriados/v1/2026`), bancos
(`/api/banks/v1`) e DDDs (`/api/ddd/v1/31`).

## 🐍 Ponte Python

[`equivalente.py`](equivalente.py) faz o mesmo — incluindo o decodificador
completo — só com a biblioteca padrão.

| Terminal | Python (stdlib) |
|---|---|
| `x="valor"` / `"$x"` | `x = "valor"` / `x` |
| `$(( a * b ))` | `a * b` |
| `if (( x > 10 ))` | `if x > 10:` |
| `case ... esac` | `match` / `if ... elif` |
| `for x in "${lista[@]}"` | `for x in lista:` |
| `for i in {1..5}` | `for i in range(1, 6):` |
| `while` / `until` | `while cond:` / `while not cond:` |
| `funcao() { ... }` | `def funcao(): ...` |
| `IFS=';' read -r a b c` | `a, b, c = linha.split(";")` |
| `rev` | `texto[::-1]` |

## 🚀 Além do curso

- **[ShellCheck](https://www.shellcheck.net/)** lê seu script e aponta erros antes de você rodá-lo (aspas esquecidas, variáveis não usadas…). `apt install shellcheck` e depois `shellcheck meu_script.sh`. Todos os scripts deste curso passam nele.
- **[Bats](https://github.com/bats-core/bats-core)** (`apt install bats`) escreve **testes** para scripts Bash: você garante que o seu coletor continua funcionando depois de mexer nele.
- Em Python, o módulo `subprocess` (stdlib) chama qualquer comando do Linux: `subprocess.run(["whois", "registro.br"], capture_output=True, text=True)`. É a ponte para misturar os dois mundos.

## 🧩 Desafio

1. Leia `desafio/pistas.txt` e entenda o formato `ordem;metodo;dado`.
2. Copie o rascunho: `cp desafio/decodificador.sh meu-decodificador.sh`.
3. Complete os `TODO`: a função `decodificar_numeros` (um laço `for`), pular
   comentários e linhas `ruido` (um `if` ou `case`) e juntar os pedaços na
   ordem da primeira coluna.
4. Monte `VAZANTE{pedaços}` e confira: `bash checar.sh 'VAZANTE{...}'`

<details>
<summary>💡 Dica 1</summary>

`${1//-/ }` troca todos os hífens por espaços. Aí `for n in ${1//-/ }` passa
por cada número. A letra de número `n` é `${alfabeto:n-1:1}` (um caractere a
partir da posição `n-1`).
</details>

<details>
<summary>💡 Dica 2</summary>

Faça o laço imprimir `ordem pedaço` em cada linha e mande tudo para
`sort -n | cut -d' ' -f2 | tr -d '\n'`. O `sort -n` põe na ordem, o `cut`
tira a coluna de ordem e o `tr` cola os pedaços.
</details>

A solução comentada está em [`solucoes/dia-02.sh`](../../solucoes/dia-02.sh) — só abra depois de tentar.

## 🛡️ Ética e OPSEC

- **Script automatiza tudo — inclusive erros e abusos.** Um laço que consulta
  uma API mil vezes por segundo pode derrubar o serviço ou bloquear o seu IP.
  Ponha um `sleep` e respeite os limites de uso de cada fonte.
- Jurema lembra: rodar um script em lote sobre dados pessoais continua sendo
  **tratamento de dados** pela LGPD (Lei 13.709/2018). Tenha base legal e
  finalidade clara antes de coletar.
- Nunca rode script baixado da internet sem ler. `bash script.sh` executa
  tudo o que estiver lá, com as **suas** permissões.

## 📝 Diário de bordo

Anote no [`DIARIO.md`](../../DIARIO.md) o que aprendeu hoje, o que travou e
uma ideia de uso real.

---

⬅️ [Dia 1](../dia-01-arquivos-e-pastas/) · [Índice](../../README.md) · [Dia 3](../dia-03-instalar-programas/) ➡️
