# {{project_name}}

<!-- A short description of your project goes here. -->

## Run

```bash
go run ./cmd/server
```

The service listens on `:8080`.

## Endpoints

- `GET /healthz` — liveness check
- `GET /readyz` — readiness check
- `GET /api/v1/ping` — example handler

## Test

```bash
go test ./...
```

## Docker

```bash
docker build -t {{project_slug}} .
docker run --rm -p 8080:8080 {{project_slug}} ```
