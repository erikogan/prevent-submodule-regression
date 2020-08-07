import sys

from prevent_submodule_regression.parser import Parser


def main():
    Parser().run(sys.argv[1:])
