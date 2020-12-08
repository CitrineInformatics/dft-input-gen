import argparse

from dftinputgen.demo.pwx import build_pwx_parser
from dftinputgen.demo.pwx import generate_pwx_input_files


def get_parser():
    """Returns an argument parser for the CLI tool."""
    # create the top-level parser
    description = """Input file generation for DFT codes."""
    parser = argparse.ArgumentParser(description=description)

    # if cli tool is run without any arguments, print usage:
    # dummy lambda to circumvent ``'Namespace' object has no attribute 'func'``
    # error if the `print_usage` function is used as is.
    # do the passed args mess up the `file=None` defaults?
    parser.set_defaults(func=lambda _: parser.print_usage())

    # add subparsers
    subparsers = parser.add_subparsers()

    # add pw.x subparser
    pwx_help = "Generate input file for pw.x (from the QE suite)"
    pwx_parser = subparsers.add_parser("pw.x", help=pwx_help)
    build_pwx_parser(pwx_parser)
    pwx_parser.set_defaults(func=generate_pwx_input_files)

    # other subparsers, to be added similarly, go here
    # e.g. ones for gpaw/vasp

    return parser


def driver(*sys_args):
    """CLI driver function."""
    parser = get_parser()
    args = parser.parse_args(*sys_args)
    args.func(args)


if __name__ == "__main__":
    driver()  # pragma: no cover
