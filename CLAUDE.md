# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A simple shopping list webapp with a FastAPI REST API backend. The project uses SQLModel/SQLAlchemy for ORM with SQLite, Alembic for database migrations, and `uv` for dependency management.

## Essential Commands

### Dependency Management
```bash
uv sync                    # Install/sync all dependencies
uv venv --allow-existing   # Create virtual environment
```

### Running the Application
```bash
uv run eggs/api.py         # Start FastAPI server (default port 8000)
PORT=3000 uv run eggs/api.py  # Start with custom port
```

### Testing
```bash
uv run pytest -s           # Run all tests with output
uv run pytest -s tests/test_api.py  # Run specific test file
uv run pytest -s tests/test_api.py::test_create_list_success  # Run single test
```

### Code Quality
```bash
uv run black .             # Format code
uv run flake8 .            # Lint code
```

### Database Migrations
```bash
alembic upgrade head       # Apply all migrations (run after git pull/checkout)
alembic revision -m "description"  # Create new migration
```

**IMPORTANT**: Always run migrations after database schema changes, git pull, or git checkout.

## Architecture

### Database Layer (`eggs/db.py`)
- Uses SQLModel (combines SQLAlchemy + Pydantic) for ORM
- Single `ListModel` table with `id` (primary key) and `name` (unique)
- `get_db()` generator provides database sessions via dependency injection
- SQLite database: `lists.db` in project root
- Schema managed via Alembic migrations in `alembic/versions/`

### API Layer (`eggs/api.py`)
- FastAPI application with dependency injection pattern
- All endpoints prefixed with `/api/v1/`
- OpenAPI docs available at `/api/v1/docs` and `/api/v1/redoc`
- Uses `Depends(get_db)` to inject database sessions into route handlers
- Error handling: `IntegrityError` → HTTP 400, not found → HTTP 404

### Testing (`tests/`)
- Uses pytest with FastAPI's TestClient
- `tests/db.py` provides `db_session` fixture with in-memory SQLite for test isolation
- Tests override `get_db` dependency to use test database session
- Each test gets a fresh database via fixture

### Key Patterns
1. **Dependency Injection**: Database sessions injected via `Depends(get_db)`
2. **Test Isolation**: Tests use in-memory SQLite with dependency override
3. **Database Session Management**: Context managers ensure proper cleanup
4. **Migration-First Schema**: Schema changes require Alembic migrations

## Issue Tracking with Beads

This project uses **bd** (beads) for issue tracking.

```bash
bd onboard                 # Get started with beads
bd ready                   # Find available work
bd show <id>               # View issue details
bd update <id> --status in_progress  # Claim work
bd close <id>              # Complete work
bd sync                    # Sync with git
```

## Session Completion Workflow

When ending a work session, complete ALL steps:

1. **File issues for remaining work** - Create beads issues for follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** (MANDATORY):
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL**: Work is NOT complete until `git push` succeeds. NEVER stop before pushing.
