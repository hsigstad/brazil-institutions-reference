#!/usr/bin/env python3
"""
STF Súmulas Vinculantes scraper.

Fetches all Súmulas Vinculantes from portal.stf.jus.br and writes
sumulas_vinculantes.yaml at the repo root with verbatim enunciado,
status, and source URLs.

# INTENT
# Reproduce sumulas_vinculantes.yaml from the canonical STF source.
# The YAML file is the source of truth for [[SV14]]-style bracket
# citations resolved by ../leis_artigos/cite.py. This scraper is the
# upstream pipeline.
#
# REASONING
# Súmulas Vinculantes are a closed, small, high-importance set (~63
# as of 2026) issued under CF Art. 103-A. Verbatim text matters because
# researchers quote them directly in papers — paraphrasing introduces
# transcription risk. The STF portal is the only authoritative source
# for verbatim text + cancellation status.
#
# Stdlib only (urllib + html.parser usage limited to regex extraction).
# No requests/bs4 dependency.

Usage:
    python3 scraper.py fetch              # download index + detail pages
    python3 scraper.py build              # parse cached pages -> YAML
    python3 scraper.py all                # fetch + build (full run)
    python3 scraper.py --help

Cache:
    ~/research/data/sumulas_stf/                (override with SUMULAS_CACHE)
    ├── index.html
    └── sv_NNN.html                             (one per súmula)

Output:
    <repo_root>/sumulas_vinculantes.yaml        (override with SV_INDEX)
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
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE = "https://portal.stf.jus.br/jurisprudencia/sumariosumulas.asp"
INDEX_URL = f"{BASE}?base=26"
DETAIL_URL = f"{BASE}?base=26&sumula={{internal_id}}"

CACHE_DIR = Path(
    os.environ.get(
        "SUMULAS_CACHE",
        Path.home() / "research" / "data" / "sumulas_stf",
    )
)

# Default output path: sumulas_vinculantes.yaml at the repo root, two
# directories above this script (tools/sumulas_scraper/scraper.py).
DEFAULT_OUTPUT = Path(
    os.environ.get(
        "SV_INDEX",
        Path(__file__).resolve().parent.parent.parent / "sumulas_vinculantes.yaml",
    )
)

REQUEST_DELAY = 0.4  # seconds; STF portal is mildly rate-limited
REQUEST_TIMEOUT = 30
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Manually maintained list of cancelled SVs. STF marks SV 9 as the only
# currently-cancelled súmula vinculante (as of 2026-04-09). Update this
# set if STF cancels more SVs in the future.
#
# REASONING: detection from page text is fragile (the word "cancelada"
# appears in many SVs as part of references to other things). The
# index page does mark cancellations with a "(cancela­da)" tag, but the
# detection is brittle enough that we keep the canonical list here.
KNOWN_CANCELLED = {9}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("sumulas_scraper")


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
def _ssl_context() -> ssl.SSLContext:
    # ASSUMES: STF portal occasionally serves a cert that the local CA
    # bundle doesn't trust. We disable verification because the only
    # consequence is reading public súmula text, not transmitting data.
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_url(url: str) -> str:
    """GET a URL with browser headers and a polite timeout."""
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
# Index parsing
# ---------------------------------------------------------------------------
INDEX_LINK_RE = re.compile(
    r"sumariosumulas\.asp\?base=26&sumula=(\d+)[^>]*>"
    r"\s*[^A-Za-z]*Súmula Vinculante[&nbsp;\s\xa0]*(\d+)"
)


def parse_index(html: str) -> List[Tuple[int, str]]:
    """Extract (sv_number, internal_id) pairs from the SV index page.

    The STF index links to detail pages by an internal numeric ID
    (e.g., sumula=1185), not by the SV number. We zip the link with
    the human-readable label that follows it.
    """
    pairs = [(int(m.group(2)), m.group(1)) for m in INDEX_LINK_RE.finditer(html)]
    if not pairs:
        raise RuntimeError(
            "No SV links found in index page — STF portal HTML may have changed. "
            "Inspect the cached index.html and update INDEX_LINK_RE."
        )
    # Validate: SV numbers should be a contiguous run starting at 1
    nums = sorted(n for n, _ in pairs)
    if nums[0] != 1 or nums != list(range(1, len(nums) + 1)):
        log.warning(
            "SV numbers are not a contiguous run from 1: got %d items, range %d-%d",
            len(nums), nums[0], nums[-1],
        )
    return pairs


# ---------------------------------------------------------------------------
# Detail parsing
# ---------------------------------------------------------------------------
def _strip_noise(html: str) -> str:
    """Remove svg/style/script blocks and unescape entities."""
    html = re.sub(r"<svg[^>]*>.*?</svg>", "", html, flags=re.DOTALL)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    return html


def _clean_text(s: str) -> str:
    """Strip remaining HTML tags and normalize whitespace."""
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"</p>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = htmlmod.unescape(s)
    s = s.replace("\u200b", "").replace("\xa0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()


PARCOM_RE = re.compile(r'<div class="parCOM">(.*?)</div>', re.DOTALL)


def parse_detail(html: str) -> Optional[str]:
    """Extract the verbatim enunciado from an SV detail page.

    The structure is:
        ... <h... class="...">Súmula Vinculante N</h...>
        <div class="parCOM"><div>VERBATIM TEXT</div></div>
        <div class="titulo">Precedente Representativo</div> ...

    We take the first parCOM div appearing after the "Súmula Vinculante"
    label. The first parCOM is consistently the enunciado; subsequent
    parCOMs hold precedents and theses.
    """
    html = _strip_noise(html)
    label_pos = html.find("Súmula Vinculante")
    if label_pos < 0:
        return None
    m = PARCOM_RE.search(html, label_pos)
    if not m:
        return None
    return _clean_text(m.group(1))


# ---------------------------------------------------------------------------
# YAML emission
# ---------------------------------------------------------------------------
HEADER = """\
# Súmulas Vinculantes — STF
#
# Closed set of binding interpretive theses issued by the Supremo
# Tribunal Federal under CF Art. 103-A. Each entry stores the
# verbatim enunciado as published by STF, the status, and the
# canonical source URL.
#
# Resolved via cite.py with bracket form `SV14`, `SV37`, etc.
# Documented in CLAUDE.md.
#
# Sources:
# - All entries scraped from portal.stf.jus.br by tools/sumulas_scraper/.
# - Verbatim enunciado matched against the first parCOM div on each
#   detail page.
#
# Status values:
#   vigente   — currently binding
#   cancelada — cancelled by STF (SV 9 is the only one as of 2026)
#   revogada  — formally revoked
#
# Fields:
#   numero     — SV number (matches the bracket-form id, e.g., 14 → `SV14`)
#   enunciado  — verbatim text as published by STF
#   status     — vigente | cancelada | revogada
#   fonte      — canonical STF portal URL
#   publicacao — DOU/DJE date (TODO: not auto-extracted; fill by hand when known)
#
# When adding/editing entries:
# - Preserve verbatim text. Do not paraphrase or reformat.
# - When STF cancels or revokes a SV, update status and add a
#   short note in a "nota" field explaining the change.

