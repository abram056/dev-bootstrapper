import argparse


def get_cli_args():

    parser = argparse.ArgumentParser(description="Dev project Bootstrapper")

    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Create a new project")

    list_parser = subparsers.add_parser("list", help="List projects")

    remove_parser = subparsers.add_parser("remove", help="Delete project")

    create_parser.add_argument(
        "project_type", choices=["fastapi", "python"], help="Project type"
    )

    create_parser.add_argument(
        "-n", "--name", metavar="project_name", required=True, help="Project name"
    )

    remove_parser.add_argument("name")

    parser.add_argument(
        "-p", "--package", metavar="package_name", required=False, help="Package name"
    )

    args = parser.parse_args()

    return args
