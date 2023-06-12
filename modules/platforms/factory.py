"""
This module provides a function to get the appropriate window manager based on the operating system.

Functions:
- get_window_manager: Returns the window manager instance based on the current operating system.

"""
from .platforms import find_os
from .window_managers.windows import get_window_mgr_on_windows
from .window_managers.linux import WindowMgrLinux


def get_window_manager():
    """
    Get the appropriate window manager based on the operating system.

    Returns:
    - Window manager instance for the current operating system.
    """
    os = find_os()

    if os == "windows":
        WindowMgrWindows = get_window_mgr_on_windows()
        return WindowMgrWindows()
    elif os == "linux":
        return WindowMgrLinux()
    else:
        raise ValueError(f"OS not recognized: {os}")
