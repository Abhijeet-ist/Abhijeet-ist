USER_QUERY = """
query($login: String!) {
  user(login: $login) {

    login
    name
    followers {
      totalCount
    }

    following {
      totalCount
    }

    repositories(
      first: 100
      ownerAffiliations: OWNER
      orderBy: {
        field: UPDATED_AT,
        direction: DESC
      }
    ) {

      totalCount

      nodes {

        name
        stargazerCount
        forkCount
        isFork
        isPrivate

        defaultBranchRef {

          target {

            ... on Commit {

              history {
                totalCount
              }

            }

          }

        }

      }

    }

    contributionsCollection {

      totalCommitContributions

      totalPullRequestContributions

      totalIssueContributions

      totalRepositoryContributions

    }

  }

}
"""