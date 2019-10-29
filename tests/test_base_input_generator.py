import os
import pytest

FOUND_ASE = False
try:
    import ase
except (ImportError, ModuleNotFoundError) as err:
    msg = 'Unable to import ase (required for testing)'
    print(msg)
else:
    FOUND_ASE = True

from dftinpgen.base import DftInputGenerator
from dftinpgen.base import DftInputGeneratorError


test_base_dir = os.path.dirname(__file__)
feo_conv_file = os.path.join(test_base_dir, 'qe', 'files', 'feo_conv.vasp')
if FOUND_ASE:
    feo_conv = ase.io.read(feo_conv_file)


@pytest.mark.skipif(not FOUND_ASE, reason='ase not imported')
def test_crystal_structure_file_input():
    dig = DftInputGenerator(crystal_structure=feo_conv_file,
                            dft_package='TEST-DFT',
                            base_recipe='TEST-RECIPE')

    assert dig.crystal_structure == feo_conv
    assert dig.dft_package == 'test-dft'
    assert dig.base_recipe == 'test-recipe'
    assert dig.custom_sett_file is None
    assert not dig.custom_sett_dict
    assert dig.write_location == os.getcwd()
    assert dig.overwrite_files


def test_crystal_structure_input_type_error():
    with pytest.raises(TypeError):
        print(DftInputGenerator(crystal_structure=27))


def test_kpoint_grid_from_spacing():
    # no crystal structure error
    dig = DftInputGenerator()
    with pytest.raises(DftInputGeneratorError):
        print(dig.get_kpoint_grid_from_spacing(0.1))
    # with crystal structure, all OK
    dig = DftInputGenerator(crystal_structure=feo_conv)
    assert dig.get_kpoint_grid_from_spacing(0.2) == [7, 7, 7]
