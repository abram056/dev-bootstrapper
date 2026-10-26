"""Tests for engine.renderer."""

from pathlib import Path

from engine.renderer import find_unrendered, render_content, render_path


class TestRenderContent:
    def test_single_var(self):
        assert render_content("hello {{name}}", {"name": "world"}) == "hello world"

    def test_multiple_vars(self):
        result = render_content("{{a}}-{{b}}", {"a": "x", "y": "z", "b": "y"})
        assert result == "x-y"

    def test_no_vars(self):
        assert render_content("no vars here", {}) == "no vars here"

    def test_missing_var_left_alone(self):
        assert render_content("{{missing}}", {"other": "x"}) == "{{missing}}"

    def test_alternate_delimiter(self):
        """{#key#} renders for files that reserve {{...}} as native syntax."""
        assert render_content("title: {#project_name#}", {"project_name": "app"}) == (
            "title: app"
        )

    def test_mixed_delimiters(self):
        ctx = {"a": "1", "b": "2"}
        assert render_content("{{a}} and {#b#}", ctx) == "1 and 2"

    def test_alternate_missing_left_alone(self):
        assert render_content("{#missing#}", {"other": "x"}) == "{#missing#}"


class TestRenderPath:
    def test_var_in_dirname(self):
        result = render_path(
            Path("src/{{package_name}}/main.py"), {"package_name": "my_pkg"}
        )
        assert result == Path("src/my_pkg/main.py")

    def test_no_vars(self):
        p = Path("src/main.py")
        assert render_path(p, {}) == p


class TestFindUnrendered:
    def test_finds_placeholder(self):
        assert find_unrendered("hello {{name}}") == ["name"]

    def test_finds_alternate_placeholder(self):
        assert find_unrendered("hello {#name#}") == ["name"]

    def test_multiple(self):
        assert find_unrendered("{{a}} and {#b#}") == ["a", "b"]

    def test_none(self):
        assert find_unrendered("all good") == []
