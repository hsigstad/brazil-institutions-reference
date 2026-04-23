# Dívida ativa e cobrança pré-judicial

O que acontece com o crédito tributário depois de definitivamente
constituído no contencioso administrativo — e **antes** de virar
execução fiscal judicial. Foco: inscrição em dívida ativa, Certidão de
Dívida Ativa (CDA), estrutura das procuradorias (PGFN/PGE/PGM),
cobrança extrajudicial (notificação, CADIN, protesto, averbação
pré-executória), e transação tributária.

Para a fase administrativa (PAF, DRJ, CARF), ver
`processo-administrativo-fiscal.md`. Para a execução judicial, ver
`execucao-fiscal.md`. Para a parte geral do direito tributário, ver
`direito-tributario.md`.

**Topics / keywords**: dívida ativa, inscrição em dívida ativa, CDA,
PGFN, PGE, PGM, CADIN, protesto de CDA, averbação pré-executória,
transação tributária, cobrança extrajudicial, certidão negativa, CND,
CPEN, tax debt registry, tax collection, extrajudicial tax enforcement.

**Snapshot as of 2026**: o rol de instrumentos pré-judiciais cresceu
bastante desde 2012 — protesto da CDA (`L12767/2012`, confirmado
constitucional pela STF ADI 5135 em 2016); averbação pré-executória
(`L13606`, parcialmente admitida pelo STF em 2020 nas ADIs 6.040 e
6.055, com ADI 7053 pendente); transação tributária (`LTT`, 2020 em
diante). A tendência estrutural é que a inscrição em dívida ativa
esteja gradualmente se tornando menos um *precedente* da EF e mais uma
alternativa a ela.

---

## 1. Inscrição em dívida ativa

### O ato e o efeito

**Inscrição em dívida ativa** é o ato administrativo da procuradoria
que atesta que o crédito é líquido e certo, e viabiliza sua cobrança
como título executivo extrajudicial. Regulada por `CTN.201`–`CTN.204`
e `LEF.2`–`LEF.3`.

Três efeitos imediatos da inscrição:

1. **Cria o título executivo** — a CDA (Certidão de Dívida Ativa) tem
   **presunção de liquidez e certeza** (`CTN.204`, `LEF.3`), ônus da
   prova invertido contra o devedor.
2. **Marca o início da presunção de fraude** — alienações posteriores
   presumem-se fraudulentas (`CTN.185`, após `LC118`). Antes de 2005
   o marco era a citação válida em EF; a antecipação é um dos
   principais endurecimentos da cobrança fiscal no século XXI.
3. **Cadastra o devedor no CADIN** (federal), com efeitos de
   restrição de acesso a crédito público e certificação.

### Quem pode inscrever

Inscrição é monopólio das procuradorias:

- **União** (tributária) — **PGFN** (Procuradoria-Geral da Fazenda
  Nacional), órgão da AGU por `LOAGU.12`.
- **União** (não-tributária) — PGF (Procuradoria-Geral Federal) para
  autarquias e fundações, também da AGU.
- **Estados** — **PGE** (Procuradoria-Geral do Estado), regulada por
  lei estadual.
- **Municípios** — **PGM** (Procuradoria-Geral do Município).

Esta estrutura importa para selecionar fontes de dados: cada
procuradoria publica separadamente seu estoque e fluxo de dívida
ativa. A PGFN publica dados consolidados anuais (Relatório PGFN em
Números); muitas PGEs publicam dados em portais próprios, com
qualidade variável.

### Dívida ativa tributária vs não-tributária

`LEF.2` abrange ambas:
- **Tributária**: impostos, taxas, contribuições, multas tributárias.
- **Não-tributária**: multas administrativas (Anvisa, Ibama, Anatel),
  ressarcimento ao erário por improbidade, FGTS não recolhido,
  contribuições sindicais, custas judiciais.

A distinção importa para competência e regime processual (não-tributária
não se beneficia das regras específicas do `CTN`, e.g., a presunção de
fraude do `CTN.185` pode ser lida mais restritivamente).

---

## 2. CDA — Certidão de Dívida Ativa

