# Generic Text File Integration for GOG Galaxy 2.0
Unofficial, community, substitute integration using the official https://github.com/gogcom/galaxy-integrations-python-api.
The idea is, that you don't wan't to add all "shelf games" or games in stores that GOG not supports right now (like BigFishGames) by hand to your GOG Galaxy 2.0 Library. 

This integration allows you to put all titles in a simple text file and loads this text file as games into your library.

# Any Questions/Problems?
Feel free to open an issue (in English prefered, but German is also ok).

**See note about used Platform ID to see why it connects as fake "Beamdog" below.**

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
- Only Titles are provided, **images and details** are loaded by GOG itself but only if the title matches a game existing on GOG
- **Why does it use the Beamdog Platform ID:** GOG currently does support a "generic" platform ID, but it doesn't work. As there is no available platform ID that says "custom" and you are limited to officially supported ones, I just chose one. If you already use Beamdog but still want this integration, change the Platform ID in the `src/manifest.json` and the `src/plugin.py` prior to installation to whatever suits you.
- Only tested on windows, but should work for other platforms, too.

# Development
- [Python 3.8](https://www.python.org/downloads/release/python-382/)
- [VSCode with Python Extension](https://code.visualstudio.com/docs/python/python-tutorial#_install-and-use-packages)
- Clone and change code
- Main file: `src/plugin.py`
- Change manifest for a new GUID and Platform ID ("test" works but not well), change Platform ID in `src/plugin.py`, too
- See `install/install.ps1` to deploy

# References
- https://www.gog.com/forum/general_beta_gog_galaxy_2.0/is_there_a_simple_noobfriendly_step_by_step_instruction_on_how_to_install_community_integrations
- https://pypi.org/
- [Integration for Discord by ertego (not affiliated with), used as a reference/example](https://github.com/Ertego/gog-galaxy-discord)
