from pathlib import Path
import re
import json

from cli.main import get_cli_args
from core.generator import generate


def get_regitry_file() -> Path:

    data_dir = Path.home() / ".dev-bootstrapper"
    data_dir.mkdir(exist_ok=True)

    file_path = data_dir / "projects.json"

    if not file_path.exists():
        with open(file_path, "w") as f:
            json.dump([], f)

    return file_path


def extract_args(args):
    if args.command == "create":
        template_name = str(args.project_type)
        project_name = str(args.name)
        package_name = str(args.package)

        if not package_name:
            package_name = normalize(project_name)

        return {
            "template": template_name,
            "project_name": project_name,
            "package_name": package_name
        }


def normalize(name: str):
    name = name.lower()
    name = re.sub(r"[^\w\s]", "", name)  # remove special chars
    name = re.sub(r"[\s\-]+", "_", name)  # spaces/dashes → underscore
    return name


def load_projects(file_path: Path):

    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def log_project(project_name: str, project_path: Path):

    file_path = get_regitry_file()

    data = load_projects(file_path)

    if not any(p["Path"] == str(project_path.resolve()) for p in data):
        data.append({"Project name": project_name,
                     "Path": str(project_path.absolute())}
                    )

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


args = get_cli_args()
parsed_args = extract_args(args)
print(
    f'creating {parsed_args["template"]} project titled "{
        parsed_args["project_name"]}"'
)
project_path = generate(parsed_args)
log_project(parsed_args["project_name"], project_path)
