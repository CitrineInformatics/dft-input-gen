"""Unit tests for the `PwxInputGenerator` class."""

import os
import pytest

from dftinpgen.qe.input_generator import PwxInputGenerator
from dftinpgen.qe.input_generator import qe_val_formatter


@pytest.fixture
def eg_struct():
    def _eg_struct(fname):
        return os.path.join(os.path.dirname(__file__), 'files', fname)
    return _eg_struct


@pytest.fixture
def eg_pwx_in():
    pseudo_dir = os.path.expanduser('~/pseudos/qe/citrine-ht')

    def _eg_pwx_in(fname):
        fpath = os.path.join(os.path.dirname(__file__), 'files', fname)
        with open(fpath, 'r') as fr:
            return fr.read().format(pseudo_dir=pseudo_dir)
    return _eg_pwx_in


def test_scf_base_calculation_settings(eg_struct):
    pig = PwxInputGenerator(crystal_structure=eg_struct('al_fcc_conv.vasp'))
    cs = pig.calculation_settings
    assert cs['calculation'] == 'scf'
    assert cs['namelists'] == ['control', 'system', 'electrons']
    assert cs['kpoints']['scheme'] == 'automatic'
    assert cs['kpoints']['shift'] == [0, 0, 0]


def test_relax_base_calculation_settings(eg_struct):
    pig = PwxInputGenerator(crystal_structure=eg_struct('al_fcc_conv.vasp'),
                            base_recipe='relax')
    cs = pig.calculation_settings
    assert cs['calculation'] == 'relax'
    assert cs['namelists'] == ['control', 'system', 'electrons', 'ions']


def test_qe_val_formatter():
    assert qe_val_formatter(True) == '.true.'
    assert qe_val_formatter('False') == '"False"'
    assert qe_val_formatter(12345) == '12345'
    assert qe_val_formatter(1E-10) == '1e-10'


def test_namelist_to_str(eg_struct, eg_pwx_in):
    pig = PwxInputGenerator(crystal_structure=eg_struct('al_fcc_conv.vasp'))
    scf_in = eg_pwx_in('TEST_al_fcc_conv_scf.in')
    control = '\n'.join(scf_in.splitlines()[:7])
    assert pig.namelist_to_str('control') == control
    electrons = '\n'.join(scf_in.splitlines()[17:20])
    assert pig.namelist_to_str('electrons') == electrons


def test_all_namelists_as_str(eg_struct, eg_pwx_in):
    pig = PwxInputGenerator(crystal_structure=eg_struct('al_fcc_conv.vasp'),
                            custom_sett_dict={'pseudo_dir': './'})
    scf_in = eg_pwx_in('TEST_al_fcc_conv_scf.in')
    namelists = '\n'.join(scf_in.splitlines()[:20])
    assert pig.all_namelists_as_str == namelists


def test_get_psp_name():
    pseudo_dir = os.path.expanduser('~/pseudos/qe/citrine-ht')
    assert PwxInputGenerator.get_psp_name('Fe-34', pseudo_dir) == \
        'fe_pbe_v1.5.uspp.F.UPF'


def test_atomic_species_card(eg_struct, eg_pwx_in):
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'))
    scf_in = eg_pwx_in('TEST_feo_conv_scf.in')
    card = '\n'.join(scf_in.splitlines()[20:23])
    assert pig.atomic_species_card == card


def test_atomic_positions_card(eg_struct, eg_pwx_in):
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'))
    scf_in = eg_pwx_in('TEST_feo_conv_scf.in')
    card = '\n'.join(scf_in.splitlines()[23:28])
    assert pig.atomic_positions_card == card


def test_kpoints_card(eg_struct):
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'))
    assert pig.kpoints_card == 'K_POINTS {automatic}\n7 7 7 0 0 0'
    pig = PwxInputGenerator(crystal_structure=eg_struct('al_fcc_conv.vasp'))
    assert pig.kpoints_card == 'K_POINTS {automatic}\n8 8 8 0 0 0'


def test_cell_parameters_card(eg_struct, eg_pwx_in):
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'))
    scf_in = eg_pwx_in('TEST_feo_conv_scf.in')
    card = '\n'.join(scf_in.splitlines()[30:])
    assert pig.cell_parameters_card == card


def test_occupations_card(eg_struct):
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'))
    with pytest.raises(NotImplementedError):
        print(pig.occupations_card)


def test_constraints_card(eg_struct):
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'))
    with pytest.raises(NotImplementedError):
        print(pig.constraints_card)


def test_atomic_forces_card(eg_struct):
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'))
    with pytest.raises(NotImplementedError):
        print(pig.atomic_forces_card)


def test_all_cards_as_str(eg_struct, eg_pwx_in):
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'))
    scf_in = eg_pwx_in('TEST_feo_conv_scf.in')
    all_cards = '\n'.join(scf_in.splitlines()[20:])
    assert pig.all_cards_as_str == all_cards


def test_pwinput_as_str(eg_struct, eg_pwx_in):
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'))
    scf_in = eg_pwx_in('TEST_feo_conv_scf.in')
    assert pig.pwinput_as_str == scf_in.rstrip('\n')
