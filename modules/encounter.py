"""
This module targets enemies and uses abilities during encounters.
"""

import logging
import random
import re
import time
from typing import List
from collections import namedtuple

from .constants import Action, Button, UIElement
from .game import countdown, waitForItOrPass
from .image_utils import find_element
from .log_board import LogHSMercs
from .mouse_utils import move_mouse, move_mouse_and_click, mouse_click
from .platforms import windowMP
from .settings import ability_order, mercsAbilities, mercslist, settings_dict

log = logging.getLogger(__name__)

default_ability_section = "Mercenary"
ability_section = default_ability_section


class Enemies(
    namedtuple("Enemies", ["red", "green", "blue", "noclass", "noclass2", "mol"])
):
    """
    Class to manage enemies in the game.
    Attributes:
    red: An integer representing the number of red enemies.
    green: An integer representing the number of green enemies.
    blue: An integer representing the number of blue enemies.
    no_class: An integer representing the number of enemies with no class.
    no_class2: An integer representing the number of enemies with no second class.
    mol: An integer representing the number of mol enemies.
    """


class Board(
    namedtuple(
        "Board",
        ["card_width", "card_height", "position_even", "position_odd", "my_board_y"],
    )
):
    """
    Class to manage the game board.
    Attributes:
    card_width: An integer representing the width of a card on the board.
    card_height: An integer representing the height of a card on the board.
    position_even: A list of integers representing the positions of the cards on the even rows of the board.
    position_odd: A list of integers representing the positions of the cards on the odd rows of the board.
    my_board_y: A float representing the y-coordinate of the board.
    """

    def __new__(cls):
        card_width = windowMP()[2] // 16
        card_height = windowMP()[3] // 6

        card_size = windowMP()[2] // 12
        first_even = windowMP()[2] // 3.6

        positions = [first_even + i * card_size // 2 for i in range(11)]
        position_even = positions[::2]
        position_odd = positions[1::2]

        my_board_y = windowMP()[3] / 1.5

        return super().__new__(
            cls, card_width, card_height, position_even, position_odd, my_board_y
        )


def select_enemy_to_attack(index):
    """
    Moves the mouse over an enemy to attack it after selecting a merc's ability.

    Args:
    index: A list of two integers representing the x and y coordinates of the enemy.

    Returns:
    A boolean value indicating whether the mouse was moved successfully.
    """
    cardWidth = windowMP()[2] // 16
    cardHeight = windowMP()[3] // 6
    retour = False

    if index:
        time.sleep(0.3)
        log.debug(
            "Move index (index, x, y) : %s %s %s",
            index,
            index[0] + (cardWidth // 2),
            index[1] - (cardWidth // 3),
        )
        move_mouse_and_click(
            windowMP(), index[0] + (cardWidth // 3), index[1] - (cardHeight // 2)
        )
        retour = True
    return retour


def select_random_enemy_to_attack(enemies=None):
    """Selects a random enemy to attack.

    Args:
    enemies: An instance of the Enemies class representing the current state of enemies.

    Returns:
    A boolean value indicating whether an enemy was selected successfully.
    """
    enemies = enemies or []
    log.debug("select_random_enemy_to_attack : %s len=%s", enemies, len(enemies))
    retour = False
    while enemies:
        toAttack = enemies.pop(random.randint(0, len(enemies) - 1))
        if select_enemy_to_attack(toAttack):
            retour = True
            break

    # attacks the middle enemy minion if you don't find any enemy
    if not retour:
        select_enemy_to_attack([windowMP()[2] / 2.01, windowMP()[3] / 2.77])
        # select_enemy_to_attack([windowMP()[2] / 2.1, windowMP()[3] / 3.6])

    # right click added to avoid some problem (if enemy wasn't clickable)
    mouse_click("right")


def priorityMercByRole(myMercs, targetrole) -> List[int]:
    """
    Prioritizes a list of mercenaries by a specified role.

    Args:
        my_mercs: A list of mercenaries.
        target_role: A role that should be prioritized when sorting the list.

    Returns:
        A list of mercenary positions where mercenaries of the target role come first, followed by non-target roles and minions at the end.
    """
    mercs_pos = []
    # add targetrole mercs first
    for i in myMercs:
        if myMercs[i] in mercslist:
            if mercslist[myMercs[i]]["role"] == targetrole:
                mercs_pos.append(int(i))
    if mercs_pos:
        return mercs_pos
    # add non targetrole mercs to the end of the list
    for i in myMercs:
        if myMercs[i] in mercslist:
            mercs_pos.append(int(i))
    if mercs_pos:
        return mercs_pos
    # add friendly minion
    for i in myMercs:
        if targetrole == "minion":
            mercs_pos.append(int(i))
    return mercs_pos


def calculate_positions(number, position):
    """
    Calculates the positions based on the given number and position.

    Args:
        number (int): The number used for position calculation.
        position (int): The position used for position calculation.

    Returns:
        tuple: A tuple containing two values - the calculated position index and the corresponding x-coordinate.
    """
    cardSize = int(windowMP()[2] / 12)
    firstOdd = int(windowMP()[2] / 3)
    firstEven = int(windowMP()[2] / 3.6)

    positionOdd = [int(firstOdd + (i * cardSize)) for i in range(5)]
    positionEven = [int(firstEven + (i * cardSize)) for i in range(6)]

    pos_and_x_calculations = {
        0: lambda: (
            int(2 - (number / 2 - 1) + (position - 1)),
            positionEven[int(2 - (number / 2 - 1) + (position - 1))],
        ),
        1: lambda: (
            int(2 - (number - 1) / 2 + (position - 1)),
            positionOdd[int(2 - (number - 1) / 2 + (position - 1))],
        ),
    }

    return pos_and_x_calculations[number % 2]()


def ability_target_friend(targettype, myMercs, enemies: Enemies, abilitySetting):
    """
    Return the X coord of one of our mercenaries
    """

    friendName = abilitySetting["name"]

    log.debug("Friend targeted is %s", targettype)
    log.debug("Friend name is %s", friendName)
    cardSize = int(windowMP()[2] / 12)
    firstOdd = int(windowMP()[2] / 3)
    firstEven = int(windowMP()[2] / 3.6)
    positionOdd = []  # positionOdd=[640,800,960,1120,1280]
    positionEven = []  # positionEven=[560,720,880,1040,1200,1360]
    for i in range(6):
        positionEven.append(int(firstEven + (i * cardSize)))
        if i != 5:
            positionOdd.append(int(firstOdd + (i * cardSize)))

    number = int(sorted(myMercs)[-1])
    if targettype == "friend":
        if friendName:
            position = findFriendNameInMercs(myMercs, friendName)
        else:
            # for future, it could also buff an alied if health drops too low
            position = pickBestAllyToBuff(enemies, myMercs, number)
    else:
        position = 1
        for i in myMercs:
            if myMercs[i] in mercslist:
                # is a Mercenary
                # "type" == Beast, Human, ... "faction" == Pirate, Horde, ...
                if (
                    targettype in mercslist[myMercs[i]]["type"]
                    or targettype == mercslist[myMercs[i]]["faction"]
                ):
                    position = int(i)
            else:
                # is a friendly Minion
                if targettype == "minion":
                    position = int(i)
                elif targettype == "Imp" and re.search(r"\bImp\b", myMercs[i]):
                    position = int(i)

    if number % 2 == 0:  # if mercenaries number is even
        pos = int(2 - (number / 2 - 1) + (position - 1))
        x = positionEven[pos]
    else:  # if mercenaries number is odd
        pos = int(2 - (number - 1) / 2 + (position - 1))
        x = positionOdd[pos]

    return x


def pickBestAllyToBuff(enemies, myMercs, number):
    """
    Selects the best ally to buff based on the enemies' roles.

    Args:
        enemies: A list of enemy mercenaries.
        my_mercs: A list of our mercenaries.
        number: The total number of our mercenaries.

    Returns:
        The position of the best ally to buff.

    TODO get multiple enemies per role for priority by weakness
    """
    if enemies.blue:
        # enemies have blue so we buff red merc first
        position = random.choice(priorityMercByRole(myMercs, "Protector"))
    elif enemies.green:
        # enemies have green so we buff blue merc first
        position = random.choice(priorityMercByRole(myMercs, "Caster"))
    elif enemies.red:
        # enemies have red so we buff green merc first
        position = random.choice(priorityMercByRole(myMercs, "Fighter"))
    else:
        position = random.randint(1, number)
    return position


def findFriendNameInMercs(myMercs, friendName):
    """
    Searches for a friend's name in a list of mercenaries.

    Args:
        myMercs (list): A list of mercenaries.
        friendName (str): The name of the friend to search for.

    Returns:
        bool: True if the friend's name is found in the list, False otherwise.
    """
    for i in myMercs:
        log.debug("***** Looking for our friend %s ... ******", friendName)
        if re.search(rf"\A{friendName}\b", myMercs[i]):
            log.debug("***** FOUND HIM AT POSITION %s", i)
            return int(i)
    return 0


def get_ability_for_this_turn(name, minionSection, turn, defaultAbility=0):
    """
    Retrieves the configured ability for a selected mercenary or minion during a specific turn.

    Args:
        name: The name of the mercenary or minion.
        minion_section: The section of minions.
        turn: The current turn.
        default_ability: The default ability to use if no specific ability is configured.

    Returns:
        The ability to use for this turn.
    """

    if minionSection in ability_order and name.lower() in ability_order[minionSection]:
        # in combo.ini, split (with ",") to find the ability to use this turn
        # use first ability if not found
        round_abilities = ability_order[minionSection][name.lower()].split(",")
        abilitiesNumber = len(round_abilities)
        if abilitiesNumber != 0:
            ability = turn % abilitiesNumber
            if ability == 0:
                ability = len(round_abilities)
            ability = round_abilities[ability - 1]
        else:
            ability = defaultAbility
    else:
        ability = defaultAbility

    log.info("%s Ability Selected : %s", name, ability)

    return str(ability)


DEFAULT_SETTINGS = {
    "ai": "byColor",
    "chooseone": 0,
    "faction": None,
    "name": None,
    "role": None,
    "type": None,
}

KEY_TO_CAST_FUNC = {
    "chooseone": lambda x: int(x) - 1,
    "ai": str,
    "name": str,
    "type": str,
    "role": str,
}


def parse_ability_setting(ability):
    """
    Parses the ability setting from a given string.

    Args:
        ability: The ability setting string to parse.

    Returns:
        A dictionary containing parsed ability settings.
    """
    retour = DEFAULT_SETTINGS.copy()

    if ":" in ability:
        ability_value, config_value = ability.split(":")
        retour["ability"] = int(ability_value)
        retour["config"] = config_value

        for i in retour["config"].split("&"):
            key, value = i.split("=")

            if key in KEY_TO_CAST_FUNC:
                retour[key] = KEY_TO_CAST_FUNC[key](value)
            else:
                log.warning("Unknown parameter")
    elif ability.isdigit():
        retour["ability"] = int(ability)
    else:
        log.warning("Invalid ability")

    return retour


def didnt_find_a_name_for_this_one(name, minionSection, turn, defaultAbility=0):
    """
    Retrieves the configuration of an ability for a specific turn and then selects this ability for a certain mercenary or minion.

    Args:
        name: The name of the mercenary or minion.
        minion_section: The section of minions.
        turn: The current turn.
        default_ability: The default ability to use if no specific ability is configured.

    Returns:
        The configuration of the selected ability.
    """
    abilitiesWidth = windowMP()[2] // 14.2
    abilitiesHeigth = windowMP()[3] // 7.2

    # abilitiesPositionY : Y coordinate to find "abilities" line during battle
    abilitiesPositionY = windowMP()[3] // 2.4
    # abilitiesPositionX :
    #   X coordinates to find the 3 "abilities" during battle
    #   (4 because sometimes, Treasure give you a new abilities
    #   but the bot doesn't support it right now)
    abilitiesPositionX = [
        windowMP()[2] // 2.68,
        windowMP()[2] // 2.17,
        windowMP()[2] // 1.8,
        windowMP()[2] // 1.56,
    ]

    abilityConfig = parse_ability_setting(
        get_ability_for_this_turn(name, minionSection, turn, defaultAbility)
    )
    ability = abilityConfig["ability"]
    if ability == 0:
        log.debug("No ability selected (0)")
    elif ability >= 1 and ability <= 3:
        log.debug(
            "abilities Y : %s | abilities X : %s",
            abilitiesPositionY,
            abilitiesPositionX,
        )
        abilityScreenshot = [
            int(abilitiesWidth),
            int(abilitiesHeigth),
            int(windowMP()[1] + abilitiesPositionY),
            int(windowMP()[0] + abilitiesPositionX[0]),
        ]
        if (
            find_element(
                UIElement.hourglass.filename,
                Action.get_coords,
                new_screen=abilityScreenshot,
            )
            is None
        ):
            move_mouse_and_click(
                windowMP(),
                int(abilitiesPositionX[ability - 1] + abilitiesWidth // 2),
                int(abilitiesPositionY + abilitiesHeigth // 2),
            )
    else:
        log.warning("No ability selected for %s", name)
        abilityConfig["ability"] = 0

    return abilityConfig


def select_ability(localhero, myBoard, enemies: Enemies, raund):
    """
    Selects an ability for a mercenary based on available abilities and the current round.

    Args:
        local_hero: The name of the mercenary for which to select an ability.
        my_board: The current state of our board.
        enemies: A list of enemy mercenaries.
        round: The current round.

    Returns:
        A boolean indicating whether or not an ability was successfully selected.
    """

    if localhero in mercsAbilities:
        retour = False
        time.sleep(0.3)
        chooseone2 = [windowMP()[2] // 2.4, windowMP()[2] // 1.7]
        time.sleep(0.3)
        chooseone3 = [windowMP()[2] // 3, windowMP()[2] // 2, windowMP()[2] // 1.5]
        time.sleep(0.3)

        abilitySetting = didnt_find_a_name_for_this_one(
            localhero, ability_section, raund, 1
        )
        if abilitySetting["ability"] != 0:
            ability = abilitySetting["ability"]
            if isinstance(mercsAbilities[localhero][str(ability)], bool):
                retour = mercsAbilities[localhero][str(ability)]
            elif mercsAbilities[localhero][str(ability)] == "chooseone3":
                time.sleep(0.3)
                move_mouse_and_click(
                    windowMP(),
                    chooseone3[abilitySetting["chooseone"]],
                    windowMP()[3] // 2,
                )
                retour = True
            elif mercsAbilities[localhero][str(ability)] == "chooseone2":
                time.sleep(0.3)
                move_mouse_and_click(
                    windowMP(),
                    chooseone2[abilitySetting["chooseone"]],
                    windowMP()[3] // 2,
                )
                retour = True
            elif mercsAbilities[localhero][str(ability)].startswith("friend"):
                time.sleep(0.3)

                # if attacks.json shows something more than just "friend" (like "Beast")
                if ":" in mercsAbilities[localhero][str(ability)]:
                    move_mouse_and_click(
                        windowMP(),
                        ability_target_friend(
                            mercsAbilities[localhero][str(ability)].split(":")[1],
                            myBoard,
                            enemies,
                            abilitySetting,
                        ),
                        windowMP()[3] / 1.5,
                    )
                else:
                    # attacks.json  only contains "friend"
                    move_mouse_and_click(
                        windowMP(),
                        ability_target_friend(
                            "friend", myBoard, enemies, abilitySetting
                        ),
                        windowMP()[3] / 1.5,
                    )
    else:
        localhero = re.sub(r" [0-9]$", "", localhero)
        abilitySetting = didnt_find_a_name_for_this_one(localhero, "Neutral", raund, 1)
        if abilitySetting["ability"] == 0:
            retour = False
        else:
            retour = True

    return retour


def take_turn_action(
    position,
    mercName,
    myMercs,
    enemies: Enemies,
    raund,
):
    """
    Function to attack an enemy (red, green or blue ideally)
    with the selected mercenary
    red attacks green (if exists)
    green attacks blue (if exists)
    blue attacks red (if exists)
    else merc attacks minion with special abilities or neutral
    """

    log.debug("Attacks function")

    number = int(sorted(myMercs)[-1])

    cardSize = int(windowMP()[2] / 12)
    firstOdd = int(windowMP()[2] / 3)
    firstEven = int(windowMP()[2] / 3.6)
    positionOdd = []  # positionOdd=[640,800,960,1120,1280]
    positionEven = []  # positionEven=[560,720,880,1040,1200,1360]
    for i in range(6):
        positionEven.append(int(firstEven + (i * cardSize)))
        if i != 5:
            positionOdd.append(int(firstOdd + (i * cardSize)))

    if number % 2 == 0:  # if mercenaries number is even
        pos = int(2 - (number / 2 - 1) + (position - 1))
        x = positionEven[pos]
    else:  # if mercenaries number is odd
        pos = int(2 - (number - 1) / 2 + (position - 1))
        x = positionOdd[pos]
    y = windowMP()[3] / 1.5

    log.info("attack with : %s ( position : %s/%s =%s)", mercName, position, number, x)

    move_mouse_and_click(windowMP(), x, y)
    time.sleep(0.3)
    move_mouse(windowMP(), windowMP()[2] / 3, windowMP()[3] / 2)
    time.sleep(0.3)
    if mercName in mercslist:
        if (
            mercslist[mercName]["role"] == "Protector"
            and select_ability(mercName, myMercs, enemies, raund)
            and not select_enemy_to_attack(enemies.green)
            and not select_enemy_to_attack(enemies.mol)
            and not select_enemy_to_attack(enemies.noclass)
            and not select_enemy_to_attack(enemies.noclass2)
        ):
            select_random_enemy_to_attack([enemies.red, enemies.blue])
        elif (
            mercslist[mercName]["role"] == "Fighter"
            and select_ability(mercName, myMercs, enemies, raund)
            and not select_enemy_to_attack(enemies.blue)
            and not select_enemy_to_attack(enemies.mol)
            and not select_enemy_to_attack(enemies.noclass)
            and not select_enemy_to_attack(enemies.noclass2)
        ):
            select_random_enemy_to_attack([enemies.red, enemies.green])
        elif (
            mercslist[mercName]["role"] == "Caster"
            and select_ability(mercName, myMercs, enemies, raund)
            and not select_enemy_to_attack(enemies.red)
            and not select_enemy_to_attack(enemies.mol)
            and not select_enemy_to_attack(enemies.noclass)
            and not select_enemy_to_attack(enemies.noclass2)
        ):
            select_random_enemy_to_attack([enemies.green, enemies.blue])
    elif select_ability(mercName, myMercs, enemies, raund):
        select_random_enemy_to_attack(
            [
                enemies.red,
                enemies.green,
                enemies.blue,
                enemies.noclass,
                enemies.noclass2,
                enemies.mol,
            ]
        )


def execute_action_sequence(window, x, y):
    """
    Execute a sequence of actions.

    Args:
        window: The game window.
        x: The x-coordinate of the target location.
        y: The y-coordinate of the target location.
    """
    move_mouse_and_click(window, x, y)
    time.sleep(0.3)
    move_mouse(window, window[2] / 3, window[3] / 2)
    time.sleep(0.3)


def find_enemies(ns=True) -> Enemies:
    """
    Find and return the count of different enemy types.

    Args:
        ns: A boolean indicating whether to consider non-standard enemy types.

    Returns:
        An instance of the Enemies class containing the count of different enemy types.

    """
    # Get the window geometry once
    window_geometry = windowMP()

    # Find all enemy types
    enemyred = find_enemy("red", window_geometry, ns)
    enemygreen = find_enemy("green", window_geometry, ns)
    enemyblue = find_enemy("blue", window_geometry, ns)
    enemynoclass = find_enemy("noclass", window_geometry, ns)
    enemynoclass2 = find_enemy("noclass2", window_geometry, ns)
    enemymol = find_enemy("sob", window_geometry, ns)

    log.info(
        "Enemies : red %s - green %s - blue %s - noclass %s - noclass2 %s - mol %s",
        enemyred,
        enemygreen,
        enemyblue,
        enemynoclass,
        enemynoclass2,
        enemymol,
    )

    return Enemies(
        enemyred, enemygreen, enemyblue, enemynoclass, enemynoclass2, enemymol
    )


def find_enemy(enemy_role, window_geometry, ns=True):
    """
    Finds the coordinates of an enemy on the game screen.

    Args:
        enemy_role (str): The role of the enemy to find.
        window_geometry (tuple): The geometry of the game window.
        ns (bool, optional): Determines whether to use a new screenshot for the search. Default is True.

    Returns:
        tuple or None: The coordinates (x, y) of the enemy if found, None otherwise.
    """
    enemy = find_element(
        getattr(UIElement, enemy_role).filename, Action.get_coords, new_screen=ns
    )
    if enemy:
        enemy = (
            enemy[0],
            enemy[1],
        )
    return enemy


def battle(zoneLog=None):
    """
    Simulate battles between the cards on the battlefield until one of your cards dies.

    Args:
        zoneLog: An instance of the zone log class.

    Returns:
        str: The outcome of the battle, either "win" or "loose".
    """
    retour = True

    raund = 1
    while True:
        time.sleep(0.3)
        move_mouse(
            windowMP(),
            windowMP()[2] // 4,
            windowMP()[3] // 2,
        )

        # we look for the (green) "ready" button because :
        # - sometimes, the bot click on it but it doesn't work very well
        # - during a battle, some enemies can return in hand and
        #   are put back on battlefield with a "ready" button
        #       but the bot is waiting for a victory / defeat /
        #   ... or the yellow button ready
        find_element(Button.allready.filename, Action.move_and_click)

        find_element(Button.onedie.filename, Action.move_and_click)

        if find_element(UIElement.win.filename, Action.screenshot) or find_element(
            UIElement.win_final.filename, Action.screenshot
        ):
            retour = "win"
            move_mouse_and_click(windowMP(), windowMP()[2] / 2, windowMP()[3] / 1.3)
            zoneLog.cleanBoard()

            break
        elif find_element(UIElement.lose.filename, Action.screenshot):
            retour = "loose"
            move_mouse_and_click(
                windowMP(),
                windowMP()[2] / 2,
                windowMP()[3] / 1.3,
            )
            zoneLog.cleanBoard()
            break
        elif find_element(
            Button.fight.filename, Action.screenshot
        ):  # or find_element(Button.startbattle1.filename, Action.screenshot):
            # looks for your enemies on board thanks to log file
            enemies = zoneLog.getEnemyBoard()
            log.info("Round %s : enemy board %s", raund, enemies)
            # looks for your Mercenaries on board thanks to log file
            mercenaries = zoneLog.getMyBoard()
            log.info("Round %s :  your board %s", raund, mercenaries)

            # click on neutral zone to avoid problem with screenshot
            # when you're looking for red/green/blue enemies
            move_mouse_and_click(windowMP(), windowMP()[2] // 2, windowMP()[3] // 1.2)

            time.sleep(0.5)

            # try to target the enemy are (smaller is better to avoid to detect
            # an enemy outside the zone)
            enemyBoard_left = int(windowMP()[0] + (windowMP()[2] // 4))
            enemyBoard_right = int(windowMP()[2] // 1.3) - (
                enemyBoard_left - windowMP()[0]
            )
            enemyBoardScreenshot = [
                enemyBoard_right,
                windowMP()[3] // 2,
                windowMP()[1],
                enemyBoard_left,
            ]

            enemies = find_enemies(enemyBoardScreenshot)

            # Go (mouse) to "central zone" and click on an empty space
            # move_mouse_and_click(windowMP(), windowMP()[2] // 2, windowMP()[3] // 1.2)
            # time.sleep(1)

            for i in mercenaries:
                # Go (mouse) to "central zone" and click on an empty space
                move_mouse_and_click(
                    windowMP(), windowMP()[2] // 2, windowMP()[3] // 1.2
                )

                take_turn_action(
                    int(i),
                    mercenaries[i],
                    # int(sorted(mercenaries)[-1]),
                    mercenaries,
                    enemies,
                    raund,
                )
                # in rare case, the bot detects an enemy ("noclass" most of the
                #   times) outside of the battlezone.
                # the second click (to select the enemy),
                #   which is on an empty space, doesnt work.
                # next move : instead of selecting the next mercenaries (to choose an
                #   ability), the mercenary is clicked on to be targeted (from
                #   previous ability). Need a "rightclick" to cancel this action.
                mouse_click("right")
                time.sleep(0.1)

            i = 0
            while not find_element(Button.allready.filename, Action.move_and_click):
                if i > 5:
                    move_mouse(windowMP(), windowMP()[2] // 1.2, windowMP()[3] // 3)
                    mouse_click("right")
                    find_element(Button.fight.filename, Action.move_and_click)
                    break
                time.sleep(0.2)
                i += 1
            time.sleep(3)
            raund += 1

    return retour


def selectCardsInHand(zL=None):
    """
    Select the cards to put on the battlefield and start the 'battle' function.
    Note: The feature of choosing cards manually from images with text has been temporarily disabled
    to support multi-language. This feature will be reintroduced in the future using HS logs.

    Args:
        zL: An instance of LogHSMercs representing the zone log.

    Returns:
        The result of the battle.

    Raises:
        None
    """

    log.debug("[ SETH - START]")
    retour = True
    global ability_section

    # while not find_element(Button.num.filename, Action.screenshot):
    #    time.sleep(2)
    waitForItOrPass(Button.num, 60, 2)

    if find_element(Button.num.filename, Action.screenshot):
        zL = LogHSMercs(settings_dict["zonelog"])
        # check if Zone.log was erased so we need to go back
        zL.find_battle_start_log()
        zL.start()
        while not zL.eof:
            # print("Reaching Zone.log end before starting")
            time.sleep(1)

        # check if HS is ready for the battle
        # and check logs to find
        boss = zL.getEnemyBoard()
        for i in boss:
            if boss[i] in ability_order:
                log.info("Specific conf found to beat: %s", boss[i])
                ability_section = boss[i]
                break

        # wait 'WaitForEXP' to make the battle last longer
        # and win more XP (for the Hearthstone reward track)
        wait_for_exp = settings_dict["waitforexp"]
        log.info("WaitForEXP - wait (second(s)) : %s", wait_for_exp)
        countdown(wait_for_exp, 10, "Wait for XP : sleeping")

        log.debug("windowMP = %s", windowMP())
        x1 = windowMP()[2] // 2.6
        y1 = windowMP()[3] // 1.09
        x2 = windowMP()[2] // 10
        y2 = windowMP()[3] // 10

        # Look if user configured the bot to select cards in hand
        # and put them on board
        if "_handselection" in ability_order[ability_section]:
            log.info("Cards in hand: %s", zL.getHand())
            cards = cardsInHand(windowMP(), zL, 3)

            for merc in ability_order[ability_section]["_handselection"].split("+"):
                cards.send_to_board(merc)
                if find_element(Button.allready.filename, Action.screenshot):
                    break

        # let the "while". In future release,
        #   we could add a function to select specifics cards
        while not (
            find_element(Button.num.filename, Action.move_and_click)
            or find_element(Button.allready.filename, Action.move_and_click)
        ):
            move_mouse(windowMP(), x1, y1)
            move_mouse(windowMP(), x2, y2)

        retour = battle(zL)
        log.debug("[ SETH - END]")

        # put back default value to selection abilities from [Mercenary] section
        ability_section = default_ability_section

        zL.stop()

    return retour


class cardsInHand:
    """
    Class to manage the cards in hand.

    Attributes:
    win: A tuple representing the window geometry.
    zone_log: An instance of LogHSMercs representing the zone log.
    in_hand: A list of cards in hand.
    on_board: An integer representing the number of cards currently on the board.
    max_on_board: An integer representing the maximum number of cards allowed on the board.

    Methods:
    send_to_board: Sends a card to the board.
    """

    def __init__(self, win, zLog, max_on_board):
        """
        Initializes an instance of the class.

        Args:
            win: The window object.
            zLog: The zone log object.
            max_on_board (int): The maximum number of mercenaries allowed on the board.

        Returns:
            None
        """
        self.win = win
        self.zone_log = zLog
        # used to init (set to False) "AutoCorrectZonesAfterServerChange"
        # self.zone_log.get_zonechanged()
        self.in_hand = self.zone_log.getHand()
        self.on_board = 0
        self.max_on_board = max_on_board

    def send_to_board(self, mercenary, i=None):
        """
        Sends a mercenary to the board.

        Args:
            mercenary: The mercenary object to be sent to the board.

        Returns:
            bool: True if the mercenary was successfully sent to the board, False otherwise.
        """
        if self.on_board < self.max_on_board:
            coord_x = self.get_coord(mercenary)
            if coord_x == 0:
                return False
            move_mouse_and_click(self.win, coord_x, self.coord_y)
            move_mouse_and_click(self.win, self.win[2] // 1.33, self.win[3] // 1.63)
            log.debug("Put on board: %s", mercenary)
            self.on_board += 1
            self.in_hand.remove(mercenary)

            while not self.zone_log.get_zonechanged():
                time.sleep(0.5)
                i += 1
                if i > 10:
                    log.error("Putting %s on board failed.", mercenary)
                    break

            
    def clean(self):
        """
        Cleans the hand and board by resetting their values.

        Returns:
            None
        """
        self.in_hand = []
        self.on_board = 0

    def get_size(self):
        """
        Gets the size of the hand.

        Returns:
            int: The size of the hand.
        """
        return len(self.in_hand)

    def get_coord(self, mercenary):
        """
        Calculates the x-coordinate for a given mercenary.

        Args:
            mercenary: The mercenary object.

        Returns:
            int: The calculated x-coordinate.
        """
        self.coord_y = self.win[3] // 1.085
        if mercenary not in self.in_hand:
            return 0
        size = self.get_size()
        if size == 6:
            card_width = self.win[2] // 21
            starting_position = self.win[2] // 2.8
        elif size == 5:
            card_width = self.win[2] // 17.39
            starting_position = self.win[2] // 2.8
        elif size == 4:
            card_width = self.win[2] // 13.91
            starting_position = self.win[2] // 2.8
        elif size == 3:
            card_width = self.win[2] // 14.55
            starting_position = self.win[2] // 2.5
        elif size == 2:
            card_width = self.win[2] // 14.55
            starting_position = self.win[2] // 2.28
        elif size == 1:
            card_width = self.win[2] // 14.55
            starting_position = self.win[2] // 2.13
        return (
            starting_position
            + (card_width // 2)
            + self.in_hand.index(mercenary) * card_width
        )
