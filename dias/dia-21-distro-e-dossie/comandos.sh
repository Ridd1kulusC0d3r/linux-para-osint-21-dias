#!/usr/bin/env bash
# =============================================================================
#  Dia 21 — O dossiê: escolher uma distro e fechar o caso
#  Rodar tudo:  bash comandos.sh
# =============================================================================
cd "$(dirname "$0")" || exit 1
source ../../lib/comum.sh

# %% Que distribuição eu estou usando?
# "Distribuição" (distro) é o pacote completo: kernel Linux + programas +
# gerenciador de pacotes + aparência. /etc/os-release é o RG da distro.
titulo "RG da distro"
cat /etc/os-release
echo
echo "Kernel: $(uname -r)  ·  Arquitetura: $(uname -m)"

# %% Qual família? (descubra pelo gerenciador de pacotes)
# As distros se agrupam em famílias. A forma mais rápida de saber a família
# é ver qual gerenciador de pacotes existe:
#   apt     -> Debian, Ubuntu, Kali, Parrot, Tails
#   dnf     -> Fedora, RHEL, Rocky
#   pacman  -> Arch, Manjaro, BlackArch
#   zypper  -> openSUSE
titulo "Família pelo gerenciador de pacotes"
for gerenciador in apt dnf pacman zypper apk; do
  if command -v "$gerenciador" >/dev/null 2>&1; then
    ok "$gerenciador encontrado"
  else
    printf '  · %s ausente\n' "$gerenciador"
  fi
done

# %% A variável ID_LIKE diz quem é o "pai"
# Muitas distros declaram de quem derivam. Ubuntu diz "debian"; Kali também.
# source carrega o arquivo como variáveis do Bash (ele é escrito nesse formato).
titulo "De quem esta distro deriva?"
(
  # shellcheck disable=SC1091
  . /etc/os-release
  echo "Distro: ${NAME:-?}  ·  Deriva de: ${ID_LIKE:-(nenhuma — é uma distro-mãe)}"
)

# %% Quantos programas eu instalei nestes 21 dias?
# dpkg -l lista todos os pacotes .deb instalados (você viu no Dia 3).
# wc -l conta linhas. As 5 primeiras linhas são cabeçalho.
titulo "Pacotes instalados"
if command -v dpkg >/dev/null 2>&1; then
  echo "$(dpkg -l | tail -n +6 | wc -l) pacotes .deb instalados nesta máquina"
else
  alerta "Esta distro não usa dpkg."
fi

# %% Seu progresso até aqui
# Cada checar.sh que deu certo guardou a flag em .progresso/ (pasta ignorada
# pelo git). Vamos contar quantas você tem.
titulo "Pistas no seu dossiê"
total="$(find "$L4O_HOME/.progresso" -name '*.flag' 2>/dev/null | wc -l)"
echo "Você tem $total de 20 pistas registradas."
if [ "$total" -lt 20 ]; then
  dica "Volte aos dias que faltam e rode: bash checar.sh 'VAZANTE{...}'"
fi

# %% Como funciona o selo (versão de brinquedo)
# O selo final usa duas ideias que você já conhece de nome:
#   1. HASH: sha256sum transforma qualquer texto num "resumo" de 64 letras.
#      Mudou uma vírgula, muda tudo.
#   2. XOR: combinar bytes com uma chave. Fazer XOR duas vezes com a mesma
#      chave devolve o original — cifra e decifra com o mesmo gesto.
titulo "Hash: uma vírgula muda tudo"
printf '%s' "maré alta" | sha256sum
printf '%s' "maré alta." | sha256sum

titulo "XOR: cifrar e decifrar com a mesma chave"
python3 - <<'PY'
chave = b"coruja"
mensagem = b"pista secreta"
cifrado = bytes(b ^ chave[i % len(chave)] for i, b in enumerate(mensagem))
decifrado = bytes(b ^ chave[i % len(chave)] for i, b in enumerate(cifrado))
print("cifrado  :", cifrado.hex())
print("decifrado:", decifrado.decode())
PY

# %% Montando o dossiê
# O montar_dossie.sh confere as 20 flags e, se estiverem todas certas, usa o
# SHA-256 delas como chave para abrir o selo. Sem as 20, o selo não abre.
titulo "Tentando abrir o selo"
bash montar_dossie.sh || dica "Ainda faltam pistas. Tudo bem — o dossiê espera por você."
