import os
from setuptools import setup
from setuptools import find_packages


with open(
    os.path.join(
        os.path.dirname(__file__), "src", "dftinputgen", "VERSION.txt"
    )
) as fr:
    version = fr.read().strip()


setup(
    name="dftinputgen",
    version=version,
    description="Unopinionated library to generate input files for DFT codes",
    url="https://github.com/CitrineInformatics/dft-input-gen",
    author="Vinay Hegde",
    author_email="vhegde@citrine.io",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=["six", "numpy", "ase <= 3.17"],
    entry_points={"console_scripts": ["dftinputgen = dftinputgen.cli:driver"]},
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
)
