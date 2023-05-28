import time
from github import Github
from github import InputGitTreeElement
from django.conf import settings
import threading


class GihubPushThread(threading.Thread):
    def __init__(self,app_name,data,file_name):
        self.app_name = app_name
        self.data = data
        self.file_name = file_name
        threading.Thread.__init__(self)

    def run(self):
        try:
            g = Github(settings.GITHUB_TOKEN)
            repo = g.get_user().get_repo(settings.GITHUB_REPO_NAME)
            commit_message = 'File updated'
            master_ref = repo.get_git_ref(f'heads/{settings.GITHUB_BRANCH}')
            master_sha = master_ref.object.sha
            base_tree = repo.get_git_tree(master_sha)

            if type(self.data) == bytes:
                repo.create_file(self.app_name + '/' + self.file_name, "committing files", self.data, branch=settings.GITHUB_BRANCH)

            else:
                element = InputGitTreeElement("apps/" + self.app_name + '/' + self.file_name, '100644', 'blob', self.data)
                tree = repo.create_git_tree([element], base_tree)
                parent = repo.get_git_commit(master_sha)
                commit = repo.create_git_commit(commit_message, tree, [parent])
                master_ref.edit(commit.sha)
            print("git push doneeeeeeeeeeeeeeeeeeeeee")
        except Exception as e:
            print('error>>>>>>>',e)
            pass

def github_push(app_name,data,file_name='settings.json'):
    time.sleep(2)
    return GihubPushThread(app_name,data,file_name).start()
