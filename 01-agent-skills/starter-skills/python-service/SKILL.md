---
name: python-service
description: Conventions for writing, testing and reviewing Python code in this repository (uv, ruff, pytest, type hints, Pydantic v2, FastAPI). Use whenever creating or editing .py files, adding dependencies, or running tests.
---

# Python service conventions

## Toolchain (always use these commands)
- Install/sync: `uv sync`
- Add a dependency: `uv add <pkg>` (dev: `uv add --dev <pkg>`). Never edit the lock file by hand.
- Lint + format: `uv run ruff check --fix . && uv run ruff format .`
- Types: `uv run pyright` (or `uv run mypy src`)
- Tests: `uv run pytest -q`

## Definition of done
1. Tests for the new behaviour exist and fail before the change (write the failing test first).
2. `ruff check`, `ruff format --check`, the type checker and `pytest` all pass.
3. No new `# type: ignore` or `noqa` without a comment explaining why.

## Code rules
- Python 3.12+. Full type hints on public functions; prefer `X | None` to `Optional[X]`.
- Data shapes are Pydantic v2 models (`model_validate`, `model_dump`); no bare dicts crossing module boundaries.
- FastAPI: inject dependencies with `Depends`; keep route handlers thin and put logic in services.
- Async: never call blocking I/O inside `async def`; use `anyio.to_thread` or an async client.
- Errors: raise domain exceptions; map them to HTTP responses in one place.
- Logging: use the `logging` module with structured `extra=`; never use `print` in library code.
- Configuration: `pydantic-settings`; secrets only from the environment.

## Tests
- pytest with fixtures in `conftest.py`; one behaviour per test; name tests `test_<unit>_<behaviour>`.
- Mock only at boundaries (HTTP, DB, clock). Use `respx` or `pytest-httpx` for HTTP.

## Before finishing
Run the full check sequence above and paste the summary line from each tool into your final message.
