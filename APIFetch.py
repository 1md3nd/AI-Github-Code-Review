import requests
from dotenv import load_dotenv
import os
from utils import fix_url
from utils import handle_request_exception
load_dotenv()

# GITHUB personal access token
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Default headers
H = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
    "Authorization":f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"}

# fetching github api with url = owner/repo
@handle_request_exception
def fetch_ratelimit():
    ratelimit_url = 'https://api.github.com/rate_limit'
    res = requests.get(ratelimit_url,headers=H)
    res.raise_for_status()
    return res.json()

def get_repo_stats(url):
    url = fix_url(url)
    res = requests.get(url,headers=H)
    res.raise_for_status()
    return res.json()
    
def get_repo_branches(url):
    url = fix_url(url)
    res = requests.get(url,headers=H)
    res.raise_for_status()

get_repo_stats('a')