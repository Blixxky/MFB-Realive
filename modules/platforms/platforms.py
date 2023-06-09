"""
This module provides a function to detect the operating system.

Functions:
- find_os: Detects the operating system and returns its name.

"""

import sys
import logging

log = logging.getLogger(__name__)


def find_os():
    """
    Detect the operating system and return its name.

    Returns:
    - Name of the detected operating system.
    """
    # try to detect the OS (Windows, Linux, Mac, ...)
    # to load specific libs
    if sys.platform in ["Windows", "win32", "cygwin"]:
        myOS = "windows"
    elif sys.platform in ["linux", "linux2"]:
        myOS = "linux"
    else:
        myOS = "unknown"
        log.info("sys.platform='%s' is unknown.", sys.platform)
        sys.exit()
    return myOS
