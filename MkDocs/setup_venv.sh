#!/bin/bash

set -e

if [ -d "venv" ]; then
  echo "[ERROR] venv already exists"
  exit
fi

if [ -z "$MATERIAL_INSIDERS_GH_TOKEN" ]; then
  echo "[WARNING] MATERIAL_INSIDERS_GH_TOKEN is empty, using public version instead"
fi

python3 -m venv venv
source venv/bin/activate
python3 -m pip install -U pip setuptools wheel
pip install mkdocs-material[imaging] mkdocs-git-revision-date-localized-plugin
pip install mkdocs-glightbox mkdocs-redirects mkdocs-minify-plugin
pip install beautifulsoup4 lxml
if [ -n "$MATERIAL_INSIDERS_GH_TOKEN" ]; then
  # pip install git+https://${MATERIAL_INSIDERS_GH_TOKEN}@github.com/squidfunk/mkdocs-material-insiders.git
  pip install git+https://${MATERIAL_INSIDERS_GH_TOKEN}@github.com/zetasp/mkdocs-material-insiders.git
fi
cd ../loop_custom
bash INSTALL.sh
exit
