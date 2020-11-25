# dftinpgen

[![Build Status](https://travis-ci.com/CitrineInformatics/dft-input-gen.svg?token=qbMA4N9P9kHgFLrLQ51g&branch=master)](https://travis-ci.com/CitrineInformatics/dft-input-gen)

Unopinionated input file generator for DFT codes.


## Requirements

Python >=2.7 or >=3.8, with dependencies listed in
[requirements.txt](https://github.com/CitrineInformatics/dft-input-gen/blob/master/requirements.txt).


## Installation

`dftinpgen` can be installed with `pip`:

```
$ pip install dftinpgen
```


## Usage

To generate input files to run an `scf` calculation using `pw.x` for a input
crystal structure in `my_crystal_structure.cif`, do:

**Option 1. Using the Python API**

```python
from dftinpgen.utils import read_crystal_structure
from dftinpgen.qe.pwx import PwxInputGenerator

# read the input crystal into an `ase.Atoms` object
crystal_structure = read_crystal_structure("/path/to/my_crystal_structure.cif")

# print formatted pw.x input to standard output
pwig = PwxInputGenerator(
   crystal_structure=crystal_structure,
   calculation_presets="scf",
)
pwig.write_input_files()
```

**Option 2. Using the `dftinpgen` command line tool**

```bash
$ dftinpgen pw.x -i /path/to/my_crystal_structure.cif -pre scf
```

Further details of the API and examples can be found in the package
documentation.


## DFT codes supported

1. [pw.x](https://www.quantum-espresso.org/Doc/INPUT_PW.html) from the
   [Quantum Espresso package](https://www.quantum-espresso.org/)
2. (under development) Post-processing utilities for pw.x:
   [dos.x](https://www.quantum-espresso.org/Doc/INPUT_DOS.html),
   [bands.x](https://www.quantum-espresso.org/Doc/INPUT_BANDS.html),
   [projwfc.x](https://www.quantum-espresso.org/Doc/INPUT_PROJWFC.html)


## Contributing

Contributions are welcome, both issues and pull requests.
Guidelines are [here](CONTRIBUTING.md).
