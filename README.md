# Eggs

A simple CLI tool that prints "Hello " followed by the parameters, or the current user's username if no parameters are provided.
It also provides a REST API powered by FastAPI.

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

API Endpoint:
```
GET /api/v1/lists/
```

Response:
```json
[]
```

## Development

Run tests:

```bash
uv run pytest
```

Format code:

```bash
uv run black .
```

Lint code:

```bash
uv run flake8 .
```