"""
This module provides a function to get the appropriate window manager based on the operating system.

Functions:
- get_window_manager: Returns the window manager instance based on the current operating system.

"""
from modules.platforms.platforms import find_os
from modules.platforms.window_managers.windows import get_window_mgr_on_windows
from modules.platforms.window_managers.linux import WindowMgrLinux


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

    if os == "linux":
        return WindowMgrLinux()

    raise ValueError(f"OS not recognized: {os}")

