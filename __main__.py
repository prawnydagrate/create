#! /usr/bin/env python3

import argparse

TYPES = [
    "py",
    # "rust",
    # "aoc",
]


def main():
    parser = argparse.ArgumentParser(
        description="Create projects with simple templates"
    )
    subparsers = parser.add_subparsers(
        title="Commands",
        help="The type of project to create",
        dest="command",
        required=True,
    )
    modules = {}
    for t in TYPES:
        modules[t] = mod = __import__("commands", fromlist=[t]).__dict__[t]  # python magic haha
        mod.add_commands(subparsers)
    args = parser.parse_args()
    next_steps = modules[args.command].run(args)
    print("\nYour project has been created! Here are your next steps:")
    padlen = len(str(len(next_steps)))
    for i, step in enumerate(next_steps):
        lines = step.splitlines()
        print(f"{i+1: >{padlen}}. ", end="")
        for j, line in enumerate(lines):
            if j == 0:
                print(line)
                continue
            print(" " * (padlen + 2) + line)


if __name__ == "__main__":
    main()
