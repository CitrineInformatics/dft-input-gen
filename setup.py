import os
from setuptools import setup
from setuptools import find_packages


with open(
    os.path.join(os.path.dirname(__file__), "src", "dftinpgen", "VERSION.txt")
) as fr:
    version = fr.read().strip()


setup(
    name="dftinpgen",
    version=version,
    description="Unopinionated library to generate input files for DFT codes",
    url="https://github.com/CitrineInformatics/dft-input-gen",
    author="Vinay Hegde",
    author_email="vhegde@citrine.io",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">2.6, >3.7",
    install_requires=["six", "numpy", "ase <= 3.17"],
    entry_points={"console_scripts": ["dftinpgen = dftinpgen.cli:driver",]},
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.8",
    ],
)
