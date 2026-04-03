from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse

from app.api.docs import versioned_swagger_ui_html
from app.api.v1.router import api_router
from app.core.config import lifespan
from app.schemas.error import build_error_response


API_V1_PREFIX = "/v1"

app = FastAPI(
    title="FastAPI Template",
    version="1.0.0",
    lifespan=lifespan,
    openapi_url=f"{API_V1_PREFIX}/openapi.json",
    docs_url=None,
    redoc_url=None,
)
app.include_router(api_router, prefix=API_V1_PREFIX)


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html() -> HTMLResponse:
    return versioned_swagger_ui_html(
        doc_versions=[{"url": f"{API_V1_PREFIX}/openapi.json", "name": "v1"}],
        title=f"{app.title} - API Docs",
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    response = build_error_response(exc.status_code, str(exc.detail), request.url.path)
    headers = exc.headers or None
    return JSONResponse(
        status_code=exc.status_code, content=response.model_dump(), headers=headers
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    response = build_error_response(500, str(exc), request.url.path)
    return JSONResponse(status_code=500, content=response.model_dump())
