"""
Error exception module
"""
class MercenariesFarmBaseException(Exception):
    """
    Base exception for all custom exceptions in the MercenariesFarm application.
    All custom exceptions should inherit from this class.
    """
    pass


class SettingsError(MercenariesFarmBaseException):
    """
    Raised when there is an issue with the settings of the MercenariesFarm application.
    This is a general exception that should be subclassed by more specific settings error exceptions.
    """
    pass


class MissingSettingsFile(SettingsError):
    """
    Raised when the settings file for the MercenariesFarm application is missing.
    This could be due to the file not being created, or it could have been moved or deleted.
    """
    pass


class MissingGameDirectory(SettingsError):
    """
    Raised when the game directory specified in the settings does not exist.
    This could be due to the directory not being created, or it could have been moved or deleted.
    """
    pass


class UnsetGameDirectory(SettingsError):
    """
    Raised when the game directory setting is not set in the settings file.
    """
    pass


class WindowManagerError(MercenariesFarmBaseException):
    """
    Raised when there is an issue with the window manager in the MercenariesFarm application.
    This is a general exception that should be subclassed by more specific window manager error exceptions.
    """
    pass


class AHKNotInstalled(WindowManagerError):
    """
    Raised when the AHK (AutoHotKey) software is not installed on the system.
    """
    pass


class NoWindowManagerFound(WindowManagerError):
    """
    Raised when no window manager can be found or initialized.
    """
    pass
