# Fluxo de transferência federal — from allocation to enforcement

Cross-cutting narrative tracing how a federal transfer becomes a
municipal expenditure and how each institutional layer generates
observable data for research design. This file connects stages
covered in depth by sibling files; it does not duplicate their
substance.

**Topics / keywords**: federal transfer flow, FPM, FUNDEB, SUS
fundo-a-fundo, municipal budget, licitação, empenho, liquidação,
pagamento, RREO, RGF, TCE, CGU, parecer prévio, Ficha Limpa,
quasi-experiment, pipeline institucional.

**Snapshot as of 2026**: institutional pipeline is stable. Monetary
thresholds (procurement dispensa, LRF caps) update periodically --
verify current values. Reforma tributária (`EC132-2023`) begins
phase-in 2026 but does not alter the transfer-to-expenditure flow
for the FPM/FUNDEB/SUS channels described here.

For fiscal federalism detail, see `federalismo-fiscal.md`. For
procurement, `licitacoes.md`. For TCE oversight,
`tribunais-contas.md` and `contas-municipais.md`. For improbidade,
`improbidade.md`. For CGU, `cgu-controle-interno.md`. For
transparency portals, `transparencia-dados.md`.

---

## 1. Constitutional allocation — money enters the municipal pipeline

Four channels dominate municipal revenue from higher levels:

- **FPM** (Fundo de Participação dos Municípios): 22.5% of IR + IPI
  (`CF.159.I`), distributed by population-tier coefficients (`LC62`;
  Decreto-Lei 1.881/1981). Additional shares from `EC55-2007`,
  `EC84-2014`, `EC112-2021` bring the effective share to ~25.5%.
  Interior municipalities receive 86.4% of the fund; capitals 10%.
  The step-function coefficient structure is the basis of the FPM-RD
  instrument (see sec. 8). Detail in `federalismo-fiscal.md` sec. 2.

- **ICMS quota-parte**: states must pass 25% of ICMS collected to
  their municipalities (`CF.158.IV`). At least 65% by valor
  adicionado fiscal; up to 35% by state-defined criteria
  (`CF.158.§unico`). Not a federal transfer stricto sensu, but
  dominates the revenue mix alongside FPM.

- **SUS fundo-a-fundo**: federal health transfers deposited directly
  into the Fundo Municipal de Saude. Constitutional floor: 15% of
  municipal RCL for health (`CF.198`; `LC141`). Federal co-financing
  follows block-grant rules (PAB fixo + variavel, MAC, FAEC).
  Reported via SIOPS.

- **FUNDEB**: successor to FUNDEF. `CF.212`; Lei 14.113/2020.
  Redistributes a basket of state and municipal tax revenue within
  each state, equalizing per-pupil spending to a minimum.
  Complemented by federal top-up (VAAF, VAAT, VARI). Reported via
  SIOPE.

All four arrive as earmarked or formula-driven deposits. The
municipality has near-zero discretion over the amount received --
variation is mechanical, driven by population, enrollment, VAF, and
federal revenue fluctuations.

## 2. Municipal budget — PPA / LDO / LOA

The budget cycle translates incoming revenue into authorized
expenditure (`CF.165`):

- **PPA** (4-year plan, aligned to the mandate): sets strategic
  priorities and multi-year capital programs.
- **LDO** (annual): fiscal targets, personnel-spending limits,
  authorization for supplementary credits.
- **LOA** (annual): line-item appropriations. Revenue forecast
  determines the expenditure ceiling.

**Receita corrente liquida (RCL)** is the denominator for LRF fiscal
limits. Key municipal caps:

- Personnel: 60% of RCL (`LRF.19`, `LRF.20`). Executive branch
  gets 54%; legislature 6%.
- Debt service: Senate Resolution 40/2001 caps net consolidated
  debt at 1.2x RCL.

Exceeding the personnel cap triggers automatic sanctions (`LRF.23`):
hiring freeze, pay-raise prohibition, mandatory reduction within two
quarters. Detail in `federalismo-fiscal.md` sec. 4.

