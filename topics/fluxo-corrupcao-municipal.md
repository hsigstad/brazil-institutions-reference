# Fluxo da corrupcao municipal — life cycle of a municipal corruption case

Cross-cutting narrative tracing how a municipal irregularity moves
through detection, fiscal oversight, civil and criminal prosecution,
sanctions, and political consequences. Each stage is described with
its institutional actors, legal basis, and selection effects. This
file synthesizes material from sibling topical files; see
cross-references at each stage for the substantive detail.

**Topics / keywords**: corruption lifecycle, municipal audit, CGU,
TCE, parecer previo, camara, Ministerio Publico, improbidade, ACP,
criminal prosecution, Ficha Limpa, selection effects, attrition,
research design, fluxo processual.

**Snapshot as of 2026**: post-`L14230-2021` reform regime. `Tema1199`
governs retroactivity; `ADPF982` governs the TCE/camara boundary for
ineligibility.

For CGU audit mechanics, see `cgu-controle-interno.md`. For TCE
institutional structure, see `tribunais-contas.md`. For the contas de
governo / contas de gestao distinction and camara vote, see
`contas-municipais.md`. For improbidade doctrine and the 2021 reform,
see `improbidade.md`. For criminal statutes, see
`anticorrupcao-penal.md`. For MP structure, see
`ministerio-publico.md`.

---

## 1. Detection

Irregularities surface through four main channels, each with
different selection profiles:

- **CGU municipal audits.** Federal auditors audit municipal use of
  federal transfers. 2003--2015: the PFS (*Programa de Fiscalizacao
  por Sorteios*) drew ~2,000 municipalities by public lottery across
  40 rounds -- genuinely random conditional on population strata,
  which is why the program anchors a large causal-inference literature
  (Ferraz--Finan 2008, 2011; Avis--Ferraz--Finan 2018). Post-2015:
  reformulated as the *Programa de Fiscalizacao em Entes Federativos*
  with risk-based / thematic selection -- still the primary federal
  detection channel for municipal irregularities, but no longer random.
  Audit reports enumerate irregularidades classified by severity; these
  feed into MP investigations and TCU/TCE proceedings. See
  `cgu-controle-interno.md` SS3.

- **TCE oversight (multiple channels).** TCE detection is not limited
  to the annual contas review. TCE receives *representacoes* and
  *denuncias* that trigger processos on specific acts (contracts,
  dispensas, payments); conducts *inspecoes* and *auditorias* on
  selected programs; and runs automated monitoring. TCE-SP's Audesp
  system ingests municipal accounting and procurement data in real time
  and flags anomalies (expenditure spikes, missing documentation, LRF
  limit breaches, bid-rigging patterns); other TCEs have lighter
  electronic systems. Flags can trigger *inspecoes extraordinarias*,
  standalone processos on a single act, or feed the relator's analysis
  of the annual accounts. See `tribunais-contas.md`.

- **TCU audits of federal money in municipalities.** TCU conducts its
  own thematic audits of federal programs delivered through
  municipalities (SUS, FUNDEB, convenios, emendas parlamentares). Its
  *tomada de contas especial* (TCE -- same acronym as Tribunal de
  Contas do Estado, different instrument) is triggered when a federal
  convenio manager or CGU audit identifies irregularities in federal
  transfers; TCU judges the responsible administrator and can impose
  ressarcimento, multas, and *declaracao de inidoneidade* for
  contracting. TCU findings feed into MP improbidade and criminal
  proceedings. See `tribunais-contas.md` and `cgu-controle-interno.md`
  on the TCU--CGU division of labor.

- **Citizen complaints (ouvidoria / denuncia).** Citizens file
  complaints with the camara, the MP ouvidoria, the CGU ouvidoria,
  or the TCE ouvidoria. These are a major but noisy source:
  high false-positive rate, political instrumentalization, but also
  the primary detection channel for localized irregularities
  (ghost employees, unauthorized purchases) that audits miss.

- **MP noticia de fato.** The MP receives information through any
  channel -- media reports, police intelligence, COAF RIFs, CGU audit
  reports, TCE deliberations, or its own GAECO investigations. A
  *noticia de fato* triggers an internal assessment
  (`CF.129.I`, `CF.129.III`) that may escalate to an inquerito civil
  (civil track) or requisition of a police inquerito (criminal track).
  See `ministerio-publico.md`.

**Selection effect**: each channel has a different reach. CGU audits
are random but cover only federal transfers in sampled municipalities.
TCE monitoring is universal but limited to accounting-legibility
violations. Citizen complaints skew toward visible, politically
salient irregularities. MP-originated cases skew toward larger schemes
with criminal dimensions.

