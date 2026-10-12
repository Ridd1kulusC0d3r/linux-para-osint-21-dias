# 🧾 Cheatsheet — Linux para OSINT em uma página

> Os comandos essenciais de cada dia. Para a explicação completa, abra o dia.
> Inspirado na [cheatsheet visual do cipher387](https://github.com/cipher387/cheatsheets/blob/main/linux_for_osint.png).

## Navegar e organizar · [Dia 1](dias/dia-01-arquivos-e-pastas/)

| Comando | Faz |
|---|---|
| `pwd` | mostra a pasta atual |
| `ls -la` | lista tudo, inclusive ocultos |
| `cd pasta` · `cd ..` · `cd -` | entra · sobe · volta |
| `mkdir -p a/b/c` | cria pastas aninhadas |
| `cp -rp origem destino` | copia preservando datas (evidência!) |
| `mv velho novo` | move ou renomeia |
| `rm -r pasta` | apaga **sem lixeira** |
| `find . -type f -name '.*'` | acha arquivos ocultos |
| `stat arquivo` | datas de acesso e modificação |

## Bash · [Dia 2](dias/dia-02-bash-script/)

```bash
alvo="pixvelox.example"                   # variável (sem espaço no =)
if [ -f arquivo ]; then ...; fi           # condição
for x in a b c; do echo "$x"; done        # laço
while read -r linha; do ...; done < lista.txt
funcao() { echo "olá, $1"; }              # função com argumento
```

## Instalar e compactar · [Dia 3](dias/dia-03-instalar-programas/)

| Comando | Faz |
|---|---|
| `sudo apt install pacote` | instala |
| `dpkg -l` | lista o que está instalado |
| `zip arq.zip a b` · `unzip arq.zip -d pasta` | compacta · extrai |
| `unzip -l arq.zip` · `zip -sf arq.zip` | lista sem extrair |

## Em lote · [Dia 4](dias/dia-04-processamento-em-lote/)

```bash
find . -name '*.txt' -type f                          # encontra
find . -name '*.zip' | xargs rm -f                    # aplica um comando a cada resultado
xargs -I {} cp {} destino/ < lista.txt                # um por linha da lista
for f in *.txt; do wc -l "$f"; done                   # laço em arquivos
```

## Web e APIs · [Dia 5](dias/dia-05-curl-e-apis/)

| Comando | Faz |
|---|---|
| `curl -o arq URL` | baixa com nome escolhido |
| `xargs -n 1 curl -O < urls.txt` | baixa uma lista |
| `curl -I URL` | só os cabeçalhos |
| `curl -sIL URL \| grep -i ^location` | segue redirecionamentos |
| `curl -s https://brasilapi.com.br/api/cep/v1/CEP \| jq` | API JSON |

## Buscar em texto · [Dia 6](dias/dia-06-grep/)

| Comando | Faz |
|---|---|
| `grep -i palavra arq` | ignora maiúsculas |
| `grep -n` · `grep -v` · `grep -c` | número da linha · inverte · conta |
| `grep -r palavra .` | em todas as subpastas |
| `grep -Eo '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' arq` | extrai e-mails |

## Editar e calcular · [Dia 7](dias/dia-07-sed-e-awk/)

| Comando | Faz |
|---|---|
| `sed 's/velho/novo/g' arq` | substitui |
| `sed -n '5,12p' arq` | imprime um intervalo de linhas |
| `awk -F, '{print $1,$3}' arq.csv` | colunas 1 e 3 |
| `awk -F, '{s[$2]+=$3} END{for(k in s) print k,s[k]}'` | soma por grupo |

## Vim · [Dia 8](dias/dia-08-vim/)

`i` inserir · `Esc` sair do modo · `:w` salvar · `:q!` sair sem salvar · `:wq` salvar e sair ·
`/texto` buscar · `:42` ir para linha 42 · `dd` apagar linha · `:%s/a/b/g` substituir tudo

## Segundo plano e agenda · [Dia 9](dias/dia-09-screen-e-cron/)

| Comando | Faz |
|---|---|
| `screen -S nome` · `Ctrl+A D` · `screen -r nome` | cria · desanexa · volta |
| `screen -dmS nome comando` | roda já em segundo plano |
| `crontab -l` · `crontab -e` | lista · edita agendamentos |
| `17 3 * * 0 comando` | todo domingo às 03:17 (min hora dia mês dia-da-semana) |

## Texto · [Dia 10](dias/dia-10-utilitarios-de-texto/)

`cat a b > c` juntar · `cut -d, -f2` coluna · `sort` · `sort -r` · `sort -u` ·
`uniq -c` contar repetidos · `wc -l` linhas · `comm -12 a b` linhas em comum · `diff a b`

## Mídia · [Dia 11](dias/dia-11-video-audio-imagem/)

```bash
ffmpeg -i video.mp4 -r 1 frame%03d.png        # 1 frame por segundo
ffmpeg -i video.mp4 -q:a 0 -map a audio.mp3   # extrai o áudio
tesseract imagem.png saida                    # OCR → saida.txt
exiftool arquivo                              # metadados
```

## PDF · [Dia 12](dias/dia-12-pdf/)

`pdftotext arq.pdf` texto · `pdfimages -png arq.pdf img` imagens · `pdfinfo arq.pdf` · `exiftool arq.pdf | grep -i author` · `ocrmypdf entrada.pdf saida.pdf`

## Office · [Dia 13](dias/dia-13-arquivos-office/)

```bash
libreoffice --headless --convert-to txt arq.docx
unzip -l arq.docx                  # docx/xlsx são ZIP!
unzip -p arq.docx docProps/core.xml   # autor, datas
pandoc -f html -t docx pagina.html -o pagina.docx
```

## Dados estruturados · [Dia 14](dias/dia-14-json-xml-csv/)

```bash
jq '.people[].firstName' arq.json
jq '.[] | select(.autor=="mare_alta")' arq.json
xmlstarlet sel -t -m '//TITLE' -v . -n arq.xml
csvcut -c dominio,porta arq.csv · csvgrep -c 2 -m termo arq.csv · in2csv arq.json
```

## Scraping · [Dia 15](dias/dia-15-scraping/)

`curl -s URL | grep -Eo 'href="[^"]+"'` links · `html2text pagina.html` · `katana -u site` crawler · `python3 -m http.server` servidor local

## Buscas · [Dia 16](dias/dia-16-automacao-de-busca/)

`ddgr termo` busca no DuckDuckGo · `netlas download "consulta"` · `jq` nos resultados

## Arquivos compartilhados · [Dia 17](dias/dia-17-compartilhamento-de-arquivos/)

`sha256sum arq` identidade de um arquivo · `transmission-show arq.torrent` · `curl ftp://servidor/`

## Domínios · [Dia 18](dias/dia-18-investigacao-de-dominio/)

`whois dominio` · `whois dominio | grep -i creat` · `dig dominio` · `dig +short NS dominio` · `dig MX dominio` · `dig TXT dominio`

## Git · [Dia 19](dias/dia-19-git-e-github/)

`git clone URL` · `git log --all --oneline` · `git log -p` histórico com mudanças · `git show <commit>` · `git log --format='%an <%ae>'` autores e e-mails

## Produtividade · [Dia 20](dias/dia-20-ferramentas-uteis/)

`shellcheck script.sh` acha bugs · `history | grep curl` · `Ctrl+R` busca no histórico · `alias ll='ls -la'` · `tldr comando` exemplos rápidos

## Distro · [Dia 21](dias/dia-21-distro-e-dossie/)

`cat /etc/os-release` · `uname -r` · `sha256sum` integridade · `bash montar_dossie.sh` 🦉
