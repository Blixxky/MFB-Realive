"""
This module provides a Linux-specific implementation of the Window Manager using the Wnck library.
It encapsulates some calls for Linux window management, including finding game windows and getting
window geometry.

Classes:
- WindowMgrLinux: A class that extends the base WindowMgr class and implements the Linux-specific
  window management functions using the Wnck library.

"""
import time
import logging
import pyautogui

from modules.platforms.window_managers.base import WindowMgr
from modules.platforms.platforms import find_os

# from ...exceptions import WindowManagerError

log = logging.getLogger(__name__)
try:
    import pgi

    pgi.install_as_gi()
    import gi

    gi.require_version("Wnck", "3.0")
    from gi.repository import Wnck, Gtk
except ImportError:
    if find_os() == "linux":
        log.error("gi.repository and/or pgi not installed")


class WindowMgrLinux(WindowMgr):
    """
    This class provides functionalities to handle windows in Linux systems.
    It extends from the base WindowMgr class and implements Linux-specific methods.
    """

    def __init__(self):
        """Constructor"""
        self.win = None
        self._win = None  # define '_win' attribute in constructor

    def find_game(self, WINDOW_NAME):
        """
        Searches for the game window named 'WINDOW_NAME' on the screen and makes it active.
        If the game window is not found, prints a message and sets the target window as None.

        Note: BNCount is not used in this method; it's included to keep the method signature consistent
        with other implementations.

        Args:
            WINDOW_NAME (str): The name of the game window to search for.

        Returns:
            win: Returns the identified game window if found, else returns None.
        """
        screenHW = Wnck.Screen.get_default()
        while Gtk.events_pending():
            Gtk.main_iteration()
        windows = screenHW.get_windows()

        win = None
        for w in windows:
            if w.get_name() == WINDOW_NAME:
                win = w
                win.activate(int(time.time()))
                win.make_above()
                win.unmake_above()
                break
        if not win:
            print(f"No '{WINDOW_NAME}' window found.")
        self._win = win  # use self._win defined in __init__
        return win

    def get_window_geometry(self):
        """
        Fetches the window geometry of the target window. If the target window is 'Battle.net',
        returns the geometry of the entire screen, else returns the client window geometry.

        Returns:
            tuple: A tuple representing the window's geometry (x, y, width, height).
        """
        # workaround for Battle.net
        if self._win.get_name() == "Battle.net":
            (width, height) = pyautogui.size()
            return (0, 0, width, height)
        return self._win.get_client_window_geometry()
