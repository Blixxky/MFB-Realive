"""
This module provides functions for interacting with the campfire screen in the game. The campfire screen is where completed tasks and rewards can be found.

Functions:
- toggle_campfire_screen: Toggle the campfire screen between party and visitor views.
- check_party_tasks: Check if there are completed tasks in the campfire party view and claim the rewards.
- check_visitor_tasks: Check if there are completed tasks in the campfire visitor view and claim the rewards.
- claim_task_reward: Claim the rewards for a completed task in the campfire.
- look_at_campfire_completed_tasks: Look at the campfire screen to find and claim rewards for completed tasks.

"""
import logging
import time

from modules.constants import UIElement, Button, Action
from modules.game import waitForItOrPass
from modules.image_utils import find_element
from modules.mouse_utils import move_mouse_and_click, move_mouse, mouse_click
from modules.platforms import windowMP

log = logging.getLogger(__name__)

# To do : add an option in settings.ini to take screenshots (boolean)
#           for rewards and completed tasks
# To do : add mouse position in positions.json


def toggle_campfire_screen():
    """
    Toggle the campfire screen between party and visitor views.
    Returns the view that is currently active ('party', 'visitor'), or None if neither view is active.
    """
    if find_element(Button.campfire_hiddenparty.filename, Action.move_and_click):
        time.sleep(2)
        return "party"

    if find_element(Button.campfire_hiddenvisitors.filename, Action.move_and_click):
        time.sleep(2)
        return "visitor"

    return None


def check_party_tasks():
    """
    Check if there are completed tasks in the campfire party view.
    If tasks are completed, claim the rewards and return True.
    If no tasks are completed, return False.
    """
    if find_element(Button.campfire_hiddenvisitors.filename, Action.screenshot):
        waitForItOrPass(Button.campfire_completed_partytask, 3)
        if find_element(
            Button.campfire_completed_partytask.filename, Action.move_and_click
        ):
            while not find_element(Button.campfire_claim.filename, Action.screenshot):
                time.sleep(0.5)
            return True
    return False


def check_visitor_tasks():
    """
    Check if there are completed tasks in the campfire visitor view.
    If tasks are completed, claim the rewards and return True.
    If no tasks are completed, return False.
    """
    if find_element(Button.campfire_hiddenparty.filename, Action.screenshot):
        waitForItOrPass(Button.campfire_completed_task, 3)
        if (
            find_element(Button.campfire_completed_task.filename, Action.move_and_click)
            or find_element(
                Button.campfire_completed_eventtask.filename, Action.move_and_click
            )
            or find_element(
                Button.campfire_completed_expansiontask.filename,
                Action.move_and_click,
            )
        ):
            return True
    return False


def claim_task_reward():
    """
    Claim the rewards for a completed task in the campfire.
    """
    while not find_element(Button.campfire_claim.filename, Action.screenshot):
        time.sleep(0.5)

    # Loop added beause sometimes the bot find the button but
    # Hearthstone is not ready, so the bot click too soon.
    # Need to make a loop to try several time to click
    while find_element(Button.campfire_claim.filename, Action.move_and_click):
        time.sleep(0.5)
        move_mouse(windowMP(), windowMP()[2] / 2, windowMP()[3] / 1.125)

    time.sleep(2)
    while not find_element(UIElement.campfire.filename, Action.screenshot):
        mouse_click()
        time.sleep(2)


def look_at_campfire_completed_tasks():
    """
    Once opened, look at campfire if you find completed tasks and,
    if so, open them.
    """

    retour = False
    if find_element(UIElement.campfire.filename, Action.screenshot):
        retour = True
        toggled = False
        while find_element(UIElement.campfire.filename, Action.move):
            if (
                find_element(Button.campfire_hiddenparty.filename, Action.screenshot)
                and check_visitor_tasks()
            ) or (
                find_element(Button.campfire_hiddenvisitors.filename, Action.screenshot)
                and check_party_tasks()
            ):
                claim_task_reward()

            if toggled:
                break

            toggle_campfire_screen()
            toggled = True

        move_mouse_and_click(windowMP(), windowMP()[2] / 1.16, windowMP()[3] / 1.93)

    return retour
