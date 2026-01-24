# Agent Instructions

This is a python project that uses `uv` for dependency management.



## Create a virtual environment

```
uv sync
uv venv --allow-existing
```

## Activate the virtual environment

```
source .venv/bin/activate
```

## Apply migrations

Always run the migrations on a fresh database, after a `git pull`, or `git checkout` and after creating a new migration.

```
alembic upgrade head
```

Use `alembic revision -m "Some description"` to create a new migration.


## Running the project

```
python eggs/main.py
```

## Testing

```
uv run pytest -s tests/
```

## Notes for agents

- Always use Context7 MCP when I need library/API documentation, code generation, setup or configuration steps without
  me having to explicitly ask.
- Always first activate the python virtualenv using `source .venv/bin/activate` before running any commands.


## Issue Tracking

This project uses **bd** (beads) for issue tracking. Run `bd onboard` to get started.

## Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --status in_progress  # Claim work
bd close <id>         # Complete work
bd sync               # Sync with git
```

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds

