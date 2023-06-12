"""
This module provides utility functions for reading, writing, and parsing configuration files in
both JSON and INI formats. It also supports copying directory files based on specified criteria
and performing a user-defined function on them.

Main Features:
    - Read and Write operations for JSON and INI files.
    - Type parsing for INI file contents.
    - Directory operations including copying and function execution on specific files.

Imported Modules:
    - os: Provides a portable way of using operating system dependent functionality.
    - json: Used for JSON file operations.
    - configparser: Provides the functionality to read and write data in INI format.
    - re: Provides regular expression matching operations.
    - logging: Provides a flexible framework for emitting log messages from Python programs.
    - modules.exceptions: Contains custom exceptions used in the program.

Functions:
    - readjson(): Reads a JSON file and returns the data.
    - read_ini_to_dict(): Reads an INI file and returns the parsed dictionary.
    - parseINI(): Transforms values into the appropriate type based on the input dictionary from an INI file.
    - readINI(): Reads an INI file and returns the data.
    - writeINI(): Writes new settings into an INI file and returns the status of the operation.
    - copy_dir_and_func_files(): Copies directory files based on specified criteria
      and performs a user-defined function on them.
"""

import os
import json
import configparser
import re
import logging
from modules.exceptions import SettingsError

log = logging.getLogger(__name__)


def readjson(jfile):
    """Reads a JSON file and returns the data."""
    with open(jfile, encoding='utf-8') as descriptor:
        data = json.load(descriptor)
    return data


def read_ini_to_dict(inifile):
    """Reads an INI file and returns the parsed dictionary."""
    log.debug("Reading %s", inifile)
    return parseINI(readINI(inifile))


def parseINI(inidict):
    """Transforms values into the appropriate type based on the input dictionary from an INI file."""
    initype = {}
    for k in inidict.keys():
        i = inidict[k].split("#")[0]
        if i in ["True", "False"]:
            initype[k] = i == "True"
        elif re.match("^[0-9]+$", i):
            initype[k] = int(i)
        elif re.match("^[0-9]+\.[0-9]+$", i):
            initype[k] = float(i)
        else:
            initype[k] = str(i)

    return initype


def readINI(inifile):
    """Reads an INI file and returns the data."""
    config = configparser.ConfigParser()
    try:
        config.read(inifile)
    except configparser.DuplicateOptionError as err:
        log.error("Error while reading ini file %s", err)
        raise SettingsError(f"Duplicate Option in Settings File: {err}") from err

    return config._sections


def writeINI(file, data):
    """Writes new settings into an INI file and returns the status of the operation."""
    config = configparser.ConfigParser()

    for section in data:
        config.add_section(section)
        for key in data[section]:
            config.set(section, key, str(data[section][key]))

    with open(file, "w", encoding='utf-8') as configfile:
        config.write(configfile)


def copy_dir_and_func_files(srcdir, dstdir, ext, func, func_params):
    """
        Recursively copies files from the source directory to the destination directory based on the specified extension.
        For each file copied, a specified function is applied with the provided function parameters.

        Args:
            srcdir (str): The source directory from which to copy files.
            dstdir (str): The destination directory to which the files should be copied.
            ext (str): The file extension to filter files for copying.
            func (callable): The function to be applied to each copied file.
            func_params (tuple, optional): Additional parameters to be passed to the function.

        Returns:
            None

        Notes:
            - If the destination directory does not exist, it will be created.
            - The function recursively copies files from the source directory and its subdirectories.
            - Only files with the specified extension will be copied.
            - The specified function will be applied to each copied file with the provided function parameters.
            - The `func_params` argument is an optional tuple of additional parameters to be passed to the function.
    """
    os.path.exists(dstdir) or os.mkdir(dstdir)

    for name in os.listdir(srcdir):
        if os.path.isdir(f"{srcdir}/{name}"):
            print(f"Processing directory: {dstdir}/{name}... wait")
            copy_dir_and_func_files(
                f"{srcdir}/{name}", f"{dstdir}/{name}", ext, func, func_params
            )
        else:
            extfile = f"{srcdir}/{name}"
            if extfile.endswith(ext):
                func(extfile, f"{dstdir}/{name}", func_params)