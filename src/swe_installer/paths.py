import sys

import platformdirs
import srctools.steam

from pathlib import Path


from swe_installer import constants
from swe_installer.constants import APP_NAME, APP_AUTHOR

def app_cache_dir() -> Path:
    return Path(platformdirs.user_cache_dir(APP_NAME, APP_AUTHOR))

def app_data_dir() -> Path:
    return Path(platformdirs.user_data_dir(APP_NAME, APP_AUTHOR))

def depot_downloader_dir() -> Path:
    return Path(f"{installer_tools_dir()}/Depot Downloader")

def bepinex_install_dir() -> Path:
    return Path(f"{installer_installs_dir()}/BepInEx")

def ror2bepinexpack_install_dir() -> Path:
    return Path(f"{installer_installs_dir()}/RoR2BepInExPack")

def hookgenpatcher_install_dir() -> Path:
    return Path(f"{installer_installs_dir()}/HookGenPatcher")

def lighterpatcher_install_dir() -> Path:
    return Path(f"{installer_installs_dir()}/LighterPatcher")


def depot_downloader_executable_path() -> Path:
    return Path(f"{depot_downloader_dir()}/{"DepotDownloader.exe" if sys.platform == "windows" else "DepotDownloader"}")

def steam_dir() -> Path:
    return srctools.steam.get_steam_install_path()

def steam_config_path() -> Path:
    return Path(f"{steam_dir()}/config/config.vdf")

def installer_tools_dir() -> Path:
    return Path(f"{app_data_dir()}/Tools")

def installer_installs_dir() -> Path:
    return Path(f"{app_data_dir()}/Installs")

def depot_downloader_archive_path() -> Path:
    return Path(f"{app_cache_dir()}/Depot Downloader.zip")

def ror2_download_path() -> Path:
    return Path(f"{installer_installs_dir()}/RoR2/{constants.ROR2_DEPOT_ID}-{constants.ROR2_MANIFEST_ID}")

def ror2_directory() -> Path:
    return srctools.steam.find_app(int(constants.ROR2_APP_ID)).path