## 3. Procurement — converting budget into contracts

Municipal expenditure above the dispensa threshold requires
competitive bidding (`CF.37.XXI`).

- **Lei 8.666/1993** (`L8666`): five modalities by value tier
  (convite, tomada de precos, concorrencia). Dispensa up to
  R$17,600 for goods/services (`L8666.24.II`). Still the relevant
  statute for pre-2021 analysis.
- **Lei 14.133/2021** (`L14133`): replaced L8666 effective April
  2023 for new contracts. Single framework: pregao, concorrencia,
  concurso, leilao, dialogo competitivo. Dispensa up to
  R$59,906.02 for goods/services (`L14133.75.II`, annually
  updated).
- **Pregao** (reverse auction): dominant modality for common
  goods/services since Lei 10.520/2002, now absorbed into
  `L14133`. Electronic pregao mandatory for federal resources.

Procurement irregularities -- directed dispensas, fractioned
purchases to stay below thresholds, bid rigging -- are the
single largest category of TCE findings on contas de gestao.
Detail in `licitacoes.md`.

## 4. Contract execution — empenho, liquidacao, pagamento

The expenditure cycle follows three legally distinct stages
(Lei 4.320/1964 Arts. 58--65):

- **Empenho**: reservation of budget credit. Creates a legal
  obligation. Observable in SIAFI (federal) or municipal contabil
  systems.
- **Liquidacao**: verification that the good was delivered or
  service rendered. Requires fiscal invoice and attestation.
- **Pagamento**: actual disbursement to the creditor.

Contract amendments: the original contract value may be increased
up to 25% (50% for building-renovation contracts) without new
licitacao (`L8666.65.§1`; `L14133.125`). Systematic use of
aditivos near the 25% ceiling is a TCE red flag.

Restos a pagar (unpaid commitments carried across fiscal years)
accumulate when empenho outpaces pagamento. `LRF.42` prohibits
contracting obligations in the last two quadrimesters of a mandate
without sufficient cash to cover them -- the "last-year-of-mandate"
fiscal restriction.

## 5. Fiscal reporting — the paper trail

LRF requires periodic disclosure:

- **RREO** (Relatorio Resumido da Execucao Orcamentaria):
  bimonthly (`LRF.52`). Revenue vs. forecast, expenditure by
  function, restos a pagar.
- **RGF** (Relatorio de Gestao Fiscal): quadrimestral
  (`LRF.55`). Personnel spending as % of RCL, debt levels,
  guarantee exposure, credit operations.
- **SIOPS** (health): quarterly self-reported health expenditure
  as % of RCL. Federal transfers conditioned on timely filing.
- **SIOPE** (education): self-reported education expenditure,
  FUNDEB application. Also conditions federal transfers.
- **SICONFI** (STN): consolidated portal receiving RREO/RGF
  data from all municipalities. Machine-readable since ~2013.

Non-filing or late filing of RREO/RGF triggers inscription in
CAUC (Cadastro Unico de Convenios) and blocks voluntary transfers
and credit operations. Detail in `transparencia-dados.md`.

## 6. External audit — TCE and CGU

### TCE (Tribunal de Contas do Estado)

Each state's TCE audits municipal accounts (`CF.31.§1`; `CF.75`).
Two tracks:

- **Contas de governo** (annual accounts of the prefeito as chief
  executive): TCE issues a *parecer previo* (approve or reject);
  final judgment belongs to the camara municipal (`CF.31.§2`). The
  parecer prevails unless overridden by 2/3 of vereadores.
- **Contas de gestao** (acts of individual gestores as ordenadores
  de despesa): TCE judges directly, with no camara override.

The contas de governo / contas de gestao distinction is the
institutional fault line that determines whether rejection triggers
Ficha Limpa ineligibility directly (gestao) or only via camara vote
(governo). Detail in `contas-municipais.md`, `tribunais-contas.md`.

