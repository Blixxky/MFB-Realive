"""
This module provides an abstract base class for Window Managers.

Classes:
- WindowMgr: An abstract base class that defines the interface for window management.
  Subclasses must implement the 'get_window_geometry' and 'find_game' methods.

"""
from abc import ABC, abstractmethod


class WindowMgr(ABC):
    """Abstract base class for Window Managers"""

    @abstractmethod
    def get_window_geometry(self):
        """Get window geometry"""

    @abstractmethod
    def find_game(self):
        """Find Game"""
