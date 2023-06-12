"""
Initialization script, handles logging, settings, and certain out strings.
"""
import configparser
import logging.config

log_config = {
    "version": 1,
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "handlers": {
        "console": {
            "formatter": "old_out",
            "class": "logging.StreamHandler",
            "level": "INFO",
        },
        "file": {
            "formatter": "std_out",
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "filename": "mfb.log",
            "mode": "w",
            "delay": True,
        },
    },
    "formatters": {
        "std_out": {
            "format": "%(asctime)s [%(levelname)-8s] %(module)s : %(message)s",
            "datefmt": "%d-%m-%Y %I:%M:%S",
        },
        "old_out": {"format": "%(message)s"},
    },
}

_usersetting = "conf/user/settings.ini"
_systsetting = "conf/system/settings.ini"
filelogs = False
_config = configparser.ConfigParser()
try:
    _config.read(_systsetting)
    if _config.has_section("BotSettings") and _config.has_option("BotSettings", "logs"):
        if _config.getboolean("BotSettings", "logs"):
            filelogs = True
except Exception:
    pass

try:
    _config.read(_usersetting)
    if _config.has_section("BotSettings") and _config.has_option("BotSettings", "logs"):
        if _config.getboolean("BotSettings", "logs"):
            filelogs = True
        else:
            filelogs = False
except Exception:
    pass


print(f"Logs: {filelogs}")
if filelogs:
    log_config["root"]["handlers"].append("file")
logging.config.dictConfig(log_config)
