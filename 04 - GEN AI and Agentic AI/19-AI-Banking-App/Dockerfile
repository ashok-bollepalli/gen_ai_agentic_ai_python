FROM python:3.12-slim

WORKDIR /app

# 1. Install libraries (cached unless requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy project code (.dockerignore skips .env, venv, k8s ...)
COPY . .

# 3. Default command = FastAPI. K8s overrides it for the MCP server and the UI.
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]