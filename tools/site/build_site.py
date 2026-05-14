#!/usr/bin/env python3
"""Static-site generator for the brazil-institutions reference.

Renders the topical markdown files and the artigos.db statute database into
a public, browsable site. Backtick legal citations (`CPC.144.§3`) get a
hover tooltip with the verbatim article text and link to the law page.
Institutional concepts declared in concepts.yaml get a browsable index and
stable `I:slug` anchors that other project sites link to.

Usage:
  python3 tools/site/build_site.py             # build to build/site/
  python3 tools/site/build_site.py --out DIR   # custom output dir
"""
from __future__ import annotations

import argparse
import html
import os
import re
import sqlite3
import sys
from pathlib import Path

import mistune

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CITE_DIR = REPO_ROOT / "tools" / "leis_artigos"
DEFAULT_OUT = REPO_ROOT / "build" / "site"

# Root-level reference files to publish (everything else at the root —
# CLAUDE.md, README.md, TODO.md, AUDITING.md, CONTRIBUTING.md — is repo
# meta and stays out of the site).
ROOT_REF_FILES = [
    "siglas.md", "glossario.md", "timeline.md", "jurisprudencia-stf.md",
    "pitfalls.md", "quasi-experimentos.md", "faq.md", "data_pointers.md",
]

SITE_TITLE = "Brazilian Institutions"
SITE_TAGLINE = ("A working reference on Brazil's legal and administrative "
                "system for empirical research.")


# ---------------------------------------------------------------------------
# Legal-citation resolver (cite.py + artigos.db) — optional, degrades cleanly
# ---------------------------------------------------------------------------

def _load_cite():
    """Import the cite module and point it at artigos.db. Returns it or None."""
    if not CITE_DIR.is_dir():
        return None
    db_candidates = [
        Path(os.environ["INSTITUTIONS_DB"]) if os.environ.get("INSTITUTIONS_DB") else None,
        REPO_ROOT.parent.parent.parent / "data" / "lei" / "artigos.db",
        REPO_ROOT / "tools" / "leis_artigos" / "artigos.db",
    ]
    for db in db_candidates:
        if db and db.is_file():
            os.environ["INSTITUTIONS_DB"] = str(db)
            break
    sys.path.insert(0, str(CITE_DIR))
    try:
        import cite as cite_mod
        return cite_mod
    except Exception:
        return None


_CITE = _load_cite()
_LEGAL_CACHE: dict[str, str] = {}


def _lookup_legal_text(citation, raw: str) -> str:
    """Verbatim text for a parsed citation — statute, súmula, or case."""
    try:
        if getattr(citation, "is_case", False):
            entry = _CITE.lookup_case(citation.identifier)
            if entry:
                holding = entry.get("holding_short") or entry.get("tese_certificada") or ""
                status = entry.get("status", "")
                parts = [raw]
                if holding:
                    parts.append(holding[:300])
                if status:
                    parts.append(f"[{status}]")
                return " — ".join(parts)
            return ""
        for flag, fn in (("is_sv", "lookup_sv"), ("is_stse", "lookup_stse"),
                         ("is_sstj", "lookup_sstj"), ("is_stst", "lookup_stst")):
            if getattr(citation, flag, False):
                entry = getattr(_CITE, fn)(citation.identifier)
                if entry and entry.get("enunciado"):
                    return f"{raw} — {entry['enunciado'][:400]}"
                return ""
        rows = _CITE.resolve(citation)
        texts = [r["texto"][:300] for r in rows[:3] if r["texto"]]
        return " | ".join(texts)
    except Exception:
        return ""


