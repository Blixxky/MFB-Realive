"""
This module provides functions for managing configuration files and settings.

Functions:
- set_settings(new_settings_data): Update the settings with new data.
- initusersettings(): Initialize the user settings file.
- get_config(base_config_folder, user_folder, system_folder, conf_setting_files):
  Retrieve the configuration settings from the files.
- update_settings_with_file(setting_data, new_file): Update the setting data with the contents of a file.
- log_setting_dict(setting_name, setting_dict): Log the setting dictionary.
- log_setting_dict_helper(setting_name, setting_dict, indent): Helper function for logging setting dictionaries.
"""
import os
import shutil
import logging

from modules.file_utils import readjson, readINI, writeINI
from modules.utils import update
from modules.exceptions import MissingSettingsFile

from .settings import get_system_user_settings

log = logging.getLogger(__name__)


BASE_CONFIG_FOLDER = "conf"
USER_CONFIG_FOLDER = "user"
SYSTEM_CONFIG_FOLDER = "system"

config_files = [
    "attacks.json",
    "combo.ini",
    "mercs.json",
    "settings.ini",
    "positions.json",
    "thresholds.json",
    "treasures.json",
]


def set_settings(new_settings_data):
    """
    Updates the user's settings file with new data. If there's no existing settings file,
    creates one and populates it with the new data.

    Args:
        new_settings_data (dict): A dictionary containing new settings data to be saved.
    """
    user_settings_file = os.path.join(
        BASE_CONFIG_FOLDER, USER_CONFIG_FOLDER, "settings.ini"
    )
    user_data = update_settings_with_file({}, user_settings_file)

    new_settings_data = {"BotSettings": new_settings_data}
    new_data = update(user_data, new_settings_data)

    writeINI(user_settings_file, new_data)


def initusersettings():
    """
    Initializes user's settings. If the user's settings file doesn't exist, it checks for
    incorrectly named settings files and renames them. If no such files exist, it copies
    the contents of the sample settings file into a new settings file.
    """
    user_settings_file = os.path.join(
        BASE_CONFIG_FOLDER, USER_CONFIG_FOLDER, "settings.ini"
    )
    sample_settings_file = os.path.join(
        BASE_CONFIG_FOLDER, USER_CONFIG_FOLDER, "settings.sample.ini"
    )
    bad_settings_file = os.path.join(
        BASE_CONFIG_FOLDER, USER_CONFIG_FOLDER, "settings.ini.ini"
    )

    if not os.path.isfile(user_settings_file):
        if os.path.isfile(bad_settings_file):
            os.rename(bad_settings_file, user_settings_file)
            log.info(
                "Bad settings filename '%s' renamed into %s",
                bad_settings_file,
                user_settings_file,
            )
        elif os.path.isfile(sample_settings_file):
            shutil.copy(sample_settings_file, user_settings_file)
            log.info(
                "No settings file found: %s copied into %s. Set your settings.",
                sample_settings_file,
                user_settings_file,
            )


def get_config(
    base_config_folder=BASE_CONFIG_FOLDER,
    user_folder=USER_CONFIG_FOLDER,
    system_folder=SYSTEM_CONFIG_FOLDER,
    conf_setting_files=config_files,
):
    """
    Retrieves and returns the configuration settings from all the relevant files in
    both the user and system config folders. Logs a message if no user settings are found.

    Args:
        base_config_folder (str): The base directory containing the configuration folders.
            Default is BASE_CONFIG_FOLDER.
        user_folder (str): The name of the user's configuration folder.
            Default is USER_CONFIG_FOLDER.
        system_folder (str): The name of the system's configuration folder.
            Default is SYSTEM_CONFIG_FOLDER.
        conf_setting_files (list): The list of configuration file names.
            Default is config_files.

    Returns:
        dict: A dictionary containing all the configuration settings.
    """
    root_settings_dict = {}

    for setting in conf_setting_files:
        setting_data = {}

        settings_file = os.path.join(base_config_folder, system_folder, setting)
        setting_data = update_settings_with_file(setting_data, settings_file)

        try:
            user_settings_file = os.path.join(base_config_folder, user_folder, setting)
            setting_data = update_settings_with_file(setting_data, user_settings_file)
        except MissingSettingsFile:
            log.debug("No User Settings found for: %s", setting)

        if not setting_data:
            log.info("No Settings found for: %s", setting)

        root_settings_dict[setting] = setting_data

        if setting in ["combo.ini"]:
            log_setting_dict(setting, setting_data)

    system_settings_file = os.path.join(
        base_config_folder, system_folder, "settings.ini"
    )
    user_settings_file = os.path.join(base_config_folder, user_folder, "settings.ini")
    root_settings_dict["settings.ini"] = get_system_user_settings(
        system_settings_file, user_settings_file
    )

    return root_settings_dict


def update_settings_with_file(setting_data, new_file):
    """
    Updates the settings data with data from a new settings file.

    Args:
        setting_data (dict): The current settings data.
        new_file (str): The path of the new settings file.

    Returns:
        dict: The updated settings data.

    Raises:
        MissingSettingsFile: If the new settings file does not exist.
    """
    if not os.path.exists(new_file):
        raise MissingSettingsFile(f"Settings file: {new_file} not found")

    new_setting_data = readjson(new_file) if new_file[-1] == "n" else readINI(new_file)

    return update(setting_data, new_setting_data)


def log_setting_dict(setting_name, setting_dict):
    """
    Logs the contents of a settings dictionary. It is a wrapper function to
    log_setting_dict_helper() function and starts the recursive logging process.

    Args:
        setting_name (str): The name of the settings file or dictionary.
        setting_dict (dict): The dictionary containing settings data to log.
    """
    log.debug("%s", setting_name)
    log_setting_dict_helper(setting_dict)


def log_setting_dict_helper(setting_dict, indent=""):
    """
    Recursively logs the contents of a settings dictionary. This function is used
    by log_setting_dict() to handle the nested dictionary structure.

    Args:
        setting_dict (dict): The dictionary containing settings data to log.
        indent (str): A string of whitespace used to indent nested dictionary entries.
            Default is an empty string.
    """
    for setting, value in setting_dict.items():
        if isinstance(value, dict):
            log_setting_dict_helper(value, indent * 4)
        else:
            log.debug(" - %s: %s", setting, value)
