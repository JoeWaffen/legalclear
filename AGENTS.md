# LegalClear — Agent instructions

## Project
Full-stack AI legal document explanation product.
Backend: FastAPI + Python 3.11
Frontend: React + Vite + TailwindCSS
Mobile: React Native + Expo
Database: Supabase (Postgres)
Payments: Stripe
AI: Anthropic API (claude-sonnet-4-6, claude-haiku-4-5-20251001)

## Python environment rules
Use uv for ALL Python environment and package management.
- Create venv: uv venv --python 3.11
- Install: uv pip install -r requirements.txt
- Run: uv run python script.py
- Never use pip directly. Never use python3 directly.
- Venv lives at backend/.venv/

## Port rules — critical
LegalClear FastAPI backend runs on port 8001.
Nemotron inference container runs on port 8000.
Never change the backend port to 8000.
Never change any API URL to use port 8000.

## Build rules
Complete each phase fully before starting the next.
Run the verification test at the end of each phase.
Fix all failing assertions before proceeding.
Print PHASE N COMPLETE when all checks pass.
If a test fails more than twice print PHASE N BLOCKED and stop.

## Code style
Python: PEP 8, type hints on all function signatures.
Always use async/await for IO operations.
All agent methods return typed dicts.
JSON parsing: always strip markdown fences before json.loads().
