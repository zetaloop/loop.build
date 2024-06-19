#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -U pip setuptools wheel
pip install mkdocs-material[imaging] mkdocs-git-revision-date-localized-plugin
pip install mkdocs-glightbox mkdocs-redirects mkdocs-minify-plugin
if [ -z "$MATERIAL_INSIDERS_GH_TOKEN" ]; then
  pip install mkdocs-material
else
  pip install git+https://${MATERIAL_INSIDERS_GH_TOKEN}@github.com/squidfunk/mkdocs-material-insiders.git
cd ../loop_custom
bash INSTALL.sh
exit
