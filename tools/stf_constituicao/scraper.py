#!/usr/bin/env python3
"""
STF "A Constituição e o Supremo" scraper.

Fetches the STF's annotated Constitution via the JSON API at
constituicao.stf.jus.br and builds a SQLite database mapping each
CF article to its STF jurisprudence annotations.

# INTENT
# Produce cf_stf_anotada.db so that cite.py can optionally show
# STF jurisprudence annotations alongside CF article text.
#
# REASONING
# The STF publishes a SPA at constituicao.stf.jus.br with a clean
# REST API (/api/v1/dispositivo, /api/v1/comentario). Each CF article
# has grouped comments (controle concentrado, repercussão geral,
# julgados correlatos) containing HTML with case citations, relator,
# date, and links to STF portal. ~700 articles; variable comment density.
#
# Stdlib only (urllib + re + html + json + sqlite3).

Usage:
    python3 scraper.py fetch        # download article list + comments to cache
    python3 scraper.py build        # parse cached JSON -> SQLite
    python3 scraper.py all          # fetch + build
    python3 scraper.py --help

Cache:
    ~/research/data/stf_constituicao/      (override with STF_CF_CACHE)
    ├── titles.json
    ├── articles/                           (one JSON per title)
    └── comments/                          (one JSON per article)

Output:
    <script_dir>/cf_stf_anotada.db         (override with STF_CF_DB)
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sqlite3
import ssl
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Optional

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

API_BASE = "https://constituicao.stf.jus.br/api/v1"
DEFAULT_CACHE = Path.home() / "research" / "data" / "stf_constituicao"
DEFAULT_DB = Path(__file__).resolve().parent / "cf_stf_anotada.db"
DELAY = 0.3  # seconds between API calls

log = logging.getLogger("stf_constituicao")

# ---------------------------------------------------------------------------
# HTML text extractor
# ---------------------------------------------------------------------------


class _TextExtractor(HTMLParser):
    """Strip HTML tags, keeping text content."""

    def __init__(self):
        super().__init__()
        self.parts: list[str] = []
        self._links: list[str] = []

    def handle_data(self, data):
        self.parts.append(data)

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v:
                    self._links.append(v)

    def get_text(self) -> str:
        return re.sub(r"\s+", " ", "".join(self.parts)).strip()

    def get_links(self) -> list[str]:
        return self._links


def strip_html(html_str: str) -> tuple[str, list[str]]:
    """Return (plain_text, [urls])."""
    ext = _TextExtractor()
    ext.feed(html_str)
    return ext.get_text(), ext.get_links()


def extract_cases(html_str: str) -> list[dict]:
    """Extract case citations from an HTML comment block."""
    text, links = strip_html(html_str)

    # Pattern: [CASE_NAME, rel. min. NAME, j. DATE, TURMA/P, PUBLICATION]
    # or: [CASE_NAME, ...]
    cases = []

    # Find bracketed citation blocks
    for m in re.finditer(
        r"\[([A-Z]{2,}[\s.]*[\d.]+[^,\]]*?)(?:,\s*rel\.?\s*min\.?\s*([^,\]]+?))?(?:,\s*j\.\s*([\d/.-]+[^,\]]*?))?(?:,\s*(\d[ªºa]?\s*T|P)\b)?",
        text,
    ):
        case_id = re.sub(r"\s+", " ", m.group(1)).strip()
        relator = m.group(2).strip() if m.group(2) else None
        date = m.group(3).strip() if m.group(3) else None
        turma = m.group(4).strip() if m.group(4) else None
        cases.append(
            {
                "caso": case_id,
                "relator": relator,
                "data": date,
                "turma": turma,
            }
        )

    return cases


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------


def _api_get(path: str) -> dict:
    """Fetch a JSON endpoint from the STF API."""
    url = f"{API_BASE}{path}"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        url, headers={"User-Agent": "brazil-institutions-scraper/1.0"}
    )
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        return json.loads(resp.read())


def fetch(cache_dir: Path) -> None:
    """Download all titles, articles, and comments to cache."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    art_dir = cache_dir / "articles"
    com_dir = cache_dir / "comments"
    art_dir.mkdir(exist_ok=True)
    com_dir.mkdir(exist_ok=True)

    # Step 1: Titles
    titles_file = cache_dir / "titles.json"
    if titles_file.exists():
        log.info("Using cached titles")
        titles = json.loads(titles_file.read_text())["data"]
    else:
        log.info("Fetching titles...")
        resp = _api_get("/dispositivo/titulos")
        titles_file.write_text(json.dumps(resp, ensure_ascii=False, indent=2))
        titles = resp["data"]
        time.sleep(DELAY)

    # Step 2: Articles per title
    all_articles = []
    for title in titles:
        tid = title["id"]
        af = art_dir / f"title_{tid}.json"
        if af.exists():
            arts = json.loads(af.read_text())["data"]
        else:
            log.info("Fetching articles for %s (id=%d)...", title["descricao"][:40], tid)
            resp = _api_get(f"/dispositivo/artigos/{tid}")
            af.write_text(json.dumps(resp, ensure_ascii=False, indent=2))
            arts = resp["data"]
            time.sleep(DELAY)
        all_articles.extend(arts)

    log.info("Total articles: %d", len(all_articles))

    # Step 3: Comments per article
    fetched = 0
    skipped = 0
    errors = 0
    for art in all_articles:
        aid = art["id"]
        cf = com_dir / f"art_{aid}.json"
        if cf.exists():
            skipped += 1
            continue
        try:
            resp = _api_get(f"/comentario/dispositivo/{aid}")
            cf.write_text(json.dumps(resp, ensure_ascii=False, indent=2))
            fetched += 1
        except Exception as e:
            # Some articles may not have comments or may error
            cf.write_text(json.dumps({"data": [], "error": str(e)}))
            errors += 1
        time.sleep(DELAY)
        if (fetched + errors) % 50 == 0:
            log.info("  Progress: %d fetched, %d errors, %d skipped", fetched, errors, skipped)

    log.info("Comments: %d fetched, %d errors, %d cached/skipped", fetched, errors, skipped)


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

