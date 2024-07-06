@echo off

if exist venv (
  echo [ERROR] venv already exists
  pause
  exit
)

if "%MATERIAL_INSIDERS_GH_TOKEN%"=="" (
  echo [WARNING] MATERIAL_INSIDERS_GH_TOKEN is empty
  pause
)

py -m venv venv
if not exist venv\Scripts\activate.bat (
  echo [ERROR] venv failed to create
  pause
  exit
)

call venv\Scripts\activate.bat
py -m pip install -U pip setuptools wheel
pip install mkdocs-material[imaging] mkdocs-git-revision-date-localized-plugin
pip install mkdocs-glightbox mkdocs-redirects mkdocs-minify-plugin
if not "%MATERIAL_INSIDERS_GH_TOKEN%" == "" (
  pip install git+https://%MATERIAL_INSIDERS_GH_TOKEN%@github.com/squidfunk/mkdocs-material-insiders.git
)
cd ..\loop_custom
call INSTALL.bat
exit
