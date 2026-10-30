from importlib.metadata import version

from fastapi import FastAPI

from safrinha.api.schemas import HealthResponse


def create_app() -> FastAPI:
    """Build the FastAPI app.

    A factory instead of a module-level `app` lets each test build a fresh app
    and, later, inject fakes for the external services.
    """
    app = FastAPI(title="Safrinha", version=version("safrinha"))

    @app.get("/health")
    def health() -> HealthResponse:
        return HealthResponse(status="ok", version=app.version)

    return app
