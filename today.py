import json

from pathlib import Path

from scripts.github_api import GitHubAPI


github = GitHubAPI()

user = github.get_user()

Path("github.json").write_text(

    json.dumps(user, indent=4),

    encoding="utf-8"

)

print("GitHub data saved.")