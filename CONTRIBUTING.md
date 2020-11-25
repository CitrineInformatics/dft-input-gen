# Contribution guidelines

## Installation and Development

Clone from github:
```bash
git clone git@github.com:CitrineInformatics/dft-input-gen.git
```

Create a virtual environment;
one option is to use conda, but it is not required:
```bash
conda create -n <env_name>
conda activate <env_name>
```

Then install requirements:
```bash
pip install -U -r requirements.txt
pip install -U -r test_requirements.txt
pip install --no-deps -e .
```

### Running tests
We use [pytest](https://docs.pytest.org/en/stable/contents.html) to run tests.
To run all tests:
```bash
pytest -svv
```

### Test coverage

We use [pytest-cov](https://pytest-cov.readthedocs.io/en/latest) to check
code coverage.
To run all tests and output a report of the coverage of the `src` directory:
```bash
pytest --cov=src/ --cov-report term-missing -svv
```

## Coding Style

`dftinpgen` follows [PEP8](https://www.python.org/dev/peps/pep-0008/), with
several docstring rules relaxed.
See `tox.ini` for a list of the ignored rules.
Docstrings must follow the
[Numpy style](https://numpydoc.readthedocs.io/en/latest/format.html).

We use [flake8](https://flake8.pycqa.org/en/latest/) as a linter.
To run the linter on the `src` directory:
```bash
flake8 src
```

A pre-commit hook is available to auto-format code with
[black](https://black.readthedocs.io/en/stable) (recommended):

1. Make sure you are using a Python version >=3.6
2. Install black: ``$ pip install black``
3. Install pre-commit: ``$ pip install pre-commit``
4. Intall git hooks in your ``.git`` directory: ``$ pre-commit install``


## PR Submission

`dftinpgen` follows the
[gitflow workflow](https://www.atlassian.com/git/tutorials/comparing-workflows#gitflow-workflow),
so all PRs must be submitted to the `develop` branch.
Versions must follow [semantic versioning](https://semver.org/).

In order to be merged, a PR must be approved by one authorized user and the
build must pass.
A passing build requires the following:
* All tests pass
* The linter finds no violations of PEP8 style
* Every line of code is executed by a test (100% coverage)

It is recommended to complement any new large module(s) with
example(s) in the `dftinpgen.demo` module.


## Documentation

Additional information useful to the user should be added to the package
documentation in `docs/src`.