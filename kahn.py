#!/usr/bin/env python3

import sys
import subprocess
from typing import List, Union

VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_PATCH = 0

VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
GRAY = "\033[90m"
RESET = "\033[0m"

def ERROR(msg: str, **kwargs):
    print(f"{RED}ERROR{RESET} :: {msg}", **kwargs)


def TODO(msg: str, **kwargs):
    print(f"{YELLOW}TODO{RESET}  :: {msg}", **kwargs)


def USAGE(msg: str, **kwargs):
    print(f"{GREEN}USAGE{RESET} :: {msg}", **kwargs)


def LOG(msg: str, **kwargs):
    print(f"{GRAY}LOG{RESET}   :: {msg}", **kwargs)




def run_shell(command: Union[List[str], str]):
    shell = type(command) == str
    if shell:
        cmd_str = command
    else:
        cmd_str = " ".join(command)
    print(f"{GREEN}-- kahn run | {YELLOW}{cmd_str}{GREEN} | --{RESET}")
    process = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in process.stdout:
        LOG(line.decode(), end='')
    error_output = process.stderr.read()
    if error_output:
        ERROR(error_output.decode(), end='')

    exit_code = process.wait()
    if exit_code != 0:
        exit(exit_code)

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

class Ls(Command):

    def exec(self, args, parents_str):
        run_shell("ls")
        run_shell(["ls", "-la"])
        if "-e" in args:
            run_shell("ls -la nonexistantdir")
        run_shell("ls -la")


class Rand(Command):

    def exec(self, args, parents_str):
        run_shell("tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 48")


class Kamal(Command):

    def exec(self, args, parents_str):
        cmd = ["kamal", self.name] + args + ["-c", "config/ggg.yaml"]
        run_shell(cmd)


prog = Command(
    name="kahn",
    subcommands=[
        Version(name="version", subcommands=[]),
        Ls(name="ls", subcommands=[]),
        Rand(name="rand", subcommands=[]),
        Command(name="dev", subcommands=[]),
        Kamal(name="deploy", subcommands=[]),
        Kamal(name="setup", subcommands=[]),
        Kamal(name="app", subcommands=[]),
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
