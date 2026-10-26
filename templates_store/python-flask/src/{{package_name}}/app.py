"""Flask application for {{project_name}}."""

from pathlib import Path

from flask import Flask, render_template

from {{package_name}} import __version__

_STATIC = Path(__file__).parent / "static"
_TEMPLATES = Path(__file__).parent / "templates"

app = Flask(
    "{{package_name}}",
    static_folder=str(_STATIC),
    template_folder=str(_TEMPLATES),
)


@app.get("/")
def index():
    return render_template("index.html", name="{{project_name}}", version=__version__)


def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    main()
