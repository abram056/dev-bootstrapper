"""Example script for {{project_name}}.

Run with: uv run scripts/process.py
"""

from {{package_name}} import analysis


def main() -> None:
    data = [10, 20, 30, 40, 50]
    print("Summary:", analysis.summarize(data))


if __name__ == "__main__":
    main()
