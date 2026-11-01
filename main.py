import os
import subprocess

import platformdirs
import sys
from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile

import vdf

DEPOT_DOWNLOADER_URL = f"https://github.com/SteamRE/DepotDownloader/releases/latest/download/DepotDownloader-{"linux" if sys.platform == "linux" else "windows"}-x64.zip"

ROR2_APP_ID = "632360"
ROR2_DEPOT_ID = "632361"
ROR2_MANIFEST_ID = "2538203695974683966"

APP_CACHE_DIRECTORY = platformdirs.user_cache_dir(appname="Somewhere Else", appauthor="Remesthesia")
APP_DATA_DIRECTORY = platformdirs.user_data_dir(appname="Somewhere Else", appauthor="Remesthesia")

Path(APP_CACHE_DIRECTORY).mkdir(parents=True, exist_ok=True)
Path(APP_DATA_DIRECTORY).mkdir(parents=True, exist_ok=True)

DEPOT_DOWNLOADER_ARCHIVE = f"{APP_CACHE_DIRECTORY}/Depot Downloader.zip"
DEPOT_DOWNLOADER_DIRECTORY = f"{APP_DATA_DIRECTORY}/Installer/Depot Downloader"
DEPOT_DOWNLOADER_EXECUTABLE = f"{DEPOT_DOWNLOADER_DIRECTORY}/{"DepotDownloader" if sys.platform == "linux" else "DepotDownloader.exe"}"

ROR2_INSTALL_DIRECTORY = f"{APP_CACHE_DIRECTORY}/Installer/RoR2 Install"
ROR2_UNINSTALL_DIRECTORY = f"{APP_CACHE_DIRECTORY}/Installer/RoR2 Uninstall"

STEAM_ROOT_PATH = ""
STEAM_PATH = ""

ROR2_MANIFEST = ""
ROR2_GAME_DIRECTORY = ""


def resolve_steam_directories():
    global STEAM_ROOT_PATH
    if sys.platform == "linux":
        STEAM_ROOT_PATH = str(Path.home().joinpath(".steam/steam").resolve())
    else:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software/Valve/Steam") as k:
            STEAM_ROOT_PATH = winreg.QueryValueEx(k, "SteamPath")[0]

    with open(f"{STEAM_ROOT_PATH}/steamapps/libraryfolders.vdf") as f:
        libs = vdf.load(f)["libraryfolders"]

    global STEAM_PATH
    STEAM_PATH = str([Path(v["path"]) for v in libs.values()][0])

    global ROR2_MANIFEST
    ROR2_MANIFEST = f"{STEAM_ROOT_PATH}/steamapps/appmanifest_{ROR2_APP_ID}.acf"
    if Path(ROR2_MANIFEST).exists():
        with open(ROR2_MANIFEST) as f:
            path = vdf.load(f)["AppState"]["installdir"]
        global ROR2_GAME_DIRECTORY
        ROR2_GAME_DIRECTORY = f"{STEAM_PATH}/steamapps/common/{path}"



def download_depot_downloader():
    if not Path(DEPOT_DOWNLOADER_EXECUTABLE).exists():
        if not Path(DEPOT_DOWNLOADER_ARCHIVE).exists():
            urlretrieve(DEPOT_DOWNLOADER_URL, DEPOT_DOWNLOADER_ARCHIVE)
        with ZipFile(DEPOT_DOWNLOADER_ARCHIVE, "r") as archive:
            archive.extractall(DEPOT_DOWNLOADER_DIRECTORY)

    if sys.platform == "linux":
        os.chmod(DEPOT_DOWNLOADER_EXECUTABLE, 0o755)

def download_ror2():
    steam_username = input("Enter account username for Steam: ")
    subprocess.run([
        DEPOT_DOWNLOADER_EXECUTABLE,
        "-username", steam_username,
        "-remember-password",
        "-app", ROR2_APP_ID,
        "-depot", ROR2_DEPOT_ID,
        "-manifest", ROR2_MANIFEST_ID,
        "-dir", ROR2_INSTALL_DIRECTORY
    ])

resolve_steam_directories()

print("Cache:" + APP_CACHE_DIRECTORY)
print("Data:" + APP_DATA_DIRECTORY)
print("App:" + platformdirs.user_applications_dir(appname="Somewhere Else", appauthor="Remesthesia"))
print("Config:" + platformdirs.user_config_dir(appname="Somewhere Else", appauthor="Remesthesia"))
print("Root:" + STEAM_ROOT_PATH)
print("Target:" + STEAM_PATH)
print("Manifest:" + ROR2_MANIFEST)
print("Game Directory:" + ROR2_GAME_DIRECTORY)

# download_depot_downloader()
# download_ror2()