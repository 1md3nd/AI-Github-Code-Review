import sys
import os

# Get the parent folder of the current script
current_folder = os.path.dirname(os.path.realpath(__file__))
parent_folder = os.path.abspath(os.path.join(current_folder, '..'))
print(current_folder,parent_folder)
# Add the parent folder to the Python path
sys.path.append(parent_folder)

import requests
from helper.helper import process_repo
from helper.utils import extract_owner_and_repo

# repo_url = 'https://github.com/1md3nd/AI-Github-Code-Review/'
repo_url = 'https://github.com/1md3nd/AI-Github-Code-Review/blob/main/helper/helper.py'
owner, repo = extract_owner_and_repo(repo_url)

print(owner,repo)

res = process_repo(owner,repo)

print(res)

# res = requests.get('http://127.0.0.1:8080/searchRepo', params={'repo_url': repo_url})

# print(res.text)