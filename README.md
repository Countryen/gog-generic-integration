# Generic Text File Integration for GOG Galaxy 2.0
Unofficial, community, substitute integration using the official https://github.com/gogcom/galaxy-integrations-python-api.
The idea is, that you don't wan't to add all "shelf games" or games in stores that GOG not supports right now (like BigFishGames) by hand to your GOG Galaxy 2.0 Library. 

This integration allows you to put all games into a simple csv file (id;title) and loads these games into your library.

# Any Questions/Problems?
Feel free to open an issue (in English prefered, but German is also ok).

# How To Install
1. Download the source code from the latest [release](https://github.com/Countryen/gog-generic-integration/releases)
2. Unzip the downloaded file into any folder and open the folder inside
3. Inside `install/` open `games.csv` and fill in your games (each row one game, id must be unique but can be whatever you want).
4. Inside `install/` execute `install.ps1` 
5. Tell the script which [platform](https://github.com/gogcom/galaxy-integrations-python-api/blob/master/PLATFORM_IDs.md) you want to use.

# About The Games CSV File

# About The Platform

# About Deployment and Manual Installation

	



# How to Use
- Clone/Download latest release source code
- Unzip into any folder on your desktop
- Put your games into /install/games.data (each line one game)
- Execute /install/install.ps1
- Or do it manually:
	- create folder: `%LocalAppData%\GOG.com\Galaxy\plugins\installed\c0_generic-55cc6f22-6b51-441e-9b8f-c1bb59d035de`
	- put all files and folders inside `src` into that new folder
	- put `install/games.data` into that new folder
- Restart/Start GOG Galaxy 2.0 client
- Connect via options
- To remove just disconnect via options, all games (and tags and stuff) are removed.

# Notes
- Games can have **UTF-8** titles like (tm), (r), €, äöü, etc.
- Only Titles are loaded, **images and details** are loaded by GOG itself but only if the title matches a game existing on GOG 
- Only tested on windows, but should work for other platforms, too.

# Development
- [Python 3.8](https://www.python.org/downloads/release/python-382/)
- [VSCode with Python Extension](https://code.visualstudio.com/docs/python/python-tutorial#_install-and-use-packages)
- Clone and change code
- Main file: `src/plugin.py`
- Change manifest for a new GUID and Platform ID ("test" works but not well), change Platform ID in `src/plugin.py`, too
- See `install/install.ps1` to deploy

# Dev Notes
- manifest.json and games.csv MUST BE utf-8 w/o BOM or it won't work.
- The plugin needs to implement authenticate (and return the Authentication) or it won't connect.
- The plugin needs to implement at least one of the get_... methods, or it will get stuck connecting.
- The plugin keeps disconnecting on close of GOG if no data is persisted (credentials)
- Platform "test" does behave weird (should not be used) and doesn't stay connected after close of GOG
- Platform ID in the `src/manifest.json` and the `src/plugin.py` needs to be the same.
- How to persist data: `self.persistent_cache["c0_empty_stub"] = "Test" , self.push_cache()`

# Helper: Upgrading older games.data -> games.csv
The old version used a simple text file with each game in a row like
````
Game 1
Game 2
...
````
The new version is a csv file with added (unique) ID.
This little PowerShell script reads an existing `games.data` and outputs the games + an individual GUID as ID as the expected format.

Just copy & paste the whole script into PowerShell (from inside the folder containing the `games.data`).
A new `games.csv` will be created next to the old file.
````
. {
    $CRLF = [Environment]::NewLine
    $data = gc "games.data"
    $datagames = $data.Split($CRLF)
    $games = $datagames | % { "$(New-Guid);$_"  }
    $csvgames = [string]::Join($CRLF, $games)
    $csv = "id;title" + $CRLF + $csvgames
    [System.IO.File]::WriteAllText("$((gi .).FullName)\games.csv", $csv)
}
````

# References
- https://www.gog.com/forum/general_beta_gog_galaxy_2.0/is_there_a_simple_noobfriendly_step_by_step_instruction_on_how_to_install_community_integrations
- https://pypi.org/
- [Integration for Discord by ertego (not affiliated with), used as a reference/example](https://github.com/Ertego/gog-galaxy-discord)
