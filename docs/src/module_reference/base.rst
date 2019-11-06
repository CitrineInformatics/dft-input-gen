.. _sec-base-input-generator:


Base input generators
+++++++++++++++++++++

``dftinpgen`` provides some base input generator classes to build DFT
code-specific classes from.


Base DFT input generator
========================

The base :class:`DftInputGenerator <dftinpgen.base.DftInputGenerator>` class
provides an interface to specify settings for input file generation (for a
user-specified crystal structure file) in three ways:

1. ``base_recipe``: a set of default parameters (packaged with ``dftinpgen``;
   see :ref:`sssec-qe-input-settings` for more information)
2. ``custom_sett_file``: a file with parameters
3. ``custom_sett_dict``: a dictionary of parameters

Any parameters defined in ``custom_sett_dict`` override those in
``custom_sett_file``, which in turn override those defined in ``base_recipe``.

This hierarchical set of parameter specification is designed for convenient
management of DFT calculations at high-throughput. For instance, default
parameters in base recipes can be used for consistency across all calculations
in a project. A custom settings file can be used to define additional
parameters for a subset of calculations in the project (say, using custom GGA+U
parameters for TM oxides). Any settings that need to be tweaked on a
per-compound basis (say, changing charge density mixing parameters to achieve
electronic self-consistency) can be specified in the custom settings
dictionary.

It uses `ASE IO module`_ to read user-specified crystal structures: all formats
supported by ASE are thus naturally supported.

.. _`ASE IO module`: https://wiki.fysik.dtu.dk/ase/ase/io/io.html

It provides some DFT code-agnostic functionality, e.g. generating a uniform
k-mesh from a user-specified k-spacing.

Note: This class is not expected to be used directly by end-users (an abstract
class, in spirit), and is to be used to build more sophisticated classes for
various DFT codes.

Note: The interfaces defined here are unopinionated by design. There are no
sanity checks for parameter values and how they correspond to the input crystal
structure.


Base PP input generator
=======================

Information about the base class for generating input for post-processing codes
such as bands.x and dos.x goes here.



Interfaces
==========

.. automodule:: dftinpgen.base
    :members:
    :undoc-members:
