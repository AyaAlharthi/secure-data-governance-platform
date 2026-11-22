from fastapi import FastAPI

from app.schemas.response import HealthResponse
from app.api import assets, auth

app = FastAPI(
    title="Secure Data Governance Platform",
    description="A platform for managing and protecting organizational data",
    version="1.0.0"
)

app.include_router(assets.router)
app.include_router(auth.router)


@app.get("/", response_model=HealthResponse)
def home():
    return {
        "message": "Secure Data Governance Platform is running",
        "status": "success"
    }
