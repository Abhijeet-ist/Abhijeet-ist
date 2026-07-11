import os
import requests

from .queries import USER_QUERY


class GitHubAPI:

    def __init__(self):

        self.token = os.environ["ACCESS_TOKEN"]

        self.username = os.environ["USER_NAME"]

        self.endpoint = "https://api.github.com/graphql"

        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }


    def execute(self, query, variables=None):

        response = requests.post(

            self.endpoint,

            headers=self.headers,

            json={

                "query": query,

                "variables": variables or {}

            }

        )

        response.raise_for_status()

        payload = response.json()

        if "errors" in payload:
            raise RuntimeError(payload["errors"])

        return payload["data"]


    def get_user(self):

        return self.execute(

            USER_QUERY,

            {

                "login": self.username

            }

        )["user"]