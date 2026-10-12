#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 21 (e, de quebra, de todo o curso).
# Ideia: rodar as 20 soluções, guardar cada flag numa pasta temporária de
# progresso e entregar essa pasta ao montar_dossie.sh.
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp" "$RAIZ/dias/dia-21-distro-e-dossie/dossie-final"' EXIT

for n in $(seq 1 20); do
  nn="$(printf '%02d' "$n")"
  pasta="$(basename "$(echo "$RAIZ"/dias/dia-"$nn"-*)")"
  bash "$RAIZ/solucoes/dia-$nn.sh" 2>/dev/null | tail -n 1 > "$tmp/$pasta.flag"
done

L4O_PROGRESSO="$tmp" bash "$RAIZ/dias/dia-21-distro-e-dossie/montar_dossie.sh" | tail -n 1
