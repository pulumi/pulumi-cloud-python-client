# Contributing

## Development Setup

This project uses pre-commit hooks to ensure code quality and consistent formatting.

### Setting up pre-commit

1. Install dependencies:

   ```bash
   poetry install
   poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg
   ```
