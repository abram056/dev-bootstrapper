from pathlib import Path


def write_file(base_path: Path, relative_path: Path, content: str):
    full_path = base_path / relative_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, 'w') as file:
        file.write(content)
