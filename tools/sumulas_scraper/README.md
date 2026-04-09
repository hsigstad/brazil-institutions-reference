# sumulas_scraper — STF and TSE súmula scrapers

Reproduces the súmula YAML indexes at the repo root from the canonical
court portals. Each scraper is one Python file in this directory:

| Script | Source | Output | Citation form |
|---|---|---|---|
| [`scraper.py`](scraper.py) | portal.stf.jus.br | [`../../sumulas_vinculantes.yaml`](../../sumulas_vinculantes.yaml) | `` `SV14` `` (STF Súmulas Vinculantes) |
| [`tse.py`](tse.py) | www.tse.jus.br | [`../../sumulas_tse.yaml`](../../sumulas_tse.yaml) | `` `STSE38` `` (TSE Súmulas) |

Both YAMLs are resolved by [`../leis_artigos/cite.py`](../leis_artigos/cite.py).

These are maintainer tools. End users who just want to look up a
súmula should use `cite.py 'SV14'` or `cite.py 'STSE38'`; the prebuilt
YAMLs are committed alongside this code.

## scraper.py — STF Súmulas Vinculantes

- Fetches the SV index page from `portal.stf.jus.br` and extracts
  the `(sv_number, internal_stf_id)` mapping.
- Downloads the detail page for each SV (one HTTP request per SV,
  ~63 as of 2026).
- Parses the verbatim *enunciado* out of the first `parCOM` div on
  each detail page.
- Emits `sumulas_vinculantes.yaml` with one entry per SV: number,
  verbatim text, status (`vigente`/`cancelada`/`revogada`), and the
  canonical STF portal URL.
- Stdlib only (`urllib`, `re`, `html`, `ssl`). No `requests`/`bs4`
  dependency.
- Polite: 0.4s delay between requests, browser User-Agent. Idempotent:
  cached pages are skipped on re-run unless `--force` is passed.

## tse.py — TSE Súmulas

- Walks the paginated TSE súmulas listing on
  `www.tse.jus.br` (Plone CMS, 20 items per page, ~4 pages total
  for ~72 entries as of 2026).
- Extracts verbatim text directly from the listing — TSE puts the
  full súmula text inline, no per-súmula detail-page fetches needed.
- Detects cancelled súmulas from the `(Cancelada)` marker in the page
  text (no hard-coded list, unlike STF SVs where text-based detection
  false-positives).
- Emits `sumulas_tse.yaml` with one entry per súmula: number, verbatim
  text, status, fonte (the listing URL).
- Same polite/idempotent/stdlib-only conventions as `scraper.py`.

## Common conventions

Both scripts follow the same shape:

## Usage

Both scrapers use the same `fetch` / `build` / `all` subcommand
interface.

```bash
# STF Súmulas Vinculantes
python3 scraper.py all                    # fetch + rebuild
python3 scraper.py all --force            # re-download all cached pages
python3 scraper.py fetch                  # refresh cache only (no YAML)
python3 scraper.py build                  # rebuild YAML from cache (no network)
python3 scraper.py build --output /tmp/svs.yaml

# TSE Súmulas
python3 tse.py all                        # fetch + rebuild
python3 tse.py fetch
python3 tse.py build --output /tmp/stse.yaml
```

## Cache

Each scraper has its own cache directory, both outside the git repo:
they're bulky raw HTML and reproducible from the courts on demand.
Only the parsed YAML outputs are committed.

| Scraper | Default cache | Env override |
|---|---|---|
| `scraper.py` | `~/research/data/sumulas_stf/` | `SUMULAS_CACHE` |
| `tse.py`     | `~/research/data/sumulas_tse/` | `TSE_CACHE`     |

```
~/research/data/sumulas_stf/
├── index.html        ← SV index page (used to discover internal IDs)
└── sv_NNN.html       ← detail page for SV NNN, one per súmula

~/research/data/sumulas_tse/
└── p_NNN.html        ← one file per pagination start (0, 20, 40, ...)
```

## Output

