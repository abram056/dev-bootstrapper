from cli.main import get_cli_args
from core.generator import generate
parsed_args = get_cli_args()
print(f'creating {parsed_args["template"]} project titled "{
      parsed_args["project_name"]}"')
generate(parsed_args)
