"""Version information for Data Contracts Studio Backend.

This module contains version and metadata information for the
Data Contracts Studio backend application.
"""

from __future__ import annotations

__version__: str = "0.0.4"
__title__: str = "Data Contracts Studio"
__description__: str = "A modern, scalable data contract management platform"
__author__: str = "Panagiotis Erodotou"
__license__: str = "MIT"


def get_version_info() -> dict[str, str]:
    """Get comprehensive version information.

    Returns:
        A dictionary containing version and metadata information.
    """
    return {
        "version": __version__,
        "title": __title__,
        "description": __description__,
        "author": __author__,
        "license": __license__,
    }
