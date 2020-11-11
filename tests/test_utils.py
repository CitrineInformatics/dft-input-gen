"""Unit tests for helper utilities in :mod:`dftinpgen.utils`."""

import os
import pytest

FOUND_ASE = False
try:
    from ase import io as ase_io
except (ImportError, ModuleNotFoundError) as err:
    print("Unable to import the `ase` package. Some tests will be skipped")
else:
    FOUND_ASE = True

from dftinpgen.utils import get_elem_symbol
from dftinpgen.utils import read_crystal_structure
from dftinpgen.utils import get_kpoint_grid_from_spacing
from dftinpgen.utils import DftinpgenUtilsError


test_base_dir = os.path.dirname(__file__)
feo_conv_file = os.path.join(test_base_dir, "qe", "files", "feo_conv.vasp")
if FOUND_ASE:
    feo_conv = ase_io.read(feo_conv_file)


def test_get_elem_symbol():
    assert get_elem_symbol("Fe-34") == "Fe"
    assert get_elem_symbol("3RGe-34") == "Ge"
    with pytest.raises(DftinpgenUtilsError):
        get_elem_symbol("G23")


@pytest.mark.skipif(not FOUND_ASE, reason="ase not imported")
def test_read_crystal_structure():
    # str with path to crystal structure file is OK
    cs = read_crystal_structure(feo_conv_file)
    assert cs == feo_conv
    # any other type of input should throw an error
    with pytest.raises(TypeError):
        read_crystal_structure(feo_conv)


def test_kpoint_grid_from_spacing():
    get_kpoint_grid_from_spacing(feo_conv, 0.2) == pytest.approx([7, 7, 7])