def resolve_legal_citations(html_text: str, law_prefix: str) -> str:
    """Turn backtick citations (<code>…</code>) into tooltip'd legal chips.

    `law_prefix` is the relative path from the current page to laws/ (e.g.
    "../laws/" for a topic page, "laws/" for a root page).
    """
    if _CITE is None:
        return html_text

    def _replacer(m):
        content = m.group(1)
        try:
            c = _CITE.parse(content)
        except Exception:
            return m.group(0)  # not a legal citation — leave as plain code
        if content in _LEGAL_CACHE:
            tooltip = _LEGAL_CACHE[content]
        else:
            tooltip = _lookup_legal_text(c, content)
            _LEGAL_CACHE[content] = tooltip
        title = f' title="{html.escape(tooltip)}"' if tooltip else ""

        href = None
        if getattr(c, "is_case", False) or getattr(c, "is_sv", False) \
                or getattr(c, "is_stse", False) or getattr(c, "is_sstj", False) \
                or getattr(c, "is_stst", False):
            href = None  # no dedicated page for jurisprudence/súmulas yet
        elif c.identifier in _LAW_STEMS:
            anchor = content.replace(".", "-").replace("§", "p")
            href = f"{law_prefix}{c.identifier}.html"
            if anchor != c.identifier:  # article-level — link to the anchor
                href += f"#{anchor}"

        if href:
            return (f'<a class="legal-cite" href="{href}"{title}>'
                    f'{html.escape(content)}</a>')
        return f'<code class="legal-cite"{title}>{html.escape(content)}</code>'

    return re.sub(r"<code>([^<]+)</code>", _replacer, html_text)


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

_md = mistune.create_markdown(
    escape=False, plugins=["table", "strikethrough", "footnotes", "task_lists"])


def _slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text).lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s+", "-", text)


def _add_heading_ids(html_text: str) -> str:
    def repl(m):
        tag, attrs, content = m.group(1), m.group(2) or "", m.group(3)
        if "id=" in attrs:
            return m.group(0)
        return f'<{tag}{attrs} id="{_slugify(content)}">{content}</{tag}>'
    return re.sub(r"<(h[1-6])([^>]*)>(.*?)</\1>", repl, html_text, flags=re.DOTALL)


def _rewrite_md_links(html_text: str, page_map: dict[str, str], prefix: str) -> str:
    """Rewrite href="X.md" and bare `X.md` mentions to the site page."""
    def href_repl(m):
        pre, href, suf = m.group(1), m.group(2), m.group(3)
        if href.startswith(("http://", "https://", "mailto:", "#")):
            return m.group(0)
        base, _, anchor = href.partition("#")
        stem = Path(base).name[:-3] if base.endswith(".md") else None
        if stem and stem in page_map:
            new = prefix + page_map[stem] + (f"#{anchor}" if anchor else "")
            return f'{pre}"{new}"{suf}'
        return m.group(0)
    html_text = re.sub(r'(href=)"([^"]*)"([^>]*>)', href_repl, html_text)

    def bare_repl(m):
        pre, name = m.group(1), m.group(2)
        stem = name[:-3]
        if stem in page_map:
            return f'{pre}<a href="{prefix}{page_map[stem]}">{name}</a>'
        return m.group(0)
    return re.sub(r'((?:^|[>\s(]))([a-zA-Z0-9_-]+\.md)\b', bare_repl, html_text)


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------

