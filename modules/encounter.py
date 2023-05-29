import re
import time
import random
import logging
from typing import List

from .platforms import windowMP
from .mouse_utils import move_mouse_and_click, move_mouse, mouse_click  # , mouse_scroll

from .image_utils import find_element
from .constants import UIElement, Button, Action
from .game import countdown, waitForItOrPass

from .log_board import LogHSMercs
from .settings import settings_dict, mercslist, mercsAbilities, ability_order

log = logging.getLogger(__name__)

default_ability_section = "Mercenary"
ability_section = default_ability_section


class Enemies:
    def __init__(self, red, green, blue, noclass, noclass2, mol):
        self.red = red
        self.green = green
        self.blue = blue
        self.noclass = noclass
        self.noclass2 = noclass2
        self.mol = mol


class Board:
    def __init__(self):
        self.card_width = windowMP()[2] // 16
        self.card_height = windowMP()[3] // 6

        card_size = windowMP()[2] // 12
        first_even = windowMP()[2] // 3.6

        positions = [first_even + i * card_size // 2 for i in range(11)]
        self.position_even = positions[::2]
        self.position_odd = positions[1::2]

        self.myboard.y = windowMP()[3] / 1.5
        # self.enemy.y =


def select_enemy_to_attack(index):
    """Used to move the mouse over an enemy to attack it
    (after selecting a merc's ability)
    """
    cardWidth = windowMP()[2] // 16
    cardHeight = windowMP()[3] // 6
    retour = False

    if index:
        time.sleep(0.1)
        log.debug(
            f"Move index (index, x, y) : {index}"
            f" {index[0] + (cardWidth // 2)} {index[1] - (cardWidth // 3)}",
        )
        move_mouse_and_click(
            windowMP(), index[0] + (cardWidth // 3), index[1] - (cardHeight // 2)
        )
        retour = True
    return retour


def select_random_enemy_to_attack(enemies=None):
    """look for a random enemy
    (used when blue mercs can't find red enemy,
    green can't find blue or
    red can't find green
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
    return merc position list prioritize by the targetRole comes first,
        non target role after and minion comes last
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


def ability_target_friend(targettype, myMercs, enemies: Enemies, abilitySetting):
    """Return the X coord of one of our mercenaries"""

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
    # TODO get multiple enemies per role for priority by
    # weakness of the most role of enemy
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


# TODO This could also be moved to an entirely new module
def findFriendNameInMercs(myMercs, friendName):
    for i in myMercs:
        log.debug("***** Looking for our friend %s ... ******", friendName)
        if re.search(rf"\A{friendName}\b", myMercs[i]):
            log.debug("***** FOUND HIM AT POSITION %s", i)
            return int(i)
    return 0


def get_ability_for_this_turn(name, minionSection, turn, defaultAbility=0):
    """Get the ability (configured) for this turned for the selected Merc/minion"""

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


def parse_ability_setting(ability):
    retour = {
        "ai": "byColor",
        "chooseone": 0,
        "faction": None,
        "name": None,
        "role": None,
        "type": None,
    }

    if ":" not in ability:
        retour["ability"] = int(ability)
    else:
        retour["ability"] = int(ability.split(":")[0])
        retour["config"] = ability.split(":")[1]
        for i in retour["config"].split("&"):
            key, value = i.split("=")
            if key == "chooseone":
                retour["chooseone"] = int(value) - 1
            elif key == "ai":
                retour["ai"] = value
            elif key == "name":
                retour["name"] = value
            elif key == "type":
                retour["type"] = value
            elif key == "role":
                # "role" should be "Protector", "Caster" or "Fighter"
                retour["role"] = value
            else:
                log.warning("Unknown parameter")
    return retour


def didnt_find_a_name_for_this_one(name, minionSection, turn, defaultAbility=0):
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
            f"abilities Y : {abilitiesPositionY} |"
            f" abilities X : {abilitiesPositionX}"
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
        log.warning(f"No ability selected for {name}")
        abilityConfig["ability"] = 0

    return abilityConfig


def select_ability(localhero, myBoard, enemies: Enemies, raund):
    """Select an ability for a mercenary.
        Depend on what is available and wich Round (battle)
    Click only on the ability (doesnt move to an enemy)
    """

    if localhero in mercsAbilities:
        retour = False
        chooseone2 = [windowMP()[2] // 2.4, windowMP()[2] // 1.7]
        chooseone3 = [windowMP()[2] // 3, windowMP()[2] // 2, windowMP()[2] // 1.5]

        abilitySetting = didnt_find_a_name_for_this_one(
            localhero, ability_section, raund, 1
        )
        if abilitySetting["ability"] != 0:
            ability = abilitySetting["ability"]
            if isinstance(mercsAbilities[localhero][str(ability)], bool):
                retour = mercsAbilities[localhero][str(ability)]
            elif mercsAbilities[localhero][str(ability)] == "chooseone3":
                time.sleep(0.2)
                move_mouse_and_click(
                    windowMP(),
                    chooseone3[abilitySetting["chooseone"]],
                    windowMP()[3] // 2,
                )
                retour = True
            elif mercsAbilities[localhero][str(ability)] == "chooseone2":
                time.sleep(0.2)
                move_mouse_and_click(
                    windowMP(),
                    chooseone2[abilitySetting["chooseone"]],
                    windowMP()[3] // 2,
                )
                retour = True
            elif mercsAbilities[localhero][str(ability)].startswith("friend"):
                time.sleep(0.2)

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
    time.sleep(0.2)
    move_mouse(windowMP(), windowMP()[2] / 3, windowMP()[3] / 2)
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


# Look for enemies
def find_enemies(ns=True) -> Enemies:
    # we use new screenshot for the first call
    # then we already have the image in memory
    enemyred = find_red_enemy(ns)
    enemygreen = find_green_enemy(ns)
    enemyblue = find_blue_enemy(ns)
    enemynoclass = find_noclass_enemy(ns)
    enemynoclass2 = find_noclass2_enemy(ns)
    enemymol = find_mol_enemy(ns)

    log.info(
        f"Enemies : red {enemyred}"
        f" - green {enemygreen}"
        f" - blue {enemyblue}"
        f" - noclass {enemynoclass}"
        f" - noclass2 {enemynoclass2}"
        f" - mol {enemymol}"
    )
    return Enemies(
        enemyred, enemygreen, enemyblue, enemynoclass, enemynoclass2, enemymol
    )


def find_red_enemy(ns=True):
    return find_enemy("red", ns)


def find_green_enemy(ns=True):
    return find_enemy("green", ns)


def find_blue_enemy(ns=True):
    return find_enemy("blue", ns)


def find_noclass_enemy(ns=True):
    return find_enemy("noclass", ns)


def find_noclass2_enemy(ns=True):
    return find_enemy("noclass2", ns)


def find_mol_enemy(ns=True):
    return find_enemy("sob", ns)


def find_enemy(enemy_role, ns=True):
    enemy = find_element(
        getattr(UIElement, enemy_role).filename, Action.get_coords, new_screen=ns
    )
    # find_element: Can be changed to return None or actual coords if exists
    if enemy:
        enemy = (
            enemy[0],
            enemy[1],
        )
    return enemy


def battle(zoneLog=None):
    """Find the cards on the battlefield (yours and those of your opponents)
    and make them battle until one of yours die
    """
    retour = True

    raund = 1
    while True:
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
            log.info(f"Round {raund} : enemy board {enemies}")
            # looks for your Mercenaries on board thanks to log file
            mercenaries = zoneLog.getMyBoard()
            log.info(f"Round {raund} :  your board {mercenaries}")

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
    """Select the cards to put on battlefield
    and then, start the 'battle' function
    Update : actually, the bot doesn't choose it anymore
    since we stopped to use image with mercenaries text
    (so we can easily support multi-language)
        this feature will come back later using HS logs
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
            print("Reaching Zone.log end before starting")
            time.sleep(1)

        # check if HS is ready for the battle
        # and check logs to find
        boss = zL.getEnemyBoard()
        for i in boss:
            if boss[i] in ability_order:
                log.info(f"Specific conf found to beat: {boss[i]}")
                ability_section = boss[i]
                break

        # wait 'WaitForEXP' (float) in minutes, to make the battle last longer
        # and win more XP (for the Hearthstone reward track)
        wait_for_exp = settings_dict["waitforexp"]
        log.info(f"WaitForEXP - wait (second(s)) : {wait_for_exp}")
        # time.sleep(wait_for_exp)
        countdown(wait_for_exp, 10, "Wait for XP : sleeping")

        log.debug(f"windowMP = {windowMP()}")
        x1 = windowMP()[2] // 2.6
        y1 = windowMP()[3] // 1.09
        x2 = windowMP()[2] // 10
        y2 = windowMP()[3] // 10

        # Look if user configured the bot to select cards in hand
        # and put them on board
        if "_handselection" in ability_order[ability_section]:
            log.info(f"Cards in hand: {zL.getHand()}")
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
    def __init__(self, win, zLog, max_on_board):
        self.win = win
        self.zone_log = zLog
        # used to init (set to False) "AutoCorrectZonesAfterServerChange"
        self.zone_log.get_zonechanged()
        self.in_hand = self.zone_log.getHand()
        self.on_board = 0
        self.max_on_board = max_on_board

    def send_to_board(self, mercenary):
        if self.on_board < self.max_on_board:
            coord_x = self.get_coord(mercenary)
            if coord_x == 0:
                return False
            move_mouse_and_click(self.win, coord_x, self.coord_y)
            move_mouse_and_click(self.win, self.win[2] // 1.33, self.win[3] // 1.63)
            log.debug(f"Put on board: {mercenary}")
            self.on_board += 1
            self.in_hand.remove(mercenary)
            i = 0
            while not self.zone_log.get_zonechanged():
                time.sleep(0.5)
                i += 1
                if i > 10:
                    log.error(f"Putting {mercenary} on board failed.")
                    break

    def clean(self):
        self.in_hand = []
        self.on_board = 0

    def get_size(self):
        return len(self.in_hand)

    def get_coord(self, mercenary):
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
