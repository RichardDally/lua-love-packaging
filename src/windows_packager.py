import os
import pathlib
import zipfile
import wget
import shutil
from loguru import logger
from pathlib import Path


class WindowsPackager:
    def __init__(self):
        self.love_version = "11.4"
        self.love_filename = f"love-{self.love_version}-win64.zip"
        self.love_directory = f"love-{self.love_version}-win64"
        self.love_executable = "love.exe"
        self.love_executable_path = Path(self.love_directory, "love.exe")
        self.love_url = f"https://github.com/love2d/love/releases/download/{self.love_version}/{self.love_filename}"
        self.game_filename = "stone-kingdoms-master.zip"
        self.game_url = f"https://gitlab.com/stone-kingdoms/stone-kingdoms/-/archive/master/{self.game_filename}"
        self.game_archive_filename = "stone-kingdoms.love"
        self.game_executable_filename = "stone-kingdoms.exe"

    def create_package(self) -> None:
        self._download_love()
        self._download_game()
        self._create_game_archive()
        self._create_game_executable()

    def _download_love(self) -> None:
        if not os.path.exists(self.love_directory):
            if not os.path.exists(self.love_filename):
                logger.info(f"Downloading [{self.love_filename}] from [{self.love_url}]")
                wget.download(self.love_url, self.love_filename)
            logger.info(f"Extracting [{self.love_filename}]")
            shutil.unpack_archive(self.love_filename, ".")

    def _download_game(self) -> None:
        if not os.path.exists(Path(self.game_filename).stem):
            if not os.path.exists(self.game_filename):
                logger.info(f"Downloading game [{self.game_filename}] from [{self.game_url}]")
                wget.download(self.game_url, self.game_filename)
            shutil.unpack_archive(self.game_filename, ".")

    def _create_game_archive(self) -> None:
        if not os.path.exists(self.game_archive_filename):
            logger.info(f"Creating game archive [{self.game_archive_filename}]")
            directory = pathlib.Path("stone-kingdoms-master/")
            with zipfile.ZipFile(self.game_archive_filename, mode="w") as archive:
                for file_path in directory.rglob("*"):
                    archive.write(file_path, arcname=file_path.relative_to(directory))

    def _create_game_executable(self) -> None:
        if not os.path.exists(self.game_executable_filename):
            logger.info(f"Creating game executable [{self.game_executable_filename}]")
            with open(self.game_archive_filename, "rb") as game_archive:
                with open(self.love_executable_path, "rb") as love_executable:
                    with open(self.game_executable_filename, "wb") as game_executable:
                        game_executable.write(love_executable.read())
                    with open(self.game_executable_filename, "ab") as game_executable:
                        game_executable.write(game_archive.read())
