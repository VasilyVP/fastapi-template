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
