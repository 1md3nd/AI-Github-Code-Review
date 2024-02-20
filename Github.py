import os
from github import Github

from github import Auth
from dotenv import load_dotenv

load_dotenv()

class GithubWrapper:
    def __init__(self) -> None:
        auth = Auth.Token(os.getenv('GITHUB_TOKEN'))
        self.github_instance = Github(auth=auth)
    
    def fetch_repo(self,url):
        repo = self.github_instance.get_repo(url)
        return repo
    
    def get_tree(self,url):
        tree = self.fetch_repo.get_git_tree(f'{url}/git/trees')
        return tree
    

