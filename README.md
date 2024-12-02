# election-app-backend
Election app backend

# Create a virtualenv

```bash
uv venv
source .venv/bin/activate
uv sync
```

# Run the dev server

```bash
fastapi dev
```

# Run the prod server

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

# Run with docker-compose

```bash
docker compose up server -d
```
