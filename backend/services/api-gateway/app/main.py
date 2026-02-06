from __future__ import annotations

from fastapi import FastAPI

from shared.app_factory import create_app
from shared.config.settings import get_settings
from shared.logging.logger import configure_logging

settings = get_settings()
settings.service_name = "api-gateway"
configure_logging(settings.log_level)

app: FastAPI = create_app(settings)
