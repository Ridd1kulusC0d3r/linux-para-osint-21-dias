#!/usr/bin/env bash
# =============================================================================
#  Testa o curso inteiro: scripts, Python, soluções, flags e notebooks.
#    bash ferramentas/testar_tudo.sh            # todos os dias
#    bash ferramentas/testar_tudo.sh 05         # só o Dia 5
#  Usado pelo GitHub Actions a cada push. Roda em modo offline para ser
#  determinístico (L4O_OFFLINE=1).
# =============================================================================
cd "$(dirname "$0")/.." || exit 1
source lib/comum.sh
export L4O_OFFLINE=1
export LANG=C.UTF-8

filtro="${1:-}"
falhas=0
log="$(mktemp)"
trap 'rm -f "$log"' EXIT

falhou() { erro "$1"; falhas=$((falhas + 1)); }

for pasta in dias/dia-*/; do
  pasta="${pasta%/}"; nome="$(basename "$pasta")"; nn="${nome#dia-}"; nn="${nn%%-*}"
  [ -n "$filtro" ] && [ "$nn" != "$filtro" ] && continue
  titulo "$nome"

  # 1. comandos.sh roda até o fim, sem "command not found" nem arquivo faltando
  if timeout 600 bash "$pasta/comandos.sh" >"$log" 2>&1; then
    # linhas marcadas com [esperado] são erros didáticos, de propósito
    if grep -v '\[esperado\]' "$log" | grep -qE 'command not found|No such file or directory|syntax error'; then
      grep -v '\[esperado\]' "$log" | grep -nE 'command not found|No such file or directory|syntax error' | head -n 5
      falhou "$nome: comandos.sh terminou com erros no meio"
    else
      ok "comandos.sh"
    fi
  else
    tail -n 15 "$log"; falhou "$nome: comandos.sh saiu com erro"
  fi

  # 2. equivalente.py roda
  if [ -f "$pasta/equivalente.py" ]; then
    if timeout 120 python3 "$pasta/equivalente.py" >"$log" 2>&1; then ok "equivalente.py"
    else tail -n 15 "$log"; falhou "$nome: equivalente.py"; fi
  fi

  # 3. a solução produz uma flag que o checar.sh aceita
  if [ -f "$pasta/checar.sh" ]; then
    sol="solucoes/dia-$nn.sh"
    if [ ! -f "$sol" ]; then
      falhou "$nome: falta $sol"
    else
      flag="$(timeout 300 bash "$sol" 2>/dev/null | tail -n 1)"
      if bash "$pasta/checar.sh" "$flag" >/dev/null 2>&1; then ok "solução → flag aceita"
      else falhou "$nome: a solução não gerou a flag correta (saiu: '$flag')"; fi
    fi
  fi

  # 4. o repositório continua limpo (nenhum arquivo de treino esquecido)
  if command -v git >/dev/null && git rev-parse --git-dir >/dev/null 2>&1; then
    sujos="$(git status --porcelain --untracked-files=all -- "$pasta" | grep -v '^ M' || true)"
    if [ -n "$sujos" ]; then echo "$sujos" | head -n 5; falhou "$nome: deixou arquivos novos na pasta"; fi
  fi
done

# 5. lint e notebooks em dia
titulo "shellcheck"
if command -v shellcheck >/dev/null; then
  if find . -name '*.sh' -not -path './.git/*' -not -path '*/desafio/*' -print0 \
     | xargs -0 shellcheck -x -S warning; then ok "shellcheck"; else falhou "shellcheck"; fi
fi
titulo "notebooks"
if python3 ferramentas/gerar_notebooks.py --checar; then ok "notebooks em dia"; else falhou "notebooks"; fi
if python3 ferramentas/gerar_site.py --checar; then ok "site em dia"; else falhou "site (docs/dados.js)"; fi

rm -rf .progresso
echo
if [ "$falhas" -eq 0 ]; then ok "Tudo certo. 🦉"; else erro "$falhas falha(s)."; exit 1; fi
