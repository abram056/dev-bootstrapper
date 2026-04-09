from pathlib import Path


def render_content(content: str, context: dict[str, str]) -> str:
    for key, value in context.items():
        content = content.replace(f"{{{{{key}}}}}", value)

    return content


def render_path(path: Path, context: dict[str, str]) -> Path:
    path_str = str(path)
    for key, value in context.items():
        path_str = path_str.replace(f"{{{{{key}}}}}", value)
    final_path = Path(path_str)
    return final_path
