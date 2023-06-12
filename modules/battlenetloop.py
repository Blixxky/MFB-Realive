"""
This module contains functions related to entering the game from Battle.net.
"""

import logging
import time
from modules.constants import Button, Action
from modules.image_utils import find_element


log = logging.getLogger(__name__)


def enter_from_battlenet():
    """
    Enters the game from the Battle.net application.
    """
    found_element = find_element(Button.battlenet.filename, Action.move_and_click)
    if found_element:
        time.sleep(1)

    found_element = find_element(
        Button.battlenet_hearthstone.filename, Action.move_and_click
    )
    if found_element:
        time.sleep(1)

    if find_element(Button.battlenet_play.filename, Action.move_and_click):
        log.info("Waiting (20s) for game to start")
        time.sleep(20)

    else:
        log.info("Wait for play button to be available")
        time.sleep(3)

    return True
