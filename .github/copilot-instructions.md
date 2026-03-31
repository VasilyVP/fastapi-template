# Project Guidelines

## Build and Test
- Use `make` as the primary command interface.
- Install dependencies with `make install`.
- Start the development server with `make dev`.
- This project targets Python 3.14+ and uses `uv` for environment and dependency management.
- `pyrightconfig.json` uses strict type checking. Keep new code fully typed and compatible with strict Pyright.
- On Windows, do not switch `make dev` to `uv run fastapi ...`. In this repo the reliable CLI form is `uv run python -m fastapi dev ./app/main.py`.

## Architecture
- Keep the current layered structure in `app/`: `api` for HTTP routes and dependencies, `services` for business logic, `repositories` for data access, `schemas` for request and response models, `core` for settings and security helpers, and `db` for backing data sources.
- Add new HTTP endpoints under `app/api/v1/endpoints/` and register them through the existing router pattern instead of mounting ad hoc routes in `app/main.py`.
- Keep `app/main.py` focused on app setup, router registration, docs wiring, and global exception handling.
- Reuse the standardized error response shape from `app/schemas/error.py` for application errors rather than returning custom payloads per endpoint.

## Conventions
- Prefer `Annotated[..., Depends(...)]` for FastAPI dependencies and keep reusable dependency aliases in `app/api/dependencies.py` when they are shared across endpoints.
- Keep repository and service logic out of route handlers. Route functions should coordinate dependencies, call a service or repository, and return schemas.
- Follow the existing singleton pattern for shared repositories and services when extending the current in-memory template structure.
- Keep schemas split by domain under `app/schemas/`, and use separate models when persisted data differs from public API data.
- Configuration is loaded through `app/core/config.py` with `BaseSettings` and a cached `get_settings()` helper. Validate required settings through that path rather than reading environment variables directly in endpoints or services.
- Preserve async signatures for repositories and request handlers where the existing code is async, even if the current mock backend is in-memory.

## Key References
- See `README.md` for setup, route overview, demo credentials, and environment variables.
- Use `app/main.py`, `app/api/dependencies.py`, `app/core/config.py`, `app/services/auth_service.py`, and `app/schemas/error.py` as the primary examples for new code.