CSS = """\
:root{--bg:#faf9f6;--card:#fffefa;--fg:#1a1a1a;--muted:#6b6860;--link:#1d4ed8;
--border:#e5e2db;--code-bg:#f0ede6;--code-block-bg:#f5f3ee;--accent:#1d4ed8;
--legal-bg:#fdf8e8;--legal-border:#e5d48b;--header-h:52px}
@media(prefers-color-scheme:dark){:root{--bg:#1a1916;--card:#222018;--fg:#e5e3dc;
--muted:#9a968c;--link:#7aa2f7;--border:#3a3830;--code-bg:#2a2820;
--code-block-bg:#252318;--legal-bg:#2a2510;--legal-border:#8b7a30}}
*{margin:0;padding:0;box-sizing:border-box}
body{font:17px/1.65 Georgia,"Times New Roman",serif;color:var(--fg);background:var(--bg)}
.header{position:sticky;top:0;height:var(--header-h);background:var(--card);
border-bottom:1px solid var(--border);display:flex;align-items:center;
padding:0 1.6rem;gap:1.4rem;z-index:50;
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
.header a{color:var(--muted);text-decoration:none;font-size:.86rem}
.header a:hover{color:var(--fg)}
.header .brand{color:var(--fg);font-weight:600;font-size:.98rem;margin-right:auto}
main{max-width:54rem;margin:0 auto;padding:2.2rem 1.6rem 5rem}
a{color:var(--link);text-decoration:none}
a:hover{text-decoration:underline}
h1,h2,h3,h4{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
line-height:1.3;margin:1.6em 0 .5em;scroll-margin-top:calc(var(--header-h) + 1rem)}
[id]{scroll-margin-top:calc(var(--header-h) + 1rem)}
h1{font-size:1.7rem;margin-top:0;border-bottom:1px solid var(--border);padding-bottom:.35rem}
h2{font-size:1.3rem}h3{font-size:1.08rem}h4{font-size:.98rem}
p{margin:.7em 0}ul,ol{margin:.5em 0 .5em 1.6em}li{margin:.2em 0}
table{border-collapse:collapse;margin:1em 0;font-size:.9rem;
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
th,td{border:1px solid var(--border);padding:.4em .7em;text-align:left;vertical-align:top}
th{background:var(--code-block-bg);font-weight:600}
pre{background:var(--code-block-bg);padding:1em;border-radius:6px;overflow-x:auto;
font-size:.84rem;margin:1em 0;border:1px solid var(--border)}
code{background:var(--code-bg);padding:.12em .35em;border-radius:3px;
font:.86em "SF Mono",Consolas,Menlo,monospace}
pre code{background:none;padding:0}
blockquote{border-left:3px solid var(--accent);padding:.7em 1em;color:var(--muted);
margin:1em 0;background:var(--code-block-bg);border-radius:0 5px 5px 0}
hr{border:none;border-top:1px solid var(--border);margin:2em 0}
.legal-cite{background:var(--legal-bg);border:1px solid var(--legal-border);
border-radius:3px;cursor:help;white-space:nowrap;color:var(--fg);
font:.84em "SF Mono",Consolas,Menlo,monospace;padding:.05em .35em}
a.legal-cite{text-decoration:none}a.legal-cite:hover{text-decoration:underline}
.concept-ref{border-bottom:1px dotted var(--link);text-decoration:none}
.concept-ref:hover{text-decoration:none;border-bottom-style:solid}
.law-chapter{margin-top:1.8em;color:var(--muted);font-size:1.15rem}
.law-section{margin-top:1.1em;color:var(--muted);font-size:.98rem;font-style:italic}
.law-caput{margin:.9em 0 .25em;font-weight:500}
.law-path{margin:.2em 0 .2em 2em;font-size:.96em}
.lead{color:var(--muted);font-size:1.05rem}
.col-list{columns:2;column-gap:2.4rem;list-style:none;margin:.6em 0;padding:0}
.col-list li{break-inside:avoid;padding:.18em 0}
.dir-section{margin-top:2.2rem}
.dir-section h2{font-size:1rem;color:var(--muted);text-transform:uppercase;
letter-spacing:.04em;border:none;margin-bottom:.4rem}
.concept{padding:.5em 0;border-bottom:1px solid var(--border)}
.concept .c-title{font-weight:600}
.concept .c-id{font:.8em "SF Mono",Consolas,monospace;color:var(--muted);margin-left:.4em}
.concept .c-summary{font-size:.92rem;color:var(--muted);margin-top:.15em}
footer{max-width:54rem;margin:0 auto;padding:1.5rem 1.6rem;color:var(--muted);
font-size:.82rem;border-top:1px solid var(--border)}
"""

