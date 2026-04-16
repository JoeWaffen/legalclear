# LegalClear Build Rules

Always use port 8001 for the LegalClear FastAPI backend.
Never use port 8000 for the LegalClear app — that port
belongs to the Nemotron inference container.

Always use uv commands. Never use pip or python3 directly.
Run tests with: uv run python test_phaseN.py

Every API endpoint except /health, /eligibility, /webhook
requires X-API-Key header matching settings.API_KEY.

All agent system prompts must use cache_control ephemeral
for prompt caching.

All JSON responses from agents must strip markdown fences
before parsing with json.loads().
