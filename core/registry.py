from pathlib import Path
import json
import sys
import os


def get_regitry_file() -> Path:

    data_dir = Path.home() / ".dev-bootstrapper"
    data_dir.mkdir(exist_ok=True)

    file_path = data_dir / "projects.json"

    if not file_path.exists():
        with open(file_path, "w") as f:
            json.dump([], f)

    return file_path


def load_projects():
    file_path = get_regitry_file()

    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_projects(data):
    file_path = get_regitry_file()

    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


def add_project(project_name: str, project_path: Path):
    data = load_projects()
    resolved_path = str(project_path.resolve())

    if not any(p["Path"] == str(project_path.resolve()) for p in data):
        data.append({"Project name": project_name, "Path": resolved_path})

        save_projects(data)


def list_projects():
    data = load_projects()

    if not data:
        print("No values found")
        return

    for i, project in enumerate(data, start=1):
        print(f"{i}. Project Name: {project['Project name']}")
        print(f"     Project Path: {project['Path']}")


def remove_project(name: str):

    data = load_projects()

    new_data = [p for p in data if p["Project name"] != name]

    if len(data) == len(new_data):
        print(f"No project found with name '{name}'")
        return

    save_projects(new_data)
    print(f"Removed project: {name}.")