A CDA (`LEF.2.§5`, `CTN.202`) é um **título executivo extrajudicial**
com conteúdo mínimo legal: valor original, juros, multa, fundamento
legal, termo inicial, número do processo administrativo de origem,
identificação do devedor.

### Presunção de liquidez e certeza

`CTN.204` / `LEF.3`: a CDA goza de presunção *relativa* de liquidez e
certeza. O devedor pode desconstituir, mas precisa de **prova
inequívoca** — inverte o ônus comum de quem executa (que tem de
comprovar seu crédito).

Vícios formais da CDA (falta de fundamento legal, ausência de dados
essenciais) podem levar à **nulidade** em sede de embargos ou exceção
de pré-executividade. A jurisprudência do STJ é consistente em não
admitir "substituição" de CDA para sanar vícios materiais (Súmula 392
STJ: admite-se substituição até a prolação de sentença, para correção
de erro material ou formal, vedada modificação do sujeito passivo da
execução).

### Ciclo de vida da CDA

- **Inscrita** mas não ajuizada: base para cobrança extrajudicial
  (notificação, protesto, CADIN). Fica no estoque de dívida ativa.
- **Ajuizada**: distribuída ao juízo competente (ver `execucao-fiscal.md`).
- **Extinta**: por pagamento, prescrição, transação, remissão, ou
  decisão judicial que anule o crédito.

---

## 3. CADIN — Cadastro Informativo de Créditos Federais (`L10522`)

Registro público de pessoas físicas e jurídicas com créditos não
quitados com órgãos federais. Principal efeito: **veda concessão de
crédito público** (`L10522.6`), **subvenções, incentivos fiscais** e
contratação com órgãos federais.

Relevante para pesquisa:
- É um dos canais pelos quais inadimplência tributária afeta
  comportamento econômico do devedor (empresas negativadas perdem
  acesso a linhas públicas).
- Permite ligação entre execução fiscal e restrição de crédito — uma
  variável de cost observável para análise de resposta à cobrança.

CADIN existe só para débitos **federais**. Estados e municípios mantêm
cadastros próprios (p. ex. CADIN estadual em SP, RJ).

---

## 4. Protesto da CDA

Introduzido por `L12767/2012` (alterou Lei 9.492/97). Permite que a
Fazenda leve a CDA a protesto em cartório, como qualquer título de
crédito, **sem ajuizar** execução fiscal.

**ADI 5135** (STF, 2016) — julgou o protesto de CDA **constitucional**
por maioria, rejeitando a tese de que protesto de crédito público
violaria devido processo legal. Argumento central: protesto é cobrança
extrajudicial legítima, não execução; preserva ampla defesa em sede
posterior.

Efeito operacional:
- Negativação do devedor em registros de crédito (Serasa, SPC, bureaus).
- Pressão reputacional sem os custos de EF judicial.
- **Dispensa o ajuizamento de EF** para créditos abaixo do limite
  (`L10522.20` e atos PGFN — ver abaixo). Para créditos médios
  (abaixo do limite de ajuizamento, acima do limite de dispensa total),
  o protesto é a ferramenta primária.

Virou **o instrumento principal** da PGFN para créditos "de baixo para
médio valor" — reduziu o volume ajuizado a partir de 2013–2014.

---

## 5. Averbação pré-executória (`L13606`, inserindo `L10522.20-B`–`L10522.20-E`)

Introduzida em 2018 pelo `L13606`. Permite que a PGFN, depois de
notificar o devedor e dar 5 dias para pagamento, **averbe a dívida
em registros de bens** (imóveis, veículos), tornando-os **inalienáveis**
**sem decisão judicial prévia**.

Crítica: sem contraditório prévio nem ordem judicial, a averbação
funciona como penhora administrativa.

**ADIs 6.040 e 6.055** (STF, 2020): reconheceram **constitucionalidade
parcial** do instituto, impondo salvaguardas — a averbação não pode
equivaler a indisponibilidade integral; só gera efeito de presunção
de fraude (análogo ao `CTN.185`) em relação a terceiros adquirentes.
**ADI 7053** sobre os atos normativos da PGFN que regulamentam a
averbação segue pendente em partes.

