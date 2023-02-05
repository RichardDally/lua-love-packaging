import os
import wget
import shutil
from loguru import logger
from pathlib import Path
from git.repo.base import Repo


def download_love():
    version = "11.4"
    filename = f"love-{version}-win64.zip"
    if not os.path.exists(f"love-{version}-win64"):
        if not os.path.exists(filename):
            logger.info(f"Downloading {filename}")
            url = f"https://github.com/love2d/love/releases/download/{version}/{filename}"
            wget.download(url, filename)
        logger.info(f"Extracting {filename}")
        shutil.unpack_archive(filename, ".")


def download_game():
    filename = "stone-kingdoms-master.zip"
    if not os.path.exists(Path(filename).stem):
        if not os.path.exists(filename):
            logger.info(f"Downloading {filename}")
            url = f"https://gitlab.com/stone-kingdoms/stone-kingdoms/-/archive/master/{filename}"
            wget.download(url, filename)
        shutil.unpack_archive(filename, ".")


def clone_repository():
    repository_name = "stone-kingdoms"
    if not os.path.exists(repository_name):
        logger.info(f"Cloning {repository_name} repository")
        Repo.clone_from(url="https://gitlab.com/stone-kingdoms/stone-kingdoms.git", to_path=Path(repository_name))


def create_game_archive():
    """
    TODO: remove stone-kingdoms-master directory within archive...
    """
    shutil.make_archive(
        base_name="stone-kingdoms",
        format='zip',
        root_dir='.',
        base_dir='stone-kingdoms-master/.',
    )


download_love()
# clone_repository()
download_game()
create_game_archive()
