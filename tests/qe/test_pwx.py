"""Unit tests for the `PwxInputGenerator` class."""

import os
import pytest
from ase import io as ase_io

from dftinpgen.qe.pwx import PwxInputGenerator
from dftinpgen.qe.pwx import PwxInputGeneratorError
from dftinpgen.qe.pwx import _qe_val_formatter


# define module-level variables used for testing
# TODO hegdevinayi@gmail.com: refactor to fixtures (`pytest-data`)
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
    # crystal structure specified, non existing pseudo dir: no error
    pwig.custom_sett_dict.update({"pseudo_dir": "missing_dir"})
    pseudo_names = pwig._get_pseudo_names()
    assert pseudo_names == {"Al": None}
    # crystal structure specified, non existing pseudo dir: error
    pwig.specify_potentials = True
    with pytest.raises(PwxInputGeneratorError):
        pwig._get_pseudo_names()
    # normal functionality
    pwig.custom_sett_dict.update({"pseudo_dir": pseudo_dir})
    pwig.calculation_settings = pwig._get_calculation_settings()
    pseudo_names = pwig._get_pseudo_names()
    assert pseudo_names == {"Al": os.path.basename(al_pseudo)}


def test_bare_base_calculation_settings():
    pwig = PwxInputGenerator(crystal_structure=al_fcc_struct)
    calc_sett = pwig._get_calculation_settings()
    assert calc_sett["nat"] == 4


def test_scf_base_calculation_settings():
    pwig = PwxInputGenerator(crystal_structure=al_fcc_struct)
    pwig.calculation_presets = "scf"
    pwig.calculation_settings = pwig._get_calculation_settings()
    cs = pwig.calculation_settings
    assert cs["calculation"] == "scf"
    assert cs["namelists"] == ["control", "system", "electrons"]
    assert cs["kpoints"]["scheme"] == "automatic"
    assert cs["kpoints"]["shift"] == [0, 0, 0]
    assert cs["pseudo_dir"] == os.path.join("~", "pseudos", "qe", "default")


def test_relax_base_calculation_settings():
    pwig = PwxInputGenerator(crystal_structure=al_fcc_struct)
    pwig.calculation_presets = "relax"
    pwig.calculation_settings = pwig._get_calculation_settings()
    cs = pwig.calculation_settings
    assert cs["calculation"] == "relax"
    assert cs["namelists"] == ["control", "system", "electrons", "ions"]


def test_control_namelist_to_str():
    # control namelist without pseudo, settings: error
    pwig = PwxInputGenerator(crystal_structure=feo_struct)
    pwig.specify_potentials = True
    with pytest.raises(PwxInputGeneratorError):
        pwig.namelist_to_str("control")
    # specify_potentials = False: no error
    pwig.specify_potentials = False
    nl = pwig.namelist_to_str("control")
    assert nl == "&CONTROL\n/"
    # with no pseudo, with settings
    pwig.custom_sett_dict.update({"calculation": "scf"})
    pwig.calculation_settings = pwig._get_calculation_settings()
    nl = pwig.namelist_to_str("control")
    assert nl == '&CONTROL\n    calculation = "scf"\n/'
    # specify_potentials = True: throw error
    pwig.specify_potentials = True
    with pytest.raises(PwxInputGeneratorError):
        pwig.namelist_to_str("control")
    # normal functionality
    pwig.custom_sett_dict.update({"pseudo_dir": pseudo_dir})
    pwig.calculation_presets = "scf"
    pwig.calculation_settings = pwig._get_calculation_settings()
    control = "\n".join(feo_scf_in.splitlines()[:7])
    assert pwig.namelist_to_str("control") == control


def test_namelist_to_str():
    pwig = PwxInputGenerator(
        crystal_structure=al_fcc_struct,
        calculation_presets="scf",
        custom_sett_dict={"pseudo_dir": pseudo_dir},
    )
    control = "\n".join(al_fcc_scf_in.splitlines()[:7])
    assert pwig.namelist_to_str("control") == control
    electrons = "\n".join(al_fcc_scf_in.splitlines()[17:20])
    assert pwig.namelist_to_str("electrons") == electrons


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
    pwig.calculation_settings = pwig._get_calculation_settings()
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
    pwig = PwxInputGenerator(
        crystal_structure=feo_struct, calculation_presets="scf"
    )
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
