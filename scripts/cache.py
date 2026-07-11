from pathlib import Path
import json


CACHE_FILE = Path("cache/repository_cache.json")


class Cache:

    def __init__(self):

        if CACHE_FILE.exists():

            self.data = json.loads(CACHE_FILE.read_text())

        else:

            self.data = {}

    def get(self, repo):

        return self.data.get(repo)

    def set(self, repo, value):

        self.data[repo] = value

    def save(self):

        CACHE_FILE.write_text(

            json.dumps(

                self.data,

                indent=4

            )

        )