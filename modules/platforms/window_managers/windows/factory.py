"""
More handling of the Windows Manager, and which controller to use, win32gui or AHK.
"""
import logging

from modules.platforms.window_managers.windows.win32gui_manager import (
    WindowMgrWindowsWin32Gui,
    HAS_WIN32GUI,
)

log = logging.getLogger(__name__)


def get_window_mgr_on_windows():
    """
    Determine if using Win32GUI. Used to support AHK but was deprecated and removed.
    """
    if HAS_WIN32GUI:
        return WindowMgrWindowsWin32Gui
    else:
        log.error("No Window Manager found for Windows")
