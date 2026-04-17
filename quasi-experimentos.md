# Quasi-experimentos — natural experiments in Brazilian institutions

Index of identification strategies and natural experiments embedded in
Brazilian institutional features that have been used in the published
empirical literature. Each entry: the institutional source, the
cutoff/threshold/event, what it identifies, and the canonical paper(s)
that exploited it.

This file is for **empirical researchers** designing causal studies on
Brazilian institutions. It complements the topical files by surfacing
the parts of those institutions that researchers have used as sources
of variation.

**Scope**: only entries that have been exploited in published (or
widely-circulated working) papers. Novel or unexploited identification
ideas are deliberately not here.

**Topics / keywords**: natural experiment, quasi-experiment,
identification strategy, regression discontinuity, RD, difference in
differences, event study, instrument, IV, cutoff, threshold, treatment
effect, causal inference, Brazilian empirical literature.

**Snapshot as of 2026**: a representative but not exhaustive list. Many
of these have multiple variations and active replication / extension
work in the literature.

---

## Cross-references

For institutional context behind each entry, follow the cited file:
- [`topics/cgu-controle-interno.md`](topics/cgu-controle-interno.md) — CGU random audits
- [`topics/federalismo-fiscal.md`](topics/federalismo-fiscal.md) — FPM, FUNDEB
- [`topics/partidos-e-sistema-eleitoral.md`](topics/partidos-e-sistema-eleitoral.md) — electoral cutoffs
- [`topics/contas-municipais.md`](topics/contas-municipais.md) — Ficha Limpa
- [`topics/justica-trabalho.md`](topics/justica-trabalho.md) — labor reform (2017)
- [`topics/cnj-administracao-judicial.md`](topics/cnj-administracao-judicial.md) — judicial random assignment

---

## 1. CGU random municipal audits — the canonical Brazilian RD

**Institutional source**: Controladoria-Geral da União (CGU), *Programa
de Fiscalização por Sorteios* (PFS), 2003–2015.

**Mechanism**: ~40 lotteries held in Caixa Econômica Federal
headquarters, each randomly drawing ~60 municipalities for federal
audit. Audits produced detailed reports of irregularities classified by
type (procurement, health, education, social programs).

**Identifies**: causal effects of audit exposure (and audit-revealed
corruption) on a wide variety of outcomes: voting, future spending,
firm-level outcomes, future corruption, etc.

**Population restriction**: municipalities above certain population
thresholds (initially ~500k, later lifted) were excluded from the random
pool and audited on different criteria.

**Canonical papers**:
- Ferraz & Finan (2008, *QJE*) — electoral punishment of corruption
  revealed by audit.
- Ferraz & Finan (2011, *AER*) — re-election incentives and corruption.
- Avis, Ferraz & Finan (2018, *JPE*) — deterrence effects of audits on
  future corruption.
- Many extensions in the broader Ferraz–Finan–Monteiro literature.

**Caveat**: random assignment applies **strictly to 2003–2015**. After
2015, the program was reformulated as risk-based selection
(*Programa de Fiscalização em Entes Federativos*). Post-2015 audits are
not randomly assigned and require different identification assumptions.

**See**: [`topics/cgu-controle-interno.md`](topics/cgu-controle-interno.md) §3.

---

## 2. FPM step function — RD on municipal revenue

**Institutional source**: Fundo de Participação dos Municípios (FPM)
distribution rules under Decreto-Lei 1.881/1981 + LC 62/1989.

**Mechanism**: FPM coefficients for interior municipalities follow a
**step function** of population — 16 brackets, with discrete jumps in
per-capita FPM as a municipality crosses a bracket boundary. Population
estimates are published annually by IBGE; coefficients are set by TCU
for year *t* based on the IBGE estimate published by August of year *t−1*.

**Identifies**: effects of marginal increases in municipal revenue on
spending, public goods provision, electoral outcomes, corruption,
political competition, etc.

