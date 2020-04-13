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
    create_and_run_plugin(GenericTextFilePlugin, sys.argv)

def dirtydebug(path, text):
    """Dirty Debug Helper to log text to a file"""
    with open(path, 'a') as f: f.write(text)

# INTEGRATION: run plugin event loop
if __name__ == "__main__":
    main()

### self._register_method:
# "init_authentication"
# "pass_login_credentials"
# "import_owned_games"
# "start_achievements_import"
# "import_local_games"
# "start_game_times_import"
# "start_game_library_settings_import"
# "start_os_compatibility_import"
# "start_user_presence_import"
# "start_local_size_import"
# "import_subscriptions"
# "start_subscription_games_import"

### self._detect_feature:
# Feature.ImportOwnedGames, ["get_owned_games"])
# Feature.ImportAchievements, ["get_unlocked_achievements"])
# Feature.ImportInstalledGames, ["get_local_games"])
# Feature.LaunchGame, ["launch_game"])
# Feature.InstallGame, ["install_game"])
# Feature.UninstallGame, ["uninstall_game"])
# Feature.ShutdownPlatformClient, ["shutdown_platform_client"])
# Feature.ImportGameTime, ["get_game_time"])
# Feature.LaunchPlatformClient, ["launch_platform_client"])
# Feature.ImportFriends, ["get_friends"])
# Feature.ImportGameLibrarySettings, ["get_game_library_settings"])
# Feature.ImportOSCompatibility, ["get_os_compatibility"])
# Feature.ImportUserPresence, ["get_user_presence"])
# Feature.ImportLocalSize, ["get_local_size"])
# Feature.ImportSubscriptions, ["get_subscriptions"])
# Feature.ImportSubscriptionGames, ["get_subscription_games"])

### self._register_notification
# "launch_game"
# "install_game"
# "uninstall_game"
# "shutdown_platform_client"
# "launch_platform_client"       