from pathlib import Path
import re
import json

from cli.main import get_cli_args
from core.generator import generate
from core.registry import (
    add_project,
    list_projects,
)


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
            "package_name": package_name,
        }


def normalize(name: str):
    name = name.lower()
    name = re.sub(r"[^\w\s]", "", name)  # remove special chars
    name = re.sub(r"[\s\-]+", "_", name)  # spaces/dashes → underscore
    return name


args = get_cli_args()

if args.command == "create":
    parsed_args = extract_args(args)
    project_path = generate(parsed_args)
    add_project(parsed_args["project_name"], parsed_args["project_path"])

elif args.command == "list":
    list_projects()
