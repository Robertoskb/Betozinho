from github import Github
from decouple import config


def get_news():
    return dict(
        Novidades="Agora você pode mandar gifs de volta para quem te marcou em **-slap**, **-hug** e **-pat** ^^",
    )


def get_commits(repo): return Github(config('GitHub')).get_user().get_repo(repo).get_commits().totalCount


def get_last_commit(repo): return Github(config('GitHub')).get_user().get_repo(repo).get_commits()[0].commit.committer


def get_bot_version(): return str(get_commits("Betozinho")).replace('', '.')[1:-1]


def get_last_commit_date(): return str(get_last_commit("Betozinho").date)


if __name__ == '__main__':
    print(get_bot_version())
    print(get_last_commit_date())
