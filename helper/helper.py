import requests
from functools import wraps
from utils import fix_url, is_ignored_files,is_ignored_folder
from dotenv import load_dotenv
import os
import base64
from utils import filter_files
from collections import defaultdict
import chardet
# import beautifulsoup

load_dotenv()

# GITHUB personal access token
BASE_URL = 'https://api.github.com'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Define the default headers
H = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

# Define the decorator
def handle_request_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Get the URL from the function's arguments
            url = func(*args, **kwargs)
            # Fix the URL if needed
            print(url)
            url = fix_url(url)
            # Combine the repetitive parts of requests.get() calls
            res = requests.get(url, headers=H)
            res.raise_for_status()
            return res.json()
        except requests.RequestException as e:
            print(f"Error occurred: {e}")
            return None
    return wrapper

# Apply the decorator to your functions
@handle_request_exception
def fetch_ratelimit():
    return f'{BASE_URL}/rate_limit'

@handle_request_exception
def get_repo_stats(owner,repo):
    return f'{BASE_URL}/repos/{owner}/{repo}'

@handle_request_exception
def get_repo_branches(owner,repo):
    return f'{BASE_URL}/repos/{owner}/{repo}/branches'

def get_repo_main_branch(owner,repo):
    branches = get_repo_branches(owner,repo)
    if not branches:
        return None
    if len(branches) == 1:
        return branches[0]
    for branch in branches:
        if branch['name'] in ('main','master'):
            return branch
    return branches[0]

@handle_request_exception
def get_tree(owner,repo,sha):
    return f'{BASE_URL}/repos/{owner}/{repo}/git/trees/{sha}'

@handle_request_exception
def get_blob(owner,repo,sha):
    return f'{BASE_URL}/repos/{owner}/{repo}/git/blobs/{sha}'

@handle_request_exception
def get_url(url):
    return url

def get_sha(paths):
    return paths['commit']['sha']


def extract_blobs_lists(owner,repo,sha):
    tree_stack = [sha]
    blobs = []
    t = ['root']
    while tree_stack:
        curr_sha = tree_stack.pop(0)
        curr_tree = get_tree(owner,repo,curr_sha)
        curr_path = t.pop(0)
        for curr in curr_tree['tree']:
            if curr['type'] == 'blob':
                curr['file_path'] = curr_path+ '/' + curr['path']
                blobs.append(curr)
            elif not is_ignored_folder(curr['path']):
                t.append(curr_path+'/'+curr['path'])
                tree_stack.append(curr['sha'])
    return blobs


def extract_blobs_data(blobs):
    data_res = []
    for blob in blobs:
        if not is_ignored_files(blob['path']):
           res = process_blob(blob)
           data_res.append(res)
    return data_res


def get_loc(content):
    count = 0
    try:
        for c in content.splitlines():
            c = c.strip()
            if c and not c.startswith('#'):
                count+=1
    except Exception as e:
        print(e)
        # print(content)
    return count


def get_comments(content):
    return 'no comments'

def process_blob(blob):
    result = {}
    result['path'] = blob['file_path']
    url = blob['url']
    res = get_url(url)
    content = base64.b64decode(res['content'])
    encoding = chardet.detect(content)['encoding']
    print(blob['path'],encoding)
    if encoding == 'UTF-16':
        content = content.decode('utf-16')
    else:
        content = content.decode('utf-8')
    result['LOC'] = get_loc(content)
    result['context'] = get_comments(content)
    return result

def get_cummlative(filtered_files_dict):
    raw_metadata = defaultdict(int)
    for file_type, files in filtered_files_dict.items():
        for file in files:
            raw_metadata[file_type] += file['LOC']
        
    return raw_metadata

def process_files(files_dict: dict):
    file_type_res = defaultdict(list)
    for file_type, files in files_dict.items():
        for file in files:
            res = process_blob(file)
            file_type_res[file_type].append(res)
    return file_type_res
        

owner = '1md3nd'
repo = 'job-scraping-apply'
main_branch = get_repo_main_branch(owner,repo)
sha = get_sha(main_branch)
res = extract_blobs_lists(owner,repo,sha)
filtered_files = filter_files(res)
filtered_files_res = process_files(filtered_files)
# data = extract_blobs_data(res)
cummlative_data = get_cummlative(filtered_files_res)
print(filtered_files_res)
# print('--------------------')
print(cummlative_data)

# print(res)
