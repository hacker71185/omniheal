import uvicorn
import os
import sys

# Ensure current directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    print("=" * 60)
    print("  OMNIHEAL™ AUTONOMOUS ENDPOINT DIAGNOSTICS & HEALING AGENT")
    print("  Endpoint Engine v2.4.0 (Windows / Linux / macOS)")
    print("  Listening on: http://127.0.0.1:8765")
    print("=" * 60)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8765, reload=False, log_level="info")
