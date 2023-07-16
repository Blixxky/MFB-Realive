@echo off

REM Create virtual environment
py -3.11 -m venv MFB

REM Activate virtual environment
call MFB\Scripts\activate

REM Install requirements
pip install -r requirements_win.txt
