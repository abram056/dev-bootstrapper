"""Tests that validate every template in the store.

These guard against regressions where a template's manifest is malformed or
uses a placeholder that the engine cannot resolve.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from core.manifest import DERIVATIONS
from templates.loader import TEMPLATES_FOLDER, discover_templates

# Placeholders the engine always provides, plus every name-derivation helper.
KNOWN_PLACEHOLDERS = {
    "project_name",
    "package_name",
    "project_slug",
    "pascal_name",
    "pascal_nounderscore",
    "snake_name",
    "snake_nounderscore",
    "camel_name",
    *DERIVATIONS.keys(),
}

# Matches both the standard {{key}} and alternate {#key#} placeholder forms.
PLACEHOLDER_RE = re.compile(r"\{\{([a-z_][a-z0-9_]*)\}\}|\{#([a-z_][a-z0-9_]*)#\}")


def _template_dirs() -> list[Path]:
    if not TEMPLATES_FOLDER.exists():
        return []
    return sorted(d for d in TEMPLATES_FOLDER.iterdir() if d.is_dir())


TEMPLATE_DIRS = _template_dirs()


@pytest.fixture(scope="module")
def manifests():
    return {m.name: m for m in discover_templates()}


def test_templates_exist():
    assert len(TEMPLATE_DIRS) >= 1


def test_every_template_has_manifest(manifests):
    for d in TEMPLATE_DIRS:
        assert (d / "template.toml").exists(), f"missing template.toml in {d.name}"
        assert d.name in manifests, f"failed to load manifest for {d.name}"


def test_manifests_are_valid(manifests):
    for name, manifest in manifests.items():
        assert manifest.name == name, f"{name}: name mismatch"
        assert manifest.language, f"{name}: missing language"
        assert manifest.description, f"{name}: missing description"
        assert manifest.source_path is not None
        assert manifest.install_commands, f"{name}: no install command"


def test_placeholders_are_declared(manifests):
    """Every {{placeholder}} in a template file must be resolvable."""
    problems: list[str] = []
    for name, manifest in manifests.items():
        declared = set(manifest.variables.keys()) | KNOWN_PLACEHOLDERS
        root = manifest.source_path
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.name == "template.toml":
                continue
            try:
                text = path.read_text()
            except UnicodeDecodeError:
                continue  # binary file; skip
            # Each match is a 2-tuple; one group is always empty.
            for match in PLACEHOLDER_RE.findall(text):
                placeholder = match[0] or match[1]
                if placeholder not in declared:
                    rel = path.relative_to(root)
                    problems.append(
                        f"{name}/{rel}: unknown placeholder {{{{{placeholder}}}}}"
                    )
    assert not problems, "\n".join(problems)


def test_conditional_rules_reference_existing_options(manifests):
    for name, manifest in manifests.items():
        for rule in manifest.file_rules:
            if rule.when is not None:
                assert rule.when in manifest.options, (
                    f"{name}: rule references unknown option {rule.when!r}"
                )
