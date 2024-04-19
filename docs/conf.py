from datetime import date

project = "bd-extrusions"
release = "0.0.1"
author = "James Keal"
copyright = f"{date.today().year}, {author}"

extensions = [
    "sphinx.ext.autodoc",
]

html_theme = "sphinx_rtd_theme"
