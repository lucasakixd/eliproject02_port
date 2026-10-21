# Gerador pseudoaleatório

## Estado e seed

- [FATO] O estado é o global de 32 bits `DAT_0049803c`.
- [FATO] `FUN_00402a84` chama `GetSystemTime` e forma a seed como milissegundos desde a meia-noite UTC: `((hora * 60 + minuto) * 60 + segundo) * 1000 + milissegundo`.
- [FATO] Este export mostra a rotina de seed, mas não prova que seja o único ponto que inicializa ou altera o estado.

## Inteiro limitado

`FUN_00402d00(limit)` atualiza o estado e retorna:

$$
state_{n+1} = (state_n \times 0x08088405 + 1) \bmod 2^{32}
$$

$$
result = \left\lfloor \frac{limit \times state_{n+1}}{2^{32}} \right\rfloor
$$

- [FATO] A implementação usa a palavra alta do produto sem sinal de `limit * state`.
- [HIPÓTESE] Para `limit > 0`, o retorno é um inteiro limitado a `[0, limit)`. A qualidade estatística do gerador e o tratamento de viés não foram avaliados.
- [FATO] Um `limit` igual a zero produz zero e ainda avança o estado.

## Caminho x87

- [FATO] `FUN_00402d18` avança o mesmo LCG e aplica `fscale` ao valor convertido para `float10` com a constante global `_DAT_0049602c`.
- [HIPÓTESE] Este é um caminho para amostras de ponto flutuante. A escala exata depende da constante e do estado x87; não foi reconstruída aqui.

## Implicações para o port

- [FATO] A seed depende da hora UTC, então execuções normais não são determinísticas.
- [HIPÓTESE] Para testes e reprodução de partidas em Godot, uma implementação deverá aceitar seed explícita e preservar o estado entre chamadas. Isso não garante equivalência sem identificar todas as chamadas e a sequência de consumo do gerador.