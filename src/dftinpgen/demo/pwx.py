"""Demo generating input files for doing a calculation with pw.x."""

import sys
import pkg_resources
import argparse
import ast

from ase import io as ase_io

from dftinpgen.qe.pwx import PwxInputGenerator


FEO_STRUCTURE_FILE = pkg_resources.resource_filename(
    "dftinpgen.demo", "feo_poscar.vasp"
)


def get_parser():
    description = """Script demonstrating input file generation for pw.x."""
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    structure_file = """Path to file with the input crystal structure."""
    parser.add_argument(
        "-i",
        "--input-structure",
        default=FEO_STRUCTURE_FILE,
        help=structure_file,
    )

    calculation_presets = """Preset group of tags and default values to use."""
    parser.add_argument(
        "-c",
        "--calculation-presets",
        choices=["scf", "relax", "vc-relax"],
        default="scf",
        help=calculation_presets,
    )

    custom_settings_file = "Path to JSON file with custom DFT settings."
    parser.add_argument(
        "-sf",
        "--custom-settings-file",
        default=None,
        help=custom_settings_file,
    )

    custom_settings_dict = """Dictionary of custom DFT settings to use. NB:
    dict items with quotes must be escaped or quoted. Example:
    '{"pseudo_dir": "/path/to/pseudo_dir/"}'."""
    parser.add_argument(
        "-sd",
        "--custom-settings-dict",
        default="{}",
        type=str,
        help=custom_settings_dict,
    )

    write_to_file = """Boolean specifying whether to write pw.x input to file
    (True) or to standard output (False)."""
    parser.add_argument(
        "-w",
        "--write-to-file",
        default=False,
        type=bool,
        help=write_to_file,
    )

    pwx_input_file = """Path to file in which to write pw.x input settings.
    NB: This argument is ignored if "write_to_file" is set to False."""
    parser.add_argument(
        "-o", "--pwx-input-file", default="./pwx.in", help=pwx_input_file
    )

    return parser


def generate_pwx_input(sys_args):
    parser = get_parser()
    args = parser.parse_args(sys_args)
    crystal_structure = ase_io.read(args.input_structure)
    custom_settings_dict = ast.literal_eval(args.custom_settings_dict)

    pwig = PwxInputGenerator(
        crystal_structure=crystal_structure,
        calculation_presets=args.calculation_presets,
        custom_sett_file=args.custom_settings_file,
        custom_sett_dict=custom_settings_dict,
        pwx_input_file=args.pwx_input_file,
    )

    if not args.write_to_file:
        print(pwig.pwx_input_as_str)
    else:
        pwig.write_input_files()


if __name__ == "__main__":
    """
    When run as a script, this module will generate input files to use with
    pw.x, for a specified crystal structure, calculation presets, and any
    custom DFT settings on top of preset defaults.

    For a list of optional arguments, see `get_parser()` or run this script
    with "-h" as an argument.
    """
    generate_pwx_input(sys.argv[1:])
