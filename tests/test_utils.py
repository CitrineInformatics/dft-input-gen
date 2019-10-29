"""Unit tests for helper utilities in :mod:`dftinpgen.utils`."""

import pytest

from dftinpgen.utils import get_elem_symbol
from dftinpgen.utils import DftinpgenUtilsError


def test_get_elem_symbol():
    assert get_elem_symbol('Fe-34') == 'Fe'
    assert get_elem_symbol('3RGe-34') == 'Ge'
    with pytest.raises(DftinpgenUtilsError):
        print(get_elem_symbol('G23'))
