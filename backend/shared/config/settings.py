from __future__ import annotations

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseModel):
    url: str = Field(default="redis://redis:6379/0")
    l2_disk_cache_path: str = Field(default="/var/cache/scaledown/l2")


class PostgresSettings(BaseModel):
    dsn: str = Field(default="postgresql+asyncpg://app:app@postgres:5432/scaledown")


class KafkaSettings(BaseModel):
    brokers: str = Field(default="kafka:9092")
    consumer_group: str = Field(default="scaledown")
    topic_prefix: str = Field(default="scaledown")


class ScaleDownSettings(BaseModel):
    base_url: str = Field(default="https://api.scaledown.ai")
    api_key: str = Field(default="")
    batch_endpoint: str = Field(default="/v2/compress/batch")
    timeout_seconds: float = Field(default=30.0)


class ObservabilitySettings(BaseModel):
    otel_endpoint: str = Field(default="http://otel-collector:4317")
    prometheus_port: int = Field(default=9000)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")

    service_name: str = Field(default="unknown-service")
    environment: str = Field(default="dev")
    log_level: str = Field(default="INFO")
    http_port: int = Field(default=8000)

    redis: RedisSettings = RedisSettings()
    postgres: PostgresSettings = PostgresSettings()
    kafka: KafkaSettings = KafkaSettings()
    scaledown: ScaleDownSettings = ScaleDownSettings()
    observability: ObservabilitySettings = ObservabilitySettings()


def get_settings() -> Settings:
    return Settings()
