# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

LedgerMe is a web application for tracking personal financial activities including income, expenses, and investments. This is currently a fresh repository with initial setup files.

## Technology Stack

Based on the .gitignore configuration, this project is intended to be a Python-based web application with support for:
- Python web frameworks (Django/Flask based on gitignore patterns)
- Multiple Python package managers (pip, poetry, pdm, uv, pixi)
- AI development tools (Abstra framework)
- Various development environments and IDEs

## Development Setup

Since this is a new project, the development workflow is not yet established. When code is added, common patterns to expect:

### Python Environment
- Virtual environment management (likely using .venv, poetry, or uv)
- Dependencies will be defined in requirements.txt, pyproject.toml, or similar
- Code formatting likely managed by ruff (based on .ruff_cache/ in gitignore)

### Testing
- Test files will likely be in a tests/ directory
- Common Python testing frameworks to expect: pytest, unittest
- Coverage reporting configured (coverage.xml patterns in gitignore)

## Common Commands

*Note: These commands will be available once the project structure is established*

### Environment Setup
- `python -m venv .venv && source .venv/bin/activate` (if using venv)
- `poetry install` (if using Poetry)
- `uv sync` (if using uv)

### Development
- Code formatting: `ruff format .`
- Linting: `ruff check .`
- Type checking: `mypy .` (if mypy is configured)

### Testing
- Run tests: `pytest` or `python -m pytest`
- Run with coverage: `pytest --cov=.`

## Architecture Notes

This repository is in its initial state. When code is added, key architectural decisions should be documented here including:
- Web framework choice (Django, Flask, FastAPI, etc.)
- Database selection and ORM
- Frontend approach (if applicable)
- API design patterns
- Authentication and authorization approach