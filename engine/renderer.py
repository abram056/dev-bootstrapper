"""Content and path rendering with template variables."""

from __future__ import annotations

import re
from pathlib import Path


def render_content(content: str, context: dict[str, str]) -> str:
    """Replace ``{{key}}`` placeholders in *content* with context values."""
    for key, value in context.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    return content


def render_path(path: Path, context: dict[str, str]) -> Path:
    """Replace ``{{key}}`` placeholders in *path* with context values."""
    path_str = str(path)
    for key, value in context.items():
        path_str = path_str.replace(f"{{{{{key}}}}}", value)
    return Path(path_str)


def find_unrendered(text: str) -> list[str]:
    """Return any ``{{word}}`` placeholders left in *text* after rendering."""
    return re.findall(r"\{\{(\w+)\}\}", text)
