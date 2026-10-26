# {{project_name}}

<!-- A short description of your project goes here. -->

## Installation

```bash
uv sync
```

## Layout

- `notebooks/` — Jupyter notebooks for exploration
- `src/{{package_name}}/` — reusable library code
- `scripts/` — runnable data-processing scripts
- `data/` — input data (git-ignored)
- `tests/` — test suite

## Usage

```bash
uv run jupyter lab      # launch Jupyter
uv run {{package_name}}  # run the example pipeline
```

## Development

```bash
uv run pytest        # tests
uv run ruff check .  # lint
```
