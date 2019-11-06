.. _sssec-qe-pwx:

Input for PWscf (pw.x)
++++++++++++++++++++++

The :class:`PwxInputGenerator <dftinpgen.qe.pwx.PwxInputGenerator>` class
(derived from :class:`DftInputGenerator <dftinpgen.base.DftInputGenerator>`)
provides functionality to generate input files for the `PWscf (pw.x)`_
package.

For a user-specified crystal structure and calculation parameters, different
parts of a typical input file (i.e. different `namelists and cards`_) can be
generated separately, if required. The ``OCCUPATIONS``, ``CONSTRAINTS``,
``ATOMIC_FORCES`` cards are currently not implemented.

For each namelist/card, the code simply formats the values for keys specified
in the settings, if that key is valid for that namelist/card. The list of valid
keys for each namelist/card is looked up from a ``QE_TAGS`` dictionary (more
information about the dictionary of valid keys, and default parameters/values
provided as "base recipes" is :ref:`here <sssec-qe-input-settings>`).

The ``KPOINTS`` card generator functionality provides options to specify the
scheme (e.g. ``gamma``, ``automatic``), and to either directly input the grid
itself or let the grid be generated automatically based on an input k-spacing.

The pseudopotentials to be listed in the input file can be specified in two
different ways in the input calculation settings:

1. ``pseudo_repo_dir`` + ``pseudo_set``
2. ``pseudo_dir``

Specifying a pseudopotentials repository + set is for convenient central
storage of all pseudopotentials, and easy switching between
internally-compatible sets of pseudopotentials.
If ``pseudo_dir`` is not specified, it is assumed to be
``[pseudo_repo_dir]/[pseudo_set]``. A directly specified ``pseudo_dir``
overrides specifying the repository and set separately. In either case, the
code looks for pseudopotential files (ending with ``*.UPF``/``*.upf``) in the
previously specified pseudopotentials directory for each elemental species, and
assigns the first pseudopotential it finds to the respective species. A
one-to-one mapping between elemental species in the input crystal structure and
pseudopotential files is enforced unless specified otherwise.

Generation of the various namelists and cards in the input file (including
automatic generation of k-point grids and setting pseudopotentials) is done
lazily: most sections are constructed only when requested.


.. _`PWscf (pw.x)`: https://www.quantum-espresso.org/Doc/pw_user_guide/
.. _`namelists and cards`: https://www.quantum-espresso.org/Doc/INPUT_PW.html


Interfaces
==========

.. automodule:: dftinpgen.qe.pwx
    :members:
    :inherited-members:
    :undoc-members:
