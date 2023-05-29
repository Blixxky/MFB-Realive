import time
import re
from pathlib import Path
import threading
import logging

log = logging.getLogger(__name__)


class LogHSMercs:
    def __init__(self, logpath):
        """Generator function that yields new lines in filelog to
        follow cards in hand and on the battlefield.
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
        # Start an infinite loop to read the log file
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
        if self.zonechange_finished:
            self.zonechange_finished = False
            return True
        else:
            return False

    def start(self):
        log.debug("Reading logfile: %s", self.logpath)
        self.__running = True
        t1 = threading.Thread(target=self.follow)
        self.thread = t1
        t1.start()

    def stop(self):
        log.debug("Closing logfile: %s", self.logpath)
        self.__running = False
        self.cleanHand()
        self.cleanBoard()
        self.logfile.close()

    def cleanHand(self):
        self.cardsInHand = []

    def getHand(self):
        return self.cardsInHand

    def cleanBoard(self):
        self.myBoard = {}
        self.mercsId = {}
        self.enemiesBoard = {}
        self.enemiesId = {}

    def getMyBoard(self):
        return {key: self.mercsId[self.myBoard[key]] for key in self.myBoard.keys()}

    def getEnemyBoard(self):
        return {
            key: self.enemiesId[self.enemiesBoard[key]]
            for key in self.enemiesBoard.keys()
        }
