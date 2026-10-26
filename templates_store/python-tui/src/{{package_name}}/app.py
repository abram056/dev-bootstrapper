"""Textual application for {{project_name}}."""

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Header, Static

from {{package_name}} import __version__


class {{pascal_nounderscore}}App(App):
    """A Textual application template."""

    TITLE = "{{project_name}}"
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Static(f"{{project_name}} v{__version__}", id="title")
            yield Static("Replace this with your UI.", id="body")
        yield Footer()


def main() -> None:
    {{pascal_nounderscore}}App().run()


if __name__ == "__main__":
    main()
