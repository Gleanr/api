FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY uv.lock pyproject.toml ./
RUN uv sync --frozen --no-dev
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app/src

COPY ./src ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]