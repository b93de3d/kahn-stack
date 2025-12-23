#!/usr/bin/env python3
import glob
import json
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

    exit_code = process.wait()
    if exit_code != 0:
        if error_output:
            ERROR(error_output.decode(), end='')
        exit(exit_code)


def replace_in_all_files_and_filepaths(path: str, find: str, replace: str):
    run_shell(
        f"find {path} -type f -exec "
        f"sed -i 's/{find}/{replace}/g' {{}} +"
    )
    run_shell(
        f"find {path} -depth -name '*{find}*' "
        f"-execdir rename '{find}' '{replace}' '{{}}' \;"
    )


REPLACE_PATTERNS = [
    ("_KAHN_PROJECT_TITLE_", lambda: ENV.get("Project Title")),
    ("_KAHN_PROJECT_SLUG_", lambda: ENV.get("Project Slug")),
    ("_KAHN_SHORT_NAME_", lambda: ENV.get("Short Name")),
]


class Component:

    def __init__(self, template_path):
        self.template_path = template_path
        with open(f"{template_path}/kahn_component.md") as f:
            md_lines = []
            for line in f.readlines():
                for replace_str, getter in REPLACE_PATTERNS:
                    line = line.replace(replace_str, getter())
                md_lines.append(line)
            self.md_lines = md_lines

        self.title = self._get_section_lines("kahn_component_title")[0]
        self.slug = self._get_section_lines("kahn_component_slug")[0]
        self.setup_lines = self._get_section_lines("kahn_setup")
        self.run_dev_lines = self._get_section_lines("kahn_run_dev")

    def _get_section_lines(self, section_title) -> List[str]:
        section_start = -1
        for i in range(len(self.md_lines)):
            line = self.md_lines[i].strip()
            if line == f"# {section_title}":
                section_start = i + 1
                break
            i += 1

        if section_start < 0:
            ERROR(f"Section not found in kahn_component.md: `{section_title}`")
            exit(1)

        section_lines = []
        for i in range(section_start, len(self.md_lines)):
            line = self.md_lines[i].strip()
            if line == "```":
                break
            if line == "":
                continue
            section_lines.append(line)

        return section_lines


class Env:

    def __init__(self):
        # Try load from file, else prompt user to provide each value
        try:
            with open("kahn_config.json", "r") as f:
                self.config = json.loads(f.read())
        except FileNotFoundError:
            self.config = {}
            self._dump()

    def _dump(self):
        with open("kahn_config.json", "w") as f:
            f.write(json.dumps(self.config, indent=4))

    def get(self, key, default=None):
        value = self.config.get(key)
        while value in ["", None]:
            if default:
                value = input(f"Provide a value for {key} ({default}): ") or default
            else:
                value = input(f"Provide a value for {key}: ")
            if value in ["", None]:
                ERROR(f"Invalid value: `{value}`")
                continue
            self.config[key] = value
            self._dump()

        return value


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


class TemplateList(Command):

    def exec(self, args, parents_str):
        run_shell(["ls", "templates"])


class TemplateDeploy(Command):

    def exec(self, args, parents_str):
        available_templates = glob.glob("templates/*")
        for arg in args:
            template_path = f"templates/{arg}"
            if template_path not in available_templates:
                ERROR(f"Template not found `{template_path}`")
                USAGE(f"AVAILABLE TEMPLATES: {available_templates}")
                exit(1)


            print(f"DEPLOYING TEMPLATE: {arg}")
            project_title = ENV.get('Project Title')
            project_slug = ENV.get('Project Slug', project_title.replace(" ", "_").lower())
            ENV.get('Short Name', "".join(p[0] for p in project_slug.split("_") if len(p) > 0))

            component = Component(template_path)
            dest_path = ENV.get(f"{component.title} Folder Name", component.slug)

            run_shell(f"cp -r {template_path} {dest_path}")

            for replace_string, getter in REPLACE_PATTERNS:
                replace_in_all_files_and_filepaths(dest_path, replace_string, getter())

            with open(f"{dest_path}/kahn_setup.sh", "w") as f:
                f.writelines([f"{l}\n" for l in component.setup_lines])
            run_shell(f"cd {dest_path} && sh kahn_setup.sh")
            run_shell(f"rm {dest_path}/kahn_setup.sh")

            for line in component.run_dev_lines:
                USAGE("Run using:")
                USAGE(line)


class ComponentList(Command):

    def exec(self, args, parents_str):
        component_mds = glob.glob("**/kahn_component.md", recursive=True)
        for md_path in component_mds:
            if not md_path.startswith("templates/"):
                component_path = md_path[:-len("/kahn_component.md")]
                component = Component(component_path)
                print("[COMPONENT]")
                print(component.title)
                print(f"[TO RUN]")
                print(f"> cd {component_path}")
                for line in component.run_dev_lines:
                    print(f"> {line}")
                print("-----------------------------")


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
        Command(name="template", subcommands=[
            TemplateList(name="list", subcommands=[]),
            TemplateDeploy(name="deploy", subcommands=[]),
        ]),
        Command(name="component", subcommands=[
            ComponentList(name="list", subcommands=[]),
        ]),
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

ENV = Env()


def main():
    prog_name = sys.argv[0].split("/")[-1]
    args = sys.argv[1:]

    prog.run(args, [prog_name])


if __name__ == "__main__":
    main()