**Threshold detail**: bracket boundaries depend on population tier;
small towns cluster in lower brackets where the absolute jumps are
smaller but per-capita effects are larger.

**Reform**: LC 143/2013 altered the reclassification mechanics — verify
which regime applies for the period of interest.

**Canonical papers**:
- Litschig & Morrison (2013, *AEJ Applied*) — public spending and
  political effects.
- Brollo, Nannicini, Perotti & Tabellini (2013, *AER*) — corruption and
  political selection.
- Many extensions on health, education, infrastructure outcomes.

**See**: [`topics/federalismo-fiscal.md`](topics/federalismo-fiscal.md) §2 ("FPM").

---

## 3. 200k voter threshold for second-round mayoral elections

**Institutional source**: CF Art. 29 II.

**Mechanism**: in municipalities with **more than 200,000 registered
voters**, prefeito elections require a second round if no candidate
gets 50%+1 in the first round. In smaller municipalities, the
first-round plurality wins outright.

**Identifies**: effects of two-round elections vs single-round on
political competition, candidate selection, ideological positioning,
corruption, policy outcomes.

**Caveat**: the 200k threshold is on **registered voters**, not
population. The two are correlated but not identical (electorate
expansion or contraction can move a municipality across the threshold
without population change).

**Canonical papers**:
- Bordignon, Nannicini & Tabellini (2016, *AER*) — moderation effects.
- Multiple Brazilian replication / extension papers on corruption and
  selection.

**See**: [`topics/partidos-e-sistema-eleitoral.md`](topics/partidos-e-sistema-eleitoral.md) §1.

---

## 4. Ficha Limpa (LC 135/2010) — introduction shock

**Institutional source**: Lei Complementar 135/2010, amending LC 64/1990
Art. 1 I "g" (Ficha Limpa).

**Mechanism**: pre-2010, ineligibility for past convictions required
**trânsito em julgado** (final, unappealable conviction). Post-2010, a
**collegiate body decision** (não unipessoal) suffices, vastly
expanding the pool of ineligible candidates.

**Identifies**: effects of stricter eligibility rules on candidate
quality, political competition, voter behavior, and turnover. Also
within-politician variation: a politician convicted at first instance
in 2009 was eligible for the 2010 election; the same conviction
post-Ficha-Limpa ruling regime would render them ineligible.

**Constitutional confirmation**: STF ADC 29/30 + ADI 4578 (2012) upheld
the constitutionality despite presunção de inocência objections.

**Canonical papers**:
- Avis, Ferraz, Finan & Varjão (2022, *AEJ Applied*) and others on
  Ficha Limpa effects on electoral selection.

**See**: [`topics/partidos-e-sistema-eleitoral.md`](topics/partidos-e-sistema-eleitoral.md) §7,
[`topics/contas-municipais.md`](topics/contas-municipais.md) §3.

---

## 5. Reforma trabalhista (Lei 13.467/2017) — filing-cost shock

**Institutional source**: Lei 13.467/2017, effective 11 November 2017.

**Mechanism**: pre-reform, Brazilian labor courts had **zero filing
costs** for workers and **no honorários de sucumbência** (loser-pays
attorney fees). The 2017 reform introduced custas (2% of claim value),
honorários (5–15%), no-show penalties, and tightened *justiça gratuita*
eligibility (40% RGPS ceiling, down from 2× minimum wage).

**Identifies**: effects of filing costs on litigation volume and
composition. The November 2017 cutoff produces:
- A **mass-filing spike** in November 2017 (workers rushing under old
  rules) — ~207k filings vs ~120k typical monthly volume.
- **34% drop** in 2018 vs 2017 filings.
- **Composition change**: speculative claims (*pedidos aventureiros*)
  dropped disproportionately.

**Partial reversal**: STF `ADI5766` (October 2021) struck down the
harshest cost provisions for *justiça gratuita* beneficiaries.

