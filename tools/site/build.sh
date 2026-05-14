#!/bin/bash
# Build / deploy the brazil-institutions public reference site.
#
#   bash tools/site/build.sh build    # build to build/site/
#   bash tools/site/build.sh deploy   # build + push to the gh-pages branch
#
# The site is PUBLIC — it carries only institutional reference material
# (topical notes + verbatim statute text from artigos.db). It is served
# at https://hsigstad.github.io/brazil-institutions/.
#
# Build requires: python3 with mistune + pyyaml. Statute text and law
# pages additionally require the consolidated artigos.db — locate it via
# $INSTITUTIONS_DB or place it at <workspace>/data/lei/artigos.db. The
# build degrades gracefully without it (citations stay plain, no law pages).

set -euo pipefail
REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
MODE="${1:-build}"
REMOTE="git@github.com:hsigstad/brazil-institutions.git"

build_site() {
    echo "=== Building brazil-institutions site ==="
    python3 "$REPO_DIR/tools/site/build_site.py"
}

deploy_site() {
    local src="$REPO_DIR/build/site"
    if [[ ! -d "$src" ]]; then
        echo "ERROR: $src does not exist. Run 'bash tools/site/build.sh build' first."
        exit 1
    fi
    echo ""
    echo "=== Deploying to GitHub Pages (hsigstad/brazil-institutions gh-pages) ==="
    TMPDIR=$(mktemp -d)
    if git ls-remote --exit-code --heads "$REMOTE" gh-pages >/dev/null 2>&1; then
        git clone --quiet --single-branch -b gh-pages "$REMOTE" "$TMPDIR"
    else
        echo "  gh-pages branch does not exist yet; initializing..."
        git clone --quiet "$REMOTE" "$TMPDIR"
        cd "$TMPDIR"
        git checkout --orphan gh-pages
        git rm -rf --quiet . 2>/dev/null || true
        cd "$REPO_DIR"
    fi
    rsync -a --delete --exclude='.git' "$src/" "$TMPDIR/"
    touch "$TMPDIR/.nojekyll"   # serve files as-is, no Jekyll processing
    cd "$TMPDIR"
    git add -A
    if git diff --cached --quiet; then
        echo "  No changes to deploy."
    else
        git commit -m "Deploy brazil-institutions site" --quiet
        git push --quiet -u origin gh-pages
        echo "  → https://hsigstad.github.io/brazil-institutions/"
    fi
    rm -rf "$TMPDIR"
    cd "$REPO_DIR"
}

case "$MODE" in
    build)  build_site ;;
    deploy) build_site; deploy_site ;;
    *) echo "Usage: bash tools/site/build.sh [build|deploy]"; exit 1 ;;
esac
