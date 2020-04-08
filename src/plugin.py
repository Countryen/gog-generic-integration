import sys
import os
from galaxy.api.plugin import Plugin, create_and_run_plugin
from galaxy.api.consts import Platform, LicenseType
from galaxy.api.types import Game, Authentication, LicenseInfo
from typing import Dict, List, Optional
from datetime import datetime

class GenericTextFilePlugin(Plugin):
    def __init__(self, reader, writer, token):
        super().__init__(
            # Not working: generic, unknown
            #Platform.Test, # Testing Purposes
            Platform.Beamdog, # Substitute until Platform.BigFishGames is available
            "0.1",
            reader,
            writer,
            token
        )

    #implement methods
    async def authenticate(self, stored_credentials=None):
        """
        Not needed, but needs to return for GOG to work. 
        INTEGRATION
        """
        return Authentication("games.data", "games.data")

    async def get_owned_games(self) -> List[Game]:
        """
        Returns games for currently logged in user.
        Reads the games.data file and returns each line as a game.
        INTEGRATION
        """

        # First read games.data file (UTF-8)
        datagamestext = ""
        curdir = os.path.dirname(__file__)
        datafile = os.path.join(curdir, 'games.data')
        with open(datafile, 'r', encoding="utf-8") as f: datagamestext = f.read()

        # Each game's title is on one line
        datagames = datagamestext.splitlines()    

        # Create Game-Array to return
        # Game-ID is just an incremented number + current date_time as string to make it unique
        # UTF-8 is allowed ((tm) , (r) , äöü , etc.)
        games = []
        now = datetime.now()
        i = 0
        for gamename in datagames:
            
            # See: galaxy.api.types.Game
            game = Game(
                game_id = "{0}-{1}-{2}".format("GAME_FROM_DATA_FILE", i, now.strftime("%Y%m%d%H%M%S")), 
                game_title = gamename.strip(), 
                dlcs = [], 
                license_info = LicenseInfo(LicenseType.SinglePurchase)
                )
            games.append(game)
            i += 1  

        return games

def main():
    """INTEGRATION: run plugin event loop"""
    create_and_run_plugin(PluginExample, sys.argv)

def dirtydebug(path, text):
    """Dirty Debug Helper to log text to a file"""
    with open(path, 'a') as f: f.write(text)

# INTEGRATION: run plugin event loop
if __name__ == "__main__":
    main()