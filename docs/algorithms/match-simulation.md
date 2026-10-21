# Simulação de partidas

## Relógio e despacho de eventos

- [FATO] `FUN_0045a574` incrementa o minuto em `param_1+0x7d`, limitado por `param_1+0x7c`.
- [FATO] A cada minuto ativo, percorre a coleção global de partidas e tenta, em ordem, `FUN_00482284`, `FUN_004825ec`, `FUN_0048275c`, `FUN_004829a4` e `FUN_00482b88`. Cada função posterior só é chamada se a anterior retornar falso; assim, no máximo um desses eventos é selecionado por partida e minuto.
- [FATO] `FUN_00482d2c` também é chamado para cada partida após a cadeia.
- [FATO] No minuto 45 (`0x2d`), `FUN_0045a574` chama uma rotina de intervalo e atualiza a exibição do relógio.
- [FATO] No minuto 90 (`0x5a`), se o modo do relógio permitir, chama `FUN_00475838`. Se ainda houver itens empatados pendentes, o limite do relógio passa para 120 (`0x78`).
- [HIPÓTESE] A extensão até 120 minutos é prorrogação para partidas empatadas. A rotina não demonstra uma etapa de pênaltis após 120 minutos.

## Preparação dos lados

- [FATO] `FUN_00482224` chama `FUN_004791f0` para cada lado quando ambos existem; o segundo lado é pulado sob o estado global `DAT_0049be1a`.
- [FATO] `FUN_004791f0` percorre a lista de membros em `side+0x0c`, recalcula valores derivados e pode reorganizar/atualizar itens e coleções do lado.
- [HIPÓTESE] Essa preparação corresponde à normalização da escalação/força antes da partida; o papel preciso de cada valor recalculado continua aberto.

## Tentativas que alteram o placar

`FUN_00482284` exige que os dois lados existam. No fluxo observado:

1. Há dois limites de ação no contexto: shorts em `match+0x54` e `match+0x56`.
2. O primeiro caminho compara `FUN_00402d00(6000)` ao limite `+0x54`; o segundo usa `FUN_00402d00(7000)` e `+0x56`, desde que o primeiro lado não tenha sido selecionado.
3. Em caminhos alternativos, `FUN_0045b824` seleciona/compara um membro de cada lado e decide se a ação é bem-sucedida.
4. Se nenhum desses caminhos selecionar a ação, chama `FUN_00479ae0` para o lado 0; só se falhar tenta o lado 1.
5. Quando há sucesso, incrementa em 1 o placar do lado correspondente em `side+0x6c`.
6. Atualiza contadores do membro selecionado, cria um registro via `FUN_00484bcc`, anexa-o à fila em `match+0x4c` e chama `FUN_00481940` para atualizar o estado/apresentação da partida.

- [FATO] `FUN_00479ae0` usa o minuto e os acumuladores do lado, chama helpers com operações x87 e usa o RNG limitado em mais de um ponto; seu retorno é consumido como indicador de sucesso pelo atualizador de placar.
- [HIPÓTESE] Esse fluxo gera gols. O código prova a alteração do placar, mas o nome do evento e a fórmula completa de probabilidade precisam ser confirmados por reconstrução das pilhas x87 em `FUN_00479994`, `FUN_00479944` e `FUN_004798d8`.
- [FATO] Os códigos numéricos gravados por `FUN_00484bcc` ficam nos registros de evento; os caminhos observados usam `1`/`2` para os dois modos de ação de placar.

## Outros eventos observados

Os rótulos abaixo são categorias numéricas do registro, não nomes confirmados de evento.

| Gerador | Condições observadas | Registro/efeito observado |
|---|---|---|
| `FUN_004825ec` | Condição global `FUN_004933c0(5)`; compara `random(90)` com o minuto; faz testes adicionais com `random(120)` e limites `+0x54`/`+0x56`. | Usa `FUN_00479c84` para escolher membro e cria evento tipo `3` ou `5`; atualiza flags/contadores do membro. |
| `FUN_0048275c` | Só após o minuto 29; compara `random(1000)` com 10 para cada lado, sujeito aos limites do contexto. | Usa `FUN_00479de0` para escolher membro e cria evento tipo `4`. |
| `FUN_004829a4` | Exige os dois lados; usa `random(500)` para escolher a ocorrência e o lado. | Usa `FUN_00479ea8` para selecionar membro e cria evento tipo `6`. |
| `FUN_00482b88` | Exige evento anterior; `random(30)` precisa ser menor ou igual a 9 e o evento precisa corresponder ao minuto anterior e ao tipo `1`. | Pode diminuir o placar do lado, ajustar contadores e alterar o tipo do registro para `7`. |

- [FATO] Esses geradores modificam campos de membros, placares, contadores de equipe e a fila de eventos.
- [HIPÓTESE] Os tipos `3`, `4`, `5`, `6` e `7` podem corresponder a faltas/cartões, lesões, substituições ou anulação de gol; não nomear esses eventos até decodificar o construtor/apresentação em `FUN_00481940` e os recursos relacionados.

## Dados do registro de evento

- [FATO] `FUN_00484bcc` inicializa um objeto curto: `+0x04` recebe o lado, `+0x06` o minuto, `+0x08` o código do evento, `+0x0a` um short do membro e `+0x0c` um byte de seus metadados.
- [HIPÓTESE] O short em `member+0x04` é camisa ou índice exibido; o byte de metadata vem do perfil em `member+0x08 + 0x19`. O papel dos dois ainda requer comparação com os resources/DFM.

## Limitações para equivalência

- [FATO] O gerador usa o estado global LCG descrito em `docs/algorithms/random.md`; consumo e ordem das chamadas alteram todos os resultados posteriores.
- [FATO] `FUN_00479ae0` mistura aritmética inteira e x87. O decompilado atual não explicita por completo os valores intermediários carregados na FPU.
- [FATO] A cadeia documenta o fluxo temporal e os pontos de mutação, mas ainda não reproduz o algoritmo completo de gols ou o significado semântico de cada evento.