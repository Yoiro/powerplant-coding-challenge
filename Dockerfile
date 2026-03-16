# Build
FROM ghcr.io/astral-sh/uv:python3.14-alpine AS builder
WORKDIR /app
COPY pyproject.toml uv.lock /app
COPY app/ /app/app
RUN uv sync --no-dev --no-install-project

# Runtime
FROM python:3.14-alpine
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app /app/app
EXPOSE 8888

CMD ["/app/.venv/bin/fastapi", "run", "/app/app/main.py", "--host", "0.0.0.0", "--port", "8888"]
