#!/usr/bin/env python3
"""
Version information for PyK150
"""

__version__ = "1.0.0-beta"
__author__ = "Faymaz"
__description__ = "Cross-platform PIC programmer GUI for K150 compatible programmers"
__license__ = "MIT"

VERSION_INFO = {
    "version": __version__,
    "author": __author__,
    "description": __description__,
    "license": __license__,
    "release_type": "beta",
    "build_date": "2025-01-22"
}

def get_version():
    """Get version string"""
    return __version__

def get_version_info():
    """Get complete version information"""
    return VERSION_INFO
