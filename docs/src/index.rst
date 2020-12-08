dftinputgen
+++++++++

Unopinionated input file generator for DFT codes.

``dftinputgen`` implements high-level interfaces that help generate input files
from user-specified key-value pairs.
By design, there is no validation of input, only formatting of the key-values
pairs for the DFT code of interest.
The package also provides default settings for some common types of DFT
calculations (``calculation_presets``), which can be used as is or used to
build more customized input settings.

Installation instructions can be found in the README_.

Examples of using the tool can be found in the `demo module`_.

.. _README: https://github.com/CitrineInformatics/dft-input-gen
.. _demo module: https://github.com/CitrineInformatics/dft-input-gen/tree/master/src/dftinputgen/demo 


.. toctree::
    :maxdepth: 3
    :hidden:

    developer_notes/index
    module_reference/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
