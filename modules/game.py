"""
This module contains functions related to controlling and interacting with the Hearthstone game window. It provides various utilities for automating actions in the game, such as finding elements on the screen, clicking on specific positions, waiting for specific elements to appear, and handling common scenarios.
Note: This module assumes the presence of relevant image files, configuration settings, and external dependencies as specified in the associated modules and configurations.
"""

import logging
import sys
import time

from modules.image_utils import find_element
from modules.constants import Action, UIElement, Button
from modules.settings import jposition
from modules.mouse_utils import move_mouse, move_mouse_and_click, mouse_position
from modules.platforms import windowMP


log = logging.getLogger(__name__)


def countdown(t, step=1, msg="Sleeping"):
    """Wait and show how many seconds til the end"""
    pad_str = " " * len(f"{step}")
    for i in range(t, 0, -step):
        sys.stdout.write(f"{msg} for the next {i} seconds {pad_str}\r")
        time.sleep(step)


def waitForItOrPass(image, duration, step=0.5):
    """
    Wait to find 'image' on screen during 'duration' seconds (max)
    and continue if you don't find it.
    The purpose is to permit to find a particular part in Hearthstone
    but if the bot doesn't find it, try to go further
    if you can find another part that it could recognize
    """
    retour = False

    log.info("Waiting (%ss max) for : %s", str(duration), image)
    for _ in range(int(duration / step)):
        time.sleep(step)
        # time.sleep(0.5)
        if find_element(image.filename, Action.screenshot):
            retour = True
            break

    return retour


def defaultCase():
    """
    Click on the right edge of the screen to dismiss popups
    Saving x,y to move back into previous position
    """
    if find_element(UIElement.quests.filename, Action.screenshot) or find_element(
        UIElement.encounter_card.filename, Action.screenshot
    ):
        x, y = mouse_position(windowMP())
        log.info("Trying to skip quests screen.")
        mx = jposition["mouse.neutral.x"]
        my = jposition["mouse.neutral.y"]
        move_mouse_and_click(windowMP(), windowMP()[2] / mx, windowMP()[3] / my)
        move_mouse(windowMP(), x, y)
    elif find_element(Button.reconnect.filename, Action.move_and_click):
        # Handle the disconnect case
        log.info("Game disconnected")
    # To Do: Is "else" needed to skip other screens ?
    # To Do: need to add a 'find_element' on the "Closed HS" screen
