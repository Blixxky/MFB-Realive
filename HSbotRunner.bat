@echo off
setlocal

py -3 prereqs_win.py

py -3.11 -m venv "MFB"
if errorlevel 1 (
    echo Python 3.11 not found, creating virtual environment with Python 3...
    py -3 -m venv MFB
)
MFB\Scripts\python.exe main.py
endlocal
pause
