import os

from dftinpgen.data import *
from dftinpgen.qe import *


# single-sourcing the package version
with open(os.path.join(os.path.dirname(__file__), 'VERSION.txt')) as fr:
    __version__ = fr.read().strip()

VERSION = __version__
__short_version__ = __version__.rpartition('.')[0]
