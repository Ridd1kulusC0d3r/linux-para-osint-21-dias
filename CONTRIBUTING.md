# Como contribuir

Este repositório nasceu como diário de estudos e é aberto. Contribuições são
muito bem-vindas — especialmente de quem está fazendo o curso pela primeira vez,
porque você enxerga o que ficou confuso.

## Formas de ajudar

- 🐛 **Comando quebrado** — uma ferramenta mudou ou um passo não funciona? Abra uma issue "Comando quebrado".
- 🇧🇷 **Nova fonte brasileira** — conhece uma base pública ou API útil para algum dia? Abra uma issue "Fonte BR".
- ✍️ **Explicação melhor** — trecho confuso, erro de português, exemplo mais claro.
- 🧩 **Desafio extra** — uma nova pista para a Operação Vazante.

## Regras do jogo

1. **Tudo fictício.** Nada de dados reais de pessoas. Domínios com sufixo `.example`,
   telefones `(31) 90000-XXXX`. Nunca CPF, nem inventado.
2. **Python só com biblioteca padrão** no `equivalente.py`. Simples > esperto.
3. **Comentários em português**, explicando o *porquê*, não só o *o quê*.
4. **Cada bloco `# %%` do `comandos.sh` é autossuficiente** (vira célula do Colab).
   Use subshell `( cd pasta && ... )` em vez de `cd` solto.
5. **Internet é opcional.** Toda seção online precisa de um caminho offline com cópia salva.
6. **Não traduza o PDF original.** Escreva com suas palavras e aponte para o original.

## Antes de abrir o PR

```bash
python3 ferramentas/gerar_notebooks.py   # atualiza os notebooks a partir dos comandos.sh
bash ferramentas/testar_tudo.sh          # testa tudo (ou: testar_tudo.sh 05 para um dia)
```

Se mexeu em evidências, altere a fábrica em `ferramentas/fabrica/diaNN.py` e
rode-a de novo — os arquivos de `desafio/` devem ser reproduzíveis.

Se mudou uma flag, atualize o hash no `checar.sh` do dia:

```bash
printf '%s' 'VAZANTE{nova_flag}' | sha256sum
```
