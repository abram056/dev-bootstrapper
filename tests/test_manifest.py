"""Tests for core.manifest."""

import pytest

from core.manifest import (
    build_context,
    camel_case,
    kebab_case,
    load_manifest,
    matches_pattern,
    pascal_case,
    resolve_files,
    resolve_options,
    slugify,
    snake_case,
)


class TestNameHelpers:
    def test_snake_case(self):
        assert snake_case("My Project") == "my_project"
        assert snake_case("my-project") == "my_project"
        assert snake_case("my_project") == "my_project"

    def test_kebab_case(self):
        assert kebab_case("My Project") == "my-project"
        assert kebab_case("my_project") == "my-project"

    def test_pascal_case(self):
        assert pascal_case("my project") == "MyProject"
        assert pascal_case("my_project") == "MyProject"
        assert pascal_case("my-project") == "MyProject"

    def test_camel_case(self):
        assert camel_case("my project") == "myProject"
        assert camel_case("MyProject") == "myproject"

    def test_slugify(self):
        assert slugify("My Project!") == "my-project"
        assert slugify("Hello World") == "hello-world"


class TestMatchesPattern:
    def test_simple(self):
        assert matches_pattern("foo.py", "*.py")
        assert not matches_pattern("foo.txt", "*.py")

    def test_double_star(self):
        assert matches_pattern("a/b/c.py", "**/*.py")
        assert matches_pattern("c.py", "**/*.py")
        assert matches_pattern("alembic/env.py", "alembic/**")
        assert not matches_pattern("other/env.py", "alembic/**")

    def test_exact(self):
        assert matches_pattern("docker-compose.yml", "docker-compose.yml")
        assert not matches_pattern("a/docker-compose.yml", "docker-compose.yml")


class TestBuildContext:
    def _manifest(self, tmp_path):
        m = tmp_path / "template.toml"
        m.write_bytes(
            b"""
name = "test"
[variables]
python_version = "3.14"
"""
        )
        return load_manifest(tmp_path)

    def test_basic(self, tmp_path):
        manifest = self._manifest(tmp_path)
        ctx = build_context(manifest, "My Project")
        assert ctx["project_name"] == "My Project"
        assert ctx["package_name"] == "my_project"
        assert ctx["project_slug"] == "my-project"
        assert ctx["pascal_name"] == "MyProject"
        assert ctx["camel_name"] == "myProject"
        assert ctx["python_version"] == "3.14"

    def test_package_override(self, tmp_path):
        manifest = self._manifest(tmp_path)
        ctx = build_context(manifest, "My Project", package_name="custom")
        assert ctx["package_name"] == "custom"

    def test_extra_vars(self, tmp_path):
        manifest = self._manifest(tmp_path)
        ctx = build_context(manifest, "X", extra_vars={"author": "me"})
        assert ctx["author"] == "me"


class TestResolveOptions:
    def _manifest(self, tmp_path):
        (tmp_path / "template.toml").write_bytes(
            b"""
name = "test"
[options]
db = { default = true, help = "with db" }
docker = false
"""
        )
        return load_manifest(tmp_path)

    def test_defaults(self, tmp_path):
        manifest = self._manifest(tmp_path)
        opts = resolve_options(manifest)
        assert opts == {"db": True, "docker": False}

    def test_override(self, tmp_path):
        manifest = self._manifest(tmp_path)
        opts = resolve_options(manifest, {"db": "false"})
        assert opts["db"] is False

    def test_unknown_raises(self, tmp_path):
        manifest = self._manifest(tmp_path)
        with pytest.raises(ValueError, match="Unknown option"):
            resolve_options(manifest, {"nope": "true"})


class TestResolveFiles:
    def _manifest(self, tmp_path):
        (tmp_path / "template.toml").write_bytes(
            b"""
name = "test"
[files]
exclude = ["template.toml", "*.pyc"]

[options]
db = true

[[files.rules]]
include = ["alembic/**", "docker-compose.yml"]
when = "db"
"""
        )
        return load_manifest(tmp_path)

    def test_base_files_always_included(self, tmp_path):
        manifest = self._manifest(tmp_path)
        result = resolve_files(
            manifest,
            ["README.md", "app/main.py", "template.toml"],
            {"db": True},
        )
        assert "README.md" in result
        assert "app/main.py" in result
        assert "template.toml" not in result

    def test_conditional_included_when_true(self, tmp_path):
        manifest = self._manifest(tmp_path)
        result = resolve_files(
            manifest,
            ["README.md", "alembic/env.py", "docker-compose.yml"],
            {"db": True},
        )
        assert "alembic/env.py" in result
        assert "docker-compose.yml" in result

    def test_conditional_excluded_when_false(self, tmp_path):
        manifest = self._manifest(tmp_path)
        result = resolve_files(
            manifest,
            ["README.md", "alembic/env.py", "docker-compose.yml"],
            {"db": False},
        )
        assert "README.md" in result
        assert "alembic/env.py" not in result
        assert "docker-compose.yml" not in result
