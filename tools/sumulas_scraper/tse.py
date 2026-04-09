#!/usr/bin/env python3
"""
TSE Súmulas scraper.

Fetches all numbered Súmulas-TSE from www.tse.jus.br and writes
sumulas_tse.yaml at the repo root with verbatim text, cancellation
status, and source URLs.

# INTENT
# Reproduce sumulas_tse.yaml from the canonical TSE source. The YAML
# is the source of truth for `STSE38`-style backtick citations resolved
# by ../leis_artigos/cite.py.
#
# REASONING
# TSE súmulas are a small (~72 as of 2026), high-relevance set for
# Brazilian electoral law. The TSE listing pages are paginated 20 per
# page and embed the full verbatim text of each súmula inline — no
# need to fetch detail pages, unlike STF SVs.
#
# Stdlib only (urllib + re + html). No requests/bs4 dependency.

Usage:
    python3 tse.py fetch              # download paginated listings
    python3 tse.py build              # parse cached pages -> YAML
    python3 tse.py all                # fetch + build
    python3 tse.py --help

Cache:
    ~/research/data/sumulas_tse/                (override with TSE_CACHE)
    └── p_NN.html                               (one per pagination start)

Output:
    <repo_root>/sumulas_tse.yaml                (override with STSE_INDEX)
"""

from __future__ import annotations

import argparse
import html as htmlmod
import logging
import os
import re
import ssl
import sys
import time
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
LISTING_URL = (
    "https://www.tse.jus.br/legislacao/codigo-eleitoral/sumulas/sumulas-do-tse"
    "?b_start:int={start}"
)
PAGE_SIZE = 20  # TSE Plone listing serves 20 items per page

CACHE_DIR = Path(
    os.environ.get(
        "TSE_CACHE",
        Path.home() / "research" / "data" / "sumulas_tse",
    )
)

DEFAULT_OUTPUT = Path(
    os.environ.get(
        "STSE_INDEX",
        Path(__file__).resolve().parent.parent.parent / "sumulas_tse.yaml",
    )
)

REQUEST_DELAY = 0.4
REQUEST_TIMEOUT = 30
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Maximum pages to scan before giving up. The TSE listing terminates
# when a page returns 0 items, so this is just a safety bound.
MAX_PAGES = 20

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("tse_scraper")


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
def _ssl_context() -> ssl.SSLContext:
    # ASSUMES: TSE portal cert validates fine in most environments,
    # but we keep verification permissive for parity with the STF
    # scraper. The consequence of MITM is reading public súmula text.
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_url(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        },
    )
    with urllib.request.urlopen(req, context=_ssl_context(), timeout=REQUEST_TIMEOUT) as r:
        return r.read().decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
# REASONING: TSE renders each súmula on the listing as a paragraph that
# starts with "Súmula-TSE nº N" optionally followed by "(Cancelada)".
# The full verbatim text continues until "Leia mais" (a link to the
# detail page) or the next "Súmula-TSE nº" header. Both terminators
# work as a non-greedy boundary in the regex below.
#
# We strip HTML to plain text first, then run the regex on cleaned
# text. This is more robust than parsing the (irregular) HTML structure.
SUMULA_RE = re.compile(
    r"Súmula-TSE\s*n[ºo°]\s*(\d+)\s*(\([^)]*\))?\s*(.*?)"
    r"(?=Súmula-TSE\s*n[ºo°]|\s*Leia mais|\Z)",
    re.DOTALL,
)


def _clean_html_to_text(html: str) -> str:
    """Strip noise tags + tags + entities to a flat text stream."""
    html = re.sub(r"<svg[^>]*>.*?</svg>", "", html, flags=re.DOTALL)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    html = re.sub(r"<[^>]+>", " ", html)
    text = htmlmod.unescape(html)
    text = text.replace("\u200b", "").replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_listing(html: str) -> List[Dict]:
    """Extract all súmula entries from one TSE listing page.

    Returns a list of dicts with keys: numero, status, enunciado.
    """
    text = _clean_html_to_text(html)
    out: List[Dict] = []
    for m in SUMULA_RE.finditer(text):
        num = int(m.group(1))
        marker = (m.group(2) or "").lower()
        body = m.group(3).strip()

        if "cancelada" in marker:
            status = "cancelada"
        elif "revogada" in marker:
            status = "revogada"
        elif "alterada" in marker:
            status = "alterada"
        else:
            status = "vigente"

        # Drop trailing "Leia mais…" or trailing dot+space artifacts
        body = re.sub(r"\s*Leia mais.*$", "", body).strip()
        out.append({"numero": num, "status": status, "enunciado": body})
    return out


# ---------------------------------------------------------------------------
# YAML emission
# ---------------------------------------------------------------------------
HEADER = """\
# Súmulas TSE — Tribunal Superior Eleitoral
#
# Numbered súmulas of the TSE consolidating electoral jurisprudence.
# Non-binding (no equivalent of súmula vinculante in the electoral
# justice system) but highly persuasive: TSE is the final word on
# electoral law and its súmulas are routinely cited as the operational
# rule by lower electoral courts.
#
# Resolved via cite.py with bracket form `STSE38`, `STSE47`, etc.
# Documented in CLAUDE.md.
#
# Sources:
# - All entries scraped from www.tse.jus.br/legislacao/codigo-eleitoral/sumulas/sumulas-do-tse
#   by tools/sumulas_scraper/tse.py.
# - Verbatim text matched against the TSE Plone listing (text inline,
#   no per-súmula detail-page fetches needed).
#
# Status values:
#   vigente   — currently in force
#   cancelada — explicitly cancelled by TSE (marked "(Cancelada)" on listing)
#   revogada  — formally revoked
#   alterada  — content altered by later resolução
#
# Fields:
#   numero     — TSE súmula number (matches the bracket-form id, e.g., 38 → `STSE38`)
#   enunciado  — verbatim text as published by TSE
#   status     — vigente | cancelada | revogada | alterada
#   fonte      — canonical TSE portal URL (listing page; TSE doesn't expose stable per-súmula URLs)
#
# When adding/editing entries:
# - Preserve verbatim text. Do not paraphrase or reformat.
# - Re-run tools/sumulas_scraper/tse.py to refresh from TSE.

schema_version: 1
last_updated: {date}

sumulas:

"""