| Scraper | Default output | Env override |
|---|---|---|
| `scraper.py` | `<repo>/sumulas_vinculantes.yaml` | `SV_INDEX`   |
| `tse.py`     | `<repo>/sumulas_tse.yaml`         | `STSE_INDEX` |

These env vars are also read by `cite.py`'s resolvers, so changing
either path moves both the writer and the reader together.

## Cancellation tracking

**STF (`scraper.py`)**: STF marks cancelled SVs in the index page
with a `(cancelada)` tag, but auto-detection from the page text is
fragile — many SVs reference revoked statutes by quoting "revogada
pela EC X", and the detection false-positives. The scraper hard-codes
the set of cancelled SVs:

```python
KNOWN_CANCELLED = {9}  # SV 9 is the only cancelled SV as of 2026-04-09
```

When STF cancels another SV, update this set in `scraper.py` and
re-run `python3 scraper.py build`.

**TSE (`tse.py`)**: TSE marks cancellations as `(Cancelada)` directly
on the listing page, in plain text with no encoding obfuscation. The
scraper detects this automatically — no hard-coded list. When TSE
cancels a súmula, just re-run `tse.py all` and the status flips.

## Caveats

- **Publication date** (`publicacao`) is not auto-extracted by either
  scraper. STF detail pages don't expose a clean publication date for
  the SV itself (only dates of the underlying precedents); TSE has no
  publication-date field at all on the listing. The field is emitted
  as `null` and can be hand-filled when needed.
- **Portal HTML changes**: each parser uses two or three regexes
  tuned to the current portal layout. If STF or TSE redesigns their
  pages, the regexes will need updating. Both scrapers validate that
  the parsed súmula numbers form a contiguous run starting at 1 and
  warn on gaps — a cheap canary against silent breakage.
- **Per-súmula URLs**: STF exposes stable per-súmula detail URLs (the
  scraper records them in `fonte`). TSE does **not** — its detail
  pages live behind opaque IDs that change across redesigns, so all
  TSE entries point to the listing index URL instead.
- **Rate limiting**: 0.4 seconds between requests is conservative.
  Don't lower it without reason — both portals are federal services.
- **TLS**: both scrapers set `ssl.CERT_NONE`. The consequence of a
  MITM is reading public súmula text — no auth, no submitted data.

## Extending to other courts

Súmulas Vinculantes (STF) and Súmulas TSE are bulk-collected because
they're small, well-defined sets that are heavily cited in this repo.
**STJ, TST, and ordinary STF súmulas are not bulk-collected** by
design — see the policy in [`../../CLAUDE.md`](../../CLAUDE.md) under
"Citing Súmulas TSE". When a topical file cites one, add it by hand
to a future `sumulas_<court>.yaml` rather than scraping the full list.

If that policy ever changes, the cleanest path is to add a new file
to this directory (e.g., `stj.py`) following the same shape as
`scraper.py` (index → detail) or `tse.py` (paginated listing). The
two existing scrapers cover both common portal patterns:

- **`scraper.py` pattern**: index lists internal IDs; verbatim text
  is on per-súmula detail pages. Use this for portals that don't
  embed full text in the listing.
- **`tse.py` pattern**: paginated listing embeds the full verbatim
  text inline. Simpler when the portal supports it (typically
  Plone-based government sites).

When a third scraper appears, common helpers (HTTP fetch, SSL
context, YAML emission) should probably be factored into a shared
`_common.py` module. With only two, the small duplication is fine.

## See also

- [`../../sumulas_vinculantes.yaml`](../../sumulas_vinculantes.yaml) — STF SV output.
- [`../../sumulas_tse.yaml`](../../sumulas_tse.yaml) — TSE súmulas output.
- [`../leis_artigos/cite.py`](../leis_artigos/cite.py) — the resolver that consumes both YAMLs.
- [`../../CLAUDE.md`](../../CLAUDE.md) — citation format and the bulk-vs-lazy collection policy.
- [`../planalto_scraper/`](../planalto_scraper/) — the parallel scraper for federal legislation.
