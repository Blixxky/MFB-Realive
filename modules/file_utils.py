import os
import json
import configparser
import re
import logging
from modules.exceptions import SettingsError

log = logging.getLogger(__name__)


def readjson(jfile):
    """Reads a JSON file and returns the data."""
    with open(jfile) as descriptor:
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

    with open(file, "w") as configfile:
        config.write(configfile)


def copy_dir_and_func_files(srcdir, dstdir, ext, func, func_params):
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