**Canonical papers**:
- Corbi, Narita, Ferreira & Souza (2022, SSRN WP) — exploits
  quasi-random assignment of labor-court judges and simulates the
  2017 reform, finding that shifting legal costs onto workers reduces
  firm financial distress and increases hiring at small firms.

**See**: [`topics/justica-trabalho.md`](topics/justica-trabalho.md) §"Filing costs"
and §"Impact on filing volumes".

---

## 6. FUNDEB complementação — federal top-up threshold

- **Source**: FUNDEB (EC 108/2020, Lei 14.113/2020). Federal government
  tops up state-level FUNDEB funds when per-student spending falls
  below a national minimum.
- **Mechanism**: states whose FUNDEB per-student value falls below the
  national complementação threshold receive federal top-up. Creates a
  kink/notch at the threshold.
- **Identifies**: effect of incremental education funding on student
  outcomes, teacher salaries, school infrastructure.
- **Caveats**: threshold moves annually; state-level sorting around the
  cutoff is possible via enrollment manipulation.
- **Canonical papers**: Gordon & Vegas (2005); Kosec (2014 *JDE*).
- **See**: [`topics/federalismo-fiscal.md`](topics/federalismo-fiscal.md) §2.

---

## 7. Judicial random case assignment — judge fixed effects

- **Source**: CNJ case-assignment rules. Cases distributed by electronic
  *sorteio* within groups of varas of the same competence.
- **Mechanism**: quasi-random assignment of cases to judges within the
  same vara-group. Prevenção creates persistence within a case but
  does not affect initial assignment.
- **Identifies**: effect of judge identity/characteristics on case
  outcomes (duration, settlement rates, sentencing).
- **Caveats**: specialization structures (cível vs. criminal, fazenda
  pública) create non-random sorting by subject matter. Must document
  the specialization structure when claiming random assignment.
  Titular/substituto splits (by case-number parity) add a second
  layer of quasi-randomness within a single vara.
- **Canonical papers**: Abrams et al. (2012); for Brazil: various TJSP
  studies exploiting vara-level random assignment.
- **See**: [`topics/cnj-administracao-judicial.md`](topics/cnj-administracao-judicial.md) §5,
  [`topics/justica-federal.md`](topics/justica-federal.md) §1,
  [`topics/justica-trabalho.md`](topics/justica-trabalho.md) §2.

---

## 8. Municipal emancipation wave (1988–2000)

- **Source**: CF/88 Art. 18 §4 (original) gave states authority to
  create new municipalities by state law. ~1,438 new municípios
  created between 1988 and 2000 before EC 15/1996 tightened the rules.
- **Mechanism**: creation of new municipalities in response to state-
  level legislative incentives (typically FPM capture — smaller
  municipalities get higher per-capita FPM due to the step function).
- **Identifies**: effects of government fragmentation on public goods,
  fiscal outcomes, political competition.
- **Caveats**: municipality creation is endogenous to local political
  interests; need instruments or boundary-based designs.
- **Canonical papers**: Litschig (2012 *JDE*); Arvate et al.
- **See**: [`topics/federalismo-fiscal.md`](topics/federalismo-fiscal.md) §2.

---

## How to add an entry

When you find or use a new natural experiment in Brazilian institutions,
add an entry to this file with:

1. **Institutional source**: the statute, regulation, or decision that
   creates the variation.
2. **Mechanism**: the precise rule that generates the assignment /
   threshold / event.
3. **Identifies**: what causal effect you can recover with this variation.
4. **Caveats**: known threats to identification (selection, anticipation,
   spillover, etc.).
5. **Canonical paper(s)**: the seminal use(s) of the variation in the
   literature. This file is scoped to variations used in published
   work — if the strategy hasn't been used yet, keep it in your own
   notes rather than listing it here.
6. **Cross-reference**: link to the topical file(s) where the
   institutional details are explained.