---

## 2. External control phase (TCE and TCU)

External fiscal control (`CF.70`--`CF.75`) runs on two parallel tracks
for municipalities: TCE for the state/municipal money, TCU for federal
transfers.

### TCE -- annual contas review

The TCE reviews the mayor's annual accounts in two distinct tracks
(`CF.71.I`/`CF.71.II`):

- **Contas de governo** (`CF.71.I`): TCE issues a *parecer previo*
  recommending approval or rejection of the consolidated annual
  accounts (budget execution, LRF compliance, fiscal targets).
  Possible recommendations: aprovacao, aprovacao com ressalvas,
  rejeicao. This parecer is advisory -- final judgment belongs to the
  camara (`CF.31.§2`).

- **Contas de gestao** (`CF.71.II`): TCE directly judges acts of the
  mayor as *ordenador de despesas* -- specific contracts, payments,
  procurement decisions. TCE can impose debitos and multas. Per
  `ADPF982`, these sanctions bind but do not trigger Ficha Limpa
  ineligibility.

### TCE -- processos on specific acts

Beyond the annual contas, TCE runs standalone processos that judge
individual acts of the municipal administration -- most prominently
licitacoes and contracts. These processos are typically faster than
the annual contas review and can reach a decision on a single ato
while that ato is still in progress.

**Trigger channels** (TCE-SP Regimento Interno; analogues in other
TCEs):

- **Representacao**: any licitante, citizen, or public servant can
  formally challenge an edital de licitacao, a contract award, or a
  payment. TCE-SP receives hundreds per year.
- **Denuncia**: formal whistleblower report, often from a
  disappointed bidder.
- **Audesp flags**: TCE-SP's Audesp system ingests municipal
  procurement and contract data in real time; anomalies (price
  outliers, repeat winners, edital specifications that match a single
  firm) can trigger inspecao. See `tribunais-contas.md` on Audesp.
- **Own-initiative auditoria**: TCE's corpo tecnico selects programs,
  contracts, or municipalities for audit based on risk scoring or
  thematic priorities.

**Instrument types**:

- **Auditoria / inspecao**: on-site or documentary examination of a
  specific contract, obra, or program. Produces a relatorio with
  findings.
- **Processo de fiscalizacao de licitacao / contrato**: formal
  processo targeting a specific edital, adjudication, or contract
  execution. Can request information and documents, hear
  administradores, and recommend action.
- **Monitoramento**: ongoing tracking of implementation of earlier
  TCE determinacoes.
- **Consulta**: abstract legal question submitted by a gestor;
  TCE-SP issues non-binding orientation.

**Timing and remedies for in-progress licitacoes**:

- **Medida cautelar**: TCE can suspend a licitacao or halt contract
  execution pending analysis -- a significant power because licitacao
  outcomes often cannot be unwound after contract signing and
  execution.
- **Determinacao**: order the municipality to correct irregularities
  (republish edital, alter criteria, re-adjudicate).
- **Declaracao de irregularidade / ilegalidade do ato**: formal
  finding that the contract or licitacao was irregular. Triggers
  sanctions and may feed into MP improbidade.
- **Multa and debito**: financial sanctions against the gestor
  personally (CF Art. 71 VIII), including when the licitacao harmed
  the erario.
- **Declaracao de inidoneidade**: TCE can bar firms from contracting
  with the state's public administration for up to 5 years (TCE-SP
  Regimento, analogous to `LOTCU.46` at federal level).
- **Referral to MP**: findings are formally communicated to the MPE
  (patrimonio publico promotoria) under standing convenios; the
  relatorio de auditoria becomes a key piece of evidence in
  subsequent ACP de improbidade.

**Relationship to annual contas**: adverse findings in specific-act
processos carry forward to the annual contas review -- a licitacao
declared irregular in a specific processo is likely to appear as
ressalva or motivo de rejeicao in that year's parecer previo.

**Relator assignment**: non-contas processos are distributed by
random electronic draw (TCE-SP Regimento Art. 36). See
`tribunais-contas.md` on relator mechanics and the empirical
exploitability of the random draw.

**Selection effect**: specific-act processos cover only what reaches
TCE through the trigger channels. Representacao skews toward
competitive markets with active losing bidders; Audesp flags skew
toward accounting-legible irregularities; own-initiative audit skews
toward priority programs. Many irregular acts -- those with no
displaced competitor, no accounting signature, and outside priority
programs -- never enter this track.

### TCU -- federal transfers to municipalities

TCU oversees federal money that reaches municipalities via convenios,
emendas parlamentares, and federally funded programs (SUS, FUNDEB,
PAC). Main instruments:

