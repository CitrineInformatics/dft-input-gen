"""Unit tests for the `PwxInputGenerator` class."""

import os
import pytest

from dftinpgen.qe.input_generator import PwxInputGenerator
from dftinpgen.qe.input_generator import PwxInputGeneratorError
from dftinpgen.qe.input_generator import qe_val_formatter


@pytest.fixture
def pseudo_dir():
    return os.path.join(os.path.dirname(__file__), 'files')


@pytest.fixture
def eg_struct():
    def _eg_struct(fname):
        return os.path.join(os.path.dirname(__file__), 'files', fname)
    return _eg_struct


@pytest.fixture
def eg_pwx_in():
    def _eg_pwx_in(fname, pseudo_dir=None):
        files_dir = os.path.join(os.path.dirname(__file__), 'files')
        if pseudo_dir is None:
            pseudo_dir = files_dir
        _pwx_in = os.path.join(files_dir, fname)
        with open(_pwx_in, 'r') as fr:
            return fr.read().format(pseudo_dir=pseudo_dir)
    return _eg_pwx_in


def test_qe_val_formatter():
    assert qe_val_formatter(True) == '.true.'
    assert qe_val_formatter('False') == '"False"'
    assert qe_val_formatter(12345) == '12345'
    assert qe_val_formatter(1E-10) == '1e-10'


def test_set_params_from_structure(eg_struct):
    # no crystal structure specified
    pig = PwxInputGenerator()
    assert not pig.custom_sett_dict
    # normal functionality
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'))
    assert pig.custom_sett_dict == {'nat': 4, 'ntyp': 2}


def test_get_pseudo_dir(pseudo_dir):
    # no pseudo_dir/repo_dir/set specified
    pig = PwxInputGenerator()
    assert pig.get_pseudo_dir() is None
    pig = PwxInputGenerator(custom_sett_dict={'pseudo_repo_dir': './'})
    assert pig.get_pseudo_dir() is None
    pig = PwxInputGenerator(custom_sett_dict={'pseudo_set': 'default'})
    assert pig.get_pseudo_dir() is None
    # default psp directory from recipe
    pig = PwxInputGenerator(base_recipe='scf')
    assert pig.get_pseudo_dir() == os.path.expanduser('~/pseudos/qe/default')
    # user-specified pseudo repo dir and pseudo set
    pig = PwxInputGenerator(custom_sett_dict={'pseudo_repo_dir': '.',
                                              'pseudo_set': 'default'})
    assert pig.get_pseudo_dir() == os.path.join('.', 'default')
    # user-specified pseudo dir
    pig = PwxInputGenerator(custom_sett_dict={'pseudo_dir': pseudo_dir})
    assert pig.get_pseudo_dir() == pseudo_dir


def test_get_psp_name(pseudo_dir, eg_struct):
    # specified pseudo_dir not found
    _pseudo_dir = os.path.expanduser('~/missing_dir/default')
    with pytest.raises(PwxInputGeneratorError):
        PwxInputGenerator.get_psp_name('Fe34', _pseudo_dir)
    # psp not found for species error
    with pytest.raises(PwxInputGeneratorError):
        print(PwxInputGenerator.get_psp_name('Cu', pseudo_dir))
    # above cases with ignore missing; no error
    assert PwxInputGenerator.get_psp_name(
        'Fe34', _pseudo_dir, ignore_missing=True) is None
    assert PwxInputGenerator.get_psp_name(
        'Cu1', pseudo_dir, ignore_missing=True) is None
    # normal function
    assert PwxInputGenerator.get_psp_name('Fe-34', pseudo_dir) == \
        'fe_pbe_v1.5.uspp.F.UPF'


