# Dev Bootstrapper

A CLI tool that scaffolds new projects from reusable, manifest-driven templates,
generating a standardised directory structure and boilerplate for the languages
and stacks you actually work in.

## Features

- 12 ready-to-use templates across Python, Rust, and Go
- Declarative manifests (`template.toml`) — no code changes to add a template
- Automatic naming: `project_name` is derived into `package_name`, `snake_name`,
  `pascal_name`, `project_slug`, and more
- Optional feature flags (for example `docker` on service templates)
- Post-scaffold hooks: `git init` and dependency installation
- Dry-run, force-overwrite, and a template validation test suite

## Requirements

- Python 3.11+
- The toolchain for whichever templates you use: `uv`, `cargo`, or `go`

## Install

```bash
python bootstrapper_app.py --help
```

## Usage

List the available templates:

```bash
python bootstrapper_app.py templates
```

Scaffold a project into the current directory:

```bash
python bootstrapper_app.py create python-lib -n my_library
python bootstrapper_app.py create rust-bin -n my_cli --no-git
python bootstrapper_app.py create go-service -n my_api --option docker=false
```

Manage the project registry:

```bash
python bootstrapper_app.py list
python bootstrapper_app.py open my_library
python bootstrapper_app.py remove my_library
```

### `create` options

| Flag | Description |
| --- | --- |
| `-n`, `--name` | Project name (required) |
| `-p`, `--package` | Override the derived package name |
| `--var KEY=VALUE` | Set an extra template variable |
| `--option KEY=VALUE` | Set a template option (`docker=false`) |
| `--no-git` | Skip `git init` |
| `--install` | Run the template's dependency install command |
| `--force` | Overwrite a non-empty target directory |
| `--dry-run` | Print what would be created without writing files |

## Template catalog

### Python

| Template | Description |
| --- | --- |
| `python-lib` | Library with `src/` layout, hatchling + uv, ruff, pytest, CI |
| `python-cli` | Typer + Rich CLI with a version flag |
| `python-tui` | Textual terminal UI |
| `python-flask` | Flask app with templates and static assets |
| `python-fastapi` | FastAPI app with a modular `api/v1` router and Dockerfile |
| `python-data` | Notebooks + `src/` + `scripts/` layout for analysis work |

### Rust

| Template | Description |
| --- | --- |
| `rust-bin` | Single-crate binary, clippy-clean |
| `rust-workspace` | Three-crate workspace (`proto`, `core`, `bin`) |
| `rust-tui` | Terminal UI using ratatui and crossterm |

### Go

| Template | Description |
| --- | --- |
| `go-cli` | Subcommand-style CLI with colocated tests |
| `go-service` | HTTP service with health checks, `slog`, and a Dockerfile |
| `go-tui` | Bubble Tea terminal UI |

## Writing a template

A template is a directory under `templates_store/` with a `template.toml` manifest
and the files to scaffold. The engine renders `{{variable}}` in both file paths and
file contents, then runs the manifest's hooks.

```toml
name = "my-template"
language = "python"
description = "What this template scaffolds"

[variables]
python_version = "3.12"

[options]
docker = { default = true, help = "Include a Dockerfile" }

[files]
exclude = ["template.toml"]

[[files.rules]]
include = ["Dockerfile"]
when = "docker"

[commands]
git = true
install = [["uv", "sync"]]
```

### Built-in variables

`project_name`, `package_name`, `project_slug`, `snake_name`,
`snake_nounderscore`, `pascal_name`, `pascal_nounderscore`, `camel_name`.

### Delimiter collision

Some scaffolding targets use `{{...}}` as their own template syntax — Jinja,
ERB, and Go templates all do. In those files, use the alternate `{#key#}` form
for bootstrapper variables; it renders to the plain value and leaves the host
syntax untouched:

```html
<title>{#project_name#}</title>
<h1>{{ name }}</h1>
```

## Development

```bash
python -m pytest tests/ -q   # run the test suite
python -m ruff check .       # lint
```

The test suite validates every template: manifests must load, and every
placeholder in a template file must be a known variable. Adding a broken
placeholder fails CI.