Efeito prático de curto prazo: a averbação é usada seletivamente, mais
como sinalização ao devedor e a terceiros do que como execução
administrativa plena. Cadastros cartorários (SERP, Sisbajud, Serasa)
recebem a averbação mesmo com os limites impostos pelo STF.

---

## 6. Transação tributária (`LTT`)

Principal inovação estrutural na cobrança da dívida ativa federal nos
anos 2020. Regulamenta `CTN.171` (transação como modalidade de extinção
do crédito), que existia no CTN desde 1966 mas nunca havia sido
efetivamente implementada.

Duas modalidades:

- **Transação por adesão a edital** (`LTT.2`) — a PGFN publica edital
  com termos (desconto, prazo, garantias) aplicáveis a uma classe de
  créditos (geralmente definidos por faixa de valor, situação
  econômica do devedor, matéria). Contribuinte adere no prazo.
- **Transação individual** (`LTT.2`) — para créditos de grande valor
  ou situações específicas, negociada caso a caso. Dependeu
  historicamente de limite de valor (`LTT.11`) ajustado por atos da
  PGFN.

Benefícios típicos: descontos de até 65% sobre multas e juros (nunca
sobre o tributo principal), prazos de até 120 meses, flexibilização
de garantias. Em contrapartida o contribuinte desiste de discussões
administrativas e judiciais e reconhece o débito.

Impacto no estoque de dívida ativa: a PGFN utiliza transações por
adesão como instrumento ativo de gestão — editais periódicos
liquidam grandes porções do estoque. Dados PGFN em Números mostram
que desde 2020 a transação é responsável pela saída de parte
significativa dos créditos, rivalizando com pagamento direto e
extinção por prescrição.

Transação de contencioso de relevante controvérsia (`LTT.14`) atinge
litígios judiciais e administrativos de temas repetitivos — é o
canal pelo qual a Fazenda resolve teses-PGFN quando derrota judicial
aparentemente inevitável torna desejável capitalizar com recuperação
parcial.

Para detalhe sobre o voto de qualidade no CARF (também alterado pelo
`LTT.28` e depois pela Lei 14.689/2023), ver
`processo-administrativo-fiscal.md`.

---

## 7. Dispensa de ajuizamento por valor

`L10522.20` autoriza o Ministro da Fazenda a dispensar o ajuizamento
de execuções fiscais federais **abaixo de um limite** (R$ 10 mil no
texto original; ajustado posteriormente por portaria — atualmente
R$ 20 mil na esfera federal).

Créditos abaixo do limite:
- Continuam inscritos em dívida ativa.
- Permanecem passíveis de cobrança extrajudicial (notificação, CADIN,
  protesto).
- Não geram execução fiscal judicial.

Implicação amostral: universos de execuções fiscais federais têm
**censura de valor mínimo** — a distribuição de valores ajuizados é
truncada à esquerda pelo limite vigente. Projetos que comparam
distribuições de valor ao longo do tempo precisam rastrear alterações
no limite.

Estados e municípios têm políticas análogas, com limites muito
variáveis (alguns municípios ajuízam débitos de qualquer valor;
outros têm limites de dispensa altos).

---

## 8. Certidões (CTN.205–206)

Prova documental da situação do devedor perante a Fazenda:

- **CND** — Certidão Negativa de Débitos: emitida quando não há
  débitos registrados.
- **CPEN / Positiva com Efeitos de Negativa** (`CTN.206`): emitida
  quando há débito, mas ele está **suspenso** (`CTN.151` — parcelamento,
  depósito, liminar, impugnação administrativa) ou **com penhora
  garantindo** a execução. Equivale à CND para efeitos de contratação,
  crédito, licitação.
- **CP** — Certidão Positiva: indica débitos em aberto.

Certidões são instrumento de pressão: débito não garantido impede
contratar com o Poder Público (`L8666.29` e `L14133.68`), obter
financiamento público, participar de leilões de bens.

---

## 9. Parcelamentos — breve histórico

Além da transação (`LTT`), a Fazenda oferece **parcelamentos ordinários**
(`L10522.10`–`L10522.14`) e **parcelamentos especiais** (Refis),
periodicamente instituídos por lei:

