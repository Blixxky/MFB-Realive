import time
from .constants import Button, Action
from .image_utils import find_element
import logging


log = logging.getLogger(__name__)


def enter_from_battlenet():
    find_element(Button.battlenet.filename, Action.move_and_click) and time.sleep(1)

    find_element(
        Button.battlenet_hearthstone.filename, Action.move_and_click
    ) and time.sleep(1)

    if find_element(Button.battlenet_play.filename, Action.move_and_click):
        log.info("Waiting (20s) for game to start")
        time.sleep(20)

    else:
        log.info("Wait for play button to be available")
        time.sleep(3)

    return True
