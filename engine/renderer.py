"""Content and path rendering with template variables."""

from __future__ import annotations

import re
from pathlib import Path


def render_content(content: str, context: dict[str, str]) -> str:
    """Replace placeholders in *content* with context values.

    Two placeholder forms are recognised so that a template file can use
    ``{{...}}`` as its own native syntax (Jinja, ERB, Go templates) without
    colliding with the bootstrapper:

    - ``{{key}}`` — standard form
    - ``{#key#}`` — alternate form for files where ``{{...}}`` is reserved
    """
    for key, value in context.items():
        content = content.replace(f"{{{{{key}}}}}", value)
        content = content.replace(f"{{#{key}#}}", value)
    return content


def render_path(path: Path, context: dict[str, str]) -> Path:
    """Replace ``{{key}}`` placeholders in *path* with context values."""
    path_str = str(path)
    for key, value in context.items():
        path_str = path_str.replace(f"{{{{{key}}}}}", value)
    return Path(path_str)


PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}|\{#(\w+)#\}")


def find_unrendered(text: str) -> list[str]:
    """Return any unresolved placeholders left in *text* after rendering.

    Detects both the standard ``{{word}}`` and alternate ``{#word#}`` forms.
    """
    return [a or b for a, b in PLACEHOLDER_RE.findall(text)]
