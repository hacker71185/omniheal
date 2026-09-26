#!/usr/bin/env bash
# OmniHeal Autonomous Endpoint Engine Launcher

set -e

echo "==============================================================================="
echo "    OMNIHEAL™ - AUTONOMOUS ENDPOINT DIAGNOSTICS & SELF-HEALING ENGINE"
echo "==============================================================================="

# Start backend
echo "[+] Starting FastAPI Local Agent on http://127.0.0.1:8765 ..."
(cd backend && python3 run_agent.py) &
BACKEND_PID=$!

# Wait for backend
sleep 2

# Start frontend
echo "[+] Starting React Command Center UI on http://127.0.0.1:5173 ..."
(cd frontend && npm run dev -- --host 127.0.0.1 --port 5173) &
FRONTEND_PID=$!

echo "[+] OmniHeal is running!"
echo "    - UI:   http://127.0.0.1:5173"
echo "    - API:  http://127.0.0.1:8765"

# Trap interrupt to cleanly terminate both
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM
wait
