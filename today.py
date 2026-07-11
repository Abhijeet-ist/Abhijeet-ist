from scripts.github_api import GitHubAPI
from scripts.statistics import Statistics
from scripts.svg import SVG

github = GitHubAPI()

user = github.get_user()

stats = Statistics(user).calculate()

SVG(stats).generate()

print("SVG generated successfully.")