schema_version: 1
last_updated: {date}

sumulas:

"""


def _format_yaml_string(s: str) -> List[str]:
    """Format an enunciado for YAML output.

    Single-line strings are double-quoted with escapes. Multi-line
    strings use the literal block style (|) with 4-space indent to
    sit cleanly under the 2-space-indented field name.
    """
    if "\n" in s:
        out = ["    enunciado: |"]
        out.extend("    " + line for line in s.split("\n"))
        return out
    text = s.replace("\\", "\\\\").replace('"', '\\"')
    return [f'    enunciado: "{text}"']


def emit_yaml(entries: List[Dict], output_path: Path) -> None:
    """Write entries to output_path as a YAML file."""
    from datetime import date

    lines: List[str] = [HEADER.format(date=date.today().isoformat())]
    for e in entries:
        lines.append(f'  SV{e["numero"]}:')
        lines.append(f'    numero: {e["numero"]}')
        lines.append(f'    status: {e["status"]}')
        lines.extend(_format_yaml_string(e["enunciado"]))
        lines.append(f'    fonte: {e["fonte"]}')
        lines.append(f'    publicacao: null')
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines))
    log.info("wrote %d entries -> %s", len(entries), output_path)


# ---------------------------------------------------------------------------
# Pipeline phases
# ---------------------------------------------------------------------------
def cmd_fetch(force: bool = False) -> List[Tuple[int, str]]:
    """Download index + all detail pages into CACHE_DIR.

    Returns the (sv_number, internal_id) mapping for downstream use.
    Pages already on disk are skipped unless force=True.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    index_path = CACHE_DIR / "index.html"
    if not index_path.exists() or force:
        log.info("fetching index: %s", INDEX_URL)
        index_path.write_text(fetch_url(INDEX_URL))
        time.sleep(REQUEST_DELAY)
    else:
        log.info("index cached: %s", index_path)

    mapping = parse_index(index_path.read_text())
    log.info("found %d SVs in index", len(mapping))

    for sv_num, internal in mapping:
        out = CACHE_DIR / f"sv_{sv_num:03d}.html"
        if out.exists() and not force:
            continue
        url = DETAIL_URL.format(internal_id=internal)
        try:
            out.write_text(fetch_url(url))
            log.info("  SV %d (%s) -> %d bytes", sv_num, internal, out.stat().st_size)
        except Exception as exc:
            log.error("  SV %d FAILED: %s", sv_num, exc)
            continue
        time.sleep(REQUEST_DELAY)

    cached = sorted(CACHE_DIR.glob("sv_*.html"))
    log.info("cache populated: %d detail pages in %s", len(cached), CACHE_DIR)
    return mapping


