"""Tests for core.generator and template discovery."""


import pytest

from core.generator import create_project
from core.manifest import build_context, load_manifest, resolve_options
from templates.loader import find_template, load_template_files


@pytest.fixture
def manifest(tmp_path):
    (tmp_path / "README.md").write_text("# {{project_name}}\n")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "{{package_name}}").mkdir()
    (tmp_path / "src" / "{{package_name}}" / "__init__.py").write_text("")
    (tmp_path / "template.toml").write_bytes(
        b"""
name = "test-tpl"
aliases = ["test"]
description = "test template"
[files]
exclude = ["template.toml"]
"""
    )
    return load_manifest(tmp_path)


class TestLoadTemplateFiles:
    def test_skips_template_toml(self, manifest):
        files = load_template_files(manifest)
        rels = [f["rel_path"] for f in files]
        assert "template.toml" not in rels
        assert "README.md" in rels

    def test_marks_text_as_text(self, manifest):
        files = load_template_files(manifest)
        readme = next(f for f in files if f["rel_path"] == "README.md")
        assert readme["is_binary"] is False


class TestCreateProject:
    def test_creates_files(self, manifest, tmp_path):
        ctx = build_context(manifest, "my_proj")
        opts = resolve_options(manifest)
        out = tmp_path / "out"
        create_project(manifest, ctx, opts, out, git=False)

        assert (out / "README.md").read_text() == "# my_proj\n"
        assert (out / "src" / "my_proj" / "__init__.py").exists()

    def test_refuses_nonempty_without_force(self, manifest, tmp_path):
        ctx = build_context(manifest, "x")
        opts = resolve_options(manifest)
        out = tmp_path / "out"
        out.mkdir()
        (out / "existing.txt").write_text("hi")

        with pytest.raises(FileExistsError):
            create_project(manifest, ctx, opts, out, git=False)

    def test_force_overwrites(self, manifest, tmp_path):
        ctx = build_context(manifest, "x")
        opts = resolve_options(manifest)
        out = tmp_path / "out"
        out.mkdir()
        (out / "existing.txt").write_text("hi")

        create_project(manifest, ctx, opts, out, force=True, git=False)
        assert (out / "README.md").exists()

    def test_dry_run_creates_nothing(self, manifest, tmp_path, capsys):
        ctx = build_context(manifest, "dry_proj")
        opts = resolve_options(manifest)
        out = tmp_path / "out"
        create_project(manifest, ctx, opts, out, dry_run=True, git=False)

        assert not out.exists()
        captured = capsys.readouterr()
        assert "Would create" in captured.out

    def test_path_rendered(self, manifest, tmp_path):
        ctx = build_context(manifest, "cool_thing")
        opts = resolve_options(manifest)
        out = tmp_path / "out"
        create_project(manifest, ctx, opts, out, git=False)
        assert (out / "src" / "cool_thing" / "__init__.py").exists()


class TestFindTemplate:
    def test_by_name(self):
        m = find_template("python")
        assert m.name

    def test_unknown_raises(self):
        with pytest.raises(ValueError, match="Unknown template"):
            find_template("does-not-exist")
