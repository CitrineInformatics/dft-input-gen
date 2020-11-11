import re
import six
import numpy as np

from ase import io as ase_io

from dftinpgen.data import STANDARD_ATOMIC_WEIGHTS


class DftinpgenUtilsError(Exception):
    """Base class for errors associated with the helper utilities."""

    pass


def get_elem_symbol(species_label):
    """Get element symbol from species label, e.g. "Fe" from "Fe1", "Fe-2".

    NB: Returns the first valid element symbol encountered.

    Raises `DftInputGeneratorError` if no valid element symbol was found.
    """
    re_formula = re.compile("([A-Z][a-z]?)")
    symbols = re_formula.findall(species_label)
    for symbol in symbols:
        if symbol in STANDARD_ATOMIC_WEIGHTS:
            return symbol
    msg = "No valid element symbol found"
    raise DftinpgenUtilsError(msg)


def read_crystal_structure(crystal_structure, **kwargs):
    """Use `ase.io.read` to from crystal structure file specified."""
    if isinstance(crystal_structure, six.string_types):
        return ase_io.read(crystal_structure, **kwargs)
    else:
        msg = "Expected type str; found {}".format(type(crystal_structure))
        raise TypeError(msg)


def get_kpoint_grid_from_spacing(crystal_structure, spacing):
    """Returns a list [k1, k2, k3] with the dimensions of a uniform
    k-point grid corresponding to the input `spacing`.

    Parameters
    ----------

    crystal_structure: `ase.Atoms` object
        Crystal structure for which to calculate k-point grid

    spacing: float
        Maximum distance between two k-points on a uniform grid in reciprocal
        space.

    Returns
    -------

    k-point grid as a 3 x 1 list of integers.

    """
    rcell = 2 * np.pi * (np.linalg.inv(crystal_structure.cell).T)
    return list(map(int, np.ceil(np.linalg.norm(rcell, axis=1) / spacing)))
