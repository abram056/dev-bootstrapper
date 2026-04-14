from cli.main import get_cli_args
from core.generator import generate
import re


def extract_args(args):
    if args.command == "create":
        template_name = args.project_type
        project_name = args.name
        package_name = args.package

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


args = get_cli_args()
parsed_args = extract_args(args)


print(
    f'creating {parsed_args["template"]} project titled "{
        parsed_args["project_name"]}"'
)
generate(parsed_args)
