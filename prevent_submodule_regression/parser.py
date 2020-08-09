import os
import re
import subprocess
import sys

import colorama
from colorama import Back
from colorama import Fore
from colorama import Style


class Parser:
    def run(self, args):

        self.chdir_root()

        if not args:
            args = self.list_of_submodules()

        for path in args:
            self.process(path)

    def process(self, path):
        if not self.is_staged(path):
            return

        current_sha = self.submodule_sha(path)

        if not current_sha:
            print(
                f"{Fore.BLACK}{Style.BRIGHT}{Back.YELLOW}[WARNING]{Style.RESET_ALL} {path} is not a submodule",
                file=sys.stderr,
            )
            return

        shas = self.past_submodule_shas(path)

        if current_sha in shas:
            exit(
                f"{Fore.WHITE}{Style.BRIGHT}{Back.RED}[ERROR]{Style.RESET_ALL}"
                f" {Fore.CYAN}{path}{Style.RESET_ALL} SHA {Fore.YELLOW}{current_sha}{Style.RESET_ALL}"
                " was already committed. This appears to be a regression."
            )
        exit(0)

    def submodule_sha(self, path):
        result = subprocess.run(
            ["git", "ls-files", "--stage", path], capture_output=True, check=True
        )
        parts = result.stdout.decode("utf-8").strip().split(" ")
        if parts[0] != "160000":
            return None
        return parts[1]

    def past_submodule_shas(self, path):
        result = subprocess.run(
            ["git", "rev-list", "HEAD", "--", path], capture_output=True, check=True
        )
        commits = result.stdout.decode("utf-8").strip().split("\n")

        def extract_sha(commit, path):
            dir = os.path.dirname(path)
            base = os.path.basename(path)
            tree = f"{commit}:{dir}" if dir else commit

            result = subprocess.run(
                ["git", "ls-tree", tree], capture_output=True, check=True
            )
            data = result.stdout.decode("utf-8")
            pat = re.compile(r"\d{6} \w+ ([0-9a-f]{40})\t" + base + "\n")

            res = pat.search(data)
            if not res:
                print(
                    f"{Fore.BLACK}{Style.BRIGHT}{Back.YELLOW}[WARNING]{Style.RESET_ALL}"
                    f" {path} not found in SHA {commit}!",
                    file=sys.stderr,
                )

                return res
            return res[1]

        return [extract_sha(c, path) for c in commits]

    def list_of_submodules(self):
        # Rely on the fact that the .gitmodules file is in git config format
        result = subprocess.run(
            ["git", "config", "--file", ".gitmodules", "--get-regexp", "path"],
            capture_output=True,
            check=True,
        )
        return [
            line.split(" ")[1]
            for line in result.stdout.decode("utf-8").strip().split("\n")
        ]

    def is_staged(self, path):
        # There is almost assuredly a better way to do this
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--", path],
            capture_output=True,
            check=True,
        )
        return not not result.stdout.decode("utf-8").strip()

    def chdir_root(self):
        # TODO: REMOVE
        os.chdir("../data-river")
        return
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], capture_output=True, check=True
        )
        os.chdir(result.stdout.decode("utf-8").strip())

    def __init__(self):
        # Safety
        colorama.init(autoreset=True)
