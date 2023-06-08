"""
This module provides the LogHSMercs class for parsing and tracking game state changes
from a specified Hearthstone Mercenaries log file. The class maintains the state of player's
hand and board, as well as the enemy's board, and provides methods to access these states. It also
supports real-time log file tracking through a separate thread, allowing the game state to be
updated as new log entries are created.
"""

import time
import re
from pathlib import Path
import threading
import logging

log = logging.getLogger(__name__)


class LogHSMercs:
    def __init__(self, logpath):
        """
        Constructs a LogHSMercs object. Opens the specified log file and prepares for
        real-time tracking of game state changes.
        Tracks cards in hand and on field.
        Args:
            logpath (str): Path to the Hearthstone Mercenaries log file.
        """
        self.logpath = logpath

        if not Path(logpath).exists():
            log.info("Logfile 'Zone.log' doesn't exist. Waiting for it...")
        while not Path(logpath).exists():
            time.sleep(1)

        self.filePos = None
        self.eof = False
        self.line = None
        self.logfile = open(self.logpath, "r", encoding="UTF-8")

        self.cardsInHand = []
        self.myBoard = {}
        self.mercsId = {}

        self.enemiesBoard = {}
        self.enemiesId = {}

        self.zonechange_finished = False

    def find_battle_start_log(self):
        """
        Identifies the starting point of a battle in the log file. This is determined
        by finding a specific pattern in the file's lines. The read position is then set to
        this line for the upcoming tracking.
        """

        line = self.logfile.readline()
        while line:
            if re.search(
                r"ZoneMgr.AddServerZoneChanges\(\) - taskListId=1"
                " changeListId=1 taskStart=0 taskEnd=",
                line,
            ):
                self.filePos = self.logfile.tell()
            line = self.logfile.readline()

        if self.filePos:
            self.logfile.seek(self.filePos)

    def follow(self):
        """
        Starts real-time tracking of the log file, continuously reading new lines and updating
        the game state based on the parsed information.
        """
        while self.__running:
            # Read the last line of the file
            line = self.logfile.readline()
            # Sleep if the file hasn't been updated
            if not line:
                self.eof = True
                time.sleep(0.1)
                continue

            if "ZoneChangeList.ProcessChanges() - processing" in line:
                if re.search(
                    r".+? tag=ZONE_POSITION .+?entityName=(.+?) +id=(.+?) .+?zonePos=(.) cardId=.+? player=1\] .+? dstPos=(.)",
                    line,
                ):
                    (mercenary, mercId, srcpos, dstpos) = re.findall(
                        r".+? tag=ZONE_POSITION .+?entityName=(.+?) +id=(.+?) .+?zonePos=(.) cardId=.+? player=1\] .+? dstPos=(.)",
                        line,
                    )[0]
                    self.mercsId[mercId] = mercenary

                    if (
                        srcpos != "0"
                        and srcpos in self.myBoard
                        and self.myBoard[srcpos] == mercId
                    ):
                        self.myBoard.pop(srcpos)

                    if dstpos != "0":
                        self.myBoard[dstpos] = mercId

                elif re.search(
                    r".+?entityName=(.+?) +id=(.+?) .+?zonePos=(.) cardId=.+? player=2\] .+? dstZoneTag=PLAY dstPos=(.)",
                    line,
                ):
                    (enemy, enemyId, srcpos, dstpos) = re.findall(
                        r".+?entityName=(.+?) +id=(.+?) .+?zonePos=(.) cardId=.+? player=2\] .+? dstZoneTag=PLAY dstPos=(.)",
                        line,
                    )[0]
                    self.enemiesId[enemyId] = enemy

                    if (
                        srcpos != "0"
                        and srcpos in self.enemiesBoard
                        and self.enemiesBoard[srcpos] == enemyId
                    ):
                        self.enemiesBoard.pop(srcpos)

                    if dstpos != "0":
                        self.enemiesBoard[dstpos] = enemyId

                elif re.search(
                    r".+? tag=ZONE_POSITION .+?entityName=(.+?) +id=(.+?) .+?zonePos=(.) cardId=.+? player=2\] .+? dstPos=(.)",
                    line,
                ):
                    (enemy, enemyId, srcpos, dstpos) = re.findall(
                        r".+? tag=ZONE_POSITION .+?entityName=(.+?) +id=(.+?) .+?zonePos=(.) cardId=.+? player=2\] .+? dstPos=(.)",
                        line,
                    )[0]
                    self.enemiesId[enemyId] = enemy

                    if (
                        srcpos != "0"
                        and srcpos in self.enemiesBoard
                        and self.enemiesBoard[srcpos] == enemyId
                    ):
                        self.enemiesBoard.pop(srcpos)

                    if dstpos != "0":
                        self.enemiesBoard[dstpos] = enemyId

                elif re.search(
                    r".+?entityName=(.+?) +id=.+? .+?cardId=.+? player=3\] .+? dstZoneTag=HAND .+?",
                    line,
                ):
                    mercenary = re.findall(
                        r".+?entityName=(.+?) +id=.+? .+?cardId=.+? player=3\] .+? dstZoneTag=HAND .+?",
                        line,
                    )[0]
                    if mercenary not in self.cardsInHand:
                        self.cardsInHand.append(mercenary)

                elif re.search(
                    r".+?entityName=.+? +id=.+? zone=PLAY zonePos=(.) .+?zone from FRIENDLY PLAY -> OPPOSING PLAY",
                    line,
                ):
                    zonepos = re.findall(
                        r".+?entityName=.+? +id=.+? zone=PLAY zonePos=(.) .+?zone from FRIENDLY PLAY -> OPPOSING PLAY",
                        line,
                    )[0]
                    self.myBoard.pop(zonepos)

                elif "ZoneMgr.AutoCorrectZonesAfterServerChange()" in line:
                    self.zonechange_finished = True

    def get_zonechanged(self):
        """
        Checks if a zone change has been completed in the log file.

        Returns:
        bool: True if a zone change has occurred, otherwise False.
        """
        if self.zonechange_finished:
            self.zonechange_finished = False
            return True
        else:
            return False

    def start(self):
        """
        Begins real-time tracking of the log file by launching the follow method in a new thread.
        """
        log.debug("Reading logfile: %s", self.logpath)
        self.__running = True
        t1 = threading.Thread(target=self.follow)
        self.thread = t1
        t1.start()

    def stop(self):
        """
        Stops real-time tracking of the log file. This method also cleans up the player's hand and board
        states and closes the log file.
        """

        log.debug("Closing logfile: %s", self.logpath)
        self.__running = False
        self.cleanHand()
        self.cleanBoard()
        self.logfile.close()

    def cleanHand(self):
        """
        Clears the player's hand state.
        """
        self.cardsInHand = []

    def getHand(self):
        """
        Retrieves the player's current hand.

        Returns:
            list: List of cards in the player's hand.
        """
        return self.cardsInHand

    def cleanBoard(self):
        """
        Clears the player's and enemy's board states.
        """
        self.myBoard = {}
        self.mercsId = {}
        self.enemiesBoard = {}
        self.enemiesId = {}

    def getMyBoard(self):
        """
        Retrieves the current state of the player's board.

        Returns:
            dict: Dictionary representing the player's board. Keys are the positions, and values are the corresponding card names.
        """
        return {key: self.mercsId[self.myBoard[key]] for key in self.myBoard.keys()}

    def getEnemyBoard(self):
        """
        Retrieves the current state of the enemy's board.

        Returns:
            dict: Dictionary representing the enemy's board. Keys are the positions, and values are the corresponding card names.
        """
        return {
            key: self.enemiesId[self.enemiesBoard[key]]
            for key in self.enemiesBoard.keys()
        }
