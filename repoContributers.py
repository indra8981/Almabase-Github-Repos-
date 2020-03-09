import requests

repo_url = "https://api.github.com/search/repositories?q=org:{organization}&sort=forks&order=desc&per_page={count}"
contributors_url = "https://api.github.com/repos/{organization}/{repo}/stats/contributors"
user_url = "https://api.github.com/users/{user}"


# Add your own Token
token = ""

headers = {
    "Authorization": "Token " + token
}


class Contrib:
    def __init__(self, id, url, total_commit):
        self.__id = id
        self.__url = url
        self.__commit_count = total_commit

    def get_id(self):
        return self.__id

    def get_url(self):
        return self.__url

    def get_commit_count(self):
        return self.__commit_count


class Repo:
    def __init__(self, id, url, f_count, contri):
        self.__id = id
        self.__url = url
        self.__fork_count = f_count
        self.__contri = contri

    def get_id(self):
        return self.__id

    def get_url(self):
        return self.__url

    def get_fork_count(self):
        return self.__fork_count

    def get_contri(self):
        return self.__contri


def get_repos(org, n, m):
    repos_json = requests.get(repo_url.format(
        organization=org, count=n), headers=headers).json()
    if("message" in repos_json):
        return "404"
    repos = []
    for i in repos_json["items"]:
        contributors = get_contributors(org, i["name"], m)
        repos.append(Repo(i["name"], i["html_url"],
                          i['forks_count'], contributors))
    return repos


def get_contributors(org, repo, m):
    contributors_json = requests.get(contributors_url.format(
        organization=org, repo=repo), headers=headers).json()
    contributors = []
    for i in contributors_json:
        if(i["author"] == None):
            continue
        contributors.append(
            (i["total"], i["author"]["login"], i["author"]["html_url"]))
    contributors = contributors[::-1]
    contr = []
    for i in range(min(len(contributors), m)):
        contr.append(
            Contrib(contributors[i][1], contributors[i][2], contributors[i][0]))
    return contr


def get_org_contribution(org, n, m):
    if(n <= 0 or m <= 0):
        return "404"
    repos = get_repos(org, n, m)
    return repos
