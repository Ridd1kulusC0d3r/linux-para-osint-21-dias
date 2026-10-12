#!/usr/bin/env bash
# =============================================================================
#  Dia 17 — O torrent do kit: compartilhamento de arquivos, torrents e FTP
#  Rodar tudo:  bash comandos.sh
#  Cada bloco "# %%" vira uma célula no notebook do Colab.
#
#  Regra do dia: a gente INSPECIONA torrents, não baixa. Nenhuma seção aqui
#  conecta em rede de torrent. Abrir o .torrent é ler um arquivo de texto.
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% Impressão digital de arquivos: sha256sum e md5sum
# Um "hash" é uma impressão digital: o mesmo conteúdo SEMPRE gera o mesmo
# hash; mudar UMA vírgula muda o hash inteiro. Serve para:
#   - provar que uma evidência não foi alterada (cadeia de custódia)
#   - reconhecer o mesmo arquivo com nomes diferentes
#   - procurar um arquivo em bases (VirusTotal, listas de vazamento...)
# md5 e sha1 são antigos (dá para forjar colisões); prefira sha256.
titulo "Hashes das amostras de roteiro"
sha256sum desafio/amostras/*.txt
echo "--- md5 (mais curto, ainda muito usado em listas antigas) ---"
md5sum desafio/amostras/roteiro_a.txt

# %% Qual arquivo tem o hash da denúncia?
# A vítima 014 informou o SHA-256 da mensagem que recebeu. Comparando com os
# hashes das amostras descobrimos QUAL roteiro foi usado — sem ler nada.
# Repare: roteiros quase iguais (um espaço, uma vírgula) têm hashes totalmente diferentes.
titulo "Procurando o hash da vítima 014"
cat desafio/denuncia_vitima014.txt
alvo=$(grep -oE '[0-9a-f]{64}' desafio/denuncia_vitima014.txt)
sha256sum desafio/amostras/*.txt | grep "$alvo"

# %% Conferindo um lote inteiro com sha256sum -c
# Guardar os hashes num arquivo e conferir depois é o jeito padrão de provar
# que nada mudou desde a coleta. "OK" = idêntico. "FAILED" = alterado.
titulo "Gravando e conferindo hashes"
mkdir -p treino
cp desafio/amostras/*.txt treino/
( cd treino && sha256sum ./*.txt > SHA256SUMS && sha256sum -c SHA256SUMS )
echo " (alterando um arquivo de propósito...)"
echo "adulterado" >> treino/roteiro_e.txt
( cd treino && sha256sum -c SHA256SUMS 2>/dev/null ) || alerta "um arquivo mudou desde a coleta!"
rm -r treino

# %% Por dentro de um .torrent: o formato bencode
# Um .torrent NÃO contém os arquivos — contém a DESCRIÇÃO deles: nomes,
# tamanhos, endereço dos "trackers" e a impressão digital de cada pedaço.
# Ele é escrito em "bencode", um formato simples e quase legível:
#   i42e         -> número 42
#   4:spam       -> texto de 4 letras "spam"
#   l...e        -> lista
#   d...e        -> dicionário (chave, valor, chave, valor...)
# Por isso dá para espiar com ferramentas de texto mesmo.
titulo "O começo do .torrent, cru"
precisa strings binutils
head -c 400 desafio/kit_golpe_pixvelox.torrent; echo
echo "--- trechos de texto (strings), quebrados em linhas de 100 caracteres ---"
strings -n 8 desafio/kit_golpe_pixvelox.torrent | fold -w 100 | head -n 4
echo "--- campos interessantes com grep -ao (-a trata binário como texto) ---"
grep -ao '7:comment[0-9]*:' desafio/kit_golpe_pixvelox.torrent
grep -ao '13:creation datei[0-9]*e' desafio/kit_golpe_pixvelox.torrent

# %% transmission-show: lendo o torrent como gente grande
# transmission-show (pacote transmission-cli) decodifica o .torrent e mostra:
# nome, quem criou, quando, comentário, trackers e a lista de arquivos.
#   -f   só a lista de arquivos      -m  gera o link magnet
#   -t   só os trackers              -b  tamanhos em bytes
titulo "transmission-show"
precisa transmission-show transmission-cli
transmission-show desafio/kit_golpe_pixvelox.torrent
echo "--- só o link magnet ---"
transmission-show -m desafio/kit_golpe_pixvelox.torrent

# %% aria2c -S: outra forma de inspecionar
# aria2 é um baixador de linha de comando que entende HTTP, FTP e BitTorrent.
# -S (--show-files) só MOSTRA o conteúdo do .torrent, sem baixar nada.
titulo "aria2c -S"
precisa aria2c aria2
aria2c -S desafio/kit_golpe_pixvelox.torrent | sed -n '1,14p'
dica "Baixar seria: aria2c arquivo.torrent  — NÃO faça isso com material criminoso."

# %% Dissecando um link magnet
# Magnet é um torrent "em forma de link": em vez do arquivo, só a impressão
# digital (info hash) + nome + trackers. Os campos vêm separados por &.
#   xt=urn:btih:HASH   o info hash (identifica o torrent no mundo inteiro)
#   dn=NOME            nome de exibição
#   tr=URL             tracker (pode haver vários)
# O info hash é ótimo para pesquisa: o mesmo kit postado em vários fóruns
# com nomes diferentes tem SEMPRE o mesmo hash.
titulo "Partes do magnet"
magnet=$(transmission-show -m desafio/kit_golpe_pixvelox.torrent)
echo "$magnet" | tr '?' '&' | tr '&' '\n'     # troca ? e & por quebra de linha
echo "--- trackers decodificados (urldecode com python) ---"
echo "$magnet" | tr '&' '\n' | grep '^tr=' | cut -d= -f2- \
  | python3 -c 'import sys, urllib.parse as u; [print(u.unquote(l.strip())) for l in sys.stdin]'

# %% Criando o seu próprio torrent (para entender o formato)
# transmission-create gera um .torrent a partir de uma pasta. Nenhum dado
# sai do seu computador: ele só calcula os hashes e escreve o arquivo.
#   -c "texto"   comentário       -t URL   tracker
titulo "transmission-create"
precisa transmission-create transmission-cli
mkdir -p treino/meu-kit
echo "relatório do Núcleo Coruja" > treino/meu-kit/relatorio.txt
transmission-create -o treino/teste.torrent -c "teste do curso" \
  -t udp://tracker.nucleo-coruja.example:6969/announce treino/meu-kit >/dev/null
transmission-show treino/teste.torrent | sed -n '1,12p'
rm -r treino

# %% FTP: o protocolo antigo que ainda guarda muita coisa
# FTP (File Transfer Protocol) é de 1971 e continua vivo em órgãos públicos,
# câmeras e roteadores. Sem criptografia: senha e arquivos passam "abertos".
#   curl ftp://servidor/pasta/            lista a pasta
#   curl -O ftp://servidor/arquivo        baixa
#   lftp ftp://servidor                   cliente completo (mirror, scripts)
#   ftp servidor                          cliente clássico, interativo
# Exemplo REAL e público: o FTP do IBGE (dados abertos de mapas e censos).
titulo "Listando um FTP público"
precisa lftp
if online && curl -s -m 20 --list-only ftp://ftp.ibge.gov.br/ -o lista_ftp.txt && [ -s lista_ftp.txt ]; then
  head -n 15 lista_ftp.txt
else
  alerta "offline (ou FTP bloqueado na rede): usando cópia salva"
  cat desafio/ftp_listagem.txt
fi
rm -f lista_ftp.txt
mostrar "lftp -e 'ls; bye' ftp://ftp.ibge.gov.br"
interativo ftp ftp.ibge.gov.br

# %% Lendo a listagem FTP com awk
# A listagem longa de FTP tem as mesmas colunas do `ls -l`: permissões,
# dono, grupo, tamanho, data e nome. awk (Dia 7) separa as colunas.
titulo "Arquivos e tamanhos da listagem salva"
awk '$1 !~ /^d/ {print $5, $NF}' desafio/ftp_listagem.txt
echo "--- só as pastas ---"
awk '$1 ~ /^d/ {print $NF "/"}' desafio/ftp_listagem.txt

# %% Sites de compartilhamento e redes sociais
# Muitos serviços têm clientes de terminal (oficiais ou não). Exemplos:
#   Google Drive: gdrive        Dropbox: dbxcli      Mega: MEGAcmd (mega-get)
#   Vídeos de redes sociais: yt-dlp (sucessor do youtube-dl)
# Link direto de arquivo? curl/wget resolvem. Só cuidado: clientes não
# oficiais podem bloquear sua conta. Use contas de investigação.
titulo "Downloads de compartilhamento (exemplos)"
mostrar "wget -O arquivo.pdf 'https://link-direto.example/arquivo.pdf'"
mostrar "yt-dlp --skip-download --write-info-json 'URL_DO_VIDEO'   # só metadados"
mostrar "mega-get 'https://mega.nz/file/...' ./evidencias/"
dica "Depois de baixar qualquer coisa: sha256sum na hora e anote no relatório."
