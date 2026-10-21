# Modelos de dados: reconstrução em andamento

## Convenções

- `[FATO]` descreve uma operação observada diretamente no decompilado ou nos exports citados.
- `[HIPÓTESE]` atribui semântica provável a offsets ou objetos sem nomes de fonte recuperados.
- Os offsets abaixo são relativos aos objetos que o decompilador apresenta. Ainda não são declarações Delphi nem contratos de serialização.

## Registro associado a equipe/participante

### Campos candidatos

| Offset | Operação observada em `FUN_00480ae4` | Interpretação |
|---:|---|---|
| `+0x18` | Incrementado uma vez para cada lado ao processar resultado. | [HIPÓTESE] Jogos disputados. |
| `+0x1c` | Incrementado no lado vencedor. | [HIPÓTESE] Vitórias. |
| `+0x20` | Incrementado em ambos os lados quando os placares são iguais. | [HIPÓTESE] Empates. |
| `+0x24` | Incrementado no lado perdedor. | [HIPÓTESE] Derrotas. |
| `+0x28` | Recebe o placar do próprio lado somado ao valor anterior. | [HIPÓTESE] Gols a favor. |
| `+0x2c` | Recebe o placar do adversário somado ao valor anterior. | [HIPÓTESE] Gols contra. |
| `+0x30` | Recebe 3 no lado vencedor; recebe 1 em cada lado no empate. | [HIPÓTESE] Pontos de classificação. |
| `+0x6c` | Inteiro lido como placar de cada lado antes da atualização. | [FATO] Valor usado como placar nesta rotina. [HIPÓTESE] Placar corrente da partida. |

[FATO] Os objetos estão disponíveis por duas referências em um objeto de contexto nos offsets `+0x30` e `+0x34`. `[HIPÓTESE]` Essas referências designam equipes participantes, ou registros de equipe dentro de uma competição.

[FATO] `FUN_00469ac4` percorre uma coleção global, chama o finalizador `FUN_00480ae4` para cada item e remove o item processado. `FUN_00475838` pode adiar um item quando `FUN_00482d5c` confirma que os dois placares são iguais, marcando o byte em `+0x58`.

### Confiança e próximos testes

As operações e os valores de incremento são fatos. A semântica de jogos/vitórias/empates/derrotas/gols/pontos é hipótese forte por corresponder ao padrão de classificação, mas deve ser confirmada por uma segunda via, por exemplo:

1. localizar a rotina que exibe a tela `TCLASSIFICATIONDLG` e verificar se lê esses mesmos offsets;
2. localizar inicialização/zeragem e cópia desses campos entre temporadas/competições;
3. encontrar leitura ou gravação do registro e comparar com a estrutura dos dados de liga;
4. seguir as funções `FUN_0047af34`, `FUN_0047bf4c`, `FUN_0047bedc` chamadas durante a finalização.

## Team

- [FATO] Strings e recursos incluem formulários `TTEAMPROPERTIESDLG`, `TTEAMSKILLDLG`, `TTEAMCOLORDLG`, `TPLANTELDLG` e rótulos de UI como `teamProp`/`textTeamShortName`.
- [FATO] `FUN_00476d90` constrói um objeto com coleções em `+0x0c`, `+0x10`, `+0x14`, `+0x84`, `+0x88` e `+0x8c`; `FUN_00477428` lê essas coleções/campos e `FUN_00477950` grava sequências correspondentes.
- [FATO] O carregador `FUN_00477428` cria em `+0x0c` uma lista de membros via `FUN_004771c4`, em `+0x84` uma lista via `FUN_004772cc`, em `+0x88` uma lista via `FUN_0047737c`, e reconstrói coleções em `+0x8c` e `+0x14` por helpers próprios.
- [FATO] O escritor `FUN_00477950` grava o comprimento de `+0x10` como short, percorre e grava a lista `+0x0c`, depois percorre `+0x84`, `+0x88` e serializa os objetos de `+0x8c`/`+0x14` por helpers.
- [FATO] Campos diretos transferidos pelo leitor/escritor de Team:

