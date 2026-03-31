from datetime import datetime, timezone

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    status_code: int
    detail: str
    path: str = Field(default="")
    timestamp: str


def build_error_response(status_code: int, detail: str, path: str) -> ErrorResponse:
    return ErrorResponse(
        status_code=status_code,
        detail=detail,
        path=path,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
