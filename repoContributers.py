import requests

repo_url = "https://api.github.com/users/{organization}/repos"
contributors_url = "https://api.github.com/repos/{organization}/{repo}/stats/contributors"
user_url = "https://api.github.com/users/{user}"
token = "a185d8545d8121ac232f75ee7628300f86b73fa4"

headers = {
    "Authorization": "Token " + token
}


def get_repos(org, n):
    repos_json = requests.get(repo_url.format(organization=org), headers=headers).json()
    repos = []
    for i in repos_json:
        repos.append((i['forks_count'], i["name"], i["html_url"]))
    repos.sort(reverse=True)
    if (len(repos) <= n):
        return repos
    else:
        return repos[0:n]


def get_contributors(org, repo, m):
    contributors_json = requests.get(contributors_url.format(organization=org, repo=repo), headers=headers).json()
    contributors = []
    for i in contributors_json:
        contributors.append((i["total"], i["author"]["login"], i["author"]["html_url"]))
    contributors.sort(reverse=True)
    if (len(contributors) <= m):
        return contributors
    else:
        return contributors[0:m]


def get_org_contribution(org, n, m):
    repos = get_repos(org, n)
    for re in repos:
        print("Repo-id: " + re[1] + " ,Url: " + re[2] + " ,Fork Count: " + str(re[0]))
        contributors = get_contributors(org, re[1], m)
        for j in contributors:
            print("\tUsername: " + j[1] + " ,User url: " + j[2] + " ,Commit Count: " + str(j[0]))
        print("\n")


get_org_contribution("microsoft", 6, 4)
