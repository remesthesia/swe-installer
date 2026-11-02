import os
import shutil
import ssl
import subprocess
import sys
from io import BytesIO
from urllib import request
from urllib.request import urlretrieve, urlopen
from zipfile import ZipFile

import vdf

from swe_installer import constants, paths

steam_username = ""
context = ssl._create_unverified_context()


def download_depot_downloader():
    paths.app_cache_dir().mkdir(parents=True, exist_ok=True)
    paths.app_data_dir().mkdir(parents=True, exist_ok=True)

    if not paths.depot_downloader_executable_path().exists():
        if not paths.depot_downloader_archive_path().exists():
            urlretrieve(constants.DEPOT_DOWNLOADER_URLS[sys.platform], paths.depot_downloader_archive_path())

        with ZipFile(paths.depot_downloader_archive_path()) as archive:
            archive.extractall(paths.depot_downloader_dir())

        if sys.platform == "linux":
            os.chmod(paths.depot_downloader_executable_path(), 0o755)

def download_ror2():
    global steam_username
    steam_username = input("Enter account username for Steam: ")

    subprocess.run([
        paths.depot_downloader_executable_path(),
        "-username", steam_username,
        "-remember-password",
        "-app", constants.ROR2_APP_ID,
        "-depot", constants.ROR2_DEPOT_ID,
        "-manifest", constants.ROR2_MANIFEST_ID,
        "-dir", paths.ror2_download_path()
    ])

def downgrade_ror2():
    shutil.rmtree(paths.ror2_directory(), ignore_errors=True)
    shutil.copytree(paths.ror2_download_path(), paths.ror2_directory())

def install_bepinex():
    with urlopen(request.Request(constants.BEPINEX_URL, headers={"User-Agent": constants.APP_NAME}), context=context) as response:
        with ZipFile(BytesIO(response.read())) as archive:
            archive.extractall(paths.bepinex_install_dir())

    shutil.copytree(f"{paths.bepinex_install_dir()}/BepInExPack", paths.ror2_directory(), dirs_exist_ok=True)

def fix_bepinex_linux():
    if sys.platform == "linux":
        with open(f"{paths.steam_dir()}/config/loginusers.vdf") as f:
            for id, info in dict(vdf.load(f)["users"]).items():
                if steam_username == info["AccountName"]:
                    steam_id = int(id) - 76561197960265728


        with open(f"{paths.steam_dir()}/userdata/{steam_id}/config/localconfig.vdf") as f:
            src = vdf.load(f)
            node = src
            for part in ["UserLocalConfigStore", "Software", "Valve", "Steam", "apps", constants.ROR2_APP_ID]:
                node = node[part]

            node["LaunchOptions"] = "WINEDLLOVERRIDES=\"winhttp=n,b\" %command%"

        with open(f"{paths.steam_dir()}/userdata/{steam_id}/config/localconfig.vdf", "w") as f:
            vdf.dump(src, f, pretty=True)

def install_ror2bepinexpack():
    with urlopen(request.Request(constants.ROR2BEPINEXPACK_URL, headers={"User-Agent": constants.APP_NAME}), context=context) as response:
        with ZipFile(BytesIO(response.read())) as archive:
            archive.extractall(paths.ror2bepinexpack_install_dir())

    shutil.copytree(f"{paths.ror2bepinexpack_install_dir()}/BepInEx", f"{paths.ror2_directory()}/BepInEx", dirs_exist_ok=True)

def install_hookgenpatcher():
    with urlopen(request.Request(constants.HOOKGENPATCHER_URL, headers={"User-Agent": constants.APP_NAME}), context=context) as response:
        with ZipFile(BytesIO(response.read())) as archive:
            archive.extractall(paths.hookgenpatcher_install_dir())

    shutil.copytree(f"{paths.hookgenpatcher_install_dir()}/BepInEx", f"{paths.ror2_directory()}/BepInEx", dirs_exist_ok=True)

def install_lighterpatcher():
    with urlopen(request.Request(constants.LIGHTERPATCHER_URL, headers={"User-Agent": constants.APP_NAME}), context=context) as response:
        with ZipFile(BytesIO(response.read())) as archive:
            archive.extractall(paths.lighterpatcher_install_dir())

    shutil.copytree(f"{paths.lighterpatcher_install_dir()}/BepInEx", f"{paths.ror2_directory()}/BepInEx", dirs_exist_ok=True)

def install():
    print("If on Linux, please make sure Steam is closed before continuing.")
    download_depot_downloader()
    download_ror2()
    downgrade_ror2()
    install_bepinex()
    install_ror2bepinexpack()
    install_hookgenpatcher()
    install_lighterpatcher()
    fix_bepinex_linux()