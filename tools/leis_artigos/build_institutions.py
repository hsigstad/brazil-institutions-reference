"""Build the consolidated institutions.db from the three source DBs.

This is the distributable database shipped as a GitHub release asset.
It bundles:

  - `artigo`, `amendment`          ← from artigos.db (statute text)
  - `cf_stf_anotacao`              ← from cf_stf_anotada.db (STF annotations on CF)
  - `ce_tse_anotacao`              ← from ce_anotado.db (TSE annotations on CE)

Each source DB has its own `anotacao` table, so they're renamed on merge
to avoid collision.

Usage:
    python3 build_institutions.py

    # Override paths:
    python3 build_institutions.py \\
        --artigos-db /path/to/artigos.db \\
        --cf-anotada-db /path/to/cf_stf_anotada.db \\
        --ce-anotado-db /path/to/ce_anotado.db \\
        --out /path/to/institutions.db
"""
from __future__ import annotations

import argparse
import os
import shutil
import sqlite3
import sys
from pathlib import Path

ARTIGOS_DB = Path(
    os.environ.get('ARTIGOS_DB',
                   Path.home() / 'research/data/lei/artigos.db')
)
CF_ANOTADA_DB = Path(__file__).resolve().parent.parent / 'stf_constituicao' / 'cf_stf_anotada.db'
CE_ANOTADO_DB = Path(__file__).resolve().parent.parent / 'tse_ce_anotado' / 'ce_anotado.db'
INSTITUTIONS_DB = Path(
    os.environ.get('INSTITUTIONS_DB',
                   Path.home() / 'research/data/institutions.db')
)


CF_ANOTACAO_SCHEMA = """
CREATE TABLE cf_stf_anotacao (
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
CREATE INDEX idx_cf_stf_anotacao_artigo ON cf_stf_anotacao(artigo);
CREATE INDEX idx_cf_stf_anotacao_tipo ON cf_stf_anotacao(tipo);
CREATE INDEX idx_cf_stf_anotacao_caso ON cf_stf_anotacao(caso);
"""

CE_ANOTACAO_SCHEMA = """
CREATE TABLE ce_tse_anotacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lei TEXT NOT NULL DEFAULT 'CE',
    artigo INTEGER NOT NULL,
    artigo_letra TEXT,
    tipo TEXT NOT NULL,
    referencia TEXT,
    texto TEXT NOT NULL
);
CREATE INDEX idx_ce_tse_anotacao_artigo ON ce_tse_anotacao(lei, artigo);
CREATE INDEX idx_ce_tse_anotacao_tipo ON ce_tse_anotacao(tipo);
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n', 1)[0])
    ap.add_argument('--artigos-db', type=Path, default=ARTIGOS_DB)
    ap.add_argument('--cf-anotada-db', type=Path, default=CF_ANOTADA_DB)
    ap.add_argument('--ce-anotado-db', type=Path, default=CE_ANOTADO_DB)
    ap.add_argument('--out', type=Path, default=INSTITUTIONS_DB)
    args = ap.parse_args()

    for label, p in [('artigos', args.artigos_db),
                     ('CF anotada', args.cf_anotada_db),
                     ('CE anotado', args.ce_anotado_db)]:
        if not p.exists():
            sys.exit(f'{label} DB not found: {p}')

    args.out.parent.mkdir(parents=True, exist_ok=True)

    print(f'Copying {args.artigos_db} → {args.out}', file=sys.stderr)
    shutil.copyfile(args.artigos_db, args.out)

    con = sqlite3.connect(str(args.out))
    cur = con.cursor()

    for name in ('cf_stf_anotacao', 'ce_tse_anotacao'):
        cur.execute(f'DROP TABLE IF EXISTS {name}')

    cur.executescript(CF_ANOTACAO_SCHEMA)
    cur.executescript(CE_ANOTACAO_SCHEMA)

    cur.execute(f"ATTACH DATABASE '{args.cf_anotada_db}' AS cf")
    cur.execute("""
        INSERT INTO cf_stf_anotacao (
            id, artigo, artigo_letra, tipo, caso,
            relator, data_julgamento, turma, texto, stf_links
        )
        SELECT id, artigo, artigo_letra, tipo, caso,
               relator, data_julgamento, turma, texto, stf_links
        FROM cf.anotacao
    """)
    cf_count = cur.execute('SELECT COUNT(*) FROM cf_stf_anotacao').fetchone()[0]
    con.commit()
    cur.execute('DETACH DATABASE cf')

    cur.execute(f"ATTACH DATABASE '{args.ce_anotado_db}' AS ce")
    cur.execute("""
        INSERT INTO ce_tse_anotacao (
            id, lei, artigo, artigo_letra, tipo, referencia, texto
        )
        SELECT id, lei, artigo, artigo_letra, tipo, referencia, texto
        FROM ce.anotacao
    """)
    ce_count = cur.execute('SELECT COUNT(*) FROM ce_tse_anotacao').fetchone()[0]
    con.commit()
    cur.execute('DETACH DATABASE ce')

    con.commit()

    artigo_count = cur.execute('SELECT COUNT(*) FROM artigo').fetchone()[0]
    amendment_count = cur.execute('SELECT COUNT(*) FROM amendment').fetchone()[0]

    con.execute('VACUUM')
    con.close()

    size_mb = args.out.stat().st_size / (1024 * 1024)
    print(f'  artigo: {artigo_count} rows', file=sys.stderr)
    print(f'  amendment: {amendment_count} rows', file=sys.stderr)
    print(f'  cf_stf_anotacao: {cf_count} rows', file=sys.stderr)
    print(f'  ce_tse_anotacao: {ce_count} rows', file=sys.stderr)
    print(f'Done. {args.out} ({size_mb:.1f} MB)', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
