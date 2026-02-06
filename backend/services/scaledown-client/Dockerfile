FROM python:3.11-slim

WORKDIR /app
COPY shared /app/shared
COPY services/scaledown-client/app /app/app

RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.4.1+cpu \
    && pip install --no-cache-dir fastapi uvicorn httpx prometheus-client pydantic pydantic-settings numpy sentence-transformers

ENV PYTHONPATH=/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