### CGU (Controladoria-Geral da Uniao)

Federal internal control. Audits municipal use of federal transfers
via the *Programa de Fiscalizacao por Sorteios Publicos* (lottery
audits, 2003--2015) and successor programs. The lottery mechanism
is quasi-random assignment of audit intensity -- a canonical
instrument in the corruption literature (Ferraz & Finan 2008, 2011).
Detail in `cgu-controle-interno.md`.

## 7. Enforcement — consequences of irregularity

When audit or investigation finds irregularity, multiple enforcement
channels activate:

- **TCE sanctions**: *multa* (fine on the gestor), *debito*
  (obligation to return misspent funds), *imputacao de debito*
  (joint and several liability). TCE can also declare the gestor
  *inabilitado* for public office (8 years, LOTCU-analogues at
  state level).
- **MP improbidade action** (`LIA`): Art. 9 (enriquecimento
  ilicito), Art. 10 (dano ao erario -- requires dolo post
  `L14230-2021`), Art. 11 (violacao de principios). Sanctions in
  `LIA.12`: suspension of political rights (up to 14 years for
  Art. 9), fine, loss of function.
- **Ficha Limpa ineligibility** (`LI.1.I.g`): accounts rejected by
  the camara (contas de governo) or directly by the TCE (contas de
  gestao) generate 8-year ineligibility *por decisao irrecorrivel
  de orgao competente*. The camara vote is the gate for governo
  accounts -- a TCE parecer previo alone does not suffice.
- **Last-year-of-mandate restriction** (`LRF.42`): obligations
  contracted in the final two quadrimesters without cash coverage
  are irregular. TCE routinely flags this in the transition audit.

These channels are not mutually exclusive. A single procurement
irregularity can trigger TCE debito, MP improbidade action, and
(if accounts are rejected) Ficha Limpa ineligibility.

## 8. Research design implications

Each stage of the pipeline generates observable data and, in some
cases, quasi-random variation:

| Stage | Data source | Quasi-random variation |
|---|---|---|
| FPM allocation | STN/TCU coefficient tables | **FPM step function**: population crossing a tier threshold produces a discrete jump in per-capita transfers (Litschig & Morrison 2013; Brollo et al. 2013). Classic RD. |
| ICMS quota-parte | State finance secretariats | VAF-based formula; less exploited empirically due to endogeneity of local economic activity. |
| SUS transfers | SIOPS, FNS | Block-grant structure; PAB fixo is per-capita (mechanical). |
| FUNDEB | SIOPE, FNDE | Per-pupil equalization; variation from enrollment shocks. |
| Budget execution | SICONFI, municipal portals | Panel data on RCL, personnel share, debt. |
| Procurement | ComprasNet (federal), state portals | Unit-price variation, number of bidders, aditivo frequency. |
| CGU audit | CGU lottery reports | **Random audit assignment** (2003--2015 lottery program). Exogenous variation in detection probability. |
| TCE parecer | TCE annual reports, Sagres-like systems | **Random relator assignment** within TCE (used in Hidalgo et al.). Assignment-to-relator as instrument for parecer severity. |
| Camara vote | Municipal legislative records | 2/3 override threshold; open vs. secret ballot (`ADPF982`). |
| Ficha Limpa | TSE candidacy records, DivulgaCand | Observable ineligibility outcome; linked to TCE/camara decisions. |

**Key identification strategies** exploiting this pipeline:

- **FPM-RD**: per-capita transfer as treatment, with outcomes at
  any downstream stage (spending composition, procurement patterns,
  audit findings, corruption).
- **CGU lottery**: audit-vs-no-audit as treatment; downstream
  outcomes include electoral accountability, incumbent re-election,
  fiscal adjustment.
- **TCE relator assignment**: variation in audit stringency; downstream
  effects on camara override probability, Ficha Limpa incidence.
- **Last-year-of-mandate**: `LRF.42` creates a temporal discontinuity
  in fiscal behavior; observable in RREO/RGF panel data.
