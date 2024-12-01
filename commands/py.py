import os
import shutil
import subprocess
import sys


def add_commands(subparsers):
    parser = subparsers.add_parser("py", help="Create a Python project")
    parser.add_argument("name", help="The name of the project")
    parser.add_argument(
        "--main",
        default="main.py",
        help="The main entry point of the project",
    )
    parser.add_argument(
        "--no-venv",
        action="store_true",
        default=False,
        help="Do not create a virtual environment with virtualenv",
    )
    parser.add_argument(
        "--no-requirements",
        action="store_true",
        default=False,
        help="Do not create a requirements.txt file",
    )
    parser.add_argument(
        "--no-git",
        action="store_true",
        default=False,
        help="Disable version control with Git",
    )


def bold(string: str) -> str:
    return f"\x1b[1m{string}\x1b[0m"


def create_proj_dir(name: str) -> list[str]:
    print(f"Creating project directory '{name}'")
    os.mkdir(name)
    os.chdir(name)
    return ["$ " + bold(f"cd '{name}'")]


def create_main(name: str) -> list[str]:
    print(f"Creating main file '{name}'")
    with open(name, "w") as f:
        f.write(
            """\
import sys


def main(argc: int, argv: list[str]) -> None:
    ...


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
"""
        )
    return ["$ " + bold(f"{os.path.basename(sys.executable)} {name}")]


def create_venv() -> list[str]:
    print("Creating virtual environment 'venv'")
    __import__("virtualenv").run.cli_run(["venv"])
    return ["Activate the virtual environment 'venv'"]


def create_requirements() -> list[str]:
    print("Creating requirements.txt file")
    open("requirements.txt", "a").close()
    return []


def create_git_repo() -> list[str]:
    print("Initializing a Git repository")
    git = shutil.which("git")
    if not git:
        print("Git installation not found; skipping this step")
        return [f"NOTE: A Git repository was {bold("not")} initialized"]
    proc = subprocess.Popen(
        [git, "init"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
    )
    _, err = proc.communicate()
    if proc.returncode != 0:
        print(bold(f"{git} init"), "yielded an error:")
        print(err.decode())
        return ["NOTE: Initializing a Git repository yielded an error"]
    return [
        f"""\
$ {bold("git add .")}
$ {bold("git commit -m 'initial commit'")}\
"""
    ]


def run(args):
    next_steps = []
    next_steps.extend(create_proj_dir(args.name))
    if not args.no_git:
        next_steps.extend(create_git_repo())
    if not args.no_venv:
        next_steps.extend(create_venv())
    if not args.no_requirements:
        next_steps.extend(create_requirements())
    next_steps.extend(create_main(args.main))
    return next_steps
