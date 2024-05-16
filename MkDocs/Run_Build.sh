#!/bin/bash

source venv/bin/activate
echo "(venv)> mkdocs build"
mkdocs build
echo
echo -e "✅ Build complete -> ./site/"

