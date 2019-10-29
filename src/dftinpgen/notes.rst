dftinpgen
=========


Overall code organization:
--------------------------

? utils.py (convert to and from CIFs, etc.)

data/
   __init__.py
   elemental_data.json (atomic weights and nominal valence electrons)

qe/
   __init__.py
   pwx.py
   settings/
      pwx/
      bandsx/
      dosx/
      phx/

vasp/
   __init__.py
   input_generator.py

configs/
   __init__.py
   qe/
      settings/
         scf.json
         relax.json
         vc-relax.json
         ...
      pseudos/
         sssp_efficient.json
         sssp_accurate.json
         ...
   vasp/
      settings/
         scf.json
         relax.json
         ...
      pseudos/
         vasp_recommended.json
         materials_project.json
         ...
   .../
      ...
      ...
   .../


The public interface to this module will take as input a ``crystal structure``
file (any format that ``ase`` can handle), the DFT code used ``dft_code``, the
type of the calculation ``calc_type``, any custom calculation settings
``custom_calc_sett``, and writes PWscf (or other QE/VASP modules in the future)
into a specified location ``write_location`` or in the current working directory
otherwise.

The individual DFT code interfaces will take as input everything except the
``dft_code`` parameter, and generate the corresponding input files.


TODO:
-----

- Add setting tag for magnetism.
- Provide ready-to-go settings for various Hubbard schemes (``wang``,
  ?? ``bennett-avg``, ?? ``aykol``).
//- Read pseudopotential configuration for the calculation from settings (or have reasonable defaults).
//- Provide option to specify the location of the pseudopotentials in a config
  file in the user home directory.
//- Provide ready-to-go settings for ``scf``, ``relax``, ``vc-relax``
  calculations. Add ``bandstructure``, ``dos``, etc. in the future.