SCHEMA = """\
CREATE TABLE IF NOT EXISTS anotacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artigo INTEGER NOT NULL,
    artigo_letra TEXT,
    tipo TEXT NOT NULL,
    caso TEXT,
    relator TEXT,
    data_julgamento TEXT,
    turma TEXT,
    texto TEXT NOT NULL,
    stf_links TEXT
);

CREATE INDEX IF NOT EXISTS idx_cf_artigo ON anotacao(artigo);
CREATE INDEX IF NOT EXISTS idx_cf_tipo ON anotacao(tipo);
CREATE INDEX IF NOT EXISTS idx_cf_caso ON anotacao(caso);
"""


def build(cache_dir: Path, db_path: Path) -> None:
    """Parse cached JSON into SQLite."""
    art_dir = cache_dir / "articles"
    com_dir = cache_dir / "comments"

    # Load all articles to build id→number mapping
    art_map = {}  # id → (artigo_num, artigo_letra)
    for af in sorted(art_dir.glob("title_*.json")):
        data = json.loads(af.read_text()).get("data", [])
        for art in data:
            num_raw = art["numeroItem"].strip()
            m = re.match(r"(\d+)([A-Z-]*)", num_raw)
            if m:
                art_map[art["id"]] = (int(m.group(1)), m.group(2) or None)

    log.info("Article map: %d entries", len(art_map))

    # Parse comments
    rows = []
    for cf in sorted(com_dir.glob("art_*.json")):
        aid = int(cf.stem.split("_")[1])
        if aid not in art_map:
            continue
        artigo, letra = art_map[aid]

        data = json.loads(cf.read_text()).get("data", [])
        for group in data:
            tipo = group.get("tipo", "unknown")
            for comment in group.get("comentarios", []):
                html_desc = comment.get("descricao", "")
                if not html_desc:
                    continue

                text, links = strip_html(html_desc)
                if not text or len(text) < 10:
                    continue

                # Extract case citations
                cases = extract_cases(html_desc)
                stf_links = [l for l in links if "stf.jus.br" in l]

                if cases:
                    for case in cases:
                        rows.append(
                            {
                                "artigo": artigo,
                                "artigo_letra": letra,
                                "tipo": tipo,
                                "caso": case["caso"],
                                "relator": case["relator"],
                                "data_julgamento": case["data"],
                                "turma": case["turma"],
                                "texto": text,
                                "stf_links": "; ".join(stf_links) if stf_links else None,
                            }
                        )
                else:
                    # No extractable case — store the text anyway
                    rows.append(
                        {
                            "artigo": artigo,
                            "artigo_letra": letra,
                            "tipo": tipo,
                            "caso": None,
                            "relator": None,
                            "data_julgamento": None,
                            "turma": None,
                            "texto": text,
                            "stf_links": "; ".join(stf_links) if stf_links else None,
                        }
                    )

    log.info("Parsed %d annotation rows", len(rows))

    # Write DB
    if db_path.exists():
        db_path.unlink()

    con = sqlite3.connect(str(db_path))
    con.executescript(SCHEMA)
    con.executemany(
        "INSERT INTO anotacao (artigo, artigo_letra, tipo, caso, relator, "
        "data_julgamento, turma, texto, stf_links) "
        "VALUES (:artigo, :artigo_letra, :tipo, :caso, :relator, "
        ":data_julgamento, :turma, :texto, :stf_links)",
        rows,
    )
    con.commit()

    # Summary stats
    count = con.execute("SELECT COUNT(*) FROM anotacao").fetchone()[0]
    arts = con.execute("SELECT COUNT(DISTINCT artigo) FROM anotacao").fetchone()[0]
    with_case = con.execute("SELECT COUNT(*) FROM anotacao WHERE caso IS NOT NULL").fetchone()[0]
    tipos = con.execute(
        "SELECT tipo, COUNT(*) FROM anotacao GROUP BY tipo ORDER BY COUNT(*) DESC"
    ).fetchall()
    con.close()

    log.info("Wrote %d annotations for %d articles to %s", count, arts, db_path)
    log.info("  %d with extracted case citations", with_case)
    log.info("By type:")
    for tipo, cnt in tipos:
        log.info("  %-45s %d", tipo, cnt)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser(
        description="Scrape STF 'A Constituição e o Supremo' into SQLite.",
    )
    ap.add_argument(
        "command",
        choices=["fetch", "build", "all"],
        help="fetch = download JSON; build = parse -> DB; all = both",
    )
    ap.add_argument(
        "--cache",
        type=Path,
        default=Path(os.environ.get("STF_CF_CACHE", str(DEFAULT_CACHE))),
    )
    ap.add_argument(
        "--db",
        type=Path,
        default=Path(os.environ.get("STF_CF_DB", str(DEFAULT_DB))),
    )
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    if args.command in ("fetch", "all"):
        fetch(args.cache)

    if args.command in ("build", "all"):
        build(args.cache, args.db)

    return 0


if __name__ == "__main__":
    sys.exit(main())
