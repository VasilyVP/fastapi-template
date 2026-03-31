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

The `Makefile` is the preferred interface for project commands. `make install` installs dependencies, and `make dev` wraps the underlying FastAPI command for this repo.

## Environment Variables

The app validates settings on startup. These values are required:

- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`

Optional settings:

- `APP_NAME` defaults to `FastAPI Template`
- `ADMIN_EMAIL`
- `ITEMS_PER_USER` defaults to `50`

Example `.env`:

```env
SECRET_KEY=change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=FastAPI Template
ADMIN_EMAIL=admin@example.com
ITEMS_PER_USER=50
```

## API Docs

- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI: `http://127.0.0.1:8000/v1/openapi.json`

## Route Overview

### System

- `GET /v1/` returns a simple health-style response
- `GET /v1/info` returns selected runtime settings
- `GET /v1/models/{model_name}` demonstrates enum path parameters
- `GET /v1/exception` exercises the custom exception handlers

### Items

- `GET /v1/items/{item_id}` reads an item with query parameters
- `POST /v1/items/{item_id}` replaces item data
- `PATCH /v1/items/{item_id}` partially updates item data

### Users

- `GET /v1/users/` demonstrates shared query parameter models
- `GET /v1/users/me` returns the authenticated user
- `GET /v1/authorized` returns the authenticated active user

### Auth

- `POST /v1/token` exchanges username and password for a bearer token

## Demo Users

- `johndoe` / `secret`
- `alice` / `secret2`

`alice` is disabled and cannot access endpoints that require an active user.

## Auth Flow

Request a token:

```bash
curl -X POST "http://127.0.0.1:8000/v1/token" ^
    -H "Content-Type: application/x-www-form-urlencoded" ^
    -d "username=johndoe&password=secret"
```

Use the returned token:

```bash
curl "http://127.0.0.1:8000/v1/users/me" ^
    -H "Authorization: Bearer <access_token>"
```

Protected endpoints return `401` for missing, malformed, invalid, or expired tokens. Disabled users are rejected before access is granted.

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
