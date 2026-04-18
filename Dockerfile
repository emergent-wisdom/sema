# Web deploy for semahash.org — builds the React frontend and runs the
# FastAPI server that fronts the pattern graph + REST API. This is the
# Dockerfile Railway auto-detects at repo root.
#
# The MCP stdio-server variant lives at `Dockerfile.mcp` (non-canonical
# name, not auto-detected) and is the artifact submitted to Glama.

# ── Stage 1: compile the React frontend ──────────────────────────────
FROM node:20-slim AS web-builder

WORKDIR /app/web

# Lockfile-first for layer caching; only invalidated when deps change.
COPY web/package.json web/package-lock.json ./
RUN npm ci

COPY web/ ./
RUN npm run build

# ── Stage 2: Python runtime serving the compiled frontend + API ──────
FROM python:3.12-slim

WORKDIR /app

# gcc is needed for a few wheels that compile native extensions.
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only what the runtime needs. `pyproject.toml` first so the pip
# install layer caches across source edits.
COPY pyproject.toml README.md LICENSE LICENSE-CONTENT ./
COPY src/ ./src/
COPY data/ ./data/
COPY docs/ ./docs/
COPY paper/sema.pdf ./paper/sema.pdf

RUN pip install --no-cache-dir -e ".[api]"

# Drop the built frontend into the path `sema serve` expects.
COPY --from=web-builder /app/web/build/client/ ./src/sema/server/static/

# Railway injects $PORT at runtime; default to 3000 for local docker runs.
EXPOSE 3000

CMD sema serve --host 0.0.0.0 --port ${PORT:-3000}