def test_set_pseudopotentials(pseudo_dir, eg_struct):
    # no crystal structure specified: no error
    pig = PwxInputGenerator()
    pig.set_pseudopotentials()
    assert 'pseudo_dir' not in pig.calculation_settings
    # ignore misssing psp: no errors
    # crystal structure specified, no pseudo dir specified
    pig = PwxInputGenerator(crystal_structure=eg_struct('al_fcc_conv.vasp'))
    pig.set_pseudopotentials(ignore_missing=True)
    assert 'pseudo_dir' not in pig.calculation_settings
    # crystal structure specified, non existing pseudo dir
    pig.custom_sett_dict.update({'pseudo_dir': 'missing_dir'})
    pig.set_pseudopotentials(ignore_missing=True)
    assert pig.custom_sett_dict['psp_names']['Al'] is None
    assert pig.custom_sett_dict['pseudo_dir'] == 'missing_dir'
    # crystal structure specified, species psp missing errors
    with pytest.raises(PwxInputGeneratorError):
        pig.set_pseudopotentials()
    pig.custom_sett_dict.update({'pseudo_dir': os.path.expanduser('~')})
    with pytest.raises(PwxInputGeneratorError):
        pig.set_pseudopotentials()
    # normal functionality
    pig.custom_sett_dict.update({'pseudo_dir': pseudo_dir})
    pig.set_pseudopotentials()
    assert pig.custom_sett_dict['pseudo_dir'] == pseudo_dir
    print(pig.custom_sett_dict)
    assert pig.custom_sett_dict['psp_names']['Al'] == \
        'al_pbe_v1.uspp.F.UPF'


def test_bare_base_calculation_settings(eg_struct):
    pig = PwxInputGenerator()
    assert not pig.calculation_settings
    pig = PwxInputGenerator(
        crystal_structure=eg_struct('al_fcc_conv.vasp'))
    assert pig.calculation_settings == {'nat': 4, 'ntyp': 1}


def test_scf_base_calculation_settings(eg_struct):
    pig = PwxInputGenerator(crystal_structure=eg_struct('al_fcc_conv.vasp'),
                            base_recipe='scf')
    cs = pig.calculation_settings
    assert cs['calculation'] == 'scf'
    assert cs['namelists'] == ['control', 'system', 'electrons']
    assert cs['kpoints']['scheme'] == 'automatic'
    assert cs['kpoints']['shift'] == [0, 0, 0]
    # test that pseudopotentials are set lazily
    assert 'pseudo_dir' not in cs
    pig.set_pseudopotentials(ignore_missing=True)
    assert pig.calculation_settings['pseudo_dir'] == \
        os.path.expanduser(os.path.join('~', 'pseudos', 'qe', 'default'))


def test_relax_base_calculation_settings(eg_struct):
    pig = PwxInputGenerator(crystal_structure=eg_struct('al_fcc_conv.vasp'),
                            base_recipe='relax')
    cs = pig.calculation_settings
    assert cs['calculation'] == 'relax'
    assert cs['namelists'] == ['control', 'system', 'electrons', 'ions']
    assert 'pseudo_dir' not in cs
    pig.set_pseudopotentials(ignore_missing=True)
    assert pig.calculation_settings['pseudo_dir'] == \
        os.path.expanduser(os.path.join('~', 'pseudos', 'qe', 'default'))


def test_control_namelist_to_str(pseudo_dir, eg_struct, eg_pwx_in):
    # control namelist without psp, settings
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'))
    # 1. ignore missing psp; no error
    nl = pig.namelist_to_str('control', ignore_missing_psp=True)
    assert nl == '&CONTROL\n/'
    # 2. do not ignore missing psp; throw error
    with pytest.raises(PwxInputGeneratorError):
        pig.namelist_to_str('control')
    # with no psp, with settings
    pig.custom_sett_dict.update({'calculation': 'scf'})
    # 1. ignore missing psp; no error
    nl = pig.namelist_to_str('control', ignore_missing_psp=True)
    assert nl == '&CONTROL\n    calculation = "scf"\n/'
    # 2. do not ignore missing psp; throw error
    with pytest.raises(PwxInputGeneratorError):
        pig.namelist_to_str('control')
    # normal functionality
    pig.custom_sett_dict.update({'pseudo_dir': pseudo_dir})
    pig.base_recipe = 'scf'
    scf_in = eg_pwx_in('TEST_feo_conv_scf.in')
    control = '\n'.join(scf_in.splitlines()[:7])
    assert pig.namelist_to_str('control') == control


