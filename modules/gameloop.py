"""
This module contains the main logic for navigating the Mercenaries mode in Hearthstone.
It provides functions to detect the current state of the game and progress through the various stages of gameplay.
"""

import logging
import sys
import time


from modules.bounty import selectGroup, travelToLevel, goToEncounter
from modules.travelpoint import travelpointSelection
from modules.constants import UIElement, Button, Action
from modules.image_utils import find_element
from modules.game import defaultCase
from modules.campfire import look_at_campfire_completed_tasks
from modules.settings import jposition
from modules.mouse_utils import move_mouse
from modules.platforms import windowMP
from modules.resolution import check_resolution
from modules.reconnects import click_wipe_button, click_reconnect, choose_mode

log = logging.getLogger(__name__)


def where():
    """Try to enter in Mercenaries mode,
    detect where the bot have to resume and go for it"""

    # Check Hearthstone resolution and compare it to settings resolution
    _, _, width, height = windowMP()
    win_game_resolution = f"{width}x{height}"
    if not check_resolution(win_game_resolution):
        log.error(
            "Game window size (%s) doesn't match your settings.", win_game_resolution
        )
        sys.exit()

    find_element(Button.join_button.filename, Action.move_and_click)

    if find_element(Button.choose_mode.filename, Action.screenshot):
        choose_mode()


    # Find PVE adventure paid, free or portal
    if (
        find_element(UIElement.battle_portal.filename, Action.move_and_click)
        or find_element(UIElement.battle.filename, Action.move_and_click)
        or find_element(UIElement.free_battle.filename, Action.move_and_click)
    ):
        mx = jposition["mouse.neutral.x"]
        my = jposition["mouse.neutral.y"]
        move_mouse(windowMP(), windowMP()[2] / mx, windowMP()[3] / my)

    if find_element(UIElement.travelpoint.filename, Action.screenshot):
        # Find the travel point and the mode (normal/heroic)
        travelpointSelection()

    if find_element(UIElement.bounties.filename, Action.screenshot):
        travelToLevel()
        time.sleep(1)

    if find_element(UIElement.team_selection.filename, Action.screenshot):
        selectGroup()
        time.sleep(1)

    if find_element(UIElement.view_party.filename, Action.screenshot):
        goToEncounter()

    if find_element(UIElement.campfire.filename, Action.screenshot):
        look_at_campfire_completed_tasks()

    if find_element(UIElement.partywipe.filename, Action.screenshot):
        click_wipe_button()

    if find_element(UIElement.reconnect_button.filename, Action.screenshot):
        click_reconnect()

    if find_element(UIElement.game_closed.filename, Action.screenshot):
        game_closed()

    else:
        defaultCase()

    return True