PAGE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Brazilian Institutions</title>
<link rel="stylesheet" href="{prefix}style.css">
</head>
<body>
<header class="header">
  <a class="brand" href="{prefix}index.html">Brazilian Institutions</a>
  <a href="{prefix}index.html">Topics</a>
  <a href="{prefix}laws/index.html">Laws</a>
  <a href="{prefix}concepts.html">Concepts</a>
</header>
<main>
{content}
</main>
<footer>
  Reference for empirical research on Brazil's legal and administrative
  system. Generated from
  <a href="https://github.com/hsigstad/brazil-institutions">hsigstad/brazil-institutions</a>;
  statute text from the consolidated <code>artigos.db</code>.
</footer>
</body>
</html>
"""


def _page(title: str, content: str, prefix: str) -> str:
    return PAGE.format(title=html.escape(title), content=content, prefix=prefix)


def _title_of(md_text: str, fallback: str) -> str:
    m = re.match(r"^#\s+(.+)", md_text, re.MULTILINE)
    return m.group(1).strip() if m else fallback


def _first_para(md_text: str) -> str:
    """First prose paragraph after the H1 — used as a directory blurb."""
    body = re.sub(r"^#\s+.+", "", md_text, count=1, flags=re.MULTILINE).strip()
    for block in body.split("\n\n"):
        block = block.strip()
        if block and not block.startswith(("#", "**Topics", "**Snapshot", "-", "|")):
            return re.sub(r"\s+", " ", re.sub(r"[`*]", "", block))[:200]
    return ""


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------

_LAW_STEMS: set[str] = set()  # populated by build_law_pages, used by resolver
_CONCEPTS: dict[str, dict] = {}  # I:slug -> concept dict; populated in main()


def _load_concepts(page_map: dict[str, str]) -> dict[str, dict]:
    """Load concepts.yaml and resolve each concept's page to a site path."""
    cpath = REPO_ROOT / "concepts.yaml"
    if not cpath.is_file():
        return {}
    import yaml
    data = yaml.safe_load(cpath.read_text(encoding="utf-8")) or {}
    out: dict[str, dict] = {}
    for slug, c in (data.get("concepts") or {}).items():
        c = dict(c)
        c["rel_html"] = page_map.get(Path(c.get("page", "")).stem, "")
        out[slug.lower()] = c
    return out


def _link_concept_refs(html_text: str, prefix: str) -> str:
    """Replace bare I:slug tokens with a link whose text is the concept title.

    I:slug is an authoring shorthand — readers see the concept's canonical
    title (e.g. "2015 civil procedure reform"), never the slug. Tokens
    already inside an <a> are left alone; unknown slugs stay as plain text.
    """
    if not _CONCEPTS:
        return html_text
    pattern = re.compile(
        r"(<a\b[^>]*>.*?</a>)|(<[^>]+>)|(\bI:([A-Za-z0-9][A-Za-z0-9-]*))",
        re.DOTALL)

    def repl(m):
        if m.group(1) or m.group(2):
            return m.group(0)
        token, slug = m.group(3), m.group(4).lower()
        c = _CONCEPTS.get(slug)
        if not c or not c.get("rel_html"):
            return token
        href = prefix + c["rel_html"]
        if c.get("anchor"):
            href += f"#{c['anchor']}"
        tip = f' title="{html.escape(c["summary"])}"' if c.get("summary") else ""
        return (f'<a class="concept-ref" href="{href}"{tip}>'
                f'{html.escape(c.get("title", token))}</a>')

    return pattern.sub(repl, html_text)


def build_law_pages(out_dir: Path) -> list[tuple[str, str]]:
    """One page per law in artigos.db. Returns [(apelido, law_title), …]."""
    db = Path(os.environ.get("INSTITUTIONS_DB", ""))
    if not db.is_file():
        print("  laws/ (skipped — artigos.db not found)")
        return []
    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row
    laws = [r[0] for r in con.execute(
        "SELECT DISTINCT apelido FROM artigo WHERE apelido IS NOT NULL "
        "ORDER BY apelido")]
    laws_dir = out_dir / "laws"
    laws_dir.mkdir(parents=True, exist_ok=True)
    built: list[tuple[str, str]] = []

    for apelido in laws:
        rows = con.execute(
            "SELECT * FROM artigo WHERE apelido = ? AND vigente_ate IS NULL "
            "ORDER BY ordem ASC", [apelido]).fetchall()
        if not rows:
            continue
        numero, ano = rows[0]["numero_lei"] or "", rows[0]["ano_lei"] or ""
        law_title = apelido + (f" — Lei {numero}/{ano}" if numero and ano else "")
        parts, cur_cap, cur_sec = [], None, None
        for row in rows:
            cap, sec = row["capitulo_titulo"], row["secao_titulo"]
            if cap and cap != cur_cap:
                parts.append(f'<h2 class="law-chapter">Cap. '
                             f'{html.escape(row["capitulo"] or "")} &mdash; '
                             f'{html.escape(cap)}</h2>')
                cur_cap, cur_sec = cap, None
            if sec and sec != cur_sec:
                parts.append(f'<h3 class="law-section">Seção '
                             f'{html.escape(row["secao"] or "")} &mdash; '
                             f'{html.escape(sec)}</h3>')
                cur_sec = sec
            art_id = f"{apelido}.{row['artigo']}"
            if row["artigo_letra"]:
                art_id += f"-{row['artigo_letra']}"
            path = row["path"] or ""
            if path and path != "caput":
                art_id += f".{path}"
            anchor = art_id.replace(".", "-").replace("§", "p")
            cls = "law-caput" if path == "caput" else "law-path"
            parts.append(f'<p class="{cls}" id="{html.escape(anchor)}">'
                         f'{html.escape(row["texto"] or "")}</p>')
        content = f"<h1>{html.escape(law_title)}</h1>\n" + "\n".join(parts)
        (laws_dir / f"{apelido}.html").write_text(
            _page(law_title, content, "../"), encoding="utf-8")
        built.append((apelido, law_title))
    con.close()

    items = "".join(
        f'<li><a href="{html.escape(ap)}.html">{html.escape(ap)}</a> '
        f'<span class="c-summary">{html.escape(t)}</span></li>'
        for ap, t in built)
    idx = (f"<h1>Laws</h1>\n<p class='lead'>{len(built)} statutes in the "
           f"consolidated database. Article text is served verbatim; "
           f"backtick citations across the site link here.</p>\n"
           f'<ul class="col-list">{items}</ul>')
    (laws_dir / "index.html").write_text(
        _page("Laws", idx, "../"), encoding="utf-8")
    print(f"  laws/ ({len(built)} law pages)")
    return built


def build_md_page(md_path: Path, out_path: Path, page_map: dict[str, str],
                  prefix: str) -> None:
    text = md_path.read_text(encoding="utf-8")
    title = _title_of(text, md_path.stem)
    body = _add_heading_ids(_md(text))
    body = _rewrite_md_links(body, page_map, prefix)
    body = resolve_legal_citations(body, f"{prefix}laws/")
    body = _link_concept_refs(body, prefix)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(_page(title, body, prefix), encoding="utf-8")


def build_concepts_page(out_dir: Path) -> int:
    """Render the concept manifest into a browsable index."""
    if not _CONCEPTS:
        return 0
    rows = []
    for slug in sorted(_CONCEPTS):
        c = _CONCEPTS[slug]
        href = c.get("rel_html", "")
        if href and c.get("anchor"):
            href += f"#{c['anchor']}"
        title = html.escape(c.get("title", slug))
        title_html = f'<a href="{href}">{title}</a>' if href else title
        rows.append(
            f'<div class="concept"><span class="c-title">{title_html}</span>'
            f'<span class="c-id">I:{html.escape(slug)}</span>'
            f'<div class="c-summary">{html.escape(c.get("summary", ""))}</div></div>')
    content = (
        "<h1>Institutional concepts</h1>\n"
        "<p class='lead'>Named institutions, doctrines, and reform episodes. "
        "Project sites cite these as <code>I:slug</code> tokens, which render "
        "as the concept's title and link back here.</p>\n" + "\n".join(rows))
    (out_dir / "concepts.html").write_text(
        _page("Institutional concepts", content, ""), encoding="utf-8")
    print(f"  concepts.html ({len(_CONCEPTS)} concepts)")
    return len(_CONCEPTS)


