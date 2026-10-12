#!/usr/bin/env bash
# =============================================================================
#  Dia 3 — A caixa trancada: instalar programas, zip e unzip
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% O que já está instalado? (dpkg -l)
# No Ubuntu/Debian, cada programa vem num "pacote" .deb. O `dpkg` é quem
# instala e registra esses pacotes. `dpkg -l` lista TODOS os instalados.
# São centenas, então mostramos só as primeiras linhas com `head`.
# As letras "ii" no começo significam: desejado=instalar, estado=instalado.
titulo "Pacotes instalados (início da lista)"
dpkg -l | head -n 12
echo "..."
echo "Total de pacotes instalados: $(dpkg -l | grep -c '^ii')"

# %% Perguntando por um pacote específico
# `dpkg -l nome` mostra só aquele pacote. `command -v` diz ONDE está o
# programa (ou nada, se não existir). `dpkg -S` diz de qual pacote ele veio.
titulo "O zip está aí?"
dpkg -l zip unzip 2>/dev/null | grep '^ii' || alerta "zip/unzip ainda não instalados"
command -v ls
dpkg -S "$(command -v ls)"     # o ls vem do pacote coreutils

# %% Instalando com apt
# O `apt` baixa pacotes da internet (dos repositórios do Ubuntu), resolve as
# dependências e chama o dpkg por você. Instalar exige ser administrador,
# por isso o `sudo` na frente:
#     sudo apt update               # atualiza a lista de pacotes disponíveis
#     sudo apt install zip unzip    # instala os dois
# Aqui usamos a função `precisa` (de lib/comum.sh): ela só instala se o
# programa ainda não existir — rodar duas vezes não faz mal.
titulo "Instalando zip e unzip (se faltar)"
mostrar "sudo apt install zip unzip"
precisa zip
precisa unzip
zip -v | head -n 2
dica "Outros comandos úteis: apt search <palavra>, apt show <pacote>, sudo apt remove <pacote>"

# %% Detalhes de um pacote antes de instalar
# `apt-cache policy` mostra versão instalada e versão disponível.
# `apt show` mostra a descrição. Bom para conferir antes de instalar algo.
titulo "Informações do pacote zip"
apt-cache policy zip 2>/dev/null | head -n 3
apt show zip 2>/dev/null | grep -E '^(Package|Version|Description):' || true

# %% Programas Python: pip
# Muitas ferramentas de OSINT são escritas em Python e se instalam com pip.
#   python3 -m pip install nome-do-pacote
# Em Ubuntu recente, prefira `pipx install ferramenta` (isola cada uma) ou um
# ambiente virtual (python3 -m venv). Aqui só conferimos a versão.
titulo "pip"
python3 -m pip --version 2>/dev/null || alerta "pip não instalado (sudo apt install python3-pip)"

# %% Compactando: zip
# `zip destino arquivos...` cria (ou atualiza) um .zip.
# A extensão .zip é posta automaticamente se você esquecer.
titulo "Criando archive.zip"
mkdir -p treino
cp desafio/test1.txt desafio/test2.txt treino/
(
  cd treino || exit 1
  zip archive test1.txt test2.txt
  ls -l
)

# %% Olhando dentro do zip SEM extrair
# Essencial em investigação: você vê o que tem antes de abrir.
#   zip -sf arquivo.zip     (show files) lista os nomes
#   unzip -l arquivo.zip    lista com tamanho e data
#   unzip -v arquivo.zip    ainda mais detalhes (método, CRC)
titulo "Listando sem extrair"
zip -sf treino/archive.zip
unzip -l treino/archive.zip

# %% Extraindo: unzip
# `unzip arquivo.zip -d pasta` extrai dentro da pasta indicada (cria se
# não existir). Sem -d, extrai na pasta atual — e pode bagunçar tudo.
titulo "Extraindo para uma pasta"
unzip -o treino/archive.zip -d treino/archive
ls -l treino/archive

# %% Zipando pastas inteiras e lendo um arquivo direto
#   zip -r      inclui subpastas (recursivo)
#   unzip -p    imprime o conteúdo de um arquivo de dentro do zip, sem extrair
titulo "zip -r e unzip -p"
zip -rq treino/pasta.zip treino/archive
unzip -l treino/pasta.zip
unzip -p treino/archive.zip test1.txt

# %% Zip com senha
#   zip -e        pede a senha (interativo)
#   zip -P senha  passa a senha na linha de comando (fica no histórico! só em treino)
#   unzip -P senha arquivo.zip   extrai com a senha
# Atenção: os NOMES dos arquivos de um zip com senha continuam visíveis.
titulo "Zip com senha"
interativo zip -e treino/secreto.zip treino/test1.txt
zip -q -P treino123 treino/secreto.zip treino/test1.txt
unzip -l treino/secreto.zip
unzip -o -q -P treino123 treino/secreto.zip -d treino/aberto && ok "abriu com a senha"
unzip -o -q -P errada treino/secreto.zip -d treino/aberto2 2>/dev/null || alerta "senha errada: unzip recusa"

# %% Testando a integridade
# `unzip -t` testa se o zip está íntegro, sem extrair nada.
titulo "Teste de integridade"
unzip -t treino/archive.zip

# %% Limpando
titulo "Limpando a pasta de treino"
rm -r treino
ls

# %% O inventário do notebook apreendido
# A evidência de hoje: dois zips. Um aberto, outro trancado.
titulo "Os zips do desafio"
ls -l desafio/*.zip
unzip -l desafio/evidencia.zip
dica "evidencia.zip pede senha. Olhe o inventario.zip com atenção — sem extrair."
