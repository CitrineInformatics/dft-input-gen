.. _sssec-qe-input-settings:

Input settings
++++++++++++++

All input tags for pw.x have been parsed from the `Input File Description`_
page (last updated November 2019).
The tags are grouped into the corresponding namelists and cards and stored in
`tags_and_groups.json`_.
These tags and the associated groups are then made available to the user via
a module level variable ``QE_TAGS``.

The settings module also makes available a few sets of default tags and
values to be used for common DFT calculation types such as ``scf``,
``relax``, and ``vc-relax``.
The default sets of tags and their values are stored in JSON files in the
`calculation_presets`_ module.
These can be accessed by the user via a module level variable ``QE_PRESETS``.
Note that these presets are only reasonable defaults and are not meant to be
prescriptive.

.. _`Input File Description`: https://www.quantum-espresso.org/Doc/INPUT_PW.html
.. _`tags_and_groups.json`: https://github.com/CitrineInformatics/dft-input-gen/blob/master/src/dftinpgen/qe/settings/tags_and_groups.json 
.. _`calculation_presets`: https://github.com/CitrineInformatics/dft-input-gen/tree/master/src/dftinpgen/qe/settings/calculation_presets

.. automodule:: dftinpgen.qe.settings
    :members:
    :undoc-members:
    :special-members:

.. automodule:: dftinpgen.qe.settings.calculation_presets
    :members:
    :undoc-members:
    :special-members:

