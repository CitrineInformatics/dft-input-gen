import os
import pytest

from dftinputgen.cli import get_parser
from dftinputgen.cli import driver


files_dir = os.path.join(os.path.dirname(__file__), "files")
test_struct = os.path.join(files_dir, "feo_conv.vasp")


def test_get_parser(capsys):
    parser = get_parser()
    assert "input file gen" in parser.description.lower()


def test_driver(capsys):
    # without-args default: print usage
    # Python 3: argparse does not complain
    # Python 2: argparse throws an error, exits
    try:
        driver([])
        msg = capsys.readouterr().out
    except SystemExit:
        msg = capsys.readouterr().err
    assert "usage: " in msg

    # subparser: invalid dft package choice error
    with pytest.raises(SystemExit):
        driver(["gpaw"])
    assert "invalid choice" in capsys.readouterr().err

    # pw.x package: missing required arguments error
    # only tests that the arguments have been passed on to the pw.x subparser
    with pytest.raises(SystemExit):
        driver(["pw.x"])
    assert "required" in capsys.readouterr().err

    # pw.x package: minimal working example
    import tempfile

    _tmp_file = tempfile.NamedTemporaryFile(mode="w", delete=True)
    filename = _tmp_file.name
    write_location = os.path.dirname(filename)
    driver(
        [
            "pw.x",
            "-i",
            test_struct,
            "-pre",
            "scf",
            "-loc",
            write_location,
            "-o",
            filename,
        ]
    )
