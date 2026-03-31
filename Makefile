# Install project dependencies
install:
	@uv sync

# Run fastapi development server
#@fastapi dev main.py
dev:
	@uv run python -m fastapi dev ./app/main.py
