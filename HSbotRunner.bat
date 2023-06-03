@echo off
setlocal

py -3 prereqs_win.py

REM Create the virtual environment
py -3.11 -m venv MFB
if errorlevel 1 (
    echo Python 3.11 not found, creating virtual environment with Python 3...
    py -3 -m venv MFB
)

REM Run your script in the virtual environment
MFB\Scripts\python.exe main.py

endlocal
