import platformdirs
import SteamPathFinder as steampathfinder

from pathlib import Path
from swe_installer.constants import APP_NAME, APP_AUTHOR

def app_cache_dir() -> Path:
    return Path(platformdirs.user_cache_dir(APP_NAME, APP_AUTHOR))

def app_data_dir() -> Path:
    return Path(platformdirs.user_data_dir(APP_NAME, APP_AUTHOR))

def steam_path() -> Path:
    return steampathfinder.get_steam_path()