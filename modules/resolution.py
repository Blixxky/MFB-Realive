"""
This module provides image-related functions for resizing and generating images based on settings.

Functions:
- resize_image: Resize an image from source to destination.
- check_resolution: Check if the window resolution matches the settings resolution.
- gen_images_new_resolution: Generate images for the new resolution.

Note: This module requires the 'cv2' and 'os' libraries.
"""

import logging
import os
import cv2
from modules.file_utils import copy_dir_and_func_files
from modules.settings import settings_dict


log = logging.getLogger(__name__)

BASEDIR = settings_dict["root_images_dir"]
orig_resolution = settings_dict["default_resolution"]


def resize_image(srcfile, dstfile, params=[]):
    """
    Resize an image from source to destination.

    Args:
        srcfile (str): Path to the source image file.
        dstfile (str): Path to the destination image file.
        params (list, optional): List of parameters. Defaults to None.
    """
    orig_resolution_w = int(params[0].split("x")[0])
    new_resolution_w = int(params[1].split("x")[0])

    img = cv2.imread(srcfile, cv2.IMREAD_UNCHANGED)
    scale_ratio = new_resolution_w / orig_resolution_w
    width = int(img.shape[1] * scale_ratio)
    height = int(img.shape[0] * scale_ratio)

    # print(f"resize: {srcfile} -> {dstfile}")

    # INTER_AREA INTER_CUBIC INTER_LANCZOS4 INTER_LINEAR INTER_NEAREST
    imgresized = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(dstfile, imgresized)


def check_resolution(window):
    """
    Check if the window resolution matches the settings resolution.
    """

    # retour=False
    # margin_error=0.1
    # windowx, windowy = window.split("x")
    # settingx, setting = setting.split("x")

    return window == settings_dict["resolution"]


def gen_images_new_resolution():
    """
    It appears that this function resizes the base images to scale to new resolutions.
    """
    new_resolution = settings_dict["resolution"]

    ox, oy = orig_resolution.split("x")
    nx, ny = new_resolution.split("x")

    if orig_resolution == new_resolution:
        log.debug("Resolution not changed : %s", orig_resolution)
    else:
        # test if directory already exists so we don't generate images file
        if (
            not os.path.isdir(f"{BASEDIR}/{new_resolution}")
            or settings_dict["gen_img_res_at_each_startup"]
        ):
            # Resolution modified so we need to generate images
            # we check it's the same ratio as the original images
            if round(int(ox) / int(oy), 2) == round(int(nx) / int(ny), 2):
                copy_dir_and_func_files(
                    f"{BASEDIR}/{orig_resolution}",
                    f"{BASEDIR}/{new_resolution}",
                    ".png",
                    resize_image,
                    [orig_resolution, new_resolution],
                )
            else:
                log.error(
                    "Resolution doesn't have the same ratio as %s", orig_resolution
                )
