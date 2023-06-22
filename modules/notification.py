"""
This module provides functions for sending notifications to webhook URLs.

Functions:
- send_notification: Send a notification message to a webhook URL from the 'notificationURL' config.
- send_slack_notification: Send a notification message to a Slack webhook URL from the 'slacknotificationurl' config.

Note: This module requires the 'urllib' library.

Constants:
- settings_dict: A dictionary containing settings.

Dependencies:
- logging: The standard Python logging module.
"""

import logging
from urllib import request, parse, error

from .settings import settings_dict


log = logging.getLogger(__name__)


def send_notification(message: dict):
    """
    Send a notification message to a webhook URL.

    Args:
        message (dict): The message to send as a dictionary.

    Raises:
        error.HTTPError: If there is an HTTP error.
        error.URLError: If there is a URL error.
        Exception: For any other unexpected error.
    """
    if "notificationurl" not in settings_dict or not settings_dict["notificationurl"]:
        return

    url = settings_dict["notificationurl"]
    try:
        data = parse.urlencode(message).encode()
        req = request.Request(url, data, method="POST")
        with request.urlopen(req) as response:
            # Handle response if needed
            pass

        log.info("Notification sent: %s", message)
    except error.HTTPError as e:
        log.error("Notification HTTP error: %s", e.code)
        raise
    except error.URLError as e:
        log.error("Notification URL error: %s", e.reason)
        raise
    except Exception as e:
        log.error("Unexpected notification error: %s", e)
        raise


def send_slack_notification(message):
    """
    Send a notification message to a Slack webhook URL.

    Args:
        message (str): The message to send.

    Raises:
        error.HTTPError: If there is an HTTP error.
        error.URLError: If there is a URL error.
    """
    if (
        "slacknotificationurl" not in settings_dict
        or not settings_dict["slacknotificationurl"]
    ):
        return

    url = settings_dict["slacknotificationurl"]
    headers = {"content-type": "application/json --data"}

    try:
        data = bytes(message, "utf-8")
        req = request.Request(url, data, headers=headers, method="POST")
        with request.urlopen(req) as response:
            # Handle response if needed
            pass

        log.info("Notification sent: %s", message)
    except error.HTTPError as e:
        log.error("Notification HTTP error: %s", e.code)
        raise
    except error.URLError as e:
        log.error("Notification URL error: %s", e.reason)
        raise
    except Exception as e:
        log.error("Unexpected notification error: %s", e)
        raise
