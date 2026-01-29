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

### API Mode

To run the FastAPI server:

```bash
uv run eggs/api.py
```

This will start a server on port 8000 by default:

```bash
uv run eggs/api.py
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

## Frontend Development

### Running the Frontend

To run the React frontend:

```bash
cd frontend
npm start
```

This will start the development server on port 3000 by default.

### Running Frontend Tests

To run the frontend tests:

```bash
cd frontend
npm test -- --watchAll=false
```

This will run all frontend tests including the tests for the shopping list service.

### Available Scripts

In the frontend directory, you can also run:

- `npm start` - Runs the app in development mode
- `npm test` - Runs the test suite
- `npm run build` - Builds the app for production
- `npm run eject` - Removes the single build dependency
