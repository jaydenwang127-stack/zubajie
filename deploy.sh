#!/bin/sh
# Rebuild site/ and publish it to the gh-pages branch (what GitHub Pages serves).
set -e
cd "$(dirname "$0")"
python3 build_site.py
git add -A && git commit -qm "Rebuild site" || true
git push origin main
git push origin "$(git subtree split --prefix site main)":gh-pages --force
echo "Published. GitHub Pages updates in about a minute."