LISTING_FONTE = (
    "https://www.tse.jus.br/legislacao/codigo-eleitoral/sumulas/sumulas-do-tse"
)


def _format_yaml_string(s: str) -> List[str]:
    if "\n" in s:
        out = ["    enunciado: |"]
        out.extend("    " + line for line in s.split("\n"))
        return out
    text = s.replace("\\", "\\\\").replace('"', '\\"')
    return [f'    enunciado: "{text}"']


def emit_yaml(entries: List[Dict], output_path: Path) -> None:
    from datetime import date

    lines: List[str] = [HEADER.format(date=date.today().isoformat())]
    for e in entries:
        lines.append(f'  STSE{e["numero"]}:')
        lines.append(f'    numero: {e["numero"]}')
        lines.append(f'    status: {e["status"]}')
        lines.extend(_format_yaml_string(e["enunciado"]))
        lines.append(f'    fonte: {LISTING_FONTE}')
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines))
    log.info("wrote %d entries -> %s", len(entries), output_path)


# ---------------------------------------------------------------------------
# Pipeline phases
# ---------------------------------------------------------------------------
def cmd_fetch(force: bool = False) -> None:
    """Download all paginated listing pages into CACHE_DIR.

    Walks pagination (start=0, 20, 40, ...) until a page yields 0
    súmulas, indicating the end of the listing.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    for page_idx in range(MAX_PAGES):
        start = page_idx * PAGE_SIZE
        out = CACHE_DIR / f"p_{start:03d}.html"
        if out.exists() and not force:
            html = out.read_text()
            entries = parse_listing(html)
            log.info("p_%03d cached: %d items", start, len(entries))
            if len(entries) == 0:
                break
            continue

        url = LISTING_URL.format(start=start)
        log.info("fetching %s", url)
        try:
            html = fetch_url(url)
        except Exception as exc:
            log.error("  page %d FAILED: %s", start, exc)
            break
        out.write_text(html)
        entries = parse_listing(html)
        log.info("  page %d -> %d items", start, len(entries))
        time.sleep(REQUEST_DELAY)
        if len(entries) == 0:
            break

    cached = sorted(CACHE_DIR.glob("p_*.html"))
    log.info("cache populated: %d pages in %s", len(cached), CACHE_DIR)


def cmd_build(output_path: Path = DEFAULT_OUTPUT) -> None:
    pages = sorted(CACHE_DIR.glob("p_*.html"))
    if not pages:
        raise SystemExit(
            f"no cached pages in {CACHE_DIR}. Run `tse.py fetch` first."
        )

    seen: Dict[int, Dict] = {}
    for p in pages:
        for entry in parse_listing(p.read_text()):
            n = entry["numero"]
            if n in seen:
                # ASSUMES: pagination overlap is impossible by design.
                # Warn if it happens (would indicate a Plone misconfig).
                log.warning("duplicate súmula %d across pages", n)
            seen[n] = entry

    if not seen:
        raise SystemExit("no entries parsed; cache may be empty or corrupt")

    nums = sorted(seen)
    log.info(
        "parsed %d súmulas, range %d-%d",
        len(seen), nums[0], nums[-1],
    )

    # Validate: TSE súmula numbers should be a contiguous run from 1.
    # Gaps indicate either parsing failures or that TSE has actually
    # removed (not just cancelled) some entries — both worth flagging.
    expected = set(range(1, nums[-1] + 1))
    missing = sorted(expected - set(nums))
    if missing:
        log.warning("missing súmula numbers (gaps): %s", missing)

    entries = [seen[n] for n in nums]
    emit_yaml(entries, output_path)


def cmd_all(force: bool = False, output_path: Path = DEFAULT_OUTPUT) -> None:
    cmd_fetch(force=force)
    cmd_build(output_path=output_path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(
        description="Scrape TSE Súmulas into sumulas_tse.yaml.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Phases:\n"
            "  fetch  — download paginated listings into the cache (idempotent)\n"
            "  build  — parse cached pages and write the YAML\n"
            "  all    — fetch + build\n"
            "\n"
            "Cache:  $TSE_CACHE   (default: ~/research/data/sumulas_tse/)\n"
            "Output: $STSE_INDEX  (default: <repo>/sumulas_tse.yaml)\n"
        ),
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp_fetch = sub.add_parser("fetch")
    sp_fetch.add_argument("--force", action="store_true")

    sp_build = sub.add_parser("build")
    sp_build.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)

    sp_all = sub.add_parser("all")
    sp_all.add_argument("--force", action="store_true")
    sp_all.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)

    args = ap.parse_args()

    if args.cmd == "fetch":
        cmd_fetch(force=args.force)
    elif args.cmd == "build":
        cmd_build(output_path=args.output)
    elif args.cmd == "all":
        cmd_all(force=args.force, output_path=args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
