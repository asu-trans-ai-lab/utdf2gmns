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
import sys
from pathlib import Path

home_dir = Path(__file__).parent.parent.parent.absolute()
sys.path.insert(0, str(home_dir))

autodoc_mock_imports = [
    "geocoder",
    "pandas"
]

# -- Project information -----------------------------------------------------
project = 'utdf2gmns'
copyright = '2022-2023, Xiangyong Luo, Xuesong (Simon) Zhou'
author = 'Xiangyong Luo, Xuesong (Simon) Zhou'

# The full version, including alpha/beta/rc tags
release = '0.2.5'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom

# -- Docstring preprocessing for autodoc
# autodoc_typehints = "both"

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']

# # Napoleon settings
# napoleon_google_docstring = True
# napoleon_numpy_docstring = True
# napoleon_include_init_with_doc = True
# napoleon_include_private_with_doc = True
# napoleon_include_special_with_doc = True
# napoleon_use_admonition_for_examples = False
# napoleon_use_admonition_for_notes = False
# napoleon_use_admonition_for_references = False
# napoleon_use_ivar = True
# napoleon_use_param = True
# napoleon_use_rtype = True

# pygments_style = "vs"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
html_static_path = ['_static']

# html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = 'footnote'
