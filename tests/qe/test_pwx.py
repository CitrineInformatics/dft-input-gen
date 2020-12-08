"""Unit tests for the `PwxInputGenerator` class."""

import os
import pytest

from ase import io as ase_io

from dftinputgen.qe.pwx import PwxInputGenerator
from dftinputgen.qe.pwx import PwxInputGeneratorError
from dftinputgen.qe.pwx import _qe_val_formatter


# define module-level variables used for testing
# TODO(@hegdevinayi): refactor to fixtures (`pytest-data`)
test_data_dir = os.path.join(os.path.dirname(__file__), "files")
pseudo_dir = os.path.join(os.path.dirname(__file__), "files")
feo_struct = ase_io.read(os.path.join(test_data_dir, "feo_conv.vasp"))
al_fcc_struct = ase_io.read(os.path.join(test_data_dir, "al_fcc_conv.vasp"))
fe_pseudo = os.path.join(test_data_dir, "fe_pbe_v1.5.uspp.F.UPF")
o_pseudo = os.path.join(test_data_dir, "o_pbe_v1.2.uspp.F.UPF")
al_pseudo = os.path.join(test_data_dir, "al_pbe_v1.uspp.F.UPF")
with open(os.path.join(test_data_dir, "TEST_feo_conv_scf.in"), "r") as fr:
    feo_scf_in = fr.read().format(pseudo_dir=pseudo_dir)
with open(os.path.join(test_data_dir, "TEST_al_fcc_conv_scf.in"), "r") as fr:
    al_fcc_scf_in = fr.read().format(pseudo_dir=pseudo_dir)


def test_qe_val_formatter():
    assert _qe_val_formatter(True) == ".true."
    assert _qe_val_formatter("False") == '"False"'
    assert _qe_val_formatter(12345) == "12345"
    assert _qe_val_formatter(1e-10) == "1e-10"


def test_no_crystal_structure_input_error():
    with pytest.raises(TypeError):
        PwxInputGenerator()


def test_parameters_from_structure():
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    assert pwig.parameters_from_structure == {"nat": 4, "ntyp": 2}


def test_specify_potentials_attribute():
    # default specify_potentials = False
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    assert not pwig.specify_potentials
    pwig = PwxInputGenerator(
        crystal_structure=feo_struct, specify_potentials=True
    )
    assert pwig.specify_potentials


def test_pwx_input_file():
    # defaults: "pwx.in" if `calculation_presets` is not input
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    assert pwig.pwx_input_file == "pwx.in"
    # default otherwise: "[calculation_presets].in"
    pwig = PwxInputGenerator(
        crystal_structure=feo_struct, calculation_presets="vc-relax"
    )
    assert pwig.pwx_input_file == "vc-relax.in"
    # or use any user-input file name
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    pwig.pwx_input_file = "test.in"
    assert pwig.pwx_input_file == "test.in"


def test_dft_package_name():
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    assert pwig.dft_package == "qe"


def test_get_pseudo_name():
    # specified pseudo_dir not found
    _pseudo_dir = os.path.expanduser("~/missing_dir/default")
    with pytest.raises(PwxInputGeneratorError):
        PwxInputGenerator._get_pseudo_name("Fe34", _pseudo_dir)
    # pseudo not found for species
    pseudo_name = PwxInputGenerator._get_pseudo_name("Cu", pseudo_dir)
    assert pseudo_name is None
    # normal function
    pseudo_name = PwxInputGenerator._get_pseudo_name("Fe-34", pseudo_dir)
    assert pseudo_name == "fe_pbe_v1.5.uspp.F.UPF"


