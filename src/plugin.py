import asyncio
import csv
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

from galaxy.api.consts import LicenseType, Platform
from galaxy.api.plugin import Plugin, create_and_run_plugin
from galaxy.api.types import Authentication, Game, LicenseInfo

now = datetime.now()
curentdir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)


class CsvFilePlugin(Plugin):
    def __init__(self, reader, writer, token):
        manifest = read_manifest()
        super().__init__(
            # Not working: generic, unknown
            manifest["platform"],  # Platform.Something
            manifest["version"],  # "1.0"
            reader,
            writer,
            token
        )

    async def authenticate(self, stored_credentials=None):
        """
        Not needed, but needs to return a galaxy.api.types.Authentication for GOG to work.\n
        Also, to stay connected we need to persist credentials here (locally in the plugin's .db file).\n
        Overrides Plugin.authenticate
        """
        # Use stored_credentials (persisted locally in the plugin's .db-file) or create new creds and store them immediately
        new_credentials = dict(
            {"user_id": "games.csv", "user_name": "games.csv"})
        creds = stored_credentials or new_credentials
        self.store_credentials(creds)
        return Authentication(creds["user_id"], creds["user_name"])

    async def get_owned_games(self) -> List[Game]:
        """
        Returns games for currently logged in user.\n
        See: get_games_from_csv.\n
        Overrides Plugin.get_owned_games
        """
        return await self.get_games_from_csv()

    async def get_games_from_csv(self) -> List[Game]:
        """
        Reads the games.csv file and returns each row as a galaxy.api.types.Game.\n
        The games are stored/provided in a UTF-8 CSV file (id;title)
        """
        games = []
        gamesfilepath = os.path.join(curentdir, 'games.csv')
        logger.info("Start reading games from file: {}".format(gamesfilepath))
        with open(gamesfilepath, 'r', encoding="utf-8") as gamesfile:
            for row in csv.DictReader(gamesfile, delimiter=";", quotechar="\"", quoting=csv.QUOTE_MINIMAL):
                # See: galaxy.api.types.Game
                game = Game(
                    game_id=row["id"].strip(),
                    game_title=row["title"].strip(),
                    dlcs=[],
                    license_info=LicenseInfo(LicenseType.SinglePurchase)
                )
                games.append(game)
        logger.info("Processed {} games".format(len(games)))
        return games


def main():
    """run plugin event loop. INTEGRATION"""
    create_and_run_plugin(CsvFilePlugin, sys.argv)


async def test():
    logging.basicConfig(filename='log.txt', level=logging.DEBUG)
    plugin = CsvFilePlugin(None, None, None)
    dirtydebug("test.txt", "{} {}".format(plugin._platform, plugin._version))
    games = await plugin.get_games_from_csv()
    dirtydebug("test.txt", games)


def dirtydebug(path: str, text: str):
    """Dirty Debug Helper to log text to a file"""
    now = datetime.now()
    nowtext = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(path, 'a') as f:
        f.write("[" + nowtext + "] : ")
        f.write(str(text))
        f.write("\n")


def read_manifest() -> Dict[str, any]:
    """Reads the manifest.json and returns the "platform" (galaxy.api.types.Platform) and "version" (str) to use."""
    platformsmap = dict([
        ("gog", "Gog"),
        ("steam", "Steam"),
        ("psn", "Psn"),
        ("xboxone", "XBoxOne"),
        ("generic", "Generic"),
        ("origin", "Origin"),
        ("uplay", "Uplay"),
        ("battlenet", "Battlenet"),
        ("epic", "Epic"),
        ("bethesda", "Bethesda"),
        ("paradox", "ParadoxPlaza"),
        ("humble", "HumbleBundle"),
        ("kartridge", "Kartridge"),
        ("itch", "ItchIo"),
        ("nswitch", "NintendoSwitch"),
        ("nwiiu", "NintendoWiiU"),
        ("nwii", "NintendoWii"),
        ("ncube", "NintendoGameCube"),
        ("riot", "RiotGames"),
        ("wargaming", "Wargaming"),
        ("ngameboy", "NintendoGameBoy"),
        ("atari", "Atari"),
        ("amiga", "Amiga"),
        ("snes", "SuperNintendoEntertainmentSystem"),
        ("beamdog", "Beamdog"),
        ("d2d", "Direct2Drive"),
        ("discord", "Discord"),
        ("dotemu", "DotEmu"),
        ("gamehouse", "GameHouse"),
        ("gmg", "GreenManGaming"),
        ("weplay", "WePlay"),
        ("zx", "ZxSpectrum"),
        ("vision", "ColecoVision"),
        ("nes", "NintendoEntertainmentSystem"),
        ("sms", "SegaMasterSystem"),
        ("c64", "Commodore64"),
        ("pce", "PcEngine"),
        ("segag", "SegaGenesis"),
        ("neo", "NeoGeo"),
        ("sega32", "Sega32X"),
        ("segacd", "SegaCd"),
        ("3do", "_3Do"),
        ("saturn", "SegaSaturn"),
        ("psx", "PlayStation"),
        ("ps2", "PlayStation2"),
        ("n64", "Nintendo64"),
        ("jaguar", "AtariJaguar"),
        ("dc", "SegaDreamcast"),
        ("xboxog", "Xbox"),
        ("amazon", "Amazon"),
        ("gg", "GamersGate"),
        ("egg", "Newegg"),
        ("bb", "BestBuy"),
        ("gameuk", "GameUk"),
        ("fanatical", "Fanatical"),
        ("playasia", "PlayAsia"),
        ("stadia", "Stadia"),
        ("arc", "Arc"),
        ("eso", "ElderScrollsOnline"),
        ("glyph", "Glyph"),
        ("aionl", "AionLegionsOfWar"),
        ("aion", "Aion"),
        ("blade", "BladeAndSoul"),
        ("gw", "GuildWars"),
        ("gw2", "GuildWars2"),
        ("lin2", "Lineage2"),
        ("ffxi", "FinalFantasy11"),
        ("ffxiv", "FinalFantasy14"),
        ("totalwar", "TotalWar"),
        ("winstore", "WindowsStore"),
        ("elites", "EliteDangerous"),
        ("star", "StarCitizen"),
        ("psp", "PlayStationPortable"),
        ("psvita", "PlayStationVita"),
        ("nds", "NintendoDs"),
        ("3ds", "Nintendo3Ds"),
        ("pathofexile", "PathOfExile"),
        ("twitch", "Twitch"),
        ("minecraft", "Minecraft"),
        ("gamesessions", "GameSessions"),
        ("nuuvem", "Nuuvem"),
        ("fxstore", "FXStore"),
        ("indiegala", "IndieGala"),
        ("playfire", "Playfire"),
        ("oculus", "Oculus"),
        ("test", "Test"),
        ("rockstar", "Rockstar")])

    with open(os.path.join(curentdir, "manifest.json"), "r") as f:
        text = f.read()
        j = json.loads(text)
        platformid = j["platform"]
        version = j["version"]
        platform = platformsmap[platformid]
        return dict([("platform", Platform[platform]), ("version", version)])


if __name__ == "__main__":
    main()
    # asyncio.run(test())
