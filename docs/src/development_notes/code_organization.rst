.. _ssec-code-organization:

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


- ``dftinpgen.base``: basic input generator classes to build DFT code-specific
  classes from (more :ref:`here <sec-base-input-generator>`)
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
