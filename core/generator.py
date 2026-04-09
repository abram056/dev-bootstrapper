from pathlib import Path
from engine.file_manager import write_file
from engine.renderer import render_content, render_path
from templates.loader import load_template
import subprocess
import os


def generate(context: dict[str, str]):
    template_name = context["template"]
    project_name = context["project_name"]

    template_files = load_template(template_name)

    output_dir = Path(project_name)

    for file in template_files:
        relative_path = file['path']
        content = file['content']

        rendered_path = render_path(relative_path, context)
        rendered_content = render_content(content, context)
        write_file(output_dir, rendered_path, rendered_content)

    create_virtual_env(output_dir)
    install_dependencies(output_dir)


def create_virtual_env(project_path: Path):
    subprocess.run(["python", "-m", "venv", ".venv"], cwd=project_path)


def install_dependencies(project_path: Path):
    pip_path = ""
    if os.name == "nt":
        pip_path = ".venv/Scripts/pip.exe"
    else:
        pip_path = ".venv/bin/pip"

    subprocess.run([str(pip_path), "install", "-r",
                   "requirements.txt"], cwd=project_path)
