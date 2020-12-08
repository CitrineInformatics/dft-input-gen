.. _sec-developer-notes:

Developer notes
---------------

Code Organization
+++++++++++++++++

``dftinputgen`` has the following overall structure::

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


- ``dftinputgen.base``: base interfaces to build DFT code-specific classes from
  (more :ref:`here <sec-base-input-generator>`)
- ``dftinputgen.qe``: derived classes that can generate input files for various
  DFT-based and postprocessing codes in the Quantum Espresso suite (more
  :ref:`here <ssec-qe>`)
- ``dftinputgen.vasp``: [under development] derived classes that can generate
  input files for the VASP package.
- ``dftinputgen.utils``: general-purpose helper functions, e.g. chemical formula
  parser/formatter (more :ref:`here <sec-helper-utilities>`)
- ``dftinputgen.data``: non-user-specified data constants required to generate
  input files, e.g. standard atomic weights of all elements (more :ref:`here
  <sec-data-constants>`)

  Support for new DFT packages must be added as a separate module, e.g.
  ``dftinputgen/new_dft_package``.
  Corresponding tests must be placed in the ``tests/new_dft_package`` folder.


.. toctree::
   :maxdepth: 2
   :hidden:
