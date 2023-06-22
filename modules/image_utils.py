"""
This module provides functions for image processing and finding elements on the screen.

Functions:
- get_resolution: Get the resolution of the screen.
- resize: Resize an image.
- get_gray_image: Load an OpenCV version of an image in memory and/or return it.
- find_element: Find an object on the screen and perform actions.
- find_element_from_file: Find element center from a template file.
- part_screen: Take a screenshot for a part of the screen.
- find_element_center_on_screen: Find element center on the screen.
"""


import logging
import os.path
import sys
import cv2
import mss
import numpy as np

from modules.constants import Action
from modules.mouse_utils import move_mouse, move_mouse_and_click
from modules.platforms import windowMP
from modules.settings import jthreshold, settings_dict


sct = mss.mss()
# workaround end

"""
mss is needed as workaround for Linux
    https://stackoverflow.com/questions/74856512/screenshot-error-xdefaultrootwindow-failed-after-closing-a-tkinter-toplevel
    https://github.com/BoboTiG/python-mss/issues/220
"""

log = logging.getLogger(__name__)


class ResolutionError(Exception):
    """Exception raised for resolution-related errors."""


class AspectRatioError(ResolutionError):
    """Exception raised when the aspect ratio of the setting resolution and window resolution are different."""


def get_resolution() -> tuple[str, int, int, float]:
    """
    Fetches the screen resolution details.

    Returns:
    tuple: A tuple containing screen resolution (resolution, width, height, scale_size).
    Raises exception if the setting resolution and windows resolution are not of the same aspect ratio.
    """
    try:
        resolution = settings_dict["resolution"]
        setting_size = resolution.split("x")
        setting_w, setting_h = int(setting_size[0]), int(setting_size[1])
        windows_w, windows_h = windowMP()[2], windowMP()[3]
        if round(windows_w / setting_w, 2) != round(windows_h / setting_h, 2):
            raise AspectRatioError(
                "Setting resolution and windows resolution have different aspect ratios"
            )

        scale_size = setting_w / windows_w
        return resolution, setting_w, setting_h, scale_size
    except KeyError as e:
        log.error("Resolution setting not found in settings_dict: %s", e)
        sys.exit(1)
    except (IndexError, ValueError) as e:
        log.error("Invalid resolution format: %s", e)
        sys.exit(1)
    except AspectRatioError as e:
        log.error(
            "Setting resolution and windows resolution have different aspect ratios: %s",
            e,
        )
        sys.exit(1)
    except Exception as e:
        log.error("An unexpected error occurred: %s", e)
        sys.exit(1)


def resize(img, width, height):
    """
    Resizes an image.

    Args:
    img (numpy.ndarray): The image to resize.
    width (int): The width to resize to.
    height (int): The height to resize to.

    Returns:
    numpy.ndarray: The resized image.
    """

    return cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)


def get_gray_image(file):
    """
    Loads a grayscale OpenCV version of an image in memory or returns it if it's already in memory.

    Args:
    file (str): The file path of the image.

    Returns:
    numpy.ndarray: The grayscale image.
    """

    if not hasattr(get_gray_image, "imagesInMemory"):
        get_gray_image.imagesInMemory = {}

    # To Do : to resize the image so we can support other resolutions
    # screenshots was made on a 1920x1080 screen resolution
    # but with Hearthstone in windowed mode so it's like : 1920x1040
    # need to resize the image in memory
    if file not in get_gray_image.imagesInMemory:
        if not os.path.isfile(file):
            log.error('Err: file "%s" doesn\'t exist.', file)
        get_gray_image.imagesInMemory[file] = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        log.debug("images in memory : %s", len(get_gray_image.imagesInMemory))
    return get_gray_image.imagesInMemory[file]


def find_element(file, action, threshold="-", new_screen=True):
    """Find an object ('file') on the screen (UI, Button, ...)
        and do some actions ('action')
                Screenshot Here  |    Screenshot Before  |  Actions   | Return
    action = 1 :       x         |                       |     -      | True / False
    action = 2 :       x         |                       |    move    | True / False
    action = 14:       x         |                       | move+click | True / False
    action = 12:                 |           x           |     -      |  x,y / 0,0
    action = 15:       x         |                       |     -      |  x,y / 0,0
      (new action needed to return a tab of object/coordinates)
    """
    click_coords = find_element_from_file(
        file,
        new_screenshot=new_screen,
        threshold=threshold,
    )
    if click_coords is not None:
        x, y = click_coords
        if action in [
            Action.get_coords_part_screen,
            Action.get_coords,
            Action.screenshot,
        ]:
            return click_coords
        if action == Action.move:
            window = windowMP()
            move_mouse(window, x, y)
            return True
        if action == Action.move_and_click:
            # move mouse and click
            window = windowMP()
            move_mouse_and_click(window, x, y)
            return True
    if action in [Action.get_coords_part_screen, Action.get_coords]:
        return None
    return False


