import os
import six
import itertools

from dftinpgen.data import STANDARD_ATOMIC_WEIGHTS
from dftinpgen.utils import get_elem_symbol
from dftinpgen.utils import get_kpoint_grid_from_spacing
from dftinpgen.qe.settings import QE_TAGS
from dftinpgen.qe.settings.calculation_presets import QE_PRESETS

from dftinpgen.base import DftInputGenerator
from dftinpgen.base import DftInputGeneratorError


def _qe_val_formatter(val):
    """Format values for QE tags into strings."""
    if isinstance(val, bool):
        return ".{}.".format(str(val).lower())
    elif isinstance(val, six.string_types):
        return '"{}"'.format(val)
    else:
        return str(val)


class PwxInputGeneratorError(DftInputGeneratorError):
    """Base class for handling errors related to input files generation for pw.x."""

    pass


class PwxInputGenerator(DftInputGenerator):
    """Base class to generate input files for pw.x."""

    def __init__(
        self,
        crystal_structure=None,
        calculation_presets=None,
        custom_sett_file=None,
        custom_sett_dict=None,
        specify_potentials=None,
        write_location=None,
        pwx_input_file=None,
        overwrite_files=None,
        **kwargs
    ):
        """
        Constructor.

        Parameters
        ----------

        crystal_structure: :class:`ase.Atoms` object
            :class:`ase.Atoms` object from `ase.io.read([crystal structure
            file])`.

        calculation_presets: str, optional
            The "base" calculation settings to use--must be one of the
            pre-defined groups of tags and values provided for pw.x.

            Pre-defined settings for some common calculation types are in
            [INSTALL_PATH]/qe/settings/calculation_presets/

        custom_sett_file: str, optional
            Location of a JSON file with custom calculation settings as a
            dictionary of tags and values.

            NB: Custom settings specified here always OVERRIDE those in
            `calculation_presets` in case of overlap.

        custom_sett_dict: dict, optional
            Dictionary with custom calculation settings as tags and values/

            NB: Custom settings specified here always OVERRIDE those in
            `calculation_presets` and `custom_sett_file`.

        specify_potentials: bool, optional
            Whether to set pseudopotentials to use for each chemical species
            in the input crystal structure.

            If set to True, it is attempted to match every chemical species
            to a pseudopotential.
            1. If `pseudo_names` dictionary (with chemical species and
               names of pseudopotential files) is specified in any of the
               previous settings arguments, they are used.
            2. For any species not in the input `pseudo_names` dictionary (or
               if `pseudo_names` is not input at all), the *first matching*
               pseudopotential file (species name in the name of the
               pseudopotential file) in the specified `pseudo_dir` is used.
               If a pseudopotential file cannot be found for a chemical
               species, an error is thrown.
               NB: If `pseudo_dir` is not provided as input, an error is
               thrown.

            NB: this above described matching is performed lazily, i.e.,
            only when a card or namelist that requires pseudopotential
            information is generated.

            If set to False, no pseudopotential is set for any chemical
            species. The generated input files have "None" in place of
            pseudopotential names for every species listed in the
            "ATOMIC_SPECIES" card.

            Default: False

        write_location: str, optional
            Path to the directory in which to write the input file(s).

            Default: Current working directory.

        pwx_input_file: str, optional
            Name of the file in which to write the formatted pw.x input
            content.

            Default: "[`calculation_presets`].in" if `calculation_presets` is specified by
            the user, else "pwx.in".

        overwrite_files: bool, optional
            To overwrite files or not, that is the question.

            Default: True

        **kwargs:
            Arbitrary keyword arguments.

        """
        # TODO(@hegdevinayi): Add default Hubbard schemes (Wang/Aykol/Bennett)
        # TODO(@hegdevinayi): Add default magnetism schemes (ferro/AFM G-type)
        # TODO(@hegdevinayi): Consider allowing psp location via config file

        super(PwxInputGenerator, self).__init__(
            crystal_structure=crystal_structure,
            calculation_presets=calculation_presets,
            custom_sett_file=custom_sett_file,
            custom_sett_dict=custom_sett_dict,
            write_location=write_location,
            overwrite_files=overwrite_files,
        )

        self._parameters_from_structure = self._get_parameters_from_structure()
        self._calculation_settings = self._get_calculation_settings()

        self._specify_potentials = False
        self.specify_potentials = specify_potentials

        self._pwx_input_file = self._get_default_pwx_input_file()
        self.pwx_input_file = pwx_input_file

    def _set_crystal_structure(self, crystal_structure):
        super(PwxInputGenerator, self)._set_crystal_structure(
            crystal_structure
        )
        self._parameters_from_structure = self._get_parameters_from_structure()

    @property
    def parameters_from_structure(self):
        return self._parameters_from_structure

    @property
    def specify_potentials(self):
        return self._specify_potentials

    @specify_potentials.setter
    def specify_potentials(self, specify_potentials):
        if specify_potentials is not None:
            self._specify_potentials = specify_potentials

    @property
    def pwx_input_file(self):
        return self._pwx_input_file

    @pwx_input_file.setter
    def pwx_input_file(self, pwx_input_file):
        if pwx_input_file is not None:
            self._pwx_input_file = pwx_input_file

    def _get_default_pwx_input_file(self):
        if self.calculation_presets is None:
            return "pwx.in"
        return "{}.in".format(self.calculation_presets)

    @property
    def dft_package(self):
        return "qe"

    def _get_parameters_from_structure(self):
        """Get settings determined by input crystal structure, e.g. number of
        atoms and the number of types of species."""
        return {
            "nat": len(self.crystal_structure),
            "ntyp": len(set(self.crystal_structure.get_chemical_symbols())),
        }

    @staticmethod
    def _get_pseudo_name(species, pseudo_dir):
        """Helper function to match species to its pseudopotential in a
        specified directory."""

        def _elem_from_fname(fname):
            bname = os.path.basename(fname)
            elem = bname.partition(".")[0].partition("_")[0].lower()
            return elem

        elem_low = get_elem_symbol(species).lower()
        # match pseudo iff a *.UPF filename matches element symbol in structure
        # Note: generic except here for py2/py3 compatibility
        try:
            pseudo_dir_files = os.listdir(os.path.expanduser(pseudo_dir))
        except:  # noqa: E722
            msg = 'Failed to list contents in "{}"'.format(pseudo_dir)
            raise PwxInputGeneratorError(msg)
        for p in pseudo_dir_files:
            ext = os.path.splitext(p)[-1].lower()
            if _elem_from_fname(p) == elem_low and ext == ".upf":
                return os.path.basename(p)

    def _get_pseudo_names(self):
        """Get names of pseudopotentials to use for each chemical species."""
        species = sorted(set(self.crystal_structure.get_chemical_symbols()))
        pseudo_names = {sp: None for sp in species}
        if not self.specify_potentials:
            return pseudo_names
        # 1. check if pseudo names are provided in input calculation settings
        input_pseudo_names = self.calculation_settings.get("pseudo_names", {})
        pseudo_names.update(input_pseudo_names)
        # 2. if pseudos for all species were input, nothing more to be done.
        if None not in set(pseudo_names.values()):
            return pseudo_names
        # 3. for species that are missing pseudos, try matching psp files in
        # the `pseudo_dir` directory (raise error if directory not specified)
        pseudo_dir = self.calculation_settings.get("pseudo_dir")
        if not pseudo_dir:
            msg = "Pseudopotential directory not specified"
            raise PwxInputGeneratorError(msg)
        matched_pseudo_names = {
            sp: self._get_pseudo_name(sp, pseudo_dir) for sp in species
        }
        # 4. overwrite with any user-specified pseudos
        for sp in pseudo_names:
            if pseudo_names[sp] is None:
                pseudo_names[sp] = matched_pseudo_names.get(sp)
        # 5. finally, if any species is missing pseudo, raise error
        missing_pseudos = [k for k, v in pseudo_names.items() if v is None]
        if missing_pseudos:
            msg = "Failed to find potential for [{}]".format(
                ", ".join(missing_pseudos)
            )
            raise PwxInputGeneratorError(msg)
        return pseudo_names

    @property
    def calculation_settings(self):
        return self._get_calculation_settings()

    def _get_calculation_settings(self):
        """Load all calculation settings: user-input and auto-determined."""
        calc_sett = {}
        if self.calculation_presets is not None:
            calc_sett.update(QE_PRESETS[self.calculation_presets])
        if self.custom_sett_from_file is not None:
            calc_sett.update(self.custom_sett_from_file)
        if self.custom_sett_dict is not None:
            calc_sett.update(self.custom_sett_dict)
        calc_sett.update(self.parameters_from_structure)
        return calc_sett

    def _namelist_to_str(self, namelist):
        """Convert all tags, values corresponding to a pw.x namelist into a
        formatted string."""
        if namelist.lower() == "control":
            if not self.calculation_settings.get("pseudo_dir"):
                if self.specify_potentials:
                    msg = "Pseudopotentials directory not specified"
                    raise PwxInputGeneratorError(msg)
        lines = ["&{}".format(namelist.upper())]
        for tag in QE_TAGS["pw.x"]["namelist_tags"][namelist]:
            if tag not in self.calculation_settings:
                continue
            lines.append(
                "    {} = {}".format(
                    tag, _qe_val_formatter(self.calculation_settings.get(tag)),
                )
            )
        lines.append("/")
        return "\n".join(lines)

    @property
    def all_namelists_as_str(self):
        blocks = []
        for namelist in QE_TAGS["pw.x"]["namelists"]:
            if namelist in self.calculation_settings.get("namelists", []):
                blocks.append(self._namelist_to_str(namelist))
        return "\n".join(blocks)

    @property
    def atomic_species_card(self):
        species = sorted(set(self.crystal_structure.get_chemical_symbols()))
        pseudo_names = self._get_pseudo_names()
        lines = ["ATOMIC_SPECIES"]
        for sp in species:
            lines.append(
                "{:4s}  {:12.8f}  {}".format(
                    sp,
                    STANDARD_ATOMIC_WEIGHTS[sp]["standard_atomic_weight"],
                    pseudo_names[sp],
                )
            )
        return "\n".join(lines)

    @property
    def atomic_positions_card(self):
        symbols = self.crystal_structure.get_chemical_symbols()
        positions = self.crystal_structure.get_scaled_positions()
        lines = ["ATOMIC_POSITIONS {crystal}"]
        for s, p in zip(symbols, positions):
            lines.append("{:4s}  {:12.8f}  {:12.8f}  {:12.8f}".format(s, *p))
        return "\n".join(lines)

    @property
    def kpoints_card(self):
        kpoints_sett = self.calculation_settings.get("kpoints", {})
        scheme = kpoints_sett.get("scheme")
        if scheme not in ["gamma", "automatic"]:
            raise NotImplementedError
        if scheme == "gamma":
            return "K_POINTS {gamma}"
        elif scheme == "automatic":
            lines = ["K_POINTS {automatic}"]
            grid = kpoints_sett.get("grid", [])
            shift = kpoints_sett["shift"]
            if not grid:
                grid = get_kpoint_grid_from_spacing(
                    self.crystal_structure, kpoints_sett["spacing"],
                )
            _l = "{} {} {} {} {} {}".format(*itertools.chain(grid, shift))
            lines.append(_l)
        return "\n".join(lines)

    @property
    def cell_parameters_card(self):
        lines = ["CELL_PARAMETERS {angstrom}"]
        for cv in self.crystal_structure.cell:
            lines.append("{:12.8f}  {:12.8f}  {:12.8f}".format(*cv))
        return "\n".join(lines)

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
        for card in QE_TAGS["pw.x"]["cards"]:
            if card in self.calculation_settings.get("cards", []):
                blocks.append(getattr(self, "{}_card".format(card)))
        return "\n".join(blocks)

    @property
    def pwx_input_as_str(self):
        return "\n".join([self.all_namelists_as_str, self.all_cards_as_str])

    def write_pwx_input(self, write_location=None, filename=None):
        """Write the pw.x input file to disk at the specified location."""
        if self.pwx_input_as_str.strip() == "":
            msg = "Nothing to write. No input settings found?"
            raise PwxInputGeneratorError(msg)
        if write_location is None:
            msg = "Location to write files not specified"
            raise PwxInputGeneratorError(msg)
        if filename is None:
            msg = "Name of the input file to write into not specified"
            raise PwxInputGeneratorError(msg)
        with open(os.path.join(write_location, filename), "w") as fw:
            fw.write(self.pwx_input_as_str)

    def write_input_files(self):
        self.write_pwx_input(
            write_location=self.write_location, filename=self.pwx_input_file,
        )
