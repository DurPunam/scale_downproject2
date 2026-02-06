FROM python:3.11-slim

WORKDIR /app
COPY shared /app/shared
COPY services/recommendation/app /app/app

RUN pip install --no-cache-dir fastapi uvicorn prometheus-client pydantic pydantic-settings lightfm scikit-learn numpy

ENV PYTHONPATH=/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