def find_element_from_file(
    file,
    new_screenshot=True,
    threshold="-",
):
    """
    Finds an element in the screen from a template file.

    Args:
        file (str): The file path of the template.
        new_screenshot (bool): Whether to take a new screenshot for matching. Defaults to True.
        threshold (str): The threshold for template matching. Defaults to '-'.

    Returns:
        tuple or None: The coordinates of the center of the element found or None if not found.
    """

    if threshold == "-":
        if file in jthreshold and jthreshold[file] != "-":
            threshold = jthreshold[file]
        else:
            threshold = jthreshold["default_grey"]

    resolution, width, height, scale_size = get_resolution()

    # choose if the bot need to look into the window or in a part of the window
    if new_screenshot is True:
        top = 0
        left = 0
        find_element_from_file.partImg = partscreen(
            windowMP()[2],
            windowMP()[3],
            windowMP()[1],
            windowMP()[0],
            resize_width=width,
            resize_height=height,
        )
    else:
        top = new_screenshot[2] - windowMP()[1]
        left = new_screenshot[3] - windowMP()[0]
        find_element_from_file.partImg = partscreen(
            new_screenshot[0],
            new_screenshot[1],
            new_screenshot[2],
            new_screenshot[3],
            scale_size=scale_size,
        )

    img = cv2.cvtColor(find_element_from_file.partImg, cv2.COLOR_BGR2GRAY)

    template = get_gray_image(f"files/{resolution}/{file}")

    click_coords = find_element_center_on_screen(img, template, threshold, scale_size)

    if click_coords is not None:
        click_coords = [click_coords[0] + left, click_coords[1] + top]
        log.info(
            "Found %s ( %s ) %s %s", file, threshold, click_coords[0], click_coords[1]
        )

    else:
        print("Waiting for... %s\033[K" % file, end="\r")
        log.debug("Looked for %s ( %s )", file, threshold)

    return click_coords


def partscreen(
    x,
    y,
    top,
    left,
    debug_mode=False,
    resize_width=None,
    resize_height=None,
    scale_size=1,
):
    """
    Takes a screenshot of a part of the screen.

    Args:
    x (int): The width of the part.
    y (int): The height of the part.
    top (int): The top position of the part.
    left (int): The left position of the part.
    debug_mode (bool): Whether to save the screenshot for debugging. Defaults to False.
    resolution (str): The resolution setting. Defaults to None.
    resize_width (int): The width to resize to. Defaults to None.
    resize_height (int): The height to resize to. Defaults to None.
    scale_size (float): The scaling factor for resizing. Defaults to 1.

    Returns:
    numpy.ndarray: The screenshot image.
    """

    # workaround for Linux  (read more info at the top of this file)
    # with mss.mss() as sct:
    global sct
    monitor = {"top": top, "left": left, "width": x, "height": y}
    sct_img = sct.grab(monitor)

    if debug_mode:
        output_file = "files/debug.png"
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_file)

    partImg = np.array(sct_img)

    if resize_width and resize_height:
        partImg = cv2.resize(
            partImg, (resize_width, resize_height), interpolation=cv2.INTER_CUBIC
        )
    elif scale_size != 1:
        partImg = cv2.resize(
            partImg,
            (int(x * scale_size), int(y * scale_size)),
            interpolation=cv2.INTER_CUBIC,
        )

    return partImg


def find_element_center_on_screen(img, template, threshold=0, scale_size=1):
    """
    Finds the center of an element on the screen.

    Args:
    img (numpy.ndarray): The image of the screen.
    template (numpy.ndarray): The image of the element to find.
    threshold (float): The threshold for template matching. Defaults to 0.
    scale_size (float): The scaling factor for resizing. Defaults to 1.

    Returns:
    tuple or None: The coordinates of the center of the element found or None if not found.
    """

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    h = template.shape[0] // 2
    w = template.shape[1] // 2
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    return (
        ((max_loc[0] + w) / scale_size, (max_loc[1] + h) / scale_size)
        if max_val > threshold
        else None
    )
