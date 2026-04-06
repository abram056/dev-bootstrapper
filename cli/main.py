import argparse


def get_cli_args():

    parser = argparse.ArgumentParser(
        description="Dev project Bootstrapper"
    )

    parser.add_argument(
        '-c', '--create', metavar='project_type', choices=['fastapi'],
        required=True, help="Project type"
    )

    parser.add_argument(
        '-n', '--name', metavar="project_name",
        required=True, help="Project name"
    )

    args = parser.parse_args()

    return {
        "template": str(args.create),
        "project_name": str(args.name)
    }
