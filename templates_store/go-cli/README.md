# {{project_name}}

<!-- A short description of your project goes here. -->

## Build

```bash
go build -o {{project_slug}} ./cmd/{{project_slug}}
```

## Run

```bash
go run ./cmd/{{project_slug}} greet World
```

## Test

```bash
go test ./...
```

## Lint

```bash
go vet ./...
gofmt -l .
```
