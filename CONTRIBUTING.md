# Contributing

Contributions are welcome — factual corrections, new topical areas,
updated statute references, improved coverage of institutions you
work with.

## What's in scope

- **Factual corrections** to statute references, article numbers,
  jurisprudence citations, or dates.
- **Updates** for recent reforms, new STF decisions, new CNJ resoluções.
- **New topical files** covering Brazilian institutional areas not yet
  in the repo (health law, environmental regulation, social security,
  tax procedure, etc.).
- **New quasi-experiment entries** for identification strategies in
  the literature.
- **Additional statute/case entries** in `leis_index.yaml` or
  `jurisprudencia_index.yaml`.
- **Cross-references** between files that would help navigation.

## What's out of scope

- **Verbatim statute text.** Topical files should explain and
  summarize, not reproduce law text. Use backtick citations (e.g.,
  `` `LIA.9` ``) that resolve via cite.py instead.
- **Original unpublished research findings.**
- **Opinions or editorializing** beyond what is needed to orient a
  researcher.
- **Jurisdictions other than Brazil.**

## How to contribute

### Small fixes (typos, broken links, citation errors)

Open a PR directly. No issue needed.

### New topical files

1. **Open an issue first** describing the institutional area and
   why it matters for empirical research.
2. Follow the existing file format:
   - Mandatory header: title, scope paragraph, `Topics / keywords`,
     `Snapshot as of YYYY`, cross-references, horizontal rule.
   - Terse, citation-dense prose. Portuguese where translation loses
     meaning, English otherwise.
   - Research-design framing: what matters for empirical work, where
     the quasi-random variation lives, what the selection effects are.
3. Add the file to the appropriate section of `README.md`.
4. Add any new acronyms to `siglas.md`, terms to `glossario.md`,
   and laws to `leis_index.yaml`.

### New statute or case entries

- **Laws**: add to `leis_index.yaml` with apelido, fonte_id, status,
  url, key articles, topics, and discussed_in fields. Follow existing
  entries for the format.
- **Cases**: add to `jurisprudencia_index.yaml` (structured metadata)
  AND `jurisprudencia-stf.md` (canonical description). See
  `CLAUDE.md` §"When to add a new case" for the checklist.
- **Súmulas**: TSE and TST are bulk-collected via scrapers. STJ
  súmulas are added on demand to `sumulas_stj.yaml`. STF ordinary
  súmulas are not yet collected.

### Citation format

Use the backtick citation form documented in `CLAUDE.md`:

```
`LIA.9`          — article 9 of Lei de Improbidade
`CF.31.§2`       — CF Art. 31 § 2
`Tema1199`       — STF repercussão geral Tema 1199
`SV14`           — Súmula Vinculante 14
`STSE38`         — TSE Súmula 38
`STST331`        — TST Súmula 331
```

Verify that new citations resolve before committing:
```bash
python3 tools/leis_artigos/cite.py 'YOUR_CITATION'
```

## Quality standards

- **Don't invent statute numbers, case numbers, or dates.** If you're
  not sure, say so or look it up.
- **Cite sources inline.** Every factual claim should be anchored in a
  statute, case, or published source.
- **Apply the deletion test.** If a section could be copy-pasted into
  a different topical file with only the topic name changed, it's
  generic procedure — cross-reference instead.
- **Write for research orientation, not legal practice.** The audience
  is a researcher designing an empirical study, not a lawyer seeking
  current binding law.

## Review

PRs are reviewed when the maintainer is working on related research.
For urgent corrections, note it in the PR description.
