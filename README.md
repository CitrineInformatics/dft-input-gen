# dftinpgen

[![Build Status](https://travis-ci.com/CitrineInformatics/dft-input-gen.svg?token=qbMA4N9P9kHgFLrLQ51g&branch=master)](https://travis-ci.com/CitrineInformatics/dft-input-gen)

Unopinionated input file generator for DFT codes.


## DFT codes supported

1. [pw.x](https://www.quantum-espresso.org/Doc/INPUT_PW.html) from the Quantum
   Espresso package.
2. (under development) Post-processing utilities for PWscf:
   [(dos.x)](https://www.quantum-espresso.org/Doc/INPUT_DOS.html),
   [(bands.x)](https://www.quantum-espresso.org/Doc/INPUT_BANDS.html),
   [(projwfc.x)](https://www.quantum-espresso.org/Doc/INPUT_PROJWFC.html)

## Installation

1. Clone from Github:

```
git clone git@github.com:CitrineInformatics/dft-input-gen.git
```

2. Install requirements (Python versions 2.7, >=3.5 are supported):

```
cd dft-input-gen
pip -r requirements.txt
```

3. Install the package:

```
pip install -e .
```

4. (optional) Unit tests can be run using `pytest`:

```
pip -r test_requirements.txt
pytest -sv
```


## Documentation

The documentation for this project is available in `docs/src`.

