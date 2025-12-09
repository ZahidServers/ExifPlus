# exifplus/__init__.py
"""
ExifPlus - A simple EXIF metadata viewer and editor.
"""

from .app import main

__version__ = "0.1.0"
__all__ = ["main", "__version__"]


def run():
    """Entry point for python -m exifplus"""
    return main()

