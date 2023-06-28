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

sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../utdf2gmns'))

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
autodoc_typehints = "both"

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.doctest',
              'sphinx.ext.intersphinx',
              'sphinx.ext.todo',
              'sphinx.ext.coverage',
              'sphinx.ext.mathjax',
              'sphinx.ext.ifconfig',
              'sphinx.ext.viewcode',
              'sphinx.ext.githubpages',
              'sphinx.ext.napoleon']

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

pygments_style = "vs"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
html_static_path = ['_static']

html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = 'footnote'


# def process_signature(app, what, name, obj, options, signature, return_annotation):
#     """Replace the create_env keyword argument accepted by decorated mods with
#     the parameters added by the decorator"""
#
#     if what in ["function", "method"] and hasattr(obj, "_decorated_mod"):
#         if "create_env" not in signature:
#             raise ValueError(
#                 f"Decorated mod {name} does not accept create_env")
#         new_signature = signature.replace(
#             "create_env", "verbose=True, logfile=None, solver_params=None"
#         )
#         print(f"Modified signature of {name}")
#         return new_signature, return_annotation
#
#     return signature, return_annotation
#
# boilerplate = """
#     **verbose** : :ref:`bool <python:bltin-boolean-values>`, optional
#         ``verbose=False`` suppresses all console output
#
#     **logfile** : :class:`python:str`, optional
#         Write all mod output to the given file path
#
#     **solver_params** : :class:`python:dict`, optional
#         Gurobi parameters to be passed to the solver"""
# boilerplate = boilerplate.split("\n")
#
#
# def process_docstring(app, what, name, obj, options, lines):
#     """Add parameter entries for decorated mods"""
#
#     if what in ["function", "method"] and hasattr(obj, "_decorated_mod"):
#         # Find where the last input parameter is listed
#         in_paramlist = False
#         lineno = None
#         for i, line in enumerate(lines):
#             if ":Parameters:" in line:
#                 in_paramlist = True
#             elif in_paramlist and (
#                 ":Returns:" in line or "processed by numpydoc" in line
#             ):
#                 lineno = i - 1
#                 break
#
#         if lineno is None:
#             raise ValueError(f"Failed to find param list for {name}")
#
#         # Insert boilerplate bits
#         for line in reversed(boilerplate):
#             lines.insert(lineno, line)
#
#     if what == "module":
#         lines.append("")
#         lines.append(f"The following mods can be imported from ``{name}``:")
#
#
# def setup(app):
#     app.connect("autodoc-process-signature", process_signature)
#     app.connect("autodoc-process-docstring", process_docstring)
