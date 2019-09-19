import os
import json

from dftinpgen.base import DftInputGenerator
from dftinpgen.qe.settings.base_recipes import QE_BASE_RECIPES


class PwxInputGenerator(DftInputGenerator):
    """Base class to generate input files for pw.x."""

    def __init__(self, crystal_structure=None, base_recipe=None,
                 custom_sett_file=None, write_location=None,
                 overwrite_files=None, **kwargs):
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

            Defaults to the "scf" recipe.

        custom_sett_file: str, optional
            Location of a JSON file with custom calculation settings as a
            dictionary of tags and values.

            NB: Custom settings specified here always OVERWRITE those in
            `base_recipe` in case of overlap.

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
            write_location=write_location,
            overwrite_files=overwrite_files,
            **kwargs)

    @property
    def calculation_settings(self):
        calc_sett = QE_BASE_RECIPES[self.base_recipe]
        with open(self.custom_sett_file, 'r') as fr:
            calc_sett.update(json.load(fr))
        return calc_sett
