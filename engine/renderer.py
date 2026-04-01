def render(content: str, context: dict[str, str]) -> str:
    for key, value in context.items():
        content = content.replace(f"{{{{{key}}}}}", value)

    return content
