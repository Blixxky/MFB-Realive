"""
This module provides functions for managing game settings and configurations.

Functions:
- add_bot_settings: Add default bot settings to the settings dictionary.
- get_system_user_settings: Get system and user settings and merge them into a single dictionary.
- get_settings: Read the settings file and return the settings as a dictionary.
- copy_config_from_sample_if_not_exists: Copy the sample config to the config file if it doesn't exist.
"""
import logging
import pathlib
import shutil
import sys
import os
from modules.exceptions import MissingGameDirectory, UnsetGameDirectory, SettingsError
from modules.file_utils import parseINI, readINI
from modules.utils import update

log = logging.getLogger(__name__)

DEFAULT_RESOLUTION = "1920x1080"
BASE_IMAGES_DIR = "files"


def add_bot_settings(set_dict):
    """
    Adds bot specific settings to a settings dictionary. The settings added include
    default resolution, root images directory, images directory and user files directory.

    Args:
        set_dict (dict): The original settings dictionary.

    Returns:
        dict: The updated settings dictionary containing the bot settings.
    """
    set_dict["default_resolution"] = DEFAULT_RESOLUTION

    set_dict["root_images_dir"] = BASE_IMAGES_DIR
    set_dict["images_dir"] = pathlib.PurePath(
        BASE_IMAGES_DIR, DEFAULT_RESOLUTION
    ).as_posix()
    set_dict["user_files_dir"] = pathlib.PurePath("conf", "user").as_posix()
    #    print(set_dict["user_files_dir"])
    #    print(set_dict["images_dir"])
    return set_dict


def get_system_user_settings(system_settings_filename, user_settings_filename):
    """
    Fetches system and user settings, updates and merges them into a single dictionary.
    Raises exceptions for unset or missing game directories, and logs all the final settings.

    Args:
        system_settings_filename (str): The name of the system settings file.
        user_settings_filename (str): The name of the user settings file.

    Returns:
        dict: The final settings dictionary containing both system and user settings.

    Raises:
        UnsetGameDirectory: If the game directory is not set.
        MissingGameDirectory: If the game directory does not exist.
    """
    try:
        system_settings_dict = get_settings(system_settings_filename)
        user_settings_dict = get_settings(user_settings_filename)
        settings_dict = update(system_settings_dict, user_settings_dict)
        if not settings_dict["gamedir"]:
            raise UnsetGameDirectory("Game Dir setting is not set")

        game_dir = pathlib.Path(settings_dict["gamedir"])
        if not game_dir.is_dir():
            raise MissingGameDirectory(f"Game directory ({game_dir}) does not exist")
        else:
            logs_dir = (settings_dict["gamedir"] + "/Logs")
            subdirectories = os.listdir(logs_dir)

            settings_dict["zonelog"] = pathlib.PurePath(
                game_dir, "Logs/" + subdirectories[len(subdirectories) - 1] + "/Zone.log"
            ).as_posix()

        log.info("Settings")
        for setting, value in settings_dict.items():
            log.info(f" - {setting}: {value}")
    except Exception as e:
        log.error("Running without settings:", e)

    return add_bot_settings(settings_dict)


def get_settings(settings_filename):
    """
    Reads the settings from a given settings file and returns them in a dictionary.
    The settings include resolution, level, location, mode, quit before boss fight status,
    monitor number, mouse speed, wait for EXP, and zone log file location.

    Args:
        settings_filename (str): The name of the settings file.

    Returns:
        dict: The settings dictionary.

    Raises:
        SettingsError: If the settings file is missing a section.
    """
    raw_settings = readINI(settings_filename)

    try:
        settings_dict = parseINI(raw_settings["BotSettings"])
    except KeyError as kerr:
        log.error(f"Settings file is missing section {kerr}")
        raise SettingsError(f"Settings file is missing section {kerr}") from kerr

    return settings_dict


def copy_config_from_sample_if_not_exists(filename):
    """
    Copies a sample configuration file to a new configuration file, only if the new file
    does not already exist.

    Args:
        filename (str): The name of the new configuration file.

    Returns:
        str: The path of the new configuration file.
    """
    filepath = pathlib.Path(filename)

    if not filepath.is_file():
        sample_file = f"{filename}.sample"
        samplepath = pathlib.Path(sample_file)
        if samplepath.is_file():
            shutil.copy(samplepath, filepath)

    return filepath.as_posix()