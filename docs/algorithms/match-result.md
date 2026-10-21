# Finalização de resultado e classificação

## Entrada observada

- [FATO] `FUN_00480ae4` recebe um contexto com referências aos dois lados em `+0x30` e `+0x34`.
- [FATO] Cada lado contém um inteiro em `+0x6c`, lido como placar para esta rotina.
- [FATO] O byte `context+0x2d` seleciona caminhos diferentes; os detalhes completos de todos os modos ainda não foram modelados.

## Atualização de contadores

No caminho `context+0x2d == 0`, a função:

1. Incrementa `side+0x18` para ambos.
2. Compara os placares.
3. Se forem iguais, incrementa `side+0x20` e `side+0x30` para ambos.
4. Se forem diferentes, incrementa `side+0x1c` no vencedor, `side+0x24` no perdedor e `side+0x30` em 3 no vencedor.
5. Soma o placar próprio a `side+0x28` e o placar adversário a `side+0x2c` para cada lado.

[HIPÓTESE] Os offsets representam, nessa ordem, jogos, vitórias, empates, derrotas, gols a favor, gols contra e pontos. A correspondência é forte pelo padrão de tabela, mas ainda precisa de confirmação na tela de classificação e no formato persistido.

## Empates adiados

- [FATO] `FUN_00482d5c` retorna verdadeiro quando ambos os lados estão presentes e seus valores `+0x6c` são iguais.
- [FATO] `FUN_00475838` não chama o finalizador nesse caso; define `context+0x58` e mantém o item para processamento posterior. Para outros casos, chama `FUN_00480ae4` e remove o item da coleção.
- [HIPÓTESE] A espera pode permitir uma decisão adicional em partidas eliminatórias. Não há evidência suficiente para nomear a etapa como prorrogação ou pênaltis.

## Efeitos nos membros

- [FATO] Os helpers `FUN_0047bedc` e `FUN_0047bf4c` percorrem a lista de ponteiros em `side+0x0c`. Para membros que satisfaçam o filtro `(member+0x18 == 1) || (member+0x10 < 0)`, podem chamar, respectivamente, `FUN_0047ef24` e `FUN_0047ef74`.
- [FATO] Essas rotinas incrementam/decrementam `member+0x0e` em 1 quando `FUN_004933c0(5)` permite e `FUN_00402d00(2)` retorna zero. Os limites 6 e 0 são observados.
- [HIPÓTESE] O efeito é uma mudança probabilística de forma/moral de membro após resultado. O significado de `+0x0e` não está confirmado.

## Limite

[FATO] Esta função contabiliza resultados já presentes nos objetos; não há nela geração do placar nem simulação de lances. A simulação deve ser reconstruída em outro conjunto de rotinas.