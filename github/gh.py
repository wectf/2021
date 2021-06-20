import os

import github
import uuid


TOKEN = "REMOVED GITHUB TOKEN"
g = github.Github(TOKEN)

user = g.get_user()
default_repo = user.get_repo("base")

for i in range(100):
    a = str(uuid.uuid4())
    try:
        repo_name = "production-" + a

        repo = user.create_repo(
            repo_name,
            allow_rebase_merge=True,
            auto_init=False,
            has_issues=True,
            has_projects=False,
            has_wiki=False,
            private=True,
        )

        # repo.add_to_collaborators("shouc", "pull")
        repo.create_secret("DOCKER_USERNAME", "wectfchall")
        repo.create_secret("DOCKER_PASSWORD", "c3f6a063-4cff-442e-81d7-1febe6d94cea")

        os.chdir("content/")
        os.system("git remote remove origin")
        os.system(f"git remote add origin https://wectf-challs:REMOVED GITHUB PASSWORD@github.com/wectf-challs/{repo_name}.git")
        os.system("git push origin main")
        os.chdir('../')

        with open("repos3", "a+") as fp:
            fp.write(repo_name + "\n")
    except:
        print(a)
