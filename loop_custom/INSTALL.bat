cd %~dp0
call ..\MkDocs\venv\Scripts\activate.bat
pip uninstall loop_custom -y
echo.
pip install .
echo.
rmdir /s /q build
echo Deleted .\build
echo.
rmdir /s /q loop_custom.egg-info
echo Deleted .\loop_custom.egg-info
echo.
pause
