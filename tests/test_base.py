import os
import pytest

from ase import io as ase_io

from dftinputgen.base import DftInputGenerator

test_data_dir = os.path.join(os.path.dirname(__file__), "files")
feo_struct = ase_io.read(os.path.join(test_data_dir, "feo_conv.vasp"))
dummy_sett_file = os.path.join(test_data_dir, "dummy_settings.json")


def test_abstractclass():
    with pytest.raises(TypeError):
        DftInputGenerator()

    class DummyInputGenerator(DftInputGenerator):
        pass

        @property
        def dft_package(self):
            return super(DummyInputGenerator, self).dft_package

        @property
        def calculation_settings(self):
            return super(DummyInputGenerator, self).calculation_settings

        def write_input_files(self):
            super(DummyInputGenerator, self).write_input_files()

    dig = DummyInputGenerator(crystal_structure=feo_struct)
    with pytest.raises(NotImplementedError):
        print(dig.dft_package)
    with pytest.raises(NotImplementedError):
        print(dig.calculation_settings)
    with pytest.raises(NotImplementedError):
        dig.write_input_files()


def test_crystal_structure():
    DftInputGenerator.__abstractmethods__ = frozenset()

    class DummyInputGenerator(DftInputGenerator):
        pass

    # no crystal structure: type error
    with pytest.raises(TypeError, match="ase.Atoms"):
        dig = DummyInputGenerator()

    # crystal structure input ok
    dig = DummyInputGenerator(crystal_structure=feo_struct)
    assert dig.crystal_structure == feo_struct


def test_constructor():
    DftInputGenerator.__abstractmethods__ = frozenset()

    class DummyInputGenerator(DftInputGenerator):
        pass

    dig = DummyInputGenerator(crystal_structure=feo_struct)
    # default constructor arguments
    assert dig.write_location == os.getcwd()
    assert dig.overwrite_files

    dig = DummyInputGenerator(
        crystal_structure=feo_struct,
        custom_sett_file=dummy_sett_file,
        custom_sett_dict={"tag_3": "FROM_DICT"},
        write_location=test_data_dir,
        overwrite_files=False,
    )
    assert dig.custom_sett_file == dummy_sett_file
    assert dig.custom_sett_from_file == {"tag_1": "FROM_FILE", "tag_2": 0}
    assert dig.custom_sett_dict == {"tag_3": "FROM_DICT"}
    assert dig.write_location == test_data_dir
    assert not dig.overwrite_files
