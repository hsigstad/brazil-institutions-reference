#!/usr/bin/env python3
"""
TST Súmulas scraper via Playwright.

Fetches all TST Súmulas from jurisprudencia.tst.jus.br by intercepting
the SPA's API response, then writes sumulas_tst.yaml at the repo root.

# INTENT
# Produce sumulas_tst.yaml so that `STST<number>` backtick citations
# resolve via cite.py. TST súmulas are the labor-law equivalent of
# TSE súmulas — non-binding but operationally authoritative.
#
# REASONING
# The TST jurisprudence SPA blocks non-browser API access (nginx 405
# on POST). Playwright launches a real browser to capture the API
# response (~463 súmulas in one request). The scraped data includes
# verbatim text, status, history, and full precedente citations.
#
# Requires: playwright (pip install playwright && playwright install chromium)

Usage:
    python3 scraper.py fetch     # capture API response via browser
    python3 scraper.py build     # parse cached JSON -> YAML
    python3 scraper.py all       # fetch + build
    python3 scraper.py --help

Cache:
    ~/research/data/tst_sumulas/              (override with TST_CACHE)
    └── sumulas_raw.json

Output:
    <repo_root>/sumulas_tst.yaml              (override with STST_INDEX)
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
from pathlib import Path

log = logging.getLogger("tst_scraper")

DEFAULT_CACHE = Path.home() / "research" / "data" / "tst_sumulas"
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_INDEX = REPO_ROOT / "sumulas_tst.yaml"

TST_URL = "https://jurisprudencia.tst.jus.br/?tipoJuris=SUM&orgao=TST&pesquisar=1"


# ---------------------------------------------------------------------------
# Fetch via Playwright
# ---------------------------------------------------------------------------


def fetch(cache_dir: Path) -> Path:
    """Launch browser, navigate to TST SPA, intercept API response."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    out = cache_dir / "sumulas_raw.json"

    if out.exists():
        age_h = (time.time() - out.stat().st_mtime) / 3600
        if age_h < 24 * 7:
            log.info("Using cached %s (%.1f hours old)", out, age_h)
            return out

    from playwright.sync_api import sync_playwright

    results = []

    def _run():
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            def on_response(response):
                if "/rest/pesquisa-textual/1/1000" in response.url:
                    try:
                        results.append(json.loads(response.body()))
                    except Exception:
                        pass

            page.on("response", on_response)
            log.info("Navigating to %s ...", TST_URL)
            page.goto(TST_URL, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(5000)
            browser.close()

    _run()

    if not results:
        log.error("Failed to capture API response")
        return out

    out.write_text(json.dumps(results[0], ensure_ascii=False, indent=2))
    n = len(results[0].get("registros", []))
    log.info("Captured %d súmulas, saved to %s", n, out)
    return out


# ---------------------------------------------------------------------------
# Build YAML
# ---------------------------------------------------------------------------


def _strip_html(s: str) -> str:
    """Remove HTML tags, control characters, and normalize whitespace."""
    if not s:
        return ""
    t = re.sub(r"<[^>]+>", "", s)
    # Remove control characters that break YAML (U+0080–U+009F range)
    t = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _status_label(sit: dict) -> str:
    """Map TST situacao codes to our status vocabulary."""
    desc = sit.get("descricao", "").upper().strip()
    mapping = {
        "CRIADA": "vigente",
        "MANTIDA": "vigente",
        "ALTERADA": "alterada",
        "CANCELADA": "cancelada",
        "CONVERTIDA": "convertida",
        "INCORPORADA": "incorporada",
    }
    return mapping.get(desc, desc.lower())


def build(cache_dir: Path, index_path: Path) -> None:
    """Parse cached JSON into sumulas_tst.yaml."""
    raw_file = cache_dir / "sumulas_raw.json"
    if not raw_file.exists():
        log.error("No cached data at %s — run 'fetch' first", raw_file)
        return

    data = json.loads(raw_file.read_text())
    regs = data.get("registros", [])
    log.info("Parsing %d registros", len(regs))

    lines = [
        "# TST Súmulas — scraped from jurisprudencia.tst.jus.br",
        f"# {len(regs)} entries, scraped {time.strftime('%Y-%m-%d')}",
        "#",
        "# Resolved via `STST<number>` backtick citations in cite.py.",
        "# TST súmulas are non-binding but operationally authoritative",
        "# in the Justiça do Trabalho.",
        "",
        "sumulas:",
    ]

    # Count stats
    status_counts = {}
    for r in sorted(regs, key=lambda x: x["registro"].get("numero", 0)):
        reg = r["registro"]
        num = reg.get("numero")
        if num is None:
            continue

        titulo = _strip_html(reg.get("titulo", ""))
        tese = _strip_html(reg.get("tese", ""))
        historico = _strip_html(reg.get("historico", ""))
        sit = reg.get("situacao", {})
        status = _status_label(sit)
        pub = reg.get("dtaPublicacao", "")

        status_counts[status] = status_counts.get(status, 0) + 1

        precs = reg.get("precedentes", [])

        # Dict-keyed format matching sumulas_tse.yaml
        lines.append(f"  STST{num}:")
        lines.append(f"    numero: {num}")
        # Escape quotes in titulo for YAML
        titulo_escaped = titulo.replace('"', '\\"')
        lines.append(f"    titulo: \"{titulo_escaped}\"")

        # Multi-line enunciado
        if tese:
            lines.append("    enunciado: >")
            words = tese.split()
            line = "      "
            for w in words:
                if len(line) + len(w) + 1 > 78:
                    lines.append(line.rstrip())
                    line = "      " + w + " "
                else:
                    line += w + " "
            if line.strip():
                lines.append(line.rstrip())

        lines.append(f"    status: {status}")
        if pub:
            lines.append(f"    publicacao: \"{pub}\"")
        if historico:
            hist_short = historico[:200] + ("..." if len(historico) > 200 else "")
            hist_escaped = hist_short.replace('"', '\\"')
            lines.append(f"    historico: \"{hist_escaped}\"")
        if precs:
            lines.append(f"    precedentes: {len(precs)}")
        lines.append("    fonte: https://jurisprudencia.tst.jus.br/?tipoJuris=SUM&orgao=TST&pesquisar=1")
        lines.append("")

    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log.info("Wrote %s with %d súmulas", index_path, len(regs))
    log.info("By status: %s", status_counts)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser(
        description="Scrape TST Súmulas via Playwright.",
    )
    ap.add_argument("command", choices=["fetch", "build", "all"])
    ap.add_argument("--cache", type=Path,
                    default=Path(os.environ.get("TST_CACHE", str(DEFAULT_CACHE))))
    ap.add_argument("--index", type=Path,
                    default=Path(os.environ.get("STST_INDEX", str(DEFAULT_INDEX))))
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    if args.command in ("fetch", "all"):
        fetch(args.cache)
    if args.command in ("build", "all"):
        build(args.cache, args.index)

    return 0


if __name__ == "__main__":
    sys.exit(main())
