PORT ?= 8080

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
	@python -m granian --interface asgi --host 0.0.0.0 --port $(PORT) --workers 1 app.main:app
