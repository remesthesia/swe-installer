import os
import subprocess
import sys
import tempfile
from zipfile import ZipFile

import platformdirs
from pathlib import Path
from urllib.request import urlretrieve

DEPOT_DOWNLOADER_LINUX_URL = "https://github.com/SteamRE/DepotDownloader/releases/latest/download/DepotDownloader-linux-x64.zip"
DEPOT_DOWNLOADER_WINDOWS_URL = "https://github.com/SteamRE/DepotDownloader/releases/latest/download/DepotDownloader-windows-x64.zip"

ROR2_APP_ID = "632360"
ROR2_DEPOT_ID = "632361"
ROR2_MANIFEST_ID = "2538203695974683966"

cache_dir = platformdirs.user_cache_dir(appname="SwE Installer", appauthor="Remesthesia")
os.makedirs(cache_dir, exist_ok=True)

depot_downloader_archive = Path(cache_dir + "/depot-downloader.zip")
if not depot_downloader_archive.exists():
    if sys.platform == "win32":
        urlretrieve(DEPOT_DOWNLOADER_WINDOWS_URL, depot_downloader_archive)
    elif sys.platform == "linux":
        urlretrieve(DEPOT_DOWNLOADER_LINUX_URL, depot_downloader_archive)

depot_downloader: Path = Path(f"{platformdirs.user_data_dir(appname="SwE Installer", appauthor="Remesthesia")}/depot_downloader")
print(depot_downloader)
if not depot_downloader.exists():
    with ZipFile(depot_downloader_archive, "r") as archive:
        archive.extractall(depot_downloader)

if sys.platform == "linux":
    os.chmod(str(depot_downloader) + "/DepotDownloader", 0o755)

ror2_path = f"{platformdirs.user_data_dir(appname="SwE Installer", appauthor="Remesthesia")}/ror2-{ROR2_DEPOT_ID}-{ROR2_MANIFEST_ID}"

steam_username = input("Enter account username for Steam: ")
if sys.platform == "win32":
    subprocess.run([
        str(str(depot_downloader) + "/DepotDownloader.exe"),
        "-username", steam_username,
        "-remember-password",
        "-app", ROR2_APP_ID,
        "-depot", ROR2_DEPOT_ID,
        "-manifest", ROR2_MANIFEST_ID,
        "-dir", ror2_path
    ])
elif sys.platform == "linux":
    subprocess.run([
        str(str(depot_downloader) + "/DepotDownloader"),
        "-username", steam_username,
        "-remember-password",
        "-app", ROR2_APP_ID,
        "-depot", ROR2_DEPOT_ID,
        "-manifest", ROR2_MANIFEST_ID,
        "-dir", ror2_path
    ])
