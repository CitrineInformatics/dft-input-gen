"""Unit tests for helper utilities in :mod:`dftinpgen.utils`."""

import os
import pytest

from ase import io as ase_io

from dftinpgen.utils import get_elem_symbol
from dftinpgen.utils import read_crystal_structure
from dftinpgen.utils import get_kpoint_grid_from_spacing
from dftinpgen.utils import DftinpgenUtilsError


test_base_dir = os.path.dirname(__file__)
feo_conv_file = os.path.join(test_base_dir, "qe", "files", "feo_conv.vasp")
feo_conv = ase_io.read(feo_conv_file)


def test_get_elem_symbol():
    assert get_elem_symbol("Fe-34") == "Fe"
    assert get_elem_symbol("3RGe-34") == "Ge"
    with pytest.raises(DftinpgenUtilsError):
        get_elem_symbol("G23")


def test_read_crystal_structure():
    # str with path to crystal structure file is OK
    cs = read_crystal_structure(feo_conv_file)
    assert cs == feo_conv
    # any other type of input should throw an error
    with pytest.raises(TypeError):
        read_crystal_structure(feo_conv)


def test_kpoint_grid_from_spacing():
    assert get_kpoint_grid_from_spacing(feo_conv, 0.2) == pytest.approx([7, 7, 7])
