call venv\Scripts\activate.bat
chcp 65001>nul
title (venv)^> mkdocs build
mkdocs build
echo.
echo ✅ Build complete -^> ./site/
echo.
echo 💕 Press any key to continue...
pause>nul
