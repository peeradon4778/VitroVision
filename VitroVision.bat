@echo off
cd /d "%~dp0shelf_manager"
start "" "C:\Users\User\miniconda3\envs\ml\python.exe" main.py
:wait
timeout /t 1 /nobreak >nul
curl -s http://localhost:5001/api/ml_status >nul 2>&1
if errorlevel 1 goto wait
start "" http://localhost:5001