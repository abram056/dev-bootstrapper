"""Command-line interface for {{project_name}}."""

import typer
from rich import print

from {{package_name}} import __version__

app = typer.Typer(help="{{project_name}} command-line tool.", no_args_is_help=True)


def _version_callback(value: bool) -> None:
    if value:
        print(f"[bold]{{package_name}}[/bold] {__version__}")
        raise typer.Exit()


@app.callback()
def main_callback(
    version: bool = typer.Option(
        None,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """{{project_name}} command-line tool."""


@app.command()
def greet(name: str = typer.Argument(..., help="Name to greet.")) -> None:
    """Greet someone."""
    print(f"[green]Hello, {name}![/green]")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
