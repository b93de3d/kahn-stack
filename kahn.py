#!/usr/bin/env python3

import sys
from typing import List

VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_PATCH = 0

VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"


def ERROR(msg: str):
    print(f"ERROR :: {msg}")


def TODO(msg: str):
    print(f"TODO  :: {msg}")


def USAGE(msg: str):
    print(f"USAGE :: {msg}")


class Command:

    def __init__(self, name: str, subcommands: List["Command"]):
        self.name = name
        self.subcommands = subcommands

    def exec(self, args, parents_str):
        cmd = f"{parents_str} {' '.join(args)}".strip()
        print(f"Running command: `{cmd}`")
        TODO(f"`{parents_str}` is not implemented")

    def run(self, args: List[str], parent_names: list[str]):
        parents_str = " ".join(name for name in parent_names)

        if len(self.subcommands) == 0:
            if "--help" in args:
                print(f"Help info for: `{parents_str}`")
                exit(0)
            self.exec(args, parents_str)
            exit(0)

        if len(args) < 1:
            ERROR("Missing subcommand")
            USAGE(f"{parents_str} <SUBCOMMAND> <ARGS>")
            USAGE(f"Run {parents_str} --help to view available subcommands")
            exit(1)

        subcommand_name = args[0]
        subcommand_args = args[1:]

        if subcommand_name in ["help", "--help", "-h"]:
            USAGE(f"{parents_str} <SUBCOMMAND> <ARGS>")
            print(f"Available subcommands:")
            for s in self.subcommands:
                print(f"    {s.name}")
            exit(0)

        subcommand = None
        for s in self.subcommands:
            if s.name == subcommand_name:
                subcommand = s
                break

        if subcommand is None:
            ERROR(f"Subcommand not found: `{subcommand_name}`")
            USAGE(f"Run {parents_str} --help to view available subcommands")
            exit(1)

        parent_names.append(subcommand_name)
        subcommand.run(subcommand_args, parent_names)


class Version(Command):

    def exec(self, args, parents_str):
        print(f"Kahn Stack [{VERSION}]")


prog = Command(
    name="kahn",
    subcommands=[
        Version(name="version", subcommands=[]),
        Command(name="dev", subcommands=[]),
        Command(name="instance", subcommands=[
            Command(name="add", subcommands=[]),
            Command(name="remove", subcommands=[]),
        ]),
    ])


def main():
    prog_name = sys.argv[0].split("/")[-1]
    args = sys.argv[1:]

    prog.run(args, [prog_name])


if __name__ == "__main__":
    main()
