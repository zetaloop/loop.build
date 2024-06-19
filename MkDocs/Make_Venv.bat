py -m venv venv
call venv\Scripts\activate.bat
pip install -U pip setuptools wheel
pip install mkdocs-material[imaging] mkdocs-git-revision-date-localized-plugin
pip install mkdocs-glightbox mkdocs-redirects mkdocs-minify-plugin
if "%MATERIAL_INSIDERS_GH_TOKEN%"=="" (
  echo "[WARNING] MATERIAL_INSIDERS_GH_TOKEN is empty"
) else (
  pip install git+https://%MATERIAL_INSIDERS_GH_TOKEN%@github.com/squidfunk/mkdocs-material-insiders.git
)
cd ..\loop_custom
call INSTALL.bat
exit
