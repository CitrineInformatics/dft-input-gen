import re

from dftinpgen.data import STANDARD_ATOMIC_WEIGHTS


class DftinpgenUtilsError(Exception):
    """Base class for errors associated with the helper utilities."""
    pass


def get_elem_symbol(species_label):
    """Get element symbol from species label, e.g. "Fe" from "Fe1", "Fe-2".

    NB: Returns the first valid element symbol encountered.

    Raises `DftInputGeneratorError` if no valid element symbol was found.
    """
    re_formula = re.compile('([A-Z][a-z]?)')
    symbols = re_formula.findall(species_label)
    for symbol in symbols:
        if symbol in STANDARD_ATOMIC_WEIGHTS:
            return symbol
    msg = 'No valid element symbol found'
    raise DftinpgenUtilsError(msg)
