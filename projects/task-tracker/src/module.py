import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DIRS = [
    PROJECT_ROOT / "src",
    PROJECT_ROOT / "tests",
    PROJECT_ROOT / "docs"
]

def init_structure():
    for d in DIRS:
        d.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {d}")

    cli_file = PROJECT_ROOT / "src" / "module.py"
    cli_code = (
        "#!/usr/bin/env python3\n"
        "\"\"\"Task Tracker CLI - Main entry point.\"\"\"\n"
        "\n"
        "import argparse\n"
        "import sys\n"
        "\n"
        "def main():\n"
        "    parser = argparse.ArgumentParser(description=\"Task Tracker CLI\")\n"
        "    subparsers = parser.add_subparsers(dest=\"command\", help=\"Available commands\")\n"
        "\n"
        "    # Example: add command\n"
        "    add_parser = subparsers.add_parser(\"add\", help=\"Add a new task\")\n"
        "    add_parser.add_argument(\"title\", help=\"Title of the task\")\n"
        "\n"
        "    # Example: list command\n"
        "    list_parser = subparsers.add_parser(\"list\", help=\"List all tasks\")\n"
        "    list_parser.add_argument(\"--status\", help=\"Filter by status\", default=None)\n"
        "\n"
        "    args = parser.parse_args()\n"
        "\n"
        "    if not args.command:\n"
        "        parser.print_help()\n"
        "        sys.exit(1)\n"
        "\n"
        "    if args.command == \"add\":\n"
        "        print(f\"Adding task: {args.title}\")\n"
        "        # TODO: Implement add functionality\n"
        "    elif args.command == \"list\":\n"
        "        print(\"Listing tasks...\")\n"
        "        # TODO: Implement list functionality\n"
        "\n"
        "if __name__ == \"__main__\":\n"
        "    main()\n"
    )
    cli_file.write_text(cli_code)
    print(f"Created CLI entry point: {cli_file}")

if __name__ == "__main__":
    init_structure()
