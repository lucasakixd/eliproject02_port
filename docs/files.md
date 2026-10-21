# Inventario de arquivos originais

## Escopo e método

[FATO] `original/` foi percorrida recursivamente em modo somente leitura. O inventário contém 584 arquivos, totalizando 5.910.054 bytes. Os tamanhos abaixo são tamanhos em disco observados; finalidade e relações não provadas pelo conteúdo estão marcadas como `[HIPÓTESE]`.

Não foram encontrados arquivos com extensões `.sav`, `.cfg` ou `.ini` nesta cópia. Extensão, nome e diretório não bastam para determinar o formato interno dos arquivos proprietários.

## Resumo por extensão

| Extensão | Quantidade | Bytes totais | Faixa por arquivo | Observação |
|---|---:|---:|---:|---|
| `.exe` | 3 | 5.225.524 | 72.748-2.856.964 | [FATO] Os três executáveis têm cabeçalhos MZ/PE e Machine `0x014C` (Intel 386, PE32). |
| `.bmp`/`.BMP` | 227 | 163.714 | 526-1.534 | [FATO] 219 em `flags/` e 8 em `icons/`. Uma amostra de `flags/BRA.BMP` começa com `4D BA`, não com `42 4D` (`BM`); o formato BMP padrão não foi confirmado. |
| `.dat` | 3 | 42.225 | 2.340-37.545 | [FATO] Conteúdo binário; formato interno não identificado. |
| `.els` | 8 | 128.228 | 9.162-24.372 | [FATO] Arquivos binários organizados por idioma; formato interno não identificado. |
| `.ilg` | 1 | 130.423 | 130.423 | [FATO] Conteúdo binário; formato interno não identificado. |
| `.ilt` | 338 | 215.314 | 465-753 | [FATO] Arquivos binários com nomes de clubes; formato interno não identificado. |
| `.txe`/`.TXE` | 3 | 3.570 | 41-3.449 | [FATO] Conteúdo binário; formato interno não identificado. |
| `.htm` | 1 | 1.056 | 1.056 | [FATO] HTML legível. |

## Arquivos na raiz

| Caminho | Bytes | Evidência e finalidade |
|---|---:|---|
| `Elifoot2002.exe` | 2.856.964 | [FATO] Executável PE32. [HIPÓTESE] Executável principal pelo nome. |
| `Elifoot2002Editor.exe` | 2.295.812 | [FATO] Executável PE32. [HIPÓTESE] Editor associado ao jogo pelo nome. |
| `unins000.exe` | 72.748 | [FATO] Executável PE32, ao lado de `unins000.dat`. [HIPÓTESE] Utilitário de desinstalação. |
| `unins000.dat` | 37.545 | [FATO] Arquivo binário. [HIPÓTESE] Dados auxiliares do desinstalador pelo nome e co-localização. |
| `Leia-me.htm` | 1.056 | [FATO] HTML com texto promocional do site Planeta Netgames e copyright de 2004; não descreve formatos do jogo. |
| `REFEREE.TXE` | 3.449 | [FATO] Arquivo binário na raiz. [HIPÓTESE] Relacionado a árbitros pelo nome; conteúdo não decodificado. |

## Diretórios de dados e recursos

| Caminho/padrão | Inventário e tamanhos | Finalidade/relacionamentos |
|---|---|---|
| `teams/*.ilt` | [FATO] 338 arquivos, 215.314 bytes no total, 465-753 bytes cada. Exemplos: `Arsenal.ilt` (676), `Ajax.ilt` (677), `Barcelona.ilt` (665). | [HIPÓTESE] Dados de equipes: os nomes/diretório e o objeto Team serializado no decompilado são compatíveis, mas ainda não foi localizado o call site que associa diretamente a extensão `.ilt` a esse leitor. O layout dos registros foi parcialmente mapeado em `docs/data-model.md`. |
| `Games/aaa.ilg` | [FATO] 130.423 bytes, binário. | [HIPÓTESE] Estado, partida ou dados de jogo pelo diretório/extensão; não confirmado. |
| `Games/elif2002.dat` | [FATO] 2.340 bytes. SHA-256 `63E3163824ECD1CE091E2ABF7FBC4CC150B7D2FA037ACAE849F0F4C53102429C`. | [FATO] Idêntico byte a byte a `Provisory Teams/elif2002.dat`. [HIPÓTESE] Arquivo de dados compartilhado/copiado entre esses contextos; conteúdo não decodificado. |
| `Provisory Teams/elif2002.dat` | [FATO] 2.340 bytes; mesmo SHA-256 de `Games/elif2002.dat`. | [HIPÓTESE] Dados usados por equipes provisórias, inferido somente pelo caminho. |
| `flags/*` | [FATO] 219 arquivos `.bmp`/`.BMP`, total 155.474 bytes; 217 têm 710 bytes e 2 têm 702 bytes. | [HIPÓTESE] Imagens de bandeiras identificadas pelos nomes curtos. A amostra `BRA.BMP` não tem assinatura BMP Windows padrão no primeiro par de bytes; precisa de validação do formato próprio. |
| `icons/happy*.bmp` | [FATO] 8 arquivos: `happy1.bmp` 1.526; `happy1_small.bmp` 526; `happy2.bmp` 1.530; `happy2_small.bmp` 530; `happy3.bmp` 1.534; `happy3_small.bmp` 534; `happy4.bmp` 1.530; `happy4_small.bmp` 530 bytes. | [HIPÓTESE] Quatro imagens em variantes grandes/pequenas; o nome sugere ícones de humor, mas o uso não foi confirmado. |
| `ctrgroup/Bosman.txe`, `ctrgroup/Plop.txe` | [FATO] 80 e 41 bytes. | [HIPÓTESE] Dados relacionados ao grupo/categoria `ctrgroup`; nomes não permitem determinar o papel. |
| `int/{BR,EN,ES,PT}/ELIF2002_01_*.els` | [FATO] 4 arquivos: BR 22.924; EN 20.886; ES 24.372; PT 23.182 bytes. | [HIPÓTESE] Recursos de idioma por sufixo e diretório. |
| `int/{BR,EN,ES,PT}/ELIF2002_02_*.els` | [FATO] 4 arquivos: BR 9.190; EN 9.254; ES 9.162; PT 9.258 bytes. | [HIPÓTESE] Segundo conjunto de recursos de idioma por sufixo; divisão funcional não identificada. |

## Formatos e lacunas

- [FATO] Os executáveis são PE32 para Intel 386 (`MZ`, assinatura `PE`, Machine `0x014C`). Isso identifica o contêiner e a arquitetura, não os algoritmos ou formatos dos dados do jogo.
- [FATO] Amostras de `.dat`, `.ilg`, `.ilt`, `.txe` e `.els` são binárias e não exibem, nos bytes inspecionados, um cabeçalho textual identificável. Nenhuma delas foi modificada.
- [HIPÓTESE] `teams/*.ilt`, `Games/*` e os arquivos sob `int/` representam, respectivamente, dados de clubes, dados da carreira/jogo e recursos localizados. Validar essas relações requer análise de parsers/recursos, fora deste inventário.
- [FATO] A igualdade de SHA-256 confirma que os dois arquivos `elif2002.dat` são idênticos; não confirma por si só como o jogo os interpreta.