- **Refis original** — Lei 9.964/2000.
- **PAES** — Lei 10.684/2003.
- **PAEX** — MP 303/2006.
- **Refis da Crise** — Lei 11.941/2009.
- **PERT** — Lei 13.496/2017.
- **Programas pós-Covid e pós-2020** — várias leis federais e
  programas PGFN específicos.

Cada Refis cria uma discontinuidade: grandes volumes de débitos
migram do estoque ativo (em cobrança/EF) para o estoque parcelado
(suspenso). **Ao usar o estoque de EFs como variável, cada Refis é
uma fonte de ruído** — processos "desaparecem" do ativo sem extinção,
e podem retornar se o parcelamento for descumprido.

Combinados com a `LTT` (vigor desde 2020), os parcelamentos
especiais tendem a perder relevância — a transação torna-se o canal
estrutural de resolução em massa.

---

## 10. Regras de triagem da PGFN — que crédito recebe qual tratamento

As ferramentas descritas acima (protesto, averbação, transação,
parcelamento, dispensa por valor, ajuizamento de EF) não se aplicam
uniformemente a todos os créditos. A PGFN opera uma **matriz de
triagem** baseada em portarias que classifica cada inscrição por
perfil de recuperabilidade e direciona o tratamento adequado. Para
pesquisa empírica, **o arranjo destas regras é o que define quais
créditos chegam a virar EF** — entender a triagem é pré-requisito
para interpretar qualquer universo de execução fiscal federal.

### Regime Diferenciado de Cobrança de Créditos (RDCC)

Instituído pela **Portaria PGFN nº 396/2016** (posteriormente
integrado em `L13606/2018` e em atos subsequentes). O RDCC é o
arcabouço pelo qual a PGFN organiza diferenciadamente a cobrança
conforme o perfil do devedor e do crédito.

Três procedimentos estruturantes:

- **PEDP** — Procedimento Especial de Diligenciamento Patrimonial:
  investigação patrimonial prévia ao ajuizamento, para localizar
  bens passíveis de constrição. Desde 2018, é quase pré-requisito
  do ajuizamento (ver "ajuizamento parametrizado" abaixo).
- **PECDA** — Procedimento Especial de Protesto Extrajudicial da
  CDA: encaminhamento para cartório de protesto sem ajuizamento de
  EF.
- **PEAN** — Procedimento Especial de Acompanhamento de Negociações:
  gestão de parcelamentos/transações em curso.

### Rating de recuperabilidade (A / B / C / D)

Regulamentado originalmente pela **Portaria PGFN nº 293/2017** (e
portarias subsequentes), aplicado operacionalmente sobre toda a DAU.
A classificação é bidimensional:

- **V-Dev** (do devedor): capacidade de pagamento, endividamento
  total, histórico de adimplemento.
- **V-Deb** (do débito): garantias oferecidas, parcelamentos ativos,
  liquidez.

Combinação produz quatro classes:

| Rating | Descrição | Share do estoque 2024 |
|---|---|---|
| **A** | Alta perspectiva de recuperação | 8,3% (R$ 255,7 bi) |
| **B** | Média perspectiva de recuperação | 32% (R$ 979,3 bi) |
| **C** | Baixa perspectiva de recuperação | 15% (R$ 456,5 bi) |
| **D** | Créditos considerados irrecuperáveis | 44% (R$ 1,3 tri) |

**Implicação da matriz**: os instrumentos diferem por classe.
Créditos C e D são os alvos preferenciais de transação com
descontos substanciais (a `LTT` permite descontos de até 65% sobre
multa/juros para créditos classificados como de difícil ou
irrecuperável). Créditos A e B concentram ajuizamento ativo,
protesto, e investigação patrimonial para constrição. A classificação
é revisada periodicamente, e reclassificações movem o crédito entre
trilhas de tratamento.

### Ajuizamento parametrizado (Portaria PGFN nº 33/2018)

