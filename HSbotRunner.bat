@echo off
setlocal

set SCRIPT_DIR=%~dp0

cd /d %SCRIPT_DIR%

py -3.11 -m venv "MFB"
MFB\Scripts\python.exe prereqs_win.py
MFB\Scripts\python.exe main.py

endlocal
pause
