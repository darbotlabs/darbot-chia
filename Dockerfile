FROM python:3.11-slim
RUN apt-get update && apt-get install -y git build-essential rust-all nodejs npm && rm -rf /var/lib/apt/lists/*
RUN pip install uvicorn[standard] fastapi
WORKDIR /app
COPY . .
CMD ["python", "-m", "chia.mcp.server"]
