import os
import glob
import json
import six

from dftinpgen.data import STANDARD_ATOMIC_WEIGHTS
from dftinpgen.base import DftInputGenerator
from dftinpgen.utils import get_elem_symbol
from dftinpgen.qe.settings import QE_TAGS
from dftinpgen.qe.settings.base_recipes import QE_BASE_RECIPES


def qe_val_formatter(val):
    """Format values for QE tags into strings."""
    if isinstance(val, bool):
        return '.{}.'.format(str(val).lower())
    elif isinstance(val, six.string_types):
        return '"{}"'.format(val)
    else:
        return str(val)


class PwxInputGeneratorError(Exception):
    pass


class PwxInputGenerator(DftInputGenerator):
    """Base class to generate input files for pw.x."""

    def __init__(self, crystal_structure=None, base_recipe=None,
                 custom_sett_file=None, custom_sett_dict=None,
                 write_location=None, overwrite_files=None, **kwargs):
        """
        Constructor.

        Parameters:
        -----------

        crystal_structure: str or :class:`ase.Atoms` object
            Path to the file with the input crystal structure or an
            :class:`ase.Atoms` object from `ase.io.read()`.

        base_recipe: str, optional
            The "base" calculation settings to use--must be one of the
            pre-defined recipes provided for QE.

            Pre-defined recipes are in
            [INSTALL_PATH]/qe/settings/base_recipes/

        custom_sett_file: str, optional
            Location of a JSON file with custom calculation settings as a
            dictionary of tags and values.

            NB: Custom settings specified here always OVERRIDE those in
            `base_recipe` in case of overlap.

        custom_sett_dict: dict, optional
            Dictionary with custom calculation settings as tags and values/

            NB: Custom settings specified here always OVERRIDE those in
            `base_recipe` and `custom_sett_file`.

        write_location: str, optional
            Path to the directory in which to write the input files.

        overwrite_files: bool, optional
            To overwrite files or not, that is the question.

        **kwargs:
            Arbitrary keyword arguments, e.g. to pass on to the crystal
            structure reader module implemented in `ase`.

        """
        super(PwxInputGenerator, self).__init__(
            crystal_structure=crystal_structure,
            dft_package='qe',
            base_recipe=base_recipe,
            custom_sett_file=custom_sett_file,
            custom_sett_dict=custom_sett_dict,
            write_location=write_location,
            overwrite_files=overwrite_files,
            **kwargs)
        self.set_params_from_structure()
        self.set_pseudopotentials()

    def set_params_from_structure(self):
        """Helper function to update some settings, e.g. number of atoms and the
        number of types of species, based on the input crystal structure."""
        if self.crystal_structure is None:
            return
        if self.custom_sett_dict is None:
            self.custom_sett_dict = {}
        self.custom_sett_dict.update({
            'nat': len(self.crystal_structure),
            'ntyp': len(set(self.crystal_structure.get_chemical_symbols()))
        })

    def set_pseudopotentials(self):
        """Helper function to set the pseudopotential for each species."""
        if self.crystal_structure is None:
            return
        if self.custom_sett_dict is None:
            self.custom_sett_dict = {}
        psp_dir = os.path.join(
            os.path.expanduser(self.calculation_settings['pseudo_repo_dir']),
            self.calculation_settings['pseudo_set'])
        if not os.path.isdir(psp_dir):
            msg = 'Pseudopotentials directory "{}" not found'.format(psp_dir)
            raise PwxInputGeneratorError(msg)
        self.custom_sett_dict['pseudo_dir'] = psp_dir
        species = sorted(set(self.crystal_structure.get_chemical_symbols()))
        if 'psp_names' not in self.custom_sett_dict:
            self.custom_sett_dict['psp_names'] = {}
        for sp in species:
            self.custom_sett_dict['psp_names'].update({
                sp: self.get_psp_name(sp, psp_dir)
            })

    @staticmethod
    def get_psp_name(species, psp_dir):
        elem_low = get_elem_symbol(species).lower()
        psp = glob.glob(os.path.join(psp_dir, '*'))
        psp = [os.path.basename(p) for p in psp]
        psp = [p for p in psp if
               p.partition('.')[0].partition('_')[0].lower() == elem_low]
        if psp:
            return psp[0]
        msg = 'Pseudopotential not found for {}'.format(species)
        raise PwxInputGeneratorError(msg)

    @property
    def calculation_settings(self):
        calc_sett = QE_BASE_RECIPES[self.base_recipe]
        if self.custom_sett_file is not None:
            with open(self.custom_sett_file, 'r') as fr:
                calc_sett.update(json.load(fr))
        if self.custom_sett_dict is not None:
            calc_sett.update(self.custom_sett_dict)
        return calc_sett

    def namelist_to_str(self, namelist):
        calc_sett = self.calculation_settings
        lines = ['&{}'.format(namelist.upper())]
        for tag in QE_TAGS['pw.x']['namelist_tags'][namelist]:
            if tag in calc_sett:
                lines.append('    {} = {}'.format(
                    tag, qe_val_formatter(calc_sett[tag])))
        lines.append('/')
        return '\n'.join(lines)

    @property
    def all_namelists_as_str(self):
        blocks = []
        for namelist in QE_TAGS['pw.x']['namelists']:
            if namelist in self.calculation_settings.get('namelists', []):
                blocks.append(self.namelist_to_str(namelist))
        return '\n'.join(blocks)

    @property
    def atomic_species_card(self):
        if self.crystal_structure is None:
            return
        species = sorted(set(self.crystal_structure.get_chemical_symbols()))
        lines = ['ATOMIC_SPECIES']
        for sp in species:
            lines.append('{:4s}  {:12.8f}  {}'.format(
                sp,
                STANDARD_ATOMIC_WEIGHTS[sp]['standard_atomic_weight'],
                self.custom_sett_dict['psp_names'][sp]
            ))
        return '\n'.join(lines)

    @property
    def atomic_positions_card(self):
        if self.crystal_structure is None:
            return
        symbols = self.crystal_structure.get_chemical_symbols()
        positions = self.crystal_structure.get_scaled_positions()
        lines = ['ATOMIC_POSITIONS {crystal}']
        for s, p in zip(symbols, positions):
            lines.append('{:4s}  {:12.8f}  {:12.8f}  {:12.8f}'.format(s, *p))
        return '\n'.join(lines)

    @property
    def kpoints_card(self):
        if self.crystal_structure is None:
            return
        kpoints_sett = self.calculation_settings.get('kpoints', {})
        scheme = kpoints_sett.get('scheme')
        if scheme not in ['gamma', 'automatic']:
            raise NotImplementedError
        if scheme == 'gamma':
            return 'K_POINTS {gamma}'
        elif scheme == 'automatic':
            lines = ['K_POINTS {automatic}']
            grid = kpoints_sett.get('grid', [])
            shift = kpoints_sett['shift']
            if not grid:
                grid = self.get_kpoint_grid_from_spacing(
                    kpoints_sett['spacing'])
            lines.append('{} {} {} {} {} {}'.format(*grid, *shift))
        return '\n'.join(lines)

    @property
    def cell_parameters_card(self):
        if self.crystal_structure is None:
            return
        lines = ['CELL_PARAMETERS {angstrom}']
        for cv in self.crystal_structure.cell:
            lines.append('{:12.8f}  {:12.8f}  {:12.8f}'.format(*cv))
        return '\n'.join(lines)

    @property
    def occupations_card(self):
        raise NotImplementedError

    @property
    def constraints_card(self):
        raise NotImplementedError

    @property
    def atomic_forces_card(self):
        raise NotImplementedError

    @property
    def all_cards_as_str(self):
        blocks = []
        for card in QE_TAGS['pw.x']['cards']:
            if card in self.calculation_settings.get('cards', []):
                blocks.append(getattr(self, '{}_card'.format(card)))
        return '\n'.join(blocks)

    @property
    def pwinput_as_str(self):
        return '\n'.join([self.all_namelists_as_str, self.all_cards_as_str])

    def write_pwxinput(self, write_location=None, filename=None):
        if write_location is None:
            write_location = self.write_location
        if filename is None:
            filename = '{}.in'.format(self.base_recipe)
        with open(os.path.join(write_location, filename), 'w') as fw:
            fw.write(self.pwinput_as_str)
