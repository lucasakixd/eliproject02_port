# Formulários, menus e componentes

## Fontes e critério

[FATO] `ghidra/strings.csv` existe e é legível. O cabeçalho apresenta quatro colunas: `Location`, `String Value`, `String Representation` e `Data Type`. Os nomes abaixo são valores observados no export; a associação de propósito é hipótese baseada nos nomes, não em execução ou análise de funções.

[FATO] Foram localizados 56 nomes de classes de formulário e 56 rótulos `Rsrc_RC_Data_T...` correspondentes em `ghidra/symbols.csv`. Esses rótulos indicam dados de recursos importados pelo Ghidra; não provam que cada formulário seja exibido no fluxo normal do jogo.

## Formulários identificados

| Classe observada | Interpretação pelo nome |
|---|---|
| `TMAINWINDOW` | [HIPÓTESE] Janela principal. |
| `TEDITORMAIN`, `TEDITOR_MAIN` | [HIPÓTESE] Janelas principais do editor. |
| `TABOUT`, `TABOUTDLG` | [HIPÓTESE] Sobre. |
| `TADDINSDLG`, `TANALYSISDLG`, `TASKMORESALARYDLG`, `TASSIGNNACDLG`, `TBALANCEDLG` | [HIPÓTESE] Complementos, análise, salário, atribuição, balanço; o significado de `NAC` não foi determinado. |
| `TCANTSAVETEAMDLG`, `TCHECKPLAYERDLG`, `TCLASSIFICATIONDLG`, `TCLOCKDLG` | [HIPÓTESE] Aviso de salvamento, verificação de jogador, classificação e relógio. |
| `TCOACHMANAGERDLG`, `TCOACHNAMEDLG`, `TCOACHOPTIONSDLG`, `TINVITECOACHDLG` | [HIPÓTESE] Gestão, nome, opções e convite de treinadores. |
| `TCODEDLG`, `TCURRENCYDLG`, `TREGINFODLG` | [HIPÓTESE] Código, moeda e informações de registro. |
| `TEDITPLAYERDLG`, `TPLAYERPROPERTIESDLG`, `TOBSERVEDPLAYERSDLG` | [HIPÓTESE] Edição, propriedades e observação de jogadores. |
| `TPREPAREGAMEDLG` | [HIPÓTESE] Preparação de uma partida/jogo, inferido pelo nome. |
| `TENDOFSEASONDLG`, `TFORCEDSUBSTITUTIONDLG`, `TJOURNEYDLG`, `TPENALTIESDLG`, `TPENALTYDLG`, `TSORTEIODLG`, `TSUBSTITUTIONDLG` | [HIPÓTESE] Fim de temporada, substituição, jornada, pênaltis, sorteio e fluxo de jogo. |
| `TGETTEAMSDLG`, `TOPENTEAMDLG`, `TSAVETEAMDLG`, `TSELECTCOUNTRIESDLG`, `TSELECTGAMEDLG`, `TSETCOUNTRYDLG`, `TSETTEAMNAMEDLG` | [HIPÓTESE] Seleção, abertura, gravação ou configuração de equipes, países e jogos. |
| `TINLINEINPUTDLG`, `TINPUTDLG`, `TOPTIONSDLG`, `TPROGRESSDLG`, `TPRINTLISTDLG`, `TWAITDLG` | [HIPÓTESE] Entrada, opções, progresso, impressão e espera. |
| `TLASTTRANSFERSDLG`, `TLOANDLG`, `TSELLPLAYERDLG`, `TTRANSFERPLAYERDLG` | [HIPÓTESE] Transferências, empréstimo e venda de jogadores. |
| `TPLANTELDLG`, `TSTADIUMDLG`, `TTEAMCOLORDLG`, `TTEAMPROPERTIESDLG`, `TTEAMSKILLDLG` | [HIPÓTESE] Elenco, estádio, cores, propriedades e nível de equipe. |
| `TREFEREEAIDDLG`, `TSELECTLANGDLG` | [HIPÓTESE] Opções relacionadas ao árbitro e seleção de idioma. |

O export também contém `TPlantelDlg` em forma com capitalização diferente e terminador de controle, além dos nomes Unicode em maiúsculas. Trate-os como ocorrências do export, não como classes distintas sem confirmação adicional.

## Menus e textos

- [FATO] Foram observadas strings genéricas de diálogo como `&Yes`, `&No`, `OK`, `Cancel` e `&Help`, além de `Elifoot 2002` em três endereços. A presença dessas strings não mapeia, por si só, menus específicos do jogo.
- [FATO] O export contém `&Help`, mas não fornece uma lista completa de captions dos menus principais. Assim, nomes e hierarquia dos menus permanecem desconhecidos.
- [FATO] Há metadados de classes/propriedades da biblioteca visual, incluindo `TMainMenu`, `TPopupMenu`, `TApplication`, `TBitmap`, `TRadioButton` e `TListBoxStrings`.
- [HIPÓTESE] Esses nomes pertencem ao runtime/metadata do Delphi VCL e não identificam componentes concretos de um formulário do jogo. Não há evidência suficiente neste CSV para associar controles individuais a cada tela.
- [FATO] `symbols.csv` lista recursos de formulário como rótulos `Rsrc_RC_Data_TMAINWINDOW_0` e `Rsrc_RC_Data_TPREPAREGAMEDLG_0`; o conteúdo binário dos recursos não foi decodificado nesta tarefa.

## Limitações

[FATO] O export permite identificar nomes de classes e alguns textos genéricos, mas não expõe uma árvore completa de componentes, captions contextualizadas nem relações de navegação. Para isso será necessário decodificar os recursos de formulário ou consultar outra fonte autorizada. `ghidra/all_functions.c` não foi analisado.