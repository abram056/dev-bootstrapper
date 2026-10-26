"""Argument parsing for the dev-bootstrapper CLI."""

from __future__ import annotations

import argparse

from templates.loader import discover_templates


def _template_choices() -> list[str]:
    names: set[str] = set()
    for manifest in discover_templates():
        names.update(manifest.all_names)
    return sorted(names)


def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dev project Bootstrapper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Create a new project")
    subparsers.add_parser("templates", help="List available templates")
    subparsers.add_parser("list", help="List projects")
    remove_parser = subparsers.add_parser("remove", help="Delete project")
    open_parser = subparsers.add_parser(
        "open", help="Open project folder in file explorer"
    )

    create_parser.add_argument(
        "project_type",
        choices=_template_choices(),
        help="Project type",
    )
    create_parser.add_argument(
        "-n",
        "--name",
        metavar="project_name",
        required=True,
        help="Project name",
    )
    create_parser.add_argument(
        "-p",
        "--package",
        metavar="package_name",
        required=False,
        help="Package name",
    )
    create_parser.add_argument(
        "--var",
        action="append",
        metavar="KEY=VALUE",
        default=[],
        help="Set a template variable (repeatable)",
    )
    create_parser.add_argument(
        "--option",
        action="append",
        metavar="KEY=VALUE",
        default=[],
        help="Set a template option (repeatable)",
    )
    create_parser.add_argument(
        "--install",
        action="store_true",
        help="Run install commands after creating",
    )
    create_parser.add_argument(
        "--with-venv",
        action="store_true",
        help="Alias for --install (deprecated)",
    )
    create_parser.add_argument(
        "--no-git",
        action="store_true",
        help="Skip git init",
    )
    create_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing non-empty directory",
    )
    create_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be created without writing files",
    )

    remove_parser.add_argument("name")
    open_parser.add_argument("name")

    return parser.parse_args()
