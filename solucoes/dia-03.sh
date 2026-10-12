#!/usr/bin/env bash
# ⚠️ SPOILER — solução do Dia 3. Tente sozinho antes!
# Ideia: a senha da evidencia.zip não está DENTRO de um texto, e sim no NOME
# de um arquivo oculto do inventario.zip. Listar sem extrair (zip -sf ou
# unzip -l) revela "cofre_senha=...". Depois, unzip -p com a senha imprime o
# relatório trancado, e grep -o pesca a flag.
cd "$(dirname "$0")/../dias/dia-03-instalar-programas/desafio" || exit 1

# 1. listar o inventário e pegar a parte depois de "cofre_senha=" e antes de ".txt"
senha=$(zip -sf inventario.zip | grep -o 'cofre_senha=[^.]*' | cut -d= -f2)
echo "Senha encontrada no nome do arquivo: $senha"

# 2. ver o que tem na caixa trancada (os nomes não são criptografados)
unzip -l evidencia.zip

# 3. ler o relatório direto do zip, sem extrair nada no disco
unzip -p -P "$senha" evidencia.zip evidencia/relatorio-saque.txt | grep -o 'VAZANTE{[^}]*}'
