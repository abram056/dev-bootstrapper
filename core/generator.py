from templates.loader import load_template


def generate(context: dict[str, str]):
    template_name = context["template"]
    template_content = load_template(template_name)
