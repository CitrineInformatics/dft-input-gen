.. _sec-base-input-generator:


Base input generators
+++++++++++++++++++++

``dftinpgen`` implements some high-level interfaces to build DFT
code-specific input generator classes from.


Base DFT input generator
========================

The abstract :class:`DftInputGenerator <dftinpgen.base.DftInputGenerator>`
class provides a common interface to model code-specific input generators.
The input crystal structure must be an `ase.Atoms`_ object obtained via,
e.g., using the `ase.io.read` module or other means.
Settings for the DFT calculation are allowed to be specified by the user
using one or more of the following inputs:

1. ``calculation_presets``: a set of default parameters to use for common
   calculation types (packaged with ``dftinpgen``; see
   :ref:`sssec-qe-input-settings` for more information)
2. ``custom_sett_file``: a JSON file with parameter names and values
3. ``custom_sett_dict``: a dictionary of parameter names and values

Any parameters defined in ``custom_sett_dict`` override those in
``custom_sett_file``, which in turn override those loaded from the specified
``calculation_presets``.

This hierarchical set of parameter specification is designed for convenient
management of DFT calculations at high-throughput.
For instance, default parameters in base recipes can be used for consistency
across all calculations in a project.
A custom settings file can be used to define additional parameters for a subset
of calculations in the project (e.g., using custom GGA+U parameters for TM
oxides).
Any settings that need to be tweaked on a per-compound basis (e.g., changing
charge density mixing parameters to achieve electronic self-consistency
during runtime) can be specified in the custom settings dictionary.

.. _`ase.Atoms`: https://wiki.fysik.dtu.dk/ase/ase/atoms.html
.. _`ase.io.read`: https://wiki.fysik.dtu.dk/ase/ase/io/io.html#ase.io.read

The interface is intended to provide a barebones structure for derived
classes and is therefore very flexible.
It requires only the following attributes to be implemented by any derived
classes:

1. ``dft_package``: a property with the name of the DFT package supported by
   the class.
2. ``calculation_settings``: a property with the aggregated dictionary of
   user-input and any autodetermined DFT settings.
3. ``write_input_files``: a method that writes input files to a specified
   location or to reasonable defaults.

**Note**: The interfaces defined here are unopinionated by design.
There are no sanity checks for parameter values and if/how they correspond to
the input crystal structure.


Interfaces
==========

.. automodule:: dftinpgen.base
    :members:
    :undoc-members:
