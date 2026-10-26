# {{project_name}}

<!-- A short description of your project goes here. -->

## Workspace

| Crate | Purpose |
| --- | --- |
| `{{project_slug}}-proto` | Shared types and protocol definitions |
| `{{project_slug}}-core` | Core logic and domain rules |
| `{{project_slug}}-bin` | Binary entry point |

## Build

```bash
cargo build --workspace
```

## Test

```bash
cargo test --workspace
```

## Lint

```bash
cargo clippy --workspace --all-targets -- -D warnings
cargo fmt --check --all
```
