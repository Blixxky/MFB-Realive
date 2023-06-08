"""
More handling of the Windows Manager, and which controller to use, win32gui or AHK.
"""
import logging

from .win32gui_manager import WindowMgrWindowsWin32Gui, HAS_WIN32GUI
from .ahk_manager import WindowMgrWindowsAHK, HAS_AHK

log = logging.getLogger(__name__)


def get_window_mgr_on_windows():
    """
    Determine if using Win32GUI or AHK (We don't use AHK anymore, it's deprecated and will be removed.
    """
    if HAS_WIN32GUI:
        return WindowMgrWindowsWin32Gui
    elif HAS_AHK:
        return WindowMgrWindowsAHK
    else:
        log.error("No Window Manager found for Windows")
