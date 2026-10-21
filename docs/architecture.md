# Arquitetura: evidências iniciais do decompilado

## Escopo

[FATO] Esta análise parte de `ghidra/all_functions.c`, `ghidra/functions.json`, `ghidra/symbols.csv` e `ghidra/strings.csv`. `original/` foi consultada apenas para contexto de arquivos; permanece somente leitura. O escopo atual é o levantamento estrutural inicial, com prioridade para Team, Player, Coach, Match e League. Não há ainda reconstrução integral dos algoritmos ou layouts dessas entidades.

## Cobertura do export

- [FATO] `functions.json` contém 2.686 entradas, correspondentes aos 2.686 cabeçalhos `FUNCTION` de `all_functions.c`.
- [FATO] 2.307 nomes começam com `FUN_`; 375 funções têm nomes não automáticos, além de quatro nomes `thunk_FUN_...` duplicados no catálogo JSON. Os nomes automáticos não comunicam o papel da função.
- [FATO] A lista de símbolos separa `Function`, `External Function`, `Thunk Function`, `Instruction Label` e `Data Label`, mas não fornece tipos Pascal dos parâmetros ou variáveis.
- [HIPÓTESE] Uma parcela expressiva das rotinas no início do export representa wrappers de DLL e infraestrutura Delphi/VCL. Elas devem ser separadas da lógica de domínio antes de atribuir responsabilidades ao jogo.

## Estruturas genéricas observadas

### Vetor de ponteiros

- [FATO] `FUN_0040d738` lê contagem em `param_1+8` e capacidade em `param_1+12`. Se ambas forem iguais, chama um callback no endereço armazenado em `param_1`. Depois grava o ponteiro no buffer indicado por `param_1+4`, no índice `contagem * 4`, e incrementa a contagem.
- [FATO] `FUN_0040d988` percorre o mesmo buffer usando `buffer + índice * 4`, compara ponteiros e retorna `-1` quando não encontra o valor.
- [FATO] `FUN_0040db48` combina a busca com a remoção; `FUN_0040d774` decrementa a contagem e desloca os ponteiros seguintes em blocos de 4 bytes.
- [HIPÓTESE] O layout é compatível com um contêiner dinâmico de ponteiros, possivelmente uma lista de estilo Delphi `TList`. O nome/classe Delphi não está confirmado; não associar esse contêiner a Team ou Player sem evidência de call sites e alocação.

### Stream de registros fixos

- [FATO] `FUN_0040526c` abre um arquivo por `CreateFileA` ou usa handles padrão. O objeto passado mantém handle, estado/modo e tamanho de registro em campos acessados como palavras de 32 bits.
- [FATO] `FUN_00404ed8` chama `ReadFile` com `tamanho_do_registro * quantidade` e converte bytes lidos de volta em quantidade de registros.
- [FATO] `FUN_00404f3c` aplica o mesmo cálculo para `WriteFile`.
- [HIPÓTESE] Os métodos compõem uma abstração de stream de registros fixos da RTL/Delphi. Não há evidência nesses wrappers de que leiam os arquivos `.ilt`, `.ilg`, `.dat`, `.els` ou `.txe` do jogo.
- [FATO] `FUN_0046b500` grava um save por stream e serializa, entre outras coleções, duas coleções de objetos Team usando `FUN_00474bb0` com os modos `1` e `0`. `FUN_0046bb20` as reconstrói com `FUN_00474ab8` e os mesmos modos.
- [FATO] O load/save do jogo também processa várias outras coleções e objetos no mesmo stream; logo, a serialização Team observada nesses call sites integra o estado da partida/carreira, não prova o formato dos arquivos individuais `teams/*.ilt`.
- [HIPÓTESE] Os modos `1` e `0` diferenciam duas categorias de equipes no save; seus nomes e regras não foram recuperados.

### Roster e RNG

- [FATO] Várias rotinas recebem um objeto com uma lista acessível por `participant+0x0c`; a lista usa o vetor de ponteiros descrito acima. `FUN_0047a674` percorre os elementos e agrega o resultado de `FUN_0047d384`.
- [HIPÓTESE] O objeto é um lado/equipe e a lista representa seu elenco; os elementos são compatíveis com registros de jogadores, mas o tipo Delphi ainda não foi identificado.
- [FATO] `FUN_00402a84` inicializa `DAT_0049803c` a partir de `GetSystemTime`, em milissegundos desde a meia-noite UTC.
- [FATO] `FUN_00402d00(limit)` atualiza o estado por `state = state * 0x08088405 + 1` em aritmética de 32 bits e retorna os 32 bits altos de `limit * state`.
- [FATO] `FUN_00402d18` também atualiza o mesmo estado e passa o valor a uma rotina x87 `fscale`; a transformação completa do caminho de ponto flutuante ainda não foi reconstruída.
- [FATO] O gerador é global e seu estado é inicializado com relógio, portanto duas execuções não são reproduzíveis apenas com a mesma lista de entrada, salvo se o estado inicial for controlado.