Portaria estrutural do novo fluxo pós-2018. Entrou em vigor em
01/10/2018. Regulamenta `L10522.20-B` (notificação com 5 dias) e o protesto da
CDA (Art. 20-C da Lei 10.522, inserido pela `L13606`) e articula o encadeamento: inscrição em DAU →
notificação com 5 dias para pagamento → PEDP → protesto/averbação
(se couber) → ajuizamento (se localizados bens passíveis de
constrição).

Princípio central: **só se ajuíza EF quando a diligência
administrativa prévia (PEDP) identificou ativos com potencial de
satisfazer a dívida**. É o fim oficial do ajuizamento indiscriminado.
Impacto quantitativo documentado (ver `execucao-fiscal.md` §8 e o
brief `fisc/docs/briefs/exfis-state-of-play.md` §7): ajuizamentos da
PGFN caíram de 382 mil (2016) para 33,8 mil (2020), queda de ~91% em
quatro anos.

Outro instrumento criado pela Portaria 33/2018: **revisão de dívida
inscrita** — contribuinte pode requerer revisão da CDA em até 30 dias
da notificação; o pedido suspende as medidas restritivas enquanto
tramita. Canal de contestação pré-judicial que reduz o volume
eventualmente ajuizado.

### Limites de valor (Portaria MF nº 75/2012 e sucessoras)

- **R$ 1.000**: limite abaixo do qual o crédito **não é sequer
  inscrito em DAU** (permanece no estoque da RFB).
- **R$ 20.000** (atualmente vigente): limite abaixo do qual a PGFN
  **não ajuíza EF**. Acima do limite, ajuizamento é a regra (sujeita
  à triagem por rating e à existência de ativos localizáveis).
  Portaria MF nº 75/2012 elevou o limite de R$ 10k (vigente desde
  Portaria MF nº 49/2004) para R$ 20k. Atos posteriores flexibilizam
  (ex.: Portaria MF/PGFN nº 51/2024 e atualizações).
- **Exceção**: a PGFN pode ajuizar créditos abaixo do limite em
  casos de alto potencial de recuperabilidade (rating A) ou por
  razões estratégicas (tese repetitiva, devedor estratégico).

**Implicação amostral**: universos de EF federal têm **truncamento à
esquerda pelo limite vigente no ano de ajuizamento**. Séries
temporais que cruzam mudanças de portaria precisam rastrear o limite
— a composição por valor muda quando o limite muda, mesmo sem
alteração no comportamento do fisco.

### Transação — modalidades e portarias

Regulamentação da `LTT` (Lei 13.988/2020) via múltiplas portarias
PGFN/MF:

- **Transação por adesão**: editais específicos por classe de
  crédito. Exemplos: editais de contencioso de relevante controvérsia
  (créditos em discussão administrativa/judicial com tese
  controvertida — `LTT.14`), editais de pequeno valor, editais
  setoriais (Saúde, MEI, etc.).
- **Transação individual**: para grandes devedores. Originalmente
  limitada a créditos acima de R$ 15 milhões; flexibilizada
  posteriormente.
- **Transação individual simplificada**: créditos entre R$ 1 milhão
  e R$ 10 milhões, procedimento mais leve.
- **PTI — Programa de Transação Integral** (Portaria Normativa MF
  nº 1.383/2024, com flexibilização pela Portaria PGFN nº
  2.044/2025): transação em casos de alto impacto econômico em
  discussão no Judiciário, cobrindo 17 teses específicas de
  controvérsia jurídica. Destina-se a grandes contribuintes com
  passivos judiciais relevantes.

Descontos padrão: até **65% sobre multa e juros** (o principal
nunca é descontado); prazos de até **120 meses**. Descontos maiores
e prazos mais longos exigem classificação C ou D do crédito.

### Como a matriz se combina

Um crédito típico, após inscrição em DAU, passa por este fluxo de
triagem:

```
Inscrição em DAU
  │
  ▼
Classificação por rating (A/B/C/D)
  │
  ├─► Rating A/B: prioridade para ajuizamento (se >R$20k e
  │   PEDP localizou ativos)
  │
  ├─► Rating C/D: prioridade para protesto, negativação,
  │   transação (não ajuíza em geral)
  │
  └─► Qualquer rating: pode ser objeto de parcelamento
      (adesão do devedor) ou de transação por adesão
      (se houver edital ativo aplicável)
```

