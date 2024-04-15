# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'cq-extrusions'
copyright = '2024, James Keal'
author = 'James Keal'
release = '0.0.1'

# -- General configuration

extensions = [
    "autodoc2",
    "myst_parser",
]
autodoc2_packages = [
    "../src/cq_extrusions",
]

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'
