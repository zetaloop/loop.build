py -m venv venv
call venv\Scripts\activate.bat
pip install -U pip
pip install -U setuptools wheel
pip install mkdocs-material mkdocs-git-revision-date-localized-plugin
pip install mkdocs-glightbox mkdocs-redirects mkdocs-minify-plugin
cd ..\loop_custom
call INSTALL.bat
exit