**Pontos críticos para pesquisa empírica**:

- O ajuizamento é **endógeno ao rating**. Quando se observa uma EF
  ajuizada, isso é um sinal de que a PGFN classificou o crédito como
  A ou B **e** a PEDP localizou ativos. Este é um filtro duplo de
  seleção, não apenas valor.
- **O rating é dinâmico** — um crédito pode ser reclassificado, e
  a disponibilidade de transação em nova classe pode levá-lo a sair
  da EF. Quebras estruturais nas portarias de rating geram quebras
  estruturais observáveis no fluxo de EF.
- **Editais de transação por adesão** têm periodicidade alta (vários
  por ano). Cada edital é uma quasi-intervenção que remove do
  estoque ativo créditos com perfil alvo específico. Em dados de EF,
  aparecem como extinções clusterizadas por tema/setor/período de
  adesão.
- **PEDP e Sisbajud interagem**: desde 2020 (com a centralização em
  Sisbajud + integração PGFN), o PEDP é crescentemente automatizado.
  Rollout de funcionalidades Sisbajud altera o *output* do PEDP e,
  portanto, altera quais créditos passam no filtro de ajuizamento.

---

## 11. PGFN em Números — o funil observável (dados 2024)

O **relatório "PGFN em Números"** (publicado anualmente desde meados
da década de 2010, com dados do ano anterior) é a principal fonte
quantitativa pública sobre o estoque e o fluxo da dívida ativa
federal. Os números desta seção são da edição 2025 (dados fechados em
dez/2024). Servem como *ground truth* macro para validar totais
extraídos de DataJud ou de consulta processual em EFs federais.

### Estoque (dez/2024)

- **Total (DA União + DA FGTS)**: R$ 3 trilhões.
- **DA União em cobrança**: R$ 2 trilhões (após subtrair créditos
  em situação regular — negociados, garantidos ou suspensos).
- **DA FGTS em cobrança**: R$ 52,9 bi; 399 mil inscrições; 236 mil
  devedores.
- **Por natureza do crédito** (do total de R$ 3 tri):
  - Tributário não-previdenciário: R$ 2,1 tri (70,15%).
  - Tributário previdenciário: R$ 748,9 bi (24,56%).
  - Não-tributário: R$ 105,7 bi (3,46%).
  - Contribuições FGTS: R$ 55,6 bi (1,82%).
- **Quantidades**: 8,4 milhões de devedores agregados; 28,4 milhões
  de inscrições.
- **Regularidade**: 65,8% em situação irregular (R$ 2 tri); 34,2% em
  situação regular (R$ 1 tri) — parcelados, garantidos, ou com
  exigibilidade suspensa.
- **Por rating de recuperabilidade**:
  - A (alta): R$ 255,7 bi (8,3%); 1,1 mi devedores.
  - B (média-alta): R$ 979,3 bi (32%); 1,5 mi devedores.
  - C (média-baixa): R$ 456,5 bi (15%); 629 mil devedores.
  - **D (baixa, "irrecuperável"): R$ 1,3 tri (44%); 3,8 mi devedores**.
- **Concentração**: 26,9 mil "grandes devedores" respondem por R$
  2,1 tri (71,7% do valor); 7 milhões de "não-grandes" somam apenas
  R$ 862 bi (28,2%).

**Observação central**: 44% do estoque é classificado pela própria
PGFN como baixa recuperabilidade (rating D). Em termos de valor, a
maior parte da dívida ativa federal **não é realisticamente cobrável**
— é passivo contábil. Qualquer métrica de "sucesso da cobrança" que
use estoque no denominador subestima a performance real.

### Recuperação em 2024 (fluxo)

- **Total recuperado** (DA União + FGTS): **R$ 61,3 bilhões** —
  recorde histórico.
  - DA União: R$ 59,9 bi.
  - DA FGTS: R$ 1,4 bi.
- **Série histórica (DA União, valores correntes)**: R$ 25,7 bi
  (2020) → R$ 31,7 bi (2021) → R$ 39,1 bi (2022) → R$ 48,3 bi
  (2023) → **R$ 59,9 bi (2024)** — dobrou em 4 anos.
