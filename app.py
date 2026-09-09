"""NEELGRIVA — application launcher.

This module lives at the repository root (NEELGRIVA/app.py) as required by
ARCHITECTURE.md. It exposes a single convenience entry point that boots the
FastAPI backend so the whole system (API + scientific modules + demo pipeline)
can be started with::

    python app.py

The frontend (React + MapLibre) is served from ``frontend/`` via Vite in
development and built into static assets for production. The backend serves the
built frontend in production when ``frontend/dist`` exists.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# Make backend importable as `app.*`
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))


def main() -> None:
    import uvicorn

    host = os.environ.get("APP_HOST", "0.0.0.0")
    port = int(os.environ.get("APP_PORT", "8000"))
    reload = os.environ.get("APP_ENV", "development") == "development"
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        reload_dirs=[str(BACKEND / "app")] if reload else None,
    )


if __name__ == "__main__":
    main()