| Offset | Largura/representação | Evidência |
|---:|---:|---|
| `+0x04` | subobjeto/string | Lido/escrito por `FUN_0048c47c`/`FUN_0048c5b8`; não é bloco fixo simples. |
| `+0x08` | 2 bytes | Carregado antes do nome; usado como identificador/índice em buscas. |
| `+0x18` | 0x50 bytes | Bloco de campos transferido em lote. |
| `+0x68` | 0x14 bytes | Segundo bloco transferido em lote. |
| `+0x7c` | 6 bytes | Bloco transferido em lote. |
| `+0x90`, `+0x94`, `+0x98`, `+0x9c` | 4 bytes cada | Campos carregados e gravados individualmente. |
| `+0xa0` | 10 bytes | Bloco transferido. |
| `+0xaa` | 6 bytes | Bloco transferido; o construtor carrega defaults de um global. |
| `+0xb0` | 0x1c bytes | Bloco transferido. |
| `+0xcc` | 0x1c bytes | Bloco transferido. |
| `+0xe8` | 8 bytes | Bloco transferido. |
| `+0xf2`, `+0xf4`, `+0xf6` | 2 bytes cada | Campos carregados e gravados individualmente. |
| `+0xf8` | 10 bytes | Bloco transferido. |
| `+0x104` | 4 bytes | Campo carregado e gravado individualmente. |
| `+0x108`, `+0x10a` | 2 bytes cada | Campos carregados e gravados individualmente. |

- [FATO] O formato do objeto também inclui comprimentos de coleção de 16 bits e itens dinâmicos, portanto não equivale a despejar em sequência uma struct C de tamanho fixo.
- [HIPÓTESE] Esse objeto Team corresponde a um registro salvo em `teams/*.ilt`, pois existem 338 arquivos com esses nomes e o construtor contém coleção de membros; a correspondência arquivo-classe ainda não está provada por um call site que abra a extensão `.ilt`.
- [FATO] Objetos passados a `FUN_0047a674`, `FUN_0047bedc` e `FUN_0047bf4c` expõem uma lista de ponteiros em `+0x0c`; as rotinas percorrem essa lista para agregar valores ou atualizar seus elementos.
- [FATO] O objeto passado como lado em `FUN_00480ae4` é entregue a helpers que percorrem a coleção de membros em `+0x0c`; ele também possui os offsets `+0x18` a `+0x30` modificados como contadores de classificação e esses offsets pertencem ao bloco serializado em `FUN_00477428`/`FUN_00477950`.
- [HIPÓTESE] Isso liga o objeto participante do Match ao registro Team carregado pelo leitor de Team; o vínculo entre esse leitor específico e a extensão `.ilt` ainda não foi encontrado.
- [FATO] Os objetos participantes descritos acima são modificados em pares durante a finalização de resultado.
- [FATO] Campos como nome, elenco, treinador, estádio, finanças e identificador ainda não foram associados a offsets comprovados.

## Player

- [FATO] Recursos/strings identificam `TPLAYERPROPERTIESDLG`, `TEDITPLAYERDLG`, `TOBSERVEDPLAYERSDLG` e controles chamados `player`.
- [FATO] `FUN_00488aa0` seleciona itens por um campo em `item+0x18` e os adiciona a listas apresentadas como `player`.
- [FATO] `FUN_004771c4` lê uma contagem de 16 bits, constrói cada elemento por `FUN_0047d4d4`, adiciona o mesmo ponteiro a uma lista local e a `DAT_0049bdf4`. `FUN_00477784` grava a contagem e chama `FUN_0047d734` para cada elemento da lista.
- [FATO] `FUN_0047d4d4` e `FUN_0047d734` são leitor/escritor pareados: transferem os mesmos campos e larguras na mesma ordem, com um subobjeto dinâmico serializado por `FUN_00403184` em `+0x08`.
- [FATO] O registro serializado contém estes campos diretos (offset relativo ao item):

| Offset | Largura | Evidência adicional |
|---:|---:|---|
| `+0x04` | 2 bytes | Lido/escrito antes do subobjeto. |
| `+0x08` | ponteiro/subobjeto | Criado por `FUN_0048bf9c`; payload processado por `FUN_00403184`. |
| `+0x0c` | 2 bytes | Lido/escrito. |
| `+0x0e` | 2 bytes | Inicializado em 3 e alterado por rotinas pós-evento. |
| `+0x10` | 16 bytes | Bloco transferido como bytes. |
| `+0x20` | 12 bytes | Bloco transferido como bytes. |
| `+0x2c` | 20 bytes | Bloco transferido como bytes. |
| `+0x40` | 2 bytes | Zerado no construtor e lido/escrito. |
| `+0x42` | 2 bytes | Zerado no construtor e lido/escrito. |
| `+0x44` | 2 bytes | Lido/escrito. |
| `+0x46` | 2 bytes | Lido/escrito; testado em uma seleção de jogador. |
| `+0x48` | 1 byte | Zerado no construtor e lido/escrito. |
| `+0x4a` | 2 bytes | Lido/escrito; usado como índice/estado em rotinas de coleção. |
| `+0x4c` | 4 bytes | Lido/escrito. |
| `+0x50` | 2 bytes | Zerado no construtor e lido/escrito. |
| `+0x52` | 1 byte | Lido/escrito. |
| `+0x53` | 1 byte | Zerado no construtor e lido/escrito. |
| `+0x54` | 4 bytes | Acessor codifica/decodifica um valor com viés `+13`. |
| `+0x58` | 2 bytes | Acessor codifica/decodifica um valor com viés `+3`. |

