.. _sec-developer-notes:

Developer notes
---------------


Contributing guidelines
+++++++++++++++++++++++

Note that, at this time, both Python 2 and 3 are supported.

Overall requirements
====================

1. This project follows the `gitflow workflow`_; all PRs should be submitted
   to the `develop` branch.
2. Any new functionality should be accompanied by unit tests.
   Full coverage is ideal; core functionality must be covered at minimum.
3. It is highly recommended to complement any new module(s) with a
   corresponding example in the ``dftinpgen.demo`` module.
4. Docstrings for any new functionality are required.
   It is recommended to add any additional information useful to the user to
   the package docs.
5. Versioning should follow `semantic versioning`_.

.. _`gitflow workflow`: https://www.atlassian.com/git/tutorials/comparing-workflows#gitflow-workflow
.. _`semantic versioning`: https://semver.org/


Coding style
============

PEP8 guidelines are followed throughout.
A pre-commit hook is available to auto-format code with black_ (recommended):

1. Make sure you are using a Python version >=3.6
2. Install black_: ``$ pip install black``
3. Install pre-commit: ``$ pip install pre-commit``
4. Intall git hooks in your ``.git`` directory: ``$ pre-commit install``

Done; every new commit will be checked and autoformatted with black.

For docstrings, follow the `numpydoc docstring guide`_.

.. _black: https://black.readthedocs.io/en/stable/
.. _`numpydoc docstring guide`: https://numpydoc.readthedocs.io/en/latest/format.html


Code Organization
+++++++++++++++++

``dftinpgen`` has the following overall structure::

    base.py
    utils.py
    data/
        standard_atomic_weights.json
        ...
    qe/
        pwx.py
        bandsx.py
        ...
        settings/
            tags_and_groups.json
            ...
            base_recipes/
                scf.json
                vc-relax.json
                ...
    vasp/
        ...


- ``dftinpgen.base``: base interfaces to build DFT code-specific classes from
  (more :ref:`here <sec-base-input-generator>`)
- ``dftinpgen.qe``: derived classes that can generate input files for various
  DFT-based and postprocessing codes in the Quantum Espresso suite (more
  :ref:`here <ssec-qe>`)
- ``dftinpgen.vasp``: [under development] derived classes that can generate
  input files for the VASP package.
- ``dftinpgen.utils``: general-purpose helper functions, e.g. chemical formula
  parser/formatter (more :ref:`here <sec-helper-utilities>`)
- ``dftinpgen.data``: non-user-specified data constants required to generate
  input files, e.g. standard atomic weights of all elements (more :ref:`here
  <sec-data-constants>`)


.. toctree::
   :maxdepth: 2
   :hidden:
