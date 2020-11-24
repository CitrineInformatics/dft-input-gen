import os
import pytest


from dftinpgen.cli import get_parser
from dftinpgen.cli import driver


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
    # this is only a barebones test to ensure that the arguments have been
    # passed on to the right subparser
    with pytest.raises(SystemExit):
        driver(["pw.x"])
    assert "required" in capsys.readouterr().err
