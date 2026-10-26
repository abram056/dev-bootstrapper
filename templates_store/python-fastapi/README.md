# {{project_name}}

<!-- A short description of your project goes here. -->

## Run locally

```bash
uv sync
uvicorn app.main:app --reload
```

The API is served at <http://127.0.0.1:8000>, with interactive docs at
<http://127.0.0.1:8000/docs>.

## Docker

```bash
docker build -t {{project_slug}} .
docker run --rm -p 8000:8000 {{project_slug}}
```

## Development

```bash
uv run pytest        # run tests
uv run ruff check .  # lint
uv run ruff format . # format
```
