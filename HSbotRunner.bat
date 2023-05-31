py -3.11 -m venv "%~dp0MFB"
MFB\Scripts\python.exe -m pip install -r requirements_win.txt
MFB\Scripts\python.exe main.py
pause