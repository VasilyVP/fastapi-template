# FastAPI Template

A small FastAPI template with versioned routes, JWT authentication, centralized error responses, and a layered application structure.

## Features

- API versioning under `/v1`
- Swagger UI at `/docs`
- JWT bearer token auth with Argon2 password hashing
- Settings loaded from `.env` with `pydantic-settings`
- Standardized error response payloads
- Layered structure for API, services, repositories, schemas, and data access

## Requirements

- Python 3.14+
- `uv`
- `make`

## Quick Start

1. Create a `.env` file in the project root.
1. Install dependencies:

```bash
make install
```

1. Start the development server:

```bash
make dev
```

The API will be available at `http://127.0.0.1:8000`.

The `Makefile` is the preferred interface for project commands. `make install` installs dependencies, `make test` runs the test suite, and `make dev` wraps the underlying FastAPI command for this repo.

## Run Tests

Run the full test suite with:

```bash
make test
```

## Environment Variables

The app validates settings on startup. These values are required:

- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `DATABASE_URL`

Optional settings:

- `APP_NAME` defaults to `FastAPI Template`
- `ADMIN_EMAIL`
- `ITEMS_PER_USER` defaults to `50`
- `REFRESH_TOKEN_EXPIRE_DAYS` defaults to `30`

Example `.env`:

```env
SECRET_KEY=change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30
DATABASE_URL=sqlite:///./app.db
APP_NAME=FastAPI Template
ADMIN_EMAIL=admin@example.com
ITEMS_PER_USER=50
```

## API Docs

- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI: `http://127.0.0.1:8000/v1/openapi.json`

## Demo Users

- `johndoe` / `secret`
- `alice` / `secret2`

`alice` is disabled and cannot access endpoints that require an active user.

## Auth Flow

Request login tokens:

```bash
curl -X POST "http://127.0.0.1:8000/v1/token" ^
    -H "Content-Type: application/x-www-form-urlencoded" ^
    -d "username=johndoe&password=secret"
```

The response includes `access_token` and `refresh_token`.

Use the access token:

```bash
curl "http://127.0.0.1:8000/v1/users/me" ^
    -H "Authorization: Bearer <access_token>"
```

Refresh an access token with the refresh token:

```bash
curl -X POST "http://127.0.0.1:8000/v1/refresh" ^
    -H "Authorization: Bearer <refresh_token>"
```

The refresh endpoint returns a new `access_token` only.

Protected endpoints return `401` for missing, malformed, invalid, or expired tokens. Refresh tokens are stateless and valid until expiry, but refresh requests are rejected if the resolved user is disabled.

## Error Response Shape

Application errors are normalized to this payload shape:

```json
{
    "status_code": 401,
    "detail": "Could not validate credentials",
    "path": "/v1/users/me",
    "timestamp": "2026-03-31T00:00:00+00:00"
}
```

## Project Structure

- `app/main.py` creates the FastAPI app, mounts versioned routes, and registers exception handlers
- `app/api` contains dependencies, docs helpers, and route modules
- `app/core` contains settings and security helpers
- `app/schemas` contains request and response models
- `app/services` contains business logic
- `app/repositories` contains data access abstractions
- `app/db` contains the current mock data source

## Development Notes

- The FastAPI CLI entrypoint is configured in `pyproject.toml` as `app.main:app`
- In this repo on Windows, `uv run fastapi dev ...` can fail because of a broken `fastapi.exe` shim
- `make dev` runs the reliable command: `uv run python -m fastapi dev ./app/main.py`