def build_index(out_dir: Path, topics: list[tuple[str, str, str]],
                refs: list[tuple[str, str]], n_laws: int, n_concepts: int) -> None:
    def _topic_li(stem, title, blurb):
        return (f'<li><a href="topics/{stem}.html">{html.escape(title)}</a>'
                + (f' <span class="c-summary">— {html.escape(blurb)}</span>'
                   if blurb else "") + "</li>")
    topic_items = "".join(_topic_li(s, t, b) for s, t, b in topics)
    ref_items = "".join(
        f'<li><a href="{s}.html">{html.escape(t)}</a></li>' for s, t in refs)
    content = f"""\
<h1>{html.escape(SITE_TITLE)}</h1>
<p class="lead">{html.escape(SITE_TAGLINE)}</p>
<div class="dir-section">
  <h2>Concepts &amp; Laws</h2>
  <ul class="col-list">
    <li><a href="concepts.html">Institutional concepts</a>
        <span class="c-summary">— {n_concepts} named doctrines &amp; reform episodes</span></li>
    <li><a href="laws/index.html">Laws</a>
        <span class="c-summary">— {n_laws} statutes, verbatim article text</span></li>
  </ul>
</div>
<div class="dir-section">
  <h2>Topics</h2>
  <ul>{topic_items}</ul>
</div>
<div class="dir-section">
  <h2>Reference</h2>
  <ul class="col-list">{ref_items}</ul>
</div>
"""
    (out_dir / "index.html").write_text(
        _page(SITE_TITLE, content, ""), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the brazil-institutions site")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    out_dir = args.out.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    topic_files = sorted((REPO_ROOT / "topics").glob("*.md"))
    ref_files = [REPO_ROOT / f for f in ROOT_REF_FILES
                 if (REPO_ROOT / f).is_file()]

    # page_map: md stem -> site-relative html path (for link rewriting)
    page_map: dict[str, str] = {}
    for p in topic_files:
        page_map[p.stem] = f"topics/{p.stem}.html"
    for p in ref_files:
        page_map[p.stem] = f"{p.stem}.html"

    global _CONCEPTS
    _CONCEPTS = _load_concepts(page_map)

    print(f"brazil-institutions site → {out_dir}")
    if _CITE is None:
        print("  (cite.py/artigos.db unavailable — citations stay plain)")

    built_laws = build_law_pages(out_dir)
    _LAW_STEMS.update(ap for ap, _ in built_laws)

    for p in topic_files:
        build_md_page(p, out_dir / "topics" / f"{p.stem}.html", page_map, "../")
    print(f"  topics/ ({len(topic_files)} topic pages)")

    for p in ref_files:
        build_md_page(p, out_dir / f"{p.stem}.html", page_map, "")
    print(f"  reference ({len(ref_files)} pages)")

    n_concepts = build_concepts_page(out_dir)

    topics_meta = []
    for p in topic_files:
        t = p.read_text(encoding="utf-8")
        topics_meta.append((p.stem, _title_of(t, p.stem), _first_para(t)))
    refs_meta = [(p.stem, _title_of(p.read_text(encoding="utf-8"), p.stem))
                 for p in ref_files]
    build_index(out_dir, topics_meta, refs_meta, len(built_laws), n_concepts)

    (out_dir / "style.css").write_text(CSS, encoding="utf-8")
    print(f"  index.html + style.css\n"
          f"Done: {len(topic_files)} topics + {len(ref_files)} reference + "
          f"{len(built_laws)} laws + {n_concepts} concepts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
