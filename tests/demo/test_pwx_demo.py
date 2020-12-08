import os
import json
import pytest
import argparse

from dftinputgen.utils import read_crystal_structure
from dftinputgen.demo.pwx import _get_default_parser
from dftinputgen.demo.pwx import build_pwx_parser
from dftinputgen.demo.pwx import run_demo


files_dir = os.path.join(os.path.dirname(__file__), "files")
feo_file = os.path.join(files_dir, "feo_poscar.vasp")
feo_struct = read_crystal_structure(feo_file)
sett_file = os.path.join(files_dir, "test_sett.json")
feo_scf_ref_in = os.path.join(files_dir, "feo_scf_ref.in")


def test_get_default_parser():
    parser = _get_default_parser()
    assert "pw.x" in parser.description


def test_get_parser_required_missing(capsys):
    parser = _get_default_parser()
    build_pwx_parser(parser)

    # input structure (required) missing: error
    with pytest.raises(SystemExit):
        parser.parse_args()
    stderr = capsys.readouterr().err
    assert "required" in stderr


def test_get_parser_default_args():
    parser = _get_default_parser()
    build_pwx_parser(parser)
    args = parser.parse_args(["-i", feo_file])
    assert args.crystal_structure == feo_struct
    assert args.calculation_presets is None
    assert args.custom_settings_file is None
    assert args.custom_settings_dict == {}
    assert not args.specify_potentials


def test_get_parser_input_args(capsys):
    parser = _get_default_parser()
    build_pwx_parser(parser)

    # invalid choice for `calculation_presets`
    with pytest.raises(SystemExit):
        parser.parse_args(["-i", feo_file, "-pre", "unsupported"])
    stderr = capsys.readouterr().err
    assert "invalid choice" in stderr

    # all ok
    args = parser.parse_args(
        [
            "-i",
            feo_file,
            "-o",
            "pwx.in",
            "-loc",
            "/path/to/location",
            "-dict",
            '{"key_1": "val", "key_2": 0}',
            "-file",
            "some_file",
            "-pre",
            "vc-relax",
        ]
    )
    assert args.calculation_presets == "vc-relax"
    assert args.custom_settings_file == "some_file"
    assert args.custom_settings_dict == {"key_1": "val", "key_2": 0}
    assert args.write_location == "/path/to/location"
    assert args.pwx_input_file == "pwx.in"


def test_run_demo():
    import tempfile

    _tmp_file = tempfile.NamedTemporaryFile(mode="w", delete=True)
    filename = _tmp_file.name
    write_location = os.path.dirname(filename)
    args = [
        "-i",
        feo_file,
        "-pre",
        "scf",
        "-file",
        sett_file,
        "-dict",
        '{"ecutwfc": 45}',
        "-loc",
        write_location,
        "-o",
        os.path.basename(filename),
    ]
    run_demo(args)

    with open(filename, "r") as fr:
        test = fr.read()
    with open(feo_scf_ref_in, "r") as fr:
        reference = fr.read().rstrip("\n")
    assert test == reference
