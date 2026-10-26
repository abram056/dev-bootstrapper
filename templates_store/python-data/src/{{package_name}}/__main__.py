"""{{project_name}} example pipeline entry point."""

from {{package_name}} import __version__


def main() -> None:
    from {{package_name}} import analysis

    print(f"{{project_name}} v{__version__}")
    result = analysis.summarize([1, 2, 3, 4, 5])
    print("Summary:", result)


if __name__ == "__main__":
    main()
