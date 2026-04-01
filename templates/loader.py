from pathlib import Path


BASEDIR = Path(__file__).resolve().parents[1]
TEMPLATES_FOLDER = BASEDIR / "templates_store"


def list_paths(path):
    posix_paths = Path(path)
    all_paths = [p for p in posix_paths.rglob('*') if p.is_file()]
    return all_paths


def load_file_contents(path: Path) -> str:
    with open(path, 'r') as f:
        content = f.read()
        return content


def load_template(template_name: str):
    template_path = TEMPLATES_FOLDER / template_name
    dir_paths = list_paths(template_path)
    # print(dir_paths)

    loaded_templates = []
    for path in dir_paths:
        content = load_file_contents(path)
        loaded_templates.append(
            {"path": path.relative_to(template_path), "content": content}
        )

    return loaded_templates
