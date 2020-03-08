import requests

repo_url = "https://api.github.com/search/repositories?q=org:{organization}&sort=forks&order=desc&per_page={count}"
contributors_url = "https://api.github.com/repos/{organization}/{repo}/stats/contributors"
user_url = "https://api.github.com/users/{user}"
#Add your own Token
token = ""

headers = {
    "Authorization": "Token " + token
}


def get_repos(org, n):
    repos_json = requests.get(repo_url.format(organization=org,count=n), headers=headers).json()
    repos = []
    for i in repos_json["items"]:
        repos.append((i['forks_count'], i["name"], i["html_url"]))
    return repos


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

#(Organization github id,n,m)
get_org_contribution("microsoft", 6, 4)
