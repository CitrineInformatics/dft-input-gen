import os
import pytest

from dftinpgen.base import DftInputGenerator


def test_dftinputgenerator_abstract():
    with pytest.raises(TypeError):
        DftInputGenerator()
