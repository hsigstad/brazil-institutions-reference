# STF "A Constituição e o Supremo" — scraper

Scrapes the STF's annotated Constitution via its JSON API into a
SQLite database, enabling `cite.py 'CF.109' --annotations` to show
STF jurisprudence cross-references for each CF article.

## Source

[constituicao.stf.jus.br](https://constituicao.stf.jus.br/) — the STF's
project mapping constitutional articles to STF decisions. Clean REST
API at `/api/v1/dispositivo` and `/api/v1/comentario`.

## Usage

```bash
# Fetch + build in one step (~3-4 minutes for 702 articles)
python3 scraper.py all

# Or separately
python3 scraper.py fetch     # download JSON to cache (~700 API calls)
python3 scraper.py build     # parse cached JSON → SQLite
```

## Output

`cf_stf_anotada.db` with one table:

```sql
CREATE TABLE anotacao (
    id INTEGER PRIMARY KEY,
    artigo INTEGER NOT NULL,
    artigo_letra TEXT,
    tipo TEXT NOT NULL,
    caso TEXT,               -- e.g., "ADI 2.473 MC", "RE 586.453"
    relator TEXT,            -- e.g., "Marco Aurélio"
    data_julgamento TEXT,    -- e.g., "20-2-2013"
    turma TEXT,              -- e.g., "P", "1ª T", "2ª T"
    texto TEXT NOT NULL,     -- plain-text holding summary
    stf_links TEXT           -- semicolon-separated STF portal URLs
);
```

### Annotation types (`tipo`)

| Type | Count | Description |
|---|---|---|
| Controle concentrado de constitucionalidade | ~796 | ADI, ADC, ADPF, ADO decisions |
| Julgados correlatos | ~726 | Related decisions (HC, RE, MS, etc.) |
| Repercussão geral | ~211 | Temas with binding effect |
| Súmula | ~13 | Ordinary STF súmulas |
| Súmula vinculante | ~12 | Binding súmulas |

Total: ~1,758 annotations with ~1,655 extractable case citations
across ~183 CF articles.

## Integration with cite.py

```bash
# Show STF annotations alongside CF article lookup
python3 ../leis_artigos/cite.py 'CF.109' --annotations

# Works even without artigos.db
python3 ../leis_artigos/cite.py 'CF.37' --annotations   # 103 annotations!
```

## Cache

JSON responses cached at `~/research/data/stf_constituicao/`
(override with `STF_CF_CACHE`). Three directories: `titles.json`,
`articles/`, `comments/`. Subsequent runs skip cached files.

## Dependencies

Stdlib only (urllib, json, re, sqlite3). No external packages.

## Error rate

~40% of articles return no comments (many CF articles have never been
directly adjudicated by STF). The scraper writes `{"data": []}` for
these, which is correct — absence of annotations is meaningful.
