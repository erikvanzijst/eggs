# Eggs

A simple shopping list webapp built as a FastAPI REST API and a React frontend.

## Dev Container Setup

This project uses a devcontainer to provide a consistent development environment.

### Getting Started

1. Install [Docker](https://www.docker.com/products/docker-desktop)
2. Install [Visual Studio Code](https://code.visualstudio.com/)
3. Install the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension for VS Code
4. Open this project in VS Code
5. When prompted, select "Reopen in Container" or run the command "Remote-Containers: Reopen in Container"

### What's Included

- Python 3.11
- All project dependencies installed in development mode
- Pre-configured Python extensions for VS Code
- Flake8 and Black formatters
- Pylance language server

## Installation

Install using uv:

```bash
uv sync
```

## Usage

### CLI Mode

```bash
uv run eggs/main.py
# Output: Hello erik (where erik is the current username)

uv run eggs/main.py World
# Output: Hello World

uv run eggs/main.py World Python
# Output: Hello World Python
```

### API Mode

To run the FastAPI server:

```bash
uv run eggs/api.py
```

This will start a server on port 8000 by default. You can also set the PORT environment variable:

```bash
PORT=3000 uv run eggs/api.py
```

API Endpoints:
```
GET /api/v1/lists/
POST /api/v1/lists/{name}
DELETE /api/v1/lists/{name}
GET /api/v1/health
```

Response:
```json
[]
```

OpenAPI Documentation:
- Interactive documentation: http://localhost:8000/api/v1/docs
- Alternative documentation: http://localhost:8000/api/v1/redoc
- JSON schema: http://localhost:8000/api/v1/openapi.json

## Development

Run tests:

```bash
uv run pytest -s
```

Format code:

```bash
uv run black .
```

Lint code:

```bash
uv run flake8 .
```
