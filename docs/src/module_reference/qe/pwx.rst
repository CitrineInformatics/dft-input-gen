.. _sssec-qe-pwx:

Input for PWscf (pw.x)
++++++++++++++++++++++

The :class:`PwxInputGenerator <dftinputgen.qe.pwx.PwxInputGenerator>` class
(derived from :class:`DftInputGenerator <dftinputgen.base.DftInputGenerator>`)
implements functionality to generate input files for the `PWscf (pw.x)`_
package.

For a user-specified crystal structure and calculation parameters, different
parts of a typical input file (i.e. different `namelists and cards`_) can be
generated separately, as required.

For each namelist/card, the code simply formats the values for keys specified
in the settings, if that key is valid for that namelist/card.
The list of valid keys for each namelist/card is looked up from a ``QE_TAGS``
dictionary (more information about the dictionary of valid keys, and default
parameters/values provided as ``calculation_presets`` is :ref:`here
<sssec-qe-input-settings>`).

The ``KPOINTS`` card generator functionality provides options to specify the
scheme (e.g. ``gamma``, ``automatic``), and to either directly input the grid
itself or let the grid be generated automatically based on an input k-spacing.

The user can specify whether to set potentials before generating input files
or not.
This key is useful for generating dummy input files without any potentials
information which can later be manually filled in, e.g., location on a remote
cluster that is not available while generating input files.
Potentials for each species can be manually specified or automatically
matched to a file in the input ``pseudo_dir``.
Note that in the latter case, the current implementation looks for
pseudopotential files (ending with ``*.UPF``/``*.upf``) in the specified
pseudopotentials directory, and matches each chemical species to a file with
the species in its name (first match).

Generation of the various namelists and cards in the input file is done
lazily, i.e., most sections are constructed only when requested.

**Note:** The ``OCCUPATIONS``, ``CONSTRAINTS``, ``ATOMIC_FORCES`` cards are
currently not implemented.

.. _`PWscf (pw.x)`: https://www.quantum-espresso.org/Doc/pw_user_guide/
.. _`namelists and cards`: https://www.quantum-espresso.org/Doc/INPUT_PW.html


Interfaces
==========

.. automodule:: dftinputgen.qe.pwx
    :members:
    :inherited-members:
    :undoc-members:
