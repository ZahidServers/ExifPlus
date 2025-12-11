# docs/conf.py
import os
import sys
from datetime import datetime

# -- Path setup --------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# -- Project information -----------------------------------------------------
project = "ExifPlus"
author = "Mohammed Zahid Wadiwale"
# Optionally read version from package
try:
    from exifplus import __version__ as release
except Exception:
    release = "0.0.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# If pyexiv2 or other native libs cause import errors during docs build,
# mock them so autodoc can still import the rest of the package.
autodoc_mock_imports = ["pyexiv2"]

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_title = f"{project} documentation"
html_last_updated_fmt = "%Y-%m-%d"

# Optional: show version in the docs
version = release
copyright = f"{datetime.now().year}, {author}"
