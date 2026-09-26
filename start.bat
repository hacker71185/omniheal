@echo off
title OmniHeal - Autonomous Endpoint Diagnostics & Self-Healing Engine
color 0b

echo ===============================================================================
echo     OMNIHEAL™ - AUTONOMOUS ENDPOINT DIAGNOSTICS & SELF-HEALING ENGINE
echo ===============================================================================
echo.
echo [*] Initializing OmniHeal Endpoint Agent and Command Center...
echo.

:: Start Python Backend in background
echo [+] Starting FastAPI Local Agent on http://127.0.0.1:8765 ...
start "OmniHeal Backend Agent" cmd /k "cd backend && python run_agent.py"

:: Wait 2 seconds for backend to initialize
timeout /t 2 /nobreak >nul

:: Start Frontend Vite server
echo [+] Starting React Command Center UI on http://127.0.0.1:5173 ...
cd frontend
start "OmniHeal Web UI" cmd /k "npm run dev -- --host 127.0.0.1 --port 5173"

:: Launch default browser
timeout /t 3 /nobreak >nul
start http://127.0.0.1:5173

echo.
echo ===============================================================================
echo     OmniHeal is active!
echo     - Command Center UI: http://127.0.0.1:5173
echo     - Local Agent API:   http://127.0.0.1:8765
echo     - API Docs:          http://127.0.0.1:8765/docs
echo ===============================================================================
echo.
pause
