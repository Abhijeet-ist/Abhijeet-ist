from pathlib import Path
import subprocess
import shutil

from .cache import Cache
from .utils import count_lines


TEMP_DIR = Path("temp")


class LOCEngine:

    def __init__(self):

        self.cache = Cache()

    def clone(self, url, directory):

        subprocess.run(

            [

                "git",

                "clone",

                "--depth",

                "1",

                url,

                str(directory)

            ],

            check=True

        )

    def repository_loc(self, url, repo_name, sha):

        cached = self.cache.get(repo_name)

        if cached and cached["sha"] == sha:

            return cached["loc"]

        directory = TEMP_DIR / repo_name.split("/")[-1]

        if directory.exists():

            shutil.rmtree(directory)

        self.clone(url, directory)

        loc = count_lines(directory)

        shutil.rmtree(directory)

        self.cache.set(

            repo_name,

            {

                "sha": sha,

                "loc": loc

            }

        )

        return loc