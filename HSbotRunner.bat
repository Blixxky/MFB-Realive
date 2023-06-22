@echo off
setlocal

py -3 -m venv "MFB"
MFB\Scripts\python.exe prereqs_win.py
MFB\Scripts\python.exe main.py
endlocal
pause
