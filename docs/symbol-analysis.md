# Análise de símbolos

## Fonte e estrutura

[FATO] `ghidra/symbols.csv` é um CSV com as colunas `Name`, `Location`, `Type`, `Namespace`, `Source`, `Reference Count` e `Offcut Ref Count`. A contagem abaixo considera 3.570 registros, excluindo o cabeçalho.

| Campo | Valores observados |
|---|---|
| `Source` | `Default`: 2.685; `Imported`: 512; `Analysis`: 373. |
| `Type` | `Function`: 2.308; `External Function`: 385; `Thunk Function`: 378; `Instruction Label`: 347; `Data Label`: 152. |
| `Namespace` | `Global`: 2.438; bibliotecas externas como `USER32.DLL` (295), `KERNEL32.DLL` (206), `GDI32.DLL` (159), `COMCTL32.DLL` (48), `ADVAPI32.DLL` (18), `OLEAUT32.DLL` (17), `WINSPOOL.DRV` (8), `OLE32.DLL` (4), `COMDLG32.DLL` (2) e `SHELL32.DLL` (2); diversos namespaces `switchD_...` gerados para seletores. |

## Interpretação

- [FATO] `Namespace=Global` é o namespace atribuído pelo Ghidra a grande parte dos símbolos; o CSV não o identifica como namespace Delphi.
- [FATO] Os namespaces de DLL e os símbolos `External Function` documentam dependências externas do executável. As APIs visíveis incluem funções de `KERNEL32.DLL`, `USER32.DLL`, `GDI32.DLL`, `ADVAPI32.DLL`, `OLEAUT32.DLL`, `COMCTL32.DLL`, `WINSPOOL.DRV`, `OLE32.DLL`, `COMDLG32.DLL` e `SHELL32.DLL`.
- [FATO] `switchD_...`, `case...` e demais `Instruction Label` refletem rótulos de análise/desmontagem do Ghidra, não nomes de unidades ou módulos Delphi.
- [FATO] Há 56 rótulos `Rsrc_RC_Data_T...` com `Type=Data Label`, `Namespace=Global` e `Source=Imported`, incluindo formulários como `TMAINWINDOW`, `TPREPAREGAMEDLG`, `TCLASSIFICATIONDLG`, `TPLANTELDLG` e `TPLAYERPROPERTIESDLG`. Isso relaciona símbolos aos recursos nomeados, não revela a lógica ou os campos dos formulários.
- [FATO] Os nomes `Finances`, `Plantel`, `playerProp` e `SelectLang` não aparecem como nomes de unidades/namespace no CSV. `Plantel` e `SelectLang` aparecem indiretamente em identificadores de formulário como `TPLANTELDLG` e `TSELECTLANGDLG`; não são prova de unidades Delphi com esses nomes.
- [HIPÓTESE] O grande volume de símbolos globais e gerados, sem nomes de unidades, é compatível com um export de análise de binário sem metadados completos de fonte. O CSV sozinho não permite reconstruir limites de módulos Delphi.

## Limites desta análise

[FATO] O arquivo lista nomes, endereços, tipos, namespaces e contagens de referências, mas não apresenta declarações Pascal, assinaturas de tipos de dados ou dependências entre funções. Não inferir modelos internos apenas dos nomes de símbolos.

[FATO] `ghidra/all_functions.c` foi deliberadamente deixado de lado, conforme o escopo solicitado. Esta análise cobre apenas `symbols.csv` e não inicia o mapeamento de funções.