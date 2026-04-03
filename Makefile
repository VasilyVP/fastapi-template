# Install project dependencies
install:
	@uv sync

# Run test suite
test:
	@uv run pytest

# Run fastapi development server
#@fastapi dev main.py
dev:
	@uv run python -m fastapi dev ./app/main.py

prod:
	@uv run granian --interface asgi app.main:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1
