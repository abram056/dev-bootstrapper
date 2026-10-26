"""Dev Bootstrapper — CLI entry point."""

from __future__ import annotations

import sys
from pathlib import Path

from cli.main import get_cli_args
from core.generator import create_project
from core.manifest import build_context, resolve_options
from core.registry import add_project, list_projects, open_project, remove_project
from templates.loader import find_template, list_templates_for_display


def parse_kv(pairs: list[str] | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for pair in pairs or []:
        key, sep, value = pair.partition("=")
        if not key or not sep:
            raise ValueError(f"Invalid KEY=VALUE: {pair!r}")
        result[key] = value
    return result


def cmd_templates() -> None:
    rows = list_templates_for_display()
    if not rows:
        print("No templates found.")
        return

    print("Available templates:\n")
    col = max(len(name) for name, _, _ in rows)
    for name, lang, desc in rows:
        print(f"  {name:<{col}}  {lang}  {desc}")


def cmd_create(args) -> None:
    manifest = find_template(args.project_type)

    extra_vars = parse_kv(args.var)
    package_name = args.package or extra_vars.pop("package_name", None)

    context = build_context(manifest, args.name, package_name, extra_vars)
    options = resolve_options(manifest, parse_kv(args.option))

    output_dir = Path(args.name)
    install = args.install or args.with_venv

    try:
        create_project(
            manifest,
            context,
            options,
            output_dir,
            force=args.force,
            dry_run=args.dry_run,
            git=not args.no_git,
            install=install,
        )
    except FileExistsError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if not args.dry_run:
        add_project(args.name, output_dir, template_name=manifest.name)
        print(f"\nProject created at ./{output_dir}")
        print(f"  template: {manifest.name}")
        print(f"  language: {manifest.language}")
        if not install and manifest.install_commands:
            hint = " & ".join(" ".join(c) for c in manifest.install_commands)
            print(f"  next:     {hint}")


def main() -> None:
    args = get_cli_args()

    if args.command == "create":
        cmd_create(args)
    elif args.command == "templates":
        cmd_templates()
    elif args.command == "list":
        list_projects()
    elif args.command == "remove":
        remove_project(args.name)
    elif args.command == "open":
        open_project(args.name)


if __name__ == "__main__":
    main()
