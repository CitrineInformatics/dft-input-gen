import os
import six
import json
import abc
from abc import abstractproperty
from abc import abstractmethod

import ase


class DftInputGeneratorError(Exception):
    """Base class for errors associated with DFT input files generation."""

    pass


@six.add_metaclass(abc.ABCMeta)
class DftInputGenerator(object):
    """Base abstract class for DFT input generators."""

    def __init__(
        self,
        crystal_structure=None,
        calculation_presets=None,
        custom_sett_file=None,
        custom_sett_dict=None,
        write_location=None,
        overwrite_files=None,
        **kwargs
    ):
        """
        Constructor.

        Parameters
        ----------
        crystal_structure: :class:`ase.Atoms` object
            :class:`ase.Atoms` object resulting from `ase.io.read([crystal
            structure file])`.

        calculation_presets: str, optional
            The "base" calculation settings to use--must be one of the
            pre-defined groups of tags and values provided for
            `self.dft_package`.

            Pre-defined settings for some common calculation types are in
            INSTALL_PATH/[dft_package]/settings/calculation_presets/[preset].json

            E.g., if `dft_package` = "vasp", `calculation_presets` = "scf",
            the settings in
            "dftinpgen/vasp/settings/calculation_presets/scf.json" are used.

        custom_sett_file: str, optional
            Location of a JSON file with custom calculation settings as a
            dictionary of tags and values.

            The settings loaded from a specified file can be accessed via an
            attribute `custom_sett_from_file`.

            NB: Custom settings specified here MUST OVERRIDE those in
            `calculation_presets` in case of overlap.

        custom_sett_dict: dict, optional
            Dictionary with custom calculation settings as tags and values.

            NB: Custom settings specified here MUST OVERRIDE those in
            `calculation_presets` and in `custom_sett_from_file`.

            Default: {}

        write_location: str, optional
            Path to the directory in which to write the input files.

            Default: current working directory.

        overwrite_files: bool, optional
            To overwrite files or not, that is the question.

            Default: True

        **kwargs:
            Arbitrary keyword arguments.

        """
        self._crystal_structure = None
        self.crystal_structure = crystal_structure

        self._calculation_presets = None
        self.calculation_presets = calculation_presets

        self._custom_sett_file = None
        self._custom_sett_from_file = {}
        self.custom_sett_file = custom_sett_file

        self._custom_sett_dict = {}
        if custom_sett_dict is not None:
            self.custom_sett_dict = custom_sett_dict

        self._write_location = None
        self.write_location = write_location

        self._overwrite_files = True
        if overwrite_files is not None:
            self.overwrite_files = overwrite_files

    @property
    def crystal_structure(self):
        """Input crystal structure as an `ase.Atoms` object."""
        return self._crystal_structure

    @crystal_structure.setter
    def crystal_structure(self, crystal_structure):
        self._set_crystal_structure(crystal_structure)

    def _set_crystal_structure(self, crystal_structure):
        if not isinstance(crystal_structure, ase.Atoms):
            input_type = type(crystal_structure)
            msg = 'Expected type "ase.Atoms"; found "{}"'.format(input_type)
            raise TypeError(msg)
        self._crystal_structure = crystal_structure

    @property
    def calculation_presets(self):
        """Default settings ("presets") to use for generating input files."""
        return self._calculation_presets

    @calculation_presets.setter
    def calculation_presets(self, calculation_presets):
        self._calculation_presets = calculation_presets

    @property
    def custom_sett_file(self):
        """Path to a JSON file with custom settings dictionary."""
        return self._custom_sett_file

    @custom_sett_file.setter
    def custom_sett_file(self, custom_sett_file):
        self._custom_sett_file = custom_sett_file
        self._custom_sett_from_file = self._read_custom_sett_from_file()

    @property
    def custom_sett_from_file(self):
        """Dictionary of custom settings read from `custom_sett_file`."""
        return self._custom_sett_from_file

    @property
    def custom_sett_dict(self):
        """Dictionary of custom settings to use for generating input."""
        return self._custom_sett_dict

    @custom_sett_dict.setter
    def custom_sett_dict(self, custom_sett_dict):
        self._custom_sett_dict = custom_sett_dict

    @property
    def write_location(self):
        """Path to the directory in which to write the DFT input files."""
        return self._write_location

    @write_location.setter
    def write_location(self, write_location):
        if write_location is None:
            self._write_location = os.getcwd()
        else:
            self._write_location = write_location

    @property
    def overwrite_files(self):
        """Should existing files at `write_location` be overwritten."""
        return self._overwrite_files

    @overwrite_files.setter
    def overwrite_files(self, overwrite_files):
        self._overwrite_files = overwrite_files

    def _read_custom_sett_from_file(self):
        if self.custom_sett_file is None:
            return {}
        with open(self.custom_sett_file, "r") as fr:
            return json.load(fr)

    @abstractproperty
    def dft_package(self):
        """Name of the DFT package input files are generated for."""
        raise NotImplementedError

    @abstractproperty
    def calculation_settings(self):
        """Dictionary of all settings used to generate input files."""
        raise NotImplementedError

    @abstractmethod
    def write_input_files(self):
        """Write DFT input files in the specified location."""
        raise NotImplementedError