def test_namelist_to_str(pseudo_dir, eg_struct, eg_pwx_in):
    pig = PwxInputGenerator(crystal_structure=eg_struct('al_fcc_conv.vasp'),
                            base_recipe='scf',
                            custom_sett_dict={'pseudo_dir': pseudo_dir})
    scf_in = eg_pwx_in('TEST_al_fcc_conv_scf.in')
    control = '\n'.join(scf_in.splitlines()[:7])
    assert pig.namelist_to_str('control') == control
    electrons = '\n'.join(scf_in.splitlines()[17:20])
    assert pig.namelist_to_str('electrons') == electrons


def test_all_namelists_as_str(pseudo_dir, eg_struct, eg_pwx_in):
    pig = PwxInputGenerator(crystal_structure=eg_struct('al_fcc_conv.vasp'),
                            base_recipe='scf',
                            custom_sett_dict={'pseudo_dir': pseudo_dir})
    scf_in = eg_pwx_in('TEST_al_fcc_conv_scf.in', pseudo_dir=pseudo_dir)
    namelists = '\n'.join(scf_in.splitlines()[:20])
    assert pig.all_namelists_as_str == namelists


def test_get_atomic_species_card(eg_struct):
    # without pseudo dir, with ignore missing
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'))
    ref_line = 'O      15.99940000  None'
    ac = pig.get_atomic_species_card(ignore_missing_psp=True)
    assert ac.splitlines()[-1] == ref_line
    # without pseudo dir, without ignore missing; error
    with pytest.raises(PwxInputGeneratorError):
        pig.get_atomic_species_card()


def test_atomic_species_card(pseudo_dir, eg_struct, eg_pwx_in):
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'),
                            base_recipe='scf',
                            custom_sett_dict={'pseudo_dir': pseudo_dir})
    scf_in = eg_pwx_in('TEST_feo_conv_scf.in')
    card = '\n'.join(scf_in.splitlines()[20:23])
    assert pig.atomic_species_card == card


def test_atomic_positions_card(eg_struct, eg_pwx_in):
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'),
                            base_recipe='scf')
    scf_in = eg_pwx_in('TEST_feo_conv_scf.in')
    card = '\n'.join(scf_in.splitlines()[23:28])
    assert pig.atomic_positions_card == card


def test_kpoints_card(eg_struct):
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'),
                            base_recipe='scf')
    assert pig.kpoints_card == 'K_POINTS {automatic}\n7 7 7 0 0 0'
    pig = PwxInputGenerator(crystal_structure=eg_struct('al_fcc_conv.vasp'),
                            base_recipe='scf')
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


def test_all_cards_as_str(pseudo_dir, eg_struct, eg_pwx_in):
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'),
                            base_recipe='scf',
                            custom_sett_dict={'pseudo_dir': pseudo_dir})
    scf_in = eg_pwx_in('TEST_feo_conv_scf.in')
    all_cards = '\n'.join(scf_in.splitlines()[20:])
    assert pig.all_cards_as_str == all_cards


def test_pwinput_as_str(pseudo_dir, eg_struct, eg_pwx_in):
    pig = PwxInputGenerator(crystal_structure=eg_struct('feo_conv.vasp'),
                            base_recipe='scf',
                            custom_sett_dict={'pseudo_dir': pseudo_dir})
    scf_in = eg_pwx_in('TEST_feo_conv_scf.in')
    assert pig.pwinput_as_str == scf_in.rstrip('\n')
