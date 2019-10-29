import os
import unittest

from dftinpgen.qe.input_generator import PwxInputGenerator
from dftinpgen.qe.input_generator import qe_val_formatter


class TestPwxInputGenerator(unittest.TestCase):
    """Unit tests for the `PwxInputGenerator` class."""

    def setUp(self):
        self.al_fcc_conv = os.path.join(
            os.path.dirname(__file__), 'files', 'al_fcc_conv.vasp')
        self.test_al_fcc_conv_scf_in = os.path.join(
            os.path.dirname(__file__), 'files', 'TEST_al_fcc_conv_scf.in')
        self.feo_conv = os.path.join(
            os.path.dirname(__file__), 'files', 'feo_conv.vasp')
        self.test_feo_conv_scf_in = os.path.join(
            os.path.dirname(__file__), 'files', 'TEST_feo_conv_scf.in')

    def test_scf_base_calculation_settings(self):
        pig = PwxInputGenerator(crystal_structure=self.al_fcc_conv)
        cs = pig.calculation_settings
        self.assertEqual(cs['calculation'], 'scf')
        self.assertListEqual(cs['namelists'],
                             ['control', 'system', 'electrons'])
        self.assertEqual(cs['kpoints']['scheme'], 'automatic')
        self.assertListEqual(cs['kpoints']['shift'], [0, 0, 0])

    def test_relax_base_calculation_settings(self):
        pig = PwxInputGenerator(crystal_structure=self.al_fcc_conv,
                                base_recipe='relax')
        cs = pig.calculation_settings
        self.assertEqual(cs['calculation'], 'relax')
        self.assertListEqual(cs['namelists'],
                             ['control', 'system', 'electrons', 'ions'])

    def test_qe_val_formatter(self):
        self.assertEqual(qe_val_formatter(True), '.true.')
        self.assertEqual(qe_val_formatter('False'), '"False"')
        self.assertEqual(qe_val_formatter(12345), '12345')
        self.assertEqual(qe_val_formatter(1E-10), '1e-10')

    def test_namelist_to_str(self):
        pig = PwxInputGenerator(crystal_structure=self.al_fcc_conv)
        with open(self.test_al_fcc_conv_scf_in, 'r') as fr:
            scf_in = fr.readlines()
        control = ''.join(scf_in[:7]).rstrip('\n')
        self.assertEqual(pig.namelist_to_str('control'), control)
        electrons = ''.join(scf_in[17:20]).rstrip('\n')
        self.assertEqual(pig.namelist_to_str('electrons'), electrons)

    def test_all_namelists_as_str(self):
        pig = PwxInputGenerator(crystal_structure=self.al_fcc_conv,
                                custom_sett_dict={'pseudo_dir': './'})
        pseudo_dir = os.path.expanduser('~/pseudo/qe/citrine-ht')
        with open(self.test_al_fcc_conv_scf_in, 'r') as fr:
            scf_in = fr.readlines()
        namelists = ''.join(scf_in[:20]).rstrip('\n')
        print(namelists)
        self.assertEqual(pig.all_namelists_as_str, namelists)

    def test_get_psp_name(self):
        # TODO: test non-default pseudopotential choices
        pig = PwxInputGenerator(crystal_structure=self.al_fcc_conv)
        self.assertEqual(pig.get_psp_name('Fe-34'),
                         'fe_pbe_v1.5.uspp.F.UPF')

    def test_atomic_species_card(self):
        pig = PwxInputGenerator(crystal_structure=self.feo_conv)
        with open(self.test_feo_conv_scf_in, 'r') as fr:
            scf_in = fr.readlines()
        card = ''.join(scf_in[20:23]).rstrip('\n')
        self.assertEqual(pig.atomic_species_card, card)

    def test_atomic_positions_card(self):
        pig = PwxInputGenerator(crystal_structure=self.feo_conv)
        with open(self.test_feo_conv_scf_in, 'r') as fr:
            scf_in = fr.readlines()
        card = ''.join(scf_in[23:28]).rstrip('\n')
        self.assertEqual(pig.atomic_positions_card, card)

    def test_kpoints_card(self):
        pig = PwxInputGenerator(crystal_structure=self.feo_conv)
        self.assertEqual(pig.kpoints_card,
                         'K_POINTS {automatic}\n7 7 7 0 0 0')
        pig = PwxInputGenerator(crystal_structure=self.al_fcc_conv)
        self.assertEqual(pig.kpoints_card,
                         'K_POINTS {automatic}\n8 8 8 0 0 0')

    def test_cell_parameters_card(self):
        pig = PwxInputGenerator(crystal_structure=self.feo_conv)
        with open(self.test_feo_conv_scf_in, 'r') as fr:
            scf_in = fr.readlines()
        card = ''.join(scf_in[30:]).rstrip('\n')
        self.assertEqual(pig.cell_parameters_card, card)

    def test_occupations_card(self):
        pig = PwxInputGenerator(crystal_structure=self.feo_conv)
        with self.assertRaises(NotImplementedError):
            print(pig.occupations_card)

    def test_constraints_card(self):
        pig = PwxInputGenerator(crystal_structure=self.feo_conv)
        with self.assertRaises(NotImplementedError):
            print(pig.constraints_card)

    def test_atomic_forces_card(self):
        pig = PwxInputGenerator(crystal_structure=self.feo_conv)
        with self.assertRaises(NotImplementedError):
            print(pig.atomic_forces_card)

    def test_all_cards_as_str(self):
        pig = PwxInputGenerator(crystal_structure=self.feo_conv)
        with open(self.test_feo_conv_scf_in, 'r') as fr:
            scf_in = fr.readlines()
        all_cards = ''.join(scf_in[20:]).rstrip('\n')
        self.assertEqual(pig.all_cards_as_str, all_cards)

    def test_pwinput_as_str(self):
        pig = PwxInputGenerator(crystal_structure=self.feo_conv)
        with open(self.test_feo_conv_scf_in, 'r') as fr:
            self.assertEqual(pig.pwinput_as_str, fr.read().rstrip('\n'))


if __name__ == '__main__':
    unittest.main()