- **Tomada de contas especial** (`CF.71.II`, `LOTCU`): triggered when
  a convenio manager, CGU auditor, or TCE identifies irregularity in
  federal transfers. TCU judges the responsible administrator (often
  the mayor or secretary), imposes ressarcimento, multas, and can
  declare *inidoneidade* barring the firm or individual from federal
  contracting for up to 5 years (`LOTCU.46`). Feeds into MP
  improbidade and criminal proceedings.
- **Thematic audits**: TCU runs program-level audits (e.g., Operacoes
  Especiais) of federal programs delivered by municipalities.

### Timing

TCE/TCU proceedings are administrative, not judicial. Annual contas:
submitted 60--90 days after fiscal year-end; parecer 1--3 years later.
Processos on specific acts and TCEs (tomadas de contas especial) can
run years longer depending on backlogs. Backlogs vary substantially by
state.

See `contas-municipais.md` SS1--SS2, `tribunais-contas.md`.

---

## 3. Camara vote (contas de governo only)

The camara municipal votes on the TCE parecer previo (`CF.31.§2`).
Override requires a **2/3 supermajority** of camara members -- i.e.,
to reject an approval recommendation or to approve despite a rejection
recommendation, 2/3 must vote against the TCE position. In practice,
TCE rejection pareceres are sustained in the large majority of cases
because assembling 2/3 to override is difficult.

Key institutional details:

- No federal rule mandates open or secret ballot; each municipio's
  Lei Organica and Regimento Interno control. Many camaras voted
  secretly until the 2010s; a diffusion of open-voting reforms
  followed `EC76-2013`. See `contas-municipais.md` SS4.
- Camara omission (failure to vote) does not generate ineligibility
  (`Tema157`).
- Per `Tema157`, both contas de governo and contas de gestao fall
  under camara jurisdiction for Ficha Limpa purposes, but `ADPF982`
  clarified that TCE retains direct sanctioning power over contas de
  gestao.

**Selection effect**: the camara vote is a political filter.
Coalitional dynamics, mayor--vereador bargaining, and the voting
modality (secret vs. open) all shape whether the TCE parecer is
sustained. Observable in municipal-level data; exploitable for
research designs comparing municipalities with open vs. secret voting.

---

## 4. MP investigation

If irregularities warrant civil or criminal pursuit, the MP is the
pivotal actor. Two instruments:

- **Inquerito civil** (IC): non-judicial investigation for civil
  improbidade. The MP gathers evidence, hears witnesses, requisitions
  documents. May conclude with an ACP filing, a TAC (termo de
  ajustamento de conduta), or archival. See `ministerio-publico.md`.
- **Requisicao de inquerito policial**: for criminal-track facts, the
  MP requests a police investigation (`CF.129.VIII`).

MP discretion is load-bearing. The decision to open an IC, to convert
it into an ACP, or to archive it is made by the individual promotor
de justica (state) or procurador da republica (federal), subject to
the *principio do promotor natural* and internal oversight by the
CSMP / camara de coordenacao. There is no external mechanism forcing
the MP to act on a TCE rejection or CGU audit finding.

**Selection effect**: MP capacity constraints, promotor rotation, and
thematic prioritization (GAECOs handle complex corruption, generalist
promotorias handle the rest) mean that not all detected irregularities
generate investigations, and not all investigations generate filings.

---

## 5. Civil improbidade action (ACP)

The MP files an ACP under `LIA` in the *primeiro grau* of the TJ
(state) or TRF (federal, when federal funds are involved). Key
features post-`L14230-2021`:

- **Standing**: MP exclusive (`LIA.17 from:L14230-2021`). Pre-reform,
  the affected public entity could also sue.
- **Element of fault**: **dolo only** (`LIA.1.§1 from:L14230-2021`).
  Culposa improbidade eliminated. This narrowed the actionable
  universe substantially.
- **Three categories**: `LIA.9` (enriquecimento ilicito), `LIA.10`
  (prejuizo ao erario), `LIA.11` (violacao de principios). Severity
  determines sanction scale -- see SS7.
- **Prescription**: 8 years from the act
  (`LIA.23 from:L14230-2021`); ressarcimento for dolosa improbidade
  is imprescritivel (`Tema897`).
- **Settlement**: acordo de nao persecucao civel
  (`LIA.17-B from:L14230-2021`) allows negotiated resolution with
  judicial homologation.

Typical timeline: IC (1--3 years) + first-instance judgment (3--7
years) + appeals (2--5 years). Total: 6--15 years from detection to
final judgment is common. The 2021 reform's procedural tightening may
extend this further.

See `improbidade.md` SS1--SS2.

---

## 6. Criminal parallel

