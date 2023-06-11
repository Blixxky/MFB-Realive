@echo off
setlocal

py -3 -m venv "MFB"
MFB\Scripts\python.exe -m pip install -r requirements_win.txt
MFB\Scripts\python.exe main.py
endlocal
pause
