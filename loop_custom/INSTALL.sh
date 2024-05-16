#!/bin/bash

cd "$(dirname "$0")"
source ../MkDocs/venv/bin/activate
pip uninstall loop_custom -y
echo
pip install .
echo
rm -rf build
echo "Deleted ./build"
echo
rm -rf loop_custom.egg-info
echo "Deleted ./loop_custom.egg-info"

