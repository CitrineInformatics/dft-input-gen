# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))


# -- Project information -----------------------------------------------------

project = "dftinputgen"
copyright = "2019, Citrine Informatics"
author = "Vinay Hegde <vhegde@citrine.io>"

# The full version, including alpha/beta/rc tags
version_file = os.path.join("..", "..", "src", "dftinputgen", "VERSION.txt")
with open(version_file, "r") as fr:
    release = fr.read().strip()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

html_theme_options = {
    "description": "\n",
    "fixed_sidebar": True,
    "github_button": True,
    "github_repo": "dft-input-gen",
    "github_user": "CitrineInformatics",
    "link_hover": "#000000",
    "font_family": "sans-serif",
    "font_size": "16px",
    "code_font_size": "14px",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Example configuration for intersphinx library
intersphinx_mapping = {"https://docs.python.org": None}

# If true, `todo` and `todoList` produce output
todo_include_todos = True
