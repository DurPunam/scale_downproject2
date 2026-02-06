FROM python:3.11-slim

WORKDIR /app
COPY shared /app/shared
COPY services/embedding/app /app/app

RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.4.1+cpu \
    && pip install --no-cache-dir fastapi uvicorn prometheus-client pydantic pydantic-settings numpy sentence-transformers scikit-learn

ENV PYTHONPATH=/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
