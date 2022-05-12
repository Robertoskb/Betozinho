from github import Github
from decouple import config


def get_news():
    return dict(
        Novidades="Agora você pode usar esse comando para saber mais sobre as minhas atualizações ^^",
        Correções=''
    )


def get_commits(repo): return Github(config('GitHub')).get_user().get_repo(repo).get_commits().totalCount


def get_bot_version(): return str(get_commits("Betozinho")).replace('', '.')[1:-1]


if __name__ == '__main__':
    print(get_bot_version())
