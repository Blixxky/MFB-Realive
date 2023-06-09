"""
This module provides functions for handling travel points in the game.

Functions:
- get_travelpoints_list: Get the list of available travel points.
- travelpoint_selection: Choose a travel point and mode.

Note: This module requires the 'time' and 're' libraries.
"""

import time
import re

from .platforms import windowMP
from .mouse_utils import (
    move_mouse,
    mouse_scroll,
)

from .constants import UIElement, Button, Action
from .image_utils import find_element
from .game import waitForItOrPass
from .settings import settings_dict, jposition, jthreshold

import logging

log = logging.getLogger(__name__)


def get_travelpoints_list():
    """
    Get the list of available travel points.

    Returns:
        list: List of travel points.
    """
    tp_list = []
    for key in jposition:
        if re.search(r"travelpoint\..+\.scroll", key):
            tp_list.append(key.split(".")[1])

    return tp_list


def travelpointSelection():
    """
    Choose a travel point and mode.
    """

    if find_element(UIElement.travelpoint.filename, Action.screenshot):
        move_mouse(windowMP(), windowMP()[2] // 1.5, windowMP()[3] // 2)

        mouse_scroll(jposition["travelpoint.scroll.top"])
        time.sleep(0.5)

        location = settings_dict["location"]
        tag = f"travelpoint.{location}.scroll"
        if location == "Barrens":
            find_element(
                UIElement.Barrens.filename,
                Action.move_and_click,
                jthreshold["travelpoints"],
            )

        else:
            try:
                mouse_scroll(jposition[tag])
                move_mouse(windowMP(), windowMP()[2] // 3, windowMP()[3] // 2)
                time.sleep(0.5)
                find_element(
                    getattr(UIElement, location).filename,
                    Action.move_and_click,
                    jthreshold["travelpoints"],
                )
            except Exception:
                log.error("Travel Point unknown : %s", location)

        move_mouse(windowMP(), windowMP()[2] // 2, windowMP()[3] // 2)
        time.sleep(0.5)

        if settings_dict["mode"] == "Normal":
            find_element(UIElement.normal.filename, Action.move_and_click)
        elif settings_dict["mode"] == "Heroic":
            find_element(UIElement.heroic.filename, Action.move_and_click)
        else:
            log.error("Settings (for Heroic/Normal) unrecognized.")

    waitForItOrPass(Button.choose_travel, 2)
    find_element(Button.choose_travel.filename, Action.move_and_click)
