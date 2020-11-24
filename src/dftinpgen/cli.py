import argparse

from dftinpgen.demo.pwx import build_pwx_parser
from dftinpgen.demo.pwx import generate_pwx_input_files


def get_parser():
    # create the top-level parser
    description = """Input file generation for DFT codes."""
    parser = argparse.ArgumentParser(description=description)

    # dummy function to print parser usage to console
    def _print_usage(*args):
        return parser.print_usage(file=None)

    # if cli tool is run without any arguments, print usage:
    parser.set_defaults(func=_print_usage)

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
    parser = get_parser()
    args = parser.parse_args(*sys_args)
    args.func(args)


if __name__ == "__main__":
    driver()  # pragma: no cover
