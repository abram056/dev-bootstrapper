from typer.testing import CliRunner

from {{package_name}}.cli import app

runner = CliRunner()


def test_greet():
    result = runner.invoke(app, ["greet", "World"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "{{package_name}}" in result.output
