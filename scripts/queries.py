USER_QUERY = """
query($login: String!, $cursor: String) {

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
      after: $cursor

      ownerAffiliations: OWNER

      orderBy: {
        field: UPDATED_AT
        direction: DESC
      }

    ) {

      totalCount

      pageInfo {

        hasNextPage
        endCursor

      }

      nodes {

  name

  nameWithOwner

  url

  isPrivate

  isFork

  stargazerCount

  forkCount

  pushedAt

  defaultBranchRef {

    target {

      ... on Commit {

        oid

        history {
          totalCount
        }

      }

    }

  }

}
"""
