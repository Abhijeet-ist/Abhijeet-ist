from dataclasses import dataclass


@dataclass
class GitHubStats:

    username: str

    name: str | None

    followers: int

    following: int

    repositories: int

    contributed_repositories: int

    commits: int

    pull_requests: int

    issues: int

    stars: int

    forks: int