def test_get_pseudo_names():
    # do not setup potentials: no errors
    pwig = PwxInputGenerator(crystal_structure=al_fcc_struct)
    pseudo_names = pwig._get_pseudo_names()
    assert pseudo_names == {"Al": None}
    # all `pseudo_names` provided in input: return them
    pwig = PwxInputGenerator(crystal_structure=al_fcc_struct)
    pwig.specify_potentials = True
    pwig.custom_sett_dict = {"pseudo_names": {"Al": al_pseudo}}
    assert pwig._get_pseudo_names() == {"Al": al_pseudo}
    # missing pseudos but non-existing `pseudo_dir`: error/no-op
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    pwig.specify_potentials = True
    # 1. no `pseudo_dir`: dir not specified error
    with pytest.raises(PwxInputGeneratorError, match="not specified"):
        pwig._get_pseudo_names()
    # 2. missing/wrong `pseudo_dir`: cannot listdir error
    pwig.custom_sett_dict = {"pseudo_dir": "wrong_dir"}
    with pytest.raises(PwxInputGeneratorError, match="list contents"):
        pwig._get_pseudo_names()
    # 3. all ok with correct `pseudo_dir`
    pwig.custom_sett_dict = {"pseudo_dir": pseudo_dir}
    pseudo_names = pwig._get_pseudo_names()
    assert pseudo_names == {
        "Fe": os.path.basename(fe_pseudo),
        "O": os.path.basename(o_pseudo),
    }
    # failed to find some pseudos: list of missing potentials error
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    pwig.specify_potentials = True
    pwig.custom_sett_dict = {"pseudo_dir": os.path.dirname(pseudo_dir)}
    with pytest.raises(PwxInputGeneratorError, match="Fe, O"):
        pwig._get_pseudo_names()


def test_bare_base_calculation_settings():
    pwig = PwxInputGenerator(crystal_structure=al_fcc_struct)
    calc_sett = pwig._get_calculation_settings()
    assert calc_sett["nat"] == 4


def test_scf_base_calculation_settings():
    pwig = PwxInputGenerator(crystal_structure=al_fcc_struct)
    pwig.calculation_presets = "scf"
    cs = pwig.calculation_settings
    assert cs["calculation"] == "scf"
    assert cs["namelists"] == ["control", "system", "electrons"]
    assert cs["kpoints"]["scheme"] == "automatic"
    assert cs["kpoints"]["shift"] == [0, 0, 0]
    assert cs["pseudo_dir"] == os.path.join("~", "pseudos", "qe", "default")


def test_relax_base_calculation_settings():
    pwig = PwxInputGenerator(crystal_structure=al_fcc_struct)
    pwig.calculation_presets = "relax"
    cs = pwig.calculation_settings
    assert cs["calculation"] == "relax"
    assert cs["namelists"] == ["control", "system", "electrons", "ions"]


def test_control_namelist_to_str():
    # control namelist without pseudo, settings: error
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    pwig.specify_potentials = True
    with pytest.raises(PwxInputGeneratorError):
        pwig._namelist_to_str("control")
    # specify_potentials = False: no error
    pwig.specify_potentials = False
    nl = pwig._namelist_to_str("control")
    assert nl == "&CONTROL\n/"
    # with no pseudo, with settings
    pwig.custom_sett_dict.update({"calculation": "scf"})
    nl = pwig._namelist_to_str("control")
    assert nl == '&CONTROL\n    calculation = "scf"\n/'
    # specify_potentials = True: throw error
    pwig.specify_potentials = True
    with pytest.raises(PwxInputGeneratorError):
        pwig._namelist_to_str("control")
    # normal functionality
    pwig.custom_sett_dict.update({"pseudo_dir": pseudo_dir})
    pwig.calculation_presets = "scf"
    control = "\n".join(feo_scf_in.splitlines()[:7])
    assert pwig._namelist_to_str("control") == control


def test_namelist_to_str():
    pwig = PwxInputGenerator(
        crystal_structure=al_fcc_struct,
        calculation_presets="scf",
        custom_sett_dict={"pseudo_dir": pseudo_dir},
    )
    control = "\n".join(al_fcc_scf_in.splitlines()[:7])
    assert pwig._namelist_to_str("control") == control
    electrons = "\n".join(al_fcc_scf_in.splitlines()[17:20])
    assert pwig._namelist_to_str("electrons") == electrons


def test_all_namelists_as_str():
    pwig = PwxInputGenerator(
        crystal_structure=al_fcc_struct,
        calculation_presets="scf",
        custom_sett_dict={"pseudo_dir": pseudo_dir},
    )
    namelists = "\n".join(al_fcc_scf_in.splitlines()[:20])
    assert pwig.all_namelists_as_str == namelists


def test_get_atomic_species_card():
    # specify_potentials = False, no pseudo_dir: no error
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    pwig.specify_potentials = False
    ref_line = "O      15.99940000  None"
    ac = pwig.atomic_species_card
    assert ac.splitlines()[-1] == ref_line
    # specify_potentials = True, no pseudo_dir: error
    pwig.specify_potentials = True
    with pytest.raises(PwxInputGeneratorError):
        pwig.atomic_species_card
    # normal functionality
    pwig.custom_sett_dict.update({"pseudo_dir": pseudo_dir})
    ref_line = "O      15.99940000  {}".format(os.path.basename(o_pseudo))
    ac = pwig.atomic_species_card
    assert ac.splitlines()[-1] == ref_line