- **Taxa de recuperação bruta**: R$ 61,3 bi / R$ 3 tri ≈ **~2,0%**.
  Sobre o estoque em situação irregular (R$ 2 tri), ≈ **~3,1%**.

### Composição da recuperação por estratégia de cobrança (R$ 61,3 bi total em 2024)

| Estratégia | R$ bi | % |
|---|---|---|
| Parcelamento | 31,2 | 53,79% |
| Dívida Previdenciária (destacada) | 8,3 | 14,29% |
| Protesto | 6,1 | 10,48% |
| **Execução Forçada (EF)** | **5,3** | **9,20%** |
| Corresponsável (redirecionamento) | 3,9 | 6,66% |
| CADIN/CND | 1,9 | 3,28% |
| FGTS/CS | 1,5 | 2,26% |

**Resultado central para pesquisa em EF**: a execução fiscal judicial
responde por **apenas ~9% da recuperação total** (≈ R$ 5,3 bi em
2024). Parcelamento + transação dominam. Uma análise de "efetividade
da cobrança fiscal federal" que se limite a EFs captura só uma
fração — e a fração residual, composta por créditos que não foram
cobráveis por canais mais baratos.

### Transação tributária (2019–2024, acumulado)

- **Valor consolidado original negociado**: R$ 777,1 bi (sem
  descontos legais).
- **Acordos firmados**: 3,2 milhões.
- **Inscrições parceladas em transação**: 8,4 milhões.
- **Fluxo anual de recuperação via transação**:
  - 2020: R$ 1,7 bi.
  - 2021: R$ 6,4 bi.
  - 2022: R$ 14,1 bi.
  - 2023: R$ 20,7 bi.
  - 2024: R$ 34,1 bi — ≈ **57% da recuperação anual total em 2024**.
- **Transação individual simplificada**: créditos entre R$ 1 mi e R$
  10 mi (Portaria PGFN específica).
- **PTI (Programa de Transação Integral)**: Portaria Normativa MF nº
  1.383/2024, para discussões judiciais em 17 teses de controvérsia.

### Contencioso judicial — intimações/citações em 2024

- **Total de intimações/citações**: **3,1 milhões** processos ao
  longo de 2024.
- **Por instância**:
  - 1ª instância: 2,7 mi.
  - 2ª instância (TRF, TR, TJ, TRT, TRE): 365 mil.
  - Cortes superiores (STJ, TNU, TST, TSE, STF): 52 mil.
- **Classes mais trabalhadas em 2024 (intimações/citações, excluídas
  EFs para não distorcer)**: Procedimento de Juizado Especial Cível
  (270 mil), Mandado de Segurança (233 mil), Cumprimento de sentença
  contra Fazenda (186 mil), Apelação (145 mil), Proc. Comum (125 mil),
  Agravo de Instrumento (109 mil), **Embargos à Execução Fiscal (41
  mil)**, Recurso Especial STJ (17 mil).

### Contencioso administrativo — CARF (perdas evitadas)

Série R$ bi evitados em favor da Fazenda no CARF:
- 2020: 51,9
- 2021: **8,4** (mínimo — coincide com o período sem voto de
  qualidade pró-Fazenda, extinto pela `LTT` em 2020).
- 2022: 34,8
- 2023: 110,4
- 2024: **321,4** (salto de ~195% vs. 2023, coincidindo com a
  restauração do voto de qualidade pela Lei 14.689/2023).

**Implicação**: a trajetória 2020→2024 das perdas evitadas no CARF é
altamente sugestiva do efeito operacional do voto de qualidade — cai
com a extinção (2020–2021), recupera parcialmente, salta após a
restauração (2023–2024). É a quebra estrutural empírica mais clara
documentada em dados PGFN públicos.

### Contencioso judicial — perdas evitadas 2024

- STF + STJ combinados: R$ 405,8 bi evitados (teses tributárias de
  grande porte — Tema 881/885 quanto à cobrança de tributos após
  trânsito em julgado individual; Tema 1.182 STJ sobre benefícios
  fiscais de ICMS na base do IRPJ/CSLL — R$ 288 bi de impacto só
  este; Tema 1.079 STJ sobre limite de 20 SM nas contribuições
  parafiscais — R$ 94,16 bi; etc.).
