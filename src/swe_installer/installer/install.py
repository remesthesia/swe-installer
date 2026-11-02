import os
import shutil
import subprocess
import sys
from urllib.request import urlretrieve
from zipfile import ZipFile

from swe_installer import constants, paths


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

def install():
    download_depot_downloader()
    download_ror2()
    downgrade_ror2()