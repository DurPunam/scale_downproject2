from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from shared.app_factory import create_app
from shared.config.settings import get_settings
from shared.logging.logger import configure_logging

settings = get_settings()
settings.service_name = "auth-service"
configure_logging(settings.log_level)

app: FastAPI = create_app(settings)


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login(payload: LoginRequest) -> dict:
    # Placeholder for JWT auth
    return {"access_token": f"token-{payload.username}", "token_type": "bearer"}
