"""
This module provides a Windows-specific implementation of the Window Manager using the win32gui library.
It encapsulates some calls to the Windows API (winapi) for window management, including finding game windows,
getting window geometry, showing windows, and setting windows to the foreground.

Changelog:
- Fixed global variable declaration for 'left', 'top', 'width', and 'height'.
- Fixed return statements in the 'find_game' function to return expressions or None.
- Defined the '_handles' attribute inside the '__init__' method.

Classes:
- WindowMgrWindowsWin32Gui: A class that extends the base WindowMgr class and implements the Windows-specific
  window management functions using the win32gui library.
"""

import re
import logging
import win32gui
import win32com.client as win32
from win32api import GetSystemMetrics
from modules.platforms.window_managers.base import WindowMgr
from modules.platforms.platforms import find_os

log = logging.getLogger(__name__)

try:
    shell = win32.Dispatch("WScript.Shell")
    HAS_WIN32GUI = True
except ImportError:
    HAS_WIN32GUI = False
    if find_os() == "windows":
        log.debug("win32gui not installed")

SW_SHOW = 5


class WindowMgrWindowsWin32Gui(WindowMgr):
    """
    This class provides functionalities to manage windows in Windows OS.
    It extends from the base WindowMgr class and implements Win32-specific methods.
    """

    def __init__(self):
        """
        Initializes an instance of the WindowMgrWindowsWin32Gui class, setting the window handle to None.
        """
        self._handle = None
        self._handles = []

    def find_game(self, WINDOW_NAME, BNCount=0):
        """
        Searches for the game window named 'WINDOW_NAME' on the screen, and brings it to the foreground if found.

        Args:
            WINDOW_NAME (str): The name of the game window to search for.
            BNCount (int): The number of instances of the game window. Default is 0.

        Returns:
            self._handle: The handle to the found game window, or None if no matching window is found.
        """
        self._find_window(WINDOW_NAME, BNCount)
        if (self._handle is not None) and (
            WINDOW_NAME != win32gui.GetWindowText(win32gui.GetForegroundWindow())
        ):
            self._show_window()
            self._set_foreground()
        return self._handle

    def get_window_geometry(self):
        """
        Fetches the window geometry of the active window. If the active window is 'Battle.net'
        or the executable name is 'Battle.net.exe', it returns the geometry of the entire screen.
        Otherwise, it returns the client window geometry.

        Returns:
            tuple: A tuple representing the window's geometry (x, y, width, height).
        """
        # To get the active window name
        WINDOW_NAME = win32gui.GetWindowText(win32gui.GetForegroundWindow())

        # Judge which window, fake the BN resolution
        if WINDOW_NAME == "Battle.net" or "Battle.net.exe" in WINDOW_NAME:
            return (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))
        else:
            left, top, width, height = win32gui.GetClientRect(self._handle)
            left, top = win32gui.ClientToScreen(self._handle, (left, top))
            return (left, top, width, height)

    def _window_enum_callback(self, hwnd, WINDOW_NAME):
        """
        Callback function used by win32gui.EnumWindows() to check all the opened windows.
        If a window title matches the given WINDOW_NAME, it sets the window handle to this window's handle.

        Args:
            hwnd: The handle to the window being checked.
            WINDOW_NAME (str): The name of the game window to search for.
        """
        if re.match(WINDOW_NAME, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handles.append(hwnd)
            self._handle = hwnd

    def _find_window(self, WINDOW_NAME, BNCount):
        """
        Enumerates through all the windows and attempts to find the one with the given WINDOW_NAME.

        Args:
            WINDOW_NAME (str): The name of the game window to search for.
            BNCount (int): The number of instances of the game window.
        """
        self._handle = None
        self._handles = []
        win32gui.EnumWindows(self._window_enum_callback, WINDOW_NAME)

        if len(self._handles) < 1:
            log.info("Matched no window")
            return False
        elif len(self._handles) > 1:
            self._handle = self._handles[BNCount]
        else:
            self._handle = self._handles[0]

        return True  # Added this line

    def _show_window(self):
        """
        Brings the identified game window to the foreground.
        """
        shell.SendKeys("%")
        win32gui.ShowWindow(self._handle, SW_SHOW)

    def _set_foreground(self):
        """
        Sets the identified game window as the foreground window.
        """
        win32gui.SetForegroundWindow(self._handle)
        shell.SendKeys("%")