The same facts underlying an improbidade action may simultaneously
trigger criminal prosecution. The two tracks are independent:
different courts, different evidentiary standards (beyond reasonable
doubt vs. preponderance), different sanctions.

Key criminal statutes:

- **`CP.312`--`CP.333`**: peculato, concussao, corrupcao passiva/ativa,
  prevaricacao. Core Codigo Penal offenses for public officials and
  bribers.
- **`CP.337-E`--`CP.337-P`**: procurement crimes (post-`L14133`).
  Replaced `L8666.89`--`L8666.98` for new conduct.
- **`LL` / `LL2`**: lavagem de dinheiro. Any criminal offense is now
  a valid predicate (post-2012 open-list reform).
- **`LCO`**: organizacao criminosa. Defines the offense and provides
  the *colaboracao premiada* framework used in complex corruption
  cases.
- **`LAC`**: Lei Anticorrupcao (corporate liability, administrative
  and civil). Enables acordos de leniencia and CEIS/CNEP listing. Not
  strictly criminal but runs on a parallel corporate track. See
  `anticorrupcao-penal.md` SS5.

Criminal prosecution of mayors follows ordinary first-instance
jurisdiction (no foro privilegiado for prefeitos after end of mandate).
Sitting mayors have foro no TJ (`CF.29.X`).

See `anticorrupcao-penal.md`, `processo-penal.md`.

---

## 7. Sanctions and consequences

### Improbidade sanctions (`LIA.12`)

| Category | Suspensao de direitos politicos | Proibicao de contratar | Multa |
|---|---|---|---|
| `LIA.9` (enriquecimento) | up to 14 years | up to 14 years | <= value of increment |
| `LIA.10` (prejuizo ao erario) | up to 12 years | up to 12 years | <= 2x the loss |
| `LIA.11` (violacao de principios) | up to 4 years | up to 4 years | <= 24x monthly remuneration |

All categories can also trigger loss of public function, full
ressarcimento, and asset forfeiture. The 14/12/4 ratio shapes MP
charging decisions.

### Ficha Limpa ineligibility (`LI.1.I.g`)

8-year ineligibility from rejected accounts, contingent on four
cumulative conditions: (1) rejection by the orgao competente (camara,
per `Tema157`), (2) irregularidade insanavel, (3) ato doloso de
improbidade, (4) decisao irrecorrivel not suspended by the Judiciary.
See `contas-municipais.md` SS3.

### TCE debitos and multas

TCE can impose financial sanctions on contas de gestao directly
(CF Art. 71 VIII). These are executable as titulo executivo but do not
generate ineligibility (`ADPF982`).

### TCU debitos, multas, and inidoneidade

TCU imposes ressarcimento and multas via *tomada de contas especial*
for federal funds (`CF.71.II`, `LOTCU`). TCU can also declare
*inidoneidade* of firms or individuals for federal contracting up to
5 years (`LOTCU.46`). Like TCE sanctions, these do not trigger Ficha
Limpa by themselves (per `ADPF982` logic).

### Criminal sanctions

Imprisonment (regime fechado/semiaberto/aberto), fines, and
accessory penalties (loss of office, inhabilitacao). Criminal
conviction with transito em julgado independently triggers
ineligibility under `LI.1.I.e`.

---

## 8. Research design implications

The lifecycle above creates a **multi-stage attrition funnel**. At
each stage, cases are selected in or out by different institutional
actors with different incentives:

- **Detection**: only irregularities that surface through one of the
  four channels enter the pipeline. CGU random audits are the only
  channel with a credible claim to random sampling.
- **TCE**: filters on accounting-legibility grounds; political
  composition of the TCE (conselheiro appointment rules) may affect
  outcomes.
- **Camara**: political filter; coalitional dynamics, voting modality,
  and mayor--vereador bargaining shape override rates.
- **MP**: capacity and prioritization filter; promotor discretion is
  unobservable in administrative data.
- **Judiciary**: timeline filter; cases that reach judgment are a
  survivor-biased subset.

**Observable populations** differ by stage. CGU audit data covers
sampled municipalities with detailed irregularity counts. TCE parecer
data covers all municipalities but with heterogeneous coding across
states. Camara votes are theoretically public but not systematically
collected. ACP filings are in TJ/TRF systems (DataJud). Criminal
cases are in separate TJ/TRF criminal dockets.

**Timing** is the binding constraint. From the fiscal year under
review to a final improbidade judgment, 6--15 years is typical.
Ficha Limpa ineligibility can attach at the camara-vote stage (faster)
but requires all four `LI.1.I.g` conditions. Research designs that
need final judicial outcomes face severe right-censoring for any
fiscal year after ~2015.
