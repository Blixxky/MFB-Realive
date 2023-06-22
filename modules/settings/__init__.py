"""Settings module

Fetches all settings from settings files used by app
"""
from modules.settings.conf import (
    jthreshold,
    jposition,
    mercslist,
    mercsAbilities,
    ability_order,
    settings_dict,
    treasures_priority,
)


__all__ = [
    "jthreshold",
    "jposition",
    "mercslist",
    "mercsAbilities",
    "ability_order",
    "settings_dict",
    "treasures_priority",
]
