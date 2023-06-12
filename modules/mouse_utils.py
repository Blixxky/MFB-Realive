"""
This module provides functions for interacting with the mouse, including mouse clicks, scrolling, and mouse movement within a window.

Functions:
- mouse_click: Perform a mouse click.
- mouse_scroll: Perform a mouse scroll.
- mouse_position: Get the current mouse position relative to a given window.
- move_mouse_and_click: Move the mouse to specified coordinates within a window and perform a click.
- move_mouse: Move the mouse to specified coordinates within a window.
- mouse_random_movement: Generate a random mouse movement function.

Constants:
- MOUSE_RANGE: The range of random mouse movement.

Note: This module requires the 'pyautogui' library.
"""

import random
import time
import pyautogui

from modules.settings import settings_dict

MOUSE_RANGE = 2


def mouse_click(btn="left"):
    """
    Simulates a mouse click.

    Args:
        btn (str, optional): Specifies the button to click. Defaults to "left".
    """
    pyautogui.click(button=btn)


def mouse_scroll(s):
    """
    Simulates mouse scroll.

    Args:
        s (int): Specifies the amount and direction to scroll. Positive values scroll up, negative values scroll down.
    """
    if s == 0:
        return
    step = s // abs(s)
    for _ in range(0, s, step):
        pyautogui.scroll(step)


def mouse_position(window):
    """
    Retrieves the current mouse position relative to a window.

    Args:
        window (tuple): The (x, y) position of the window's top left corner.

    Returns:
        tuple: The current mouse position relative to the window's top left corner.
    """
    x, y = pyautogui.position()
    return (x - window[0], y - window[1])


def move_mouse_and_click(window, x, y):
    """
    Moves the mouse to a specified location relative to a window and simulates a click.

    Args:
        window (tuple): The (x, y) position of the window's top left corner.
        x (int): The x-coordinate for the mouse to move to, relative to the window.
        y (int): The y-coordinate for the mouse to move to, relative to the window.
    """
    move_mouse(window, x, y, with_random=True)
    time.sleep(0.1)
    pyautogui.click()


def move_mouse(window, x, y, with_random=False):
    """
    Moves the mouse to a specified location relative to a window, optionally with random offset.

    Args:
        window (tuple): The (x, y) position of the window's top left corner.
        x (int): The x-coordinate for the mouse to move to, relative to the window.
        y (int): The y-coordinate for the mouse to move to, relative to the window.
        with_random (bool, optional): If True, a random offset is added to the x and y coordinates. Defaults to False.
    """
    p = random.randint(-MOUSE_RANGE, MOUSE_RANGE) if with_random else 0
    s = random.randint(-MOUSE_RANGE, MOUSE_RANGE) if with_random else 0

    try:
        pyautogui.moveTo(
            window[0] + x + p,
            window[1] + y + s,
            settings_dict["mousespeed"],
            mouse_random_movement(),
        )
    except pyautogui.FailSafeException:
        pyautogui.alert(text="Do you want to resume ?", title="Paused", button="Yes")
        pyautogui.moveTo(
            window[0] + x + p,
            window[1] + y + s,
            settings_dict["mousespeed"],
            mouse_random_movement(),
        )


def mouse_random_movement():
    """
    Randomly selects a PyAutoGUI easing function to use for mouse movement.

    Returns:
        function: A PyAutoGUI easing function.
    """
    return random.choices(
        [pyautogui.easeInQuad, pyautogui.easeOutQuad, pyautogui.easeInOutQuad]
    )[0]
