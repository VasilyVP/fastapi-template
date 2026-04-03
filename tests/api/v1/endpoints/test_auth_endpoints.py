from collections.abc import Generator

from fastapi.testclient import TestClient
import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.core.security import decode_access_token, decode_refresh_token
from app.db.seed import seed_demo_data
from app.db.session import get_session
from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    # Use a dedicated in-memory DB for endpoint tests, shared via StaticPool.
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        seed_demo_data(session)

    def override_get_session() -> Generator[Session, None, None]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_login_returns_token_pair_for_valid_credentials(client: TestClient) -> None:
    response = client.post(
        "/v1/auth/token",
        data={"username": "johndoe", "password": "secret"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str) and data["access_token"]
    assert isinstance(data["refresh_token"], str) and data["refresh_token"]

    access_payload = decode_access_token(data["access_token"])
    refresh_payload = decode_refresh_token(data["refresh_token"])
    assert access_payload["sub"] == "johndoe"
    assert refresh_payload["sub"] == "johndoe"


def test_login_returns_400_for_invalid_credentials(client: TestClient) -> None:
    response = client.post(
        "/v1/auth/token",
        data={"username": "johndoe", "password": "wrong"},
    )

    assert response.status_code == 400
    data = response.json()
    assert data["status_code"] == 400
    assert data["detail"] == "Incorrect username or password"
    assert data["path"] == "/v1/auth/token"


def test_refresh_returns_new_access_token_for_valid_refresh_token(client: TestClient) -> None:
    login_response = client.post(
        "/v1/auth/token",
        data={"username": "johndoe", "password": "secret"},
    )
    refresh_token = login_response.json()["refresh_token"]

    response = client.post(
        "/v1/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    payload = decode_access_token(data["access_token"])
    assert payload["sub"] == "johndoe"


def test_refresh_returns_401_for_invalid_token(client: TestClient) -> None:
    response = client.post(
        "/v1/auth/refresh",
        headers={"Authorization": "Bearer not.a.valid.token"},
    )

    assert response.status_code == 401
    assert response.headers.get("www-authenticate") == "Bearer"
    data = response.json()
    assert data["status_code"] == 401
    assert data["detail"] == "Could not validate credentials"
    assert data["path"] == "/v1/auth/refresh"


def test_refresh_rejects_access_token_instead_of_refresh_token(client: TestClient) -> None:
    login_response = client.post(
        "/v1/auth/token",
        data={"username": "johndoe", "password": "secret"},
    )
    access_token = login_response.json()["access_token"]

    response = client.post(
        "/v1/auth/refresh",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 401
    data = response.json()
    assert data["status_code"] == 401
    assert data["detail"] == "Could not validate credentials"


def test_refresh_rejects_disabled_user(client: TestClient) -> None:
    login_response = client.post(
        "/v1/auth/token",
        data={"username": "alice", "password": "secret2"},
    )
    refresh_token = login_response.json()["refresh_token"]

    response = client.post(
        "/v1/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )

    assert response.status_code == 401
    data = response.json()
    assert data["status_code"] == 401
    assert data["detail"] == "Could not validate credentials"
