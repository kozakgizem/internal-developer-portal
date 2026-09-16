FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -e .

EXPOSE 8000

ENV PYTHONPATH=/app/src/internal_developer_portal

CMD ["uvicorn", "internal_developer_portal.app.main:app", "--host", "0.0.0.0", "--port", "8000"]