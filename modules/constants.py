"""
Some filename enumeration, magic numbers
"""
from enum import Enum, auto


class StrEnum(str, Enum):
    """
    An enumeration class that inherits from `str` and `Enum`.
    """

    def __new__(cls, value, *args, **kwargs):
        """
        Create a new instance of the `StrEnum` class.

        Args:
            value (str): The string value of the enumeration.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            StrEnum: A new instance of the `StrEnum` class.

        Raises:
            TypeError: If the value is not a string or `auto`.
        """
        if not isinstance(value, (str, auto)):
            raise TypeError(
                f"Values of StrEnums must be strings: {value!r} is a {type(value)}"
            )
        return super().__new__(cls, value, *args, **kwargs)

    def __str__(self):
        """
        Return the string representation of the `StrEnum` instance.

        Returns:
            str: The string representation of the `StrEnum` instance.
        """
        return str(self.value)

    def _generate_next_value_(name, *_):
        """
        Generate the next value for the `StrEnum` enumeration.

        Args:
            name (str): The name of the enumeration value.
            *_: Variable length argument list.

        Returns:
            str: The next value for the `StrEnum` enumeration.
        """
        return name


class ImageFragment(StrEnum):
    """
    An enumeration of image fragments.
    """

    @property
    def filename(self):
        """
        Get the filename associated with the image fragment.

        Returns:
            str: The filename of the image fragment.
        """
        return f"{self._dir_name}/{self.value}.png"


class UIElement(ImageFragment):
    """
    An enumeration of UI elements.
    """

    game_closed = "closed_sign"
    closed_sign = "closed_sign"
    partywipe = "wipe_button"
    reconnect_button = "reconnect_button"
    _dir_name = "UI_elements"

    Alterac = "Alterac"
    Barrens = "Barrens"
    Bossrush = "Bossrush"
    Blackrock = "Blackrock"
    Darkshore = "Darkshore"
    Darkmoon = "Darkmoon"
    Felwood = "Felwood"
    Onyxia = "Onyxia"
    Sunken = "Sunken"
    Winterspring = "Winterspring"
    battle = "battle"
    battle_portal = "battle_portal"
    blue = "blue"
    encounter_booncaster = "encounter_booncaster"
    encounter_boonfighter = "encounter_boonfighter"
    encounter_boonprotector = "encounter_boonprotector"
    encounter_caster = "encounter_caster"
    encounter_fighter = "encounter_fighter"
    encounter_protector = "encounter_protector"
    encounter_elite = "encounter_elite"
    boss = "boss"
    bounties = "bounties"
    campfire = "campfire"
    encounter_card = "encounter_card"
    free_battle = "free_battle"
    green = "green"
    heroic = "heroic"
    hourglass = "hourglass"
    lose = "lose"
    mystery = "mystery"
    noclass = "noclass"
    noclass2 = "noclass2"
    normal = "normal"
    quests = "quests"
    red = "red"
    replace_grey = "take_grey"
    reward_chest = "reward_chest"
    sob = "sob"
    spirithealer = "spirithealer"
    take_grey = "take_grey"
    task_completed = "task_completed"
    task_event_completed = "task_event_completed"
    task_expansion_completed = "task_expansion_completed"
    team_selection = "team_selection"
    travelpoint = "travelpoint"
    treasure_passive = "treasure_passive"
    view_party = "view_party"
    win = "win"
    win_final = "win_final"
    your_party = "your_party"


class Button(ImageFragment):
    """
    An enumeration of buttons.
    """

    _dir_name = "buttons"
    allready = "allready"
    arrow_prev = "arrow_prev"
    arrow_next = "arrow_next"
    back = "back"
    campfire_claim = "campfire_claim"
    campfire_completed_task = "campfire_completed_task"
    campfire_completed_eventtask = "campfire_completed_event-task"
    campfire_completed_partytask = "campfire_completed_party-task"
    campfire_completed_expansiontask = "campfire_completed_expansion-task"
    campfire_hiddenparty = "campfire_hidden-party"
    campfire_hiddenvisitors = "campfire_hidden-visitors"
    choose_level = "choose_level"
    choose_team = "choose_team"
    choose_travel = "choose_travel"
    done = "done"
    done_bonus = "done_bonus"
    fight = "fight"
    finishok = "finishok"
    group_name = "group_name"
    join_button = "join_button"
    keep = "take"
    lockin = "lockin"
    num = "num"
    ok = "ok"
    onedie = "num"
    pick = "pick"
    play = "play"
    portal_warp = "portal_warp"
    reconnect = "reconnect"
    replace = "take"
    retire = "retire"
    reveal = "reveal"
    take = "take"
    tavern = "tavern"
    view_party = "view_party"
    visit = "visit"
    battlenet_play = "battlenet_play"
    battlenet = "battlenet"
    battlenet_hearthstone = "battlenet_hearthstone"
    choose_mode = "choose_mode"


class Action(StrEnum):
    """
    An enumeration of actions.
    """

    screenshot = "1"
    move = "2"
    get_coords_part_screen = "12"
    move_and_click = "14"
    get_coords = "15"
