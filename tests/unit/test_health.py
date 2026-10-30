from importlib.metadata import version

from fastapi.testclient import TestClient

from safrinha.api.main import create_app


def test_health_returns_status_and_version() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": version("safrinha")}