def cmd_build(output_path: Path = DEFAULT_OUTPUT) -> None:
    """Parse cached pages and emit sumulas_vinculantes.yaml."""
    index_path = CACHE_DIR / "index.html"
    if not index_path.exists():
        raise SystemExit(
            f"index not cached at {index_path}. Run `scraper.py fetch` first."
        )

    mapping = parse_index(index_path.read_text())
    mapping_by_num = {n: i for n, i in mapping}

    entries: List[Dict] = []
    missing: List[int] = []
    for sv_num, internal in sorted(mapping):
        page = CACHE_DIR / f"sv_{sv_num:03d}.html"
        if not page.exists():
            missing.append(sv_num)
            continue
        enunciado = parse_detail(page.read_text())
        if not enunciado:
            log.warning("SV %d: enunciado not found in detail page", sv_num)
            missing.append(sv_num)
            continue
        entries.append({
            "numero": sv_num,
            "enunciado": enunciado,
            "status": "cancelada" if sv_num in KNOWN_CANCELLED else "vigente",
            "fonte": DETAIL_URL.format(internal_id=internal),
        })

    if missing:
        log.warning("missing/unparseable SVs: %s", missing)
    if not entries:
        raise SystemExit("no entries parsed; cache may be empty or corrupt")

    emit_yaml(entries, output_path)


def cmd_all(force: bool = False, output_path: Path = DEFAULT_OUTPUT) -> None:
    cmd_fetch(force=force)
    cmd_build(output_path=output_path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(
        description="Scrape STF Súmulas Vinculantes into sumulas_vinculantes.yaml.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Phases:\n"
            "  fetch  — download index + detail pages into the cache (idempotent)\n"
            "  build  — parse cached pages and write the YAML\n"
            "  all    — fetch + build\n"
            "\n"
            "Cache:  $SUMULAS_CACHE  (default: ~/research/data/sumulas_stf/)\n"
            "Output: $SV_INDEX       (default: <repo>/sumulas_vinculantes.yaml)\n"
        ),
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp_fetch = sub.add_parser("fetch", help="download index + detail pages")
    sp_fetch.add_argument("--force", action="store_true", help="re-download cached pages")

    sp_build = sub.add_parser("build", help="parse cached pages -> YAML")
    sp_build.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)

    sp_all = sub.add_parser("all", help="fetch + build")
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
