FROM python:3.11-slim

WORKDIR /app
COPY shared /app/shared
COPY services/spatial/app /app/app

RUN pip install --no-cache-dir fastapi uvicorn prometheus-client pydantic pydantic-settings numpy

ENV PYTHONPATH=/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
