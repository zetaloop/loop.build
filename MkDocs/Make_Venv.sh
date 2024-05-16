#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -U pip setuptools wheel
pip install mkdocs-material mkdocs-glightbox mkdocs-redirects mkdocs-minify-plugin
cd ../loop_custom
bash INSTALL.sh
exit

