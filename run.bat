@echo off
rem Jalankan Sahabat KB di Windows
cd /d %~dp0
if not exist .venv ( python -m venv .venv )
call .venv\Scripts\activate
pip install -q -r requirements.txt
python app.py
pause