## Evidência de interface relacionada às entidades

- [FATO] `FUN_00488aa0` percorre duas coleções por índice e testa um campo em `item+0x18` contra os valores `1` e `2`; em seguida insere os ponteiros encontrados em listas e cria nós com o texto literal `player`.
- [FATO] A função usa o vetor genérico acima e envia operações a objetos por despacho virtual. O nome literal e o contexto indicam uma apresentação em interface, não uma definição serializada do jogador.
- [HIPÓTESE] O campo `item+0x18` funciona como discriminante de categoria nessa rotina específica. Seu significado semântico e sua relação com tipos de jogador ainda não foram estabelecidos.
- [FATO] `FUN_00480ae4` trata um objeto com referências em `+0x30` e `+0x34`. Lê o placar de cada objeto referenciado em `+0x6c`, compara a diferença, e incrementa contadores nos dois objetos. Ao final, soma cada placar a acumuladores distintos em `+0x28` e `+0x2c`.
- [FATO] Para placares diferentes, o lado vencedor recebe incremento de 3 em `+0x30`, e os lados recebem incrementos assimétricos em `+0x1c`/`+0x24`. Para empate, incrementa `+0x20` nos dois lados e `+0x30` em 1 para cada.
- [FATO] `FUN_00469ac4` aplica `FUN_00480ae4` aos itens de uma coleção global e os remove. `FUN_00475838` chama `FUN_00482d5c`; esta última retorna verdadeiro quando os dois objetos referenciados existem e seus valores `+0x6c` são iguais. Nesse caso, `FUN_00475838` marca `+0x58` e adia a finalização.
- [HIPÓTESE] `FUN_00480ae4` é uma rotina de finalização/registro de resultado, provavelmente atualizando classificação. O tratamento separado de empates pode representar partida que precisa de etapa adicional; ainda não está provado que seja prorrogação ou disputa de pênaltis.
- [HIPÓTESE] Os offsets `+0x18`, `+0x1c`, `+0x20`, `+0x24`, `+0x28`, `+0x2c` e `+0x30` se comportam como jogos, vitórias, empates, derrotas, gols a favor, gols contra e pontos, respectivamente. A identificação nominal depende de confirmação independente.
- [HIPÓTESE] Os objetos referenciados em `+0x30` e `+0x34` representam os lados/equipes participantes, mas ainda pode haver uma estrutura intermediária de classificação.
- [FATO] `FUN_004650e8` contém atribuições de propriedades visuais e caption `Teams`; a função não comprova um registro `Team`.
- [FATO] `strings.csv` contém nomes de formulários e componentes relacionados a jogadores, equipes, treinadores, classificação, partidas e estádio. As strings não expõem, por si só, campos ou relacionamentos dos modelos.

## O que ainda não foi reconstruído

| Prioridade | Estado atual |
|---|---|
| Team | [FATO] Há formulários/strings de interface, uma lista em `participant+0x0c` percorrida em agregado e contadores atualizados após resultado. [HIPÓTESE] A lista é o elenco e os offsets do grupo acima são estatísticas de classificação; o layout completo do Team não está confirmado. |
| Player | [FATO] Há nós de interface chamados `player`, campos numéricos codificados em `+0x54`/`+0x58` e uma rotina que modifica `+0x0e` nos elementos da lista. [HIPÓTESE] Esses elementos são jogadores; o significado dos atributos não está confirmado. |
| Coach | [FATO] Há formulários de gestão/opções/nome de treinador; nenhum layout de registro confirmado. |
| Match | [FATO] Contexto de partida com dois lados, relógio e fila de eventos; foram mapeados geração de placar e finalização. [HIPÓTESE] Significados completos dos eventos e fórmula de probabilidade ainda abertos. |
| League | [FATO] Há formulário de classificação e registros candidatos de tabela; nenhuma estrutura League/Division completa confirmada. |

## Próximos passos de análise

1. Correlacionar funções que leem/escrevem os objetos das entidades com call sites de abertura/seleção/salvamento de equipes e jogadores.
2. Agrupar rotinas por referências a recursos, strings, globais e offsets de objeto; registrar endereços e exemplos de uso antes de nomear campos.
3. Analisar estruturas de listas/coleções e objetos específicos separadamente da RTL/VCL.
4. Só então atualizar `docs/data-model.md` com campos confirmados e hipóteses explicitamente marcadas.

## Limitação do decompilado

[FATO] `all_functions.c` usa nomes `FUN_...`, tipos genéricos como `undefined4`, chamadas virtuais e rótulos `DAT_...`/`PTR_...`. Os tipos inferidos pelo Ghidra podem estar incompletos ou incorretos; assinaturas e semântica devem ser trianguladas com disassembly, referências cruzadas, strings e recursos antes de serem tratadas como fatos.