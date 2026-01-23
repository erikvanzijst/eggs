# Eggs

A simple CLI tool that prints "Hello " followed by the parameters, or the current user's username if no parameters are provided.

## Installation

Install using uv:

```bash
uv pip install .
```

Or install in development mode:

```bash
uv pip install -e .
```

## Usage

```bash
eggs
# Output: Hello erik (where erik is the current username)

eggs World
# Output: Hello World

eggs World Python
# Output: Hello World Python
```

## Development

Install development dependencies:

```bash
uv pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Format code:

```bash
black .
```

Lint code:

```bash
flake8 .
```