- Total "perdas evitadas 2024" (CARF + judicial): **R$ 727,19 bi** —
  ≈ 12× o valor recuperado no ano. Contencioso defensivo é, em
  ordem de magnitude, mais relevante para o caixa da União do que
  cobrança ativa.

### Plataforma Comprei (alienação de bens penhorados)

- Lançada 2023; em seu 2º ano em 2024.
- **R$ 1,37 bi em dívidas negociadas e pagas**; R$ 326,32 mi em
  bens efetivamente vendidos.
- 1,17 mil imóveis cadastrados; 7,3 mil compradores; 371 imóveis
  vendidos; 20 mil anúncios; 961,3 mil visitas à plataforma.
- Percentual da venda sobre avaliação: **65,16%** — leilão
  institucional recupera cerca de 2/3 do valor de avaliação do bem.
- Valor médio da venda: R$ 886,75 mil; maior venda: R$ 27,8 mi.

---

## 12. Implicações para desenho empírico

- **Inscrição em dívida ativa ≠ ajuizamento em EF**. Boa parte do
  estoque de dívida ativa nunca vira EF: dispensa por valor, protesto
  sem ajuizamento, transação, prescrição no curso da cobrança
  administrativa. Para estudar "cobrança tributária", EFs captam só
  uma fatia — e uma fatia selecionada por valor, idade e capacidade
  de localizar devedor e bens.
- **Três marcos temporais** costumam ser confundidos: fato gerador,
  constituição definitiva (fim do PAF), inscrição em dívida ativa.
  A prescrição corre entre constituição e cobrança; a presunção de
  fraude nasce com a inscrição. Projetos que modelam "tempo do débito"
  devem escolher o marco coerente com a pergunta.
- **Transação (pós-2020)** introduz seleção endógena: débitos com
  característica X (tamanho, tipo, devedor) são mais prováveis de
  serem objeto de transação e saírem do estoque executado. EFs
  remanescentes representam o *hard core* mais resistente a
  negociação.
- **Heterogeneidade federativa**: PGFN é centralizada e bem
  documentada; PGEs e PGMs variam enormemente em estrutura, dados
  publicados, políticas de cobrança. Comparações entre estados ou
  entre municípios requerem caracterização caso a caso.
- **EF ≈ 9% da recuperação, não ≈ 100%**: dados PGFN em Números 2024
  mostram que execução forçada responde por apenas R$ 5,3 bi dos R$
  61,3 bi recuperados. Parcelamento (54%) e transação (~57% em
  2024 — há sobreposição com parcelamento no enquadramento PGFN)
  dominam. Qualquer claim de que EF é "o" mecanismo de cobrança
  federal é empiricamente falso em magnitude; é um canal residual.
- **44% do estoque em rating D** (R$ 1,3 tri) é classificado como
  baixa recuperabilidade pela própria PGFN. Modelos que usam
  "estoque de DA" como potencial de recuperação superestimam
  enormemente — o passivo real cobrável é uma fração do estoque
  nominal.
- **Concentração em grandes devedores**: 26,9 mil devedores = 72%
  do valor; 7 mi de devedores "não-grandes" = 28% do valor.
  Desenhos que modelam o devedor representativo pesando por valor
  olham um universo completamente diferente dos desenhos ponderando
  por quantidade de inscrições.
- **Perdas evitadas >> recuperação**: contencioso defensivo (R$
  727 bi evitados em 2024) é ≈ 12× o valor recuperado no ano.
  Avaliações de "produtividade" da PGFN que olham só recuperação
  desconsideram a dimensão dominante da atuação.

See also:
- `direito-tributario.md` — parte geral (obrigação, crédito,
  prescrição, responsabilidade).
- `processo-administrativo-fiscal.md` — o contencioso antes da
  inscrição.
- `execucao-fiscal.md` — a fase judicial.
- `funcoes-essenciais.md` — procuraturas da Fazenda (AGU/PGFN, PGE,
  PGM) e seu papel institucional.
