from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common import simulate_image_to_url_pipeline, simulate_import_db_beauty_pipeline


app = FastAPI(
    title="Jenkins Dummy APIs",
    description="Dummy endpoints that simulate NOC Jenkins pipeline responses.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, Any]:
    return {
        "message": "Jenkins Dummy APIs",
        "description": "Use POST /image-to-url or POST /import-db-beauty to simulate pipeline responses.",
        "endpoints": ["/image-to-url", "/import-db-beauty", "/health"],
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/image-to-url")
def image_to_url(payload: dict[str, Any]) -> dict[str, Any]:
    return simulate_image_to_url_pipeline(payload)


@app.post("/import-db-beauty")
def import_db_beauty(payload: dict[str, Any]) -> dict[str, Any]:
    return simulate_import_db_beauty_pipeline(payload)
