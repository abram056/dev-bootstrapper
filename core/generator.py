from pathlib import Path
from engine.file_manager import write_file
from engine.renderer import render
from templates.loader import load_template


def generate(context: dict[str, str]):
    template_name = context["template"]
    project_name = context["project_name"]

    template_files = load_template(template_name)

    output_dir = Path(project_name)

    for file in template_files:
        relative_path = file['path']
        content = file['content']

        rendered_content = render(content, context)
        write_file(output_dir, relative_path, rendered_content)
