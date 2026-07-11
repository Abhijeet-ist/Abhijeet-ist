from .models import GitHubStats
from typing import Any

class Statistics:

    def __init__(self, user: dict[str, Any]):

        self.user = user

    def calculate(self):

        repos = self.user["repositories"]["nodes"]

        total_stars = sum(
            repo["stargazerCount"]
            for repo in repos
        )

        total_forks = sum(
            repo["forkCount"]
            for repo in repos
        )

        total_commits = 0

        for repo in repos:

            branch = repo.get("defaultBranchRef")

            if branch is None:
                continue

            target = branch.get("target")

            if target is None:
                continue

            total_commits += target["history"]["totalCount"]

        contrib = self.user["contributionsCollection"]

        return GitHubStats(

            username=self.user["login"],

            name=self.user["name"],

            followers=self.user["followers"]["totalCount"],

            following=self.user["following"]["totalCount"],

            repositories=self.user["repositories"]["totalCount"],

            contributed_repositories=contrib[
                "totalRepositoryContributions"
            ],

            commits=total_commits,

            pull_requests=contrib[
                "totalPullRequestContributions"
            ],

            issues=contrib[
                "totalIssueContributions"
            ],

            stars=total_stars,

            forks=total_forks,

        )