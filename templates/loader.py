"""Template discovery and file loading."""

from __future__ import annotations

import fnmatch
import sys
from pathlib import Path

from core.manifest import TemplateManifest, load_manifest

BASEDIR = Path(__file__).resolve().parents[1]
TEMPLATES_FOLDER = BASEDIR / "templates_store"

_SKIP_DIRS = {
    ".git",
    "target",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    ".hypothesis",
    "dist",
    "build",
    "docs",
    ".cache",
}

_SKIP_FILES = {"*.pyc", "*.pyo", ".DS_Store", "Cargo.lock", "go.sum", "*.swp", "*.swo"}


def discover_templates() -> list[TemplateManifest]:
    """Return all valid template manifests found in ``templates_store``."""
    manifests: list[TemplateManifest] = []
    if not TEMPLATES_FOLDER.exists():
        return manifests
    for d in sorted(TEMPLATES_FOLDER.iterdir()):
        if d.is_dir() and (d / "template.toml").exists():
            try:
                manifests.append(load_manifest(d))
            except Exception as exc:
                print(
                    f"Warning: failed to load template {d.name}: {exc}",
                    file=sys.stderr,
                )
    return manifests


def find_template(name_or_alias: str) -> TemplateManifest:
    """Look up a template by name or alias."""
    for manifest in discover_templates():
        if name_or_alias in manifest.all_names:
            return manifest
    raise ValueError(f"Unknown template: {name_or_alias!r}")


def _should_skip(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    for part in rel.parts[:-1]:
        if part in _SKIP_DIRS:
            return True
    name = path.name
    return any(fnmatch.fnmatch(name, pattern) for pattern in _SKIP_FILES)


def _is_binary(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            chunk = f.read(8192)
            return b"\x00" in chunk
    except Exception:
        return True


def load_template_files(manifest: TemplateManifest) -> list[dict]:
    """Load all files from a template directory.

    Returns a list of dicts with keys:
    - ``rel_path``: POSIX-relative path string
    - ``content``: ``str`` for text files, ``bytes`` for binary files
    - ``is_binary``: ``bool``
    """
    root = manifest.source_path
    files: list[dict] = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if _should_skip(p, root):
            continue
        rel = p.relative_to(root)
        if rel.name == "template.toml":
            continue
        if _is_binary(p):
            files.append(
                {
                    "rel_path": rel.as_posix(),
                    "content": p.read_bytes(),
                    "is_binary": True,
                }
            )
        else:
            files.append(
                {
                    "rel_path": rel.as_posix(),
                    "content": p.read_text(),
                    "is_binary": False,
                }
            )
    return files


def list_templates_for_display() -> list[tuple[str, str, str]]:
    """Return ``(name_line, language, description)`` for each template."""
    result: list[tuple[str, str, str]] = []
    for m in discover_templates():
        names = m.name
        if m.aliases:
            names += f" ({', '.join(m.aliases)})"
        result.append((names, m.language, m.description))
    return result