- [FATO] A sequência não é uma cópia contígua de todo o objeto: há campos não serializados entre os campos listados e o subobjeto em `+0x08` tem serialização própria.
- [HIPÓTESE] Este é um wrapper persistente de membro de elenco que aponta para um objeto Player compartilhado/global. A associação é sustentada pelo carregador de coleção e pelo uso de membros em listas de equipe, mas a classe Delphi e a semântica de todos os campos permanecem desconhecidas.
- [FATO] `FUN_0047d35c` e `FUN_0047d384` escrevem/leem um short em `+0x58` com deslocamento de `+3`/`-3`. `FUN_0047d3ac` e `FUN_0047d3d0` fazem o mesmo com um inteiro em `+0x54` e deslocamento `+13`/`-13`.
- [FATO] `FUN_0047a674` percorre a lista em `side+0x0c` e agrega `FUN_0047d384(element)`. `FUN_00488308` grava o resultado de `FUN_0047d384` num registro de evento para um elemento selecionado.
- [FATO] `FUN_0047ed2c` inicializa o short `+0x0e` em `3`. `FUN_0047ef24`/`FUN_0047ef74` podem incrementar/decrementar esse short em 1 usando `FUN_00402d00(2)`, sob a condição de `FUN_004933c0(5)`; limites observados são 6 e 0.
- [FATO] A simulação tenta resolver ações para os lados do match chamando `FUN_00479ae0`; quando a rotina retorna verdadeiro, o chamador incrementa `side+0x6c` e registra o evento. `FUN_0045b824` também compara dois elementos escolhidos dos elencos para uma resolução alternativa.
- [HIPÓTESE] `+0x58` é um atributo numérico agregado para estimar força/desempenho; `+0x54` é outro atributo de faixa limitada; `+0x0e` pode representar moral/forma. Nenhum desses rótulos semânticos está provado.
- [HIPÓTESE] O campo `+0x18` testado por `FUN_00488aa0` e nas atualizações de roster pode distinguir categoria/status do elemento, mas não está confirmado como atributo Player.
- [FATO] O layout completo, nome e serialização de Player ainda não foram reconstruídos.

## Coach

- [FATO] Há recursos `TCOACHMANAGERDLG`, `TCOACHNAMEDLG`, `TCOACHOPTIONSDLG` e `TINVITECOACHDLG`.
- [FATO] Nenhum layout de objeto, campo persistente ou associação Coach-Team foi confirmado ainda.

## Match

- [FATO] O objeto usado por `FUN_00480ae4` contém referências aos dois lados em `+0x30`/`+0x34`; ele também tem um byte de estado/modo em `+0x2d` e outros valores lidos em `+0x48`, `+0x50`, `+0x58`, `+0x5c` e `+0x60`.
- [FATO] A rotina de resultado escreve resumos em coleções alcançadas a partir dos dois objetos participantes, e atualiza os contadores de resultado listados acima.
- [HIPÓTESE] O objeto é um contexto/evento de partida. Os significados de modo, data/hora e outros campos ainda não estão estabelecidos.
- [FATO] `FUN_0045a574` percorre o relógio minuto a minuto e chama os geradores em `docs/algorithms/match-simulation.md`; a geração do placar foi localizada, embora a fórmula numérica completa ainda dependa de reconstruir o fluxo x87 de `FUN_00479ae0` e seus helpers.
- [FATO] `FUN_00402d00` é usado por rotinas no setor `00479...` que avaliam valores individuais e escolhem resultados discretos. O gerador é documentado separadamente em `docs/algorithms/random.md`.

## League

- [FATO] Há formulário `TCLASSIFICATIONDLG`, callbacks de interação para `ListBoxDivision1/2/3MouseDown` e o componente `textLeagueWinnerTimes`.
- [HIPÓTESE] O registro de estatísticas associado a participantes pode servir a uma tabela de classificação de liga/divisão.
- [FATO] Não há ainda estrutura confirmada de League ou Division, nem regra de ordenação da tabela.

## Coach, Referee, Stadium e demais entidades

[FATO] `symbols.csv` e `strings.csv` fornecem nomes de formulários e componentes, mas ainda não há campos internos confirmados para Referee ou Stadium. O próximo levantamento deve manter a mesma distinção entre classe de UI, objeto de domínio e registro serializado.