def test_atomic_species_card():
    pwig = PwxInputGenerator(
        crystal_structure=feo_struct,
        calculation_presets="scf",
        custom_sett_dict={"pseudo_dir": pseudo_dir},
        specify_potentials=True,
    )
    card = "\n".join(feo_scf_in.splitlines()[20:23])
    assert pwig.atomic_species_card == card


def test_atomic_positions_card():
    pwig = PwxInputGenerator(
        crystal_structure=feo_struct, calculation_presets="scf"
    )
    card = "\n".join(feo_scf_in.splitlines()[23:28])
    assert pwig.atomic_positions_card == card


def test_kpoints_card():
    # unknown scheme: error
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    pwig.custom_sett_dict = {"kpoints": {"scheme": "monkhorst-pack"}}
    with pytest.raises(NotImplementedError):
        print(pwig.kpoints_card)
    # default scheme from presets
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    pwig.calculation_presets = "scf"
    assert pwig.kpoints_card == "K_POINTS {automatic}\n9 9 9 0 0 0"
    pwig = PwxInputGenerator(
        crystal_structure=al_fcc_struct,
        custom_sett_dict={"kpoints": {"scheme": "gamma"}},
    )
    assert pwig.kpoints_card == "K_POINTS {gamma}"


def test_cell_parameters_card():
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    card = "\n".join(feo_scf_in.splitlines()[30:])
    assert pwig.cell_parameters_card == card


def test_occupations_card():
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    with pytest.raises(NotImplementedError):
        print(pwig.occupations_card)


def test_constraints_card():
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    with pytest.raises(NotImplementedError):
        print(pwig.constraints_card)


def test_atomic_forces_card():
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    with pytest.raises(NotImplementedError):
        print(pwig.atomic_forces_card)


def test_all_cards_as_str():
    pwig = PwxInputGenerator(
        crystal_structure=feo_struct,
        calculation_presets="scf",
        custom_sett_dict={"pseudo_dir": pseudo_dir},
        specify_potentials=True,
    )
    all_cards = "\n".join(feo_scf_in.splitlines()[20:])
    assert pwig.all_cards_as_str == all_cards


def test_pwx_input_as_str():
    pwig = PwxInputGenerator(
        crystal_structure=feo_struct,
        calculation_presets="scf",
        custom_sett_dict={"pseudo_dir": pseudo_dir},
        specify_potentials=True,
    )
    assert pwig.pwx_input_as_str == feo_scf_in.rstrip("\n")


def test_write_pwx_input():
    # no input settings: error
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    with pytest.raises(PwxInputGeneratorError, match="input settings"):
        pwig.write_pwx_input()
    # no `write_location` input: error
    pwig.calculation_presets = "scf"
    with pytest.raises(PwxInputGeneratorError, match="Location to write"):
        pwig.write_pwx_input()
    # no input filename: error
    with pytest.raises(PwxInputGeneratorError, match="file to write"):
        pwig.write_pwx_input(write_location="/path/to/write_location")

    # all ok
    import tempfile

    _tmp_file = tempfile.NamedTemporaryFile(mode="w", delete=True)
    filename = _tmp_file.name
    write_location = os.path.dirname(filename)
    pwig.specify_potentials = True
    pwig.custom_sett_dict = {"pseudo_dir": pseudo_dir}
    pwig.write_pwx_input(write_location=write_location, filename=filename)
    with open(filename, "r") as fr:
        assert fr.read() == feo_scf_in.rstrip("\n")


def test_write_input_files():
    import tempfile

    _tmp_file = tempfile.NamedTemporaryFile(mode="w", delete=True)
    filename = _tmp_file.name
    write_location = os.path.dirname(filename)
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    pwig.calculation_presets = "scf"
    pwig.specify_potentials = True
    pwig.custom_sett_dict["pseudo_dir"] = pseudo_dir
    pwig.write_location = write_location
    pwig.pwx_input_file = filename
    pwig.write_input_files()
    with open(filename, "r") as fr:
        assert fr.read() == feo_scf_in.rstrip("\n")
