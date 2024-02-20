import requests
from functools import wraps
from utils import fix_url, is_ignored_files,is_ignored_folder
from dotenv import load_dotenv
import os
import base64
from utils import clean_and_format_python_code, clean_and_format_markdown, clean_and_format_text, clean_and_format_ipynb
from utils import clean_dockerfile, clean_shell_script
# import beautifulsoup

load_dotenv()

# GITHUB personal access token
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
    return 'https://api.github.com/rate_limit'

@handle_request_exception
def get_repo_stats(url):
    return 'https://api.github.com/repos/'+ url

@handle_request_exception
def get_repo_branches(url):
    return 'https://api.github.com/repos/'+ url + '/branches'

def get_repo_main_branch(url):
    branches = get_repo_branches(url)
    if not branches:
        return None
    if len(branches) == 1:
        return branches[0]
    for branch in branches:
        if branch['name'] in ('main','master'):
            return branch
    return branches[0]

@handle_request_exception
def get_tree(url,sha):
    return 'https://api.github.com/repos/' + url + '/git/trees/' + sha

@handle_request_exception
def get_blob(url,sha):
    return 'https://api.github.com/repos/' + url + '/git/blobs/' + sha

@handle_request_exception
def get_url(url):
    return url

# res = get_repo_main_branch('1md3nd/materials_backend')
# sha = res['commit']['sha']
# r1 = get_tree('1md3nd/materials_backend',sha)
# for r in r1['tree']:
#     if r['type'] == 'blob':
#         print(r['path'] )
#         enc = get_blob('1md3nd/materials_backend',r['sha'])
#         dec = base64.b64decode(enc['content'])
#         print(dec)

def get_sha(paths):
    return paths['commit']['sha']


def extract_blobs_lists(url,sha):
    tree_stack = [sha]
    blobs = []
    t = ['root']
    while tree_stack:
        curr_sha = tree_stack.pop(0)
        curr_tree = get_tree(url,curr_sha)
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
    for c in content.splitlines():
        c = c.strip()
        if c and not c.startswith('#'):
            count+=1
    return count

def get_comments(content):
    return 'no comments'

def process_blob(blob):
    result = {}
    result['path'] = blob['file_path']
    url = blob['url']
    res = get_url(url)
    content = base64.b64decode(res['content'])
    file_name = blob['path'].lower()
    result['type'] = None
    if file_name.endswith('.py'):
        content = clean_and_format_python_code(content)
        result['LOC'] = get_loc(content)
        result['type'] = 'python'
    elif file_name.endswith('.md'):
        content = clean_and_format_markdown(content)
        result['type'] = 'Markdown'
    elif file_name.endswith('.txt'):
        content = clean_and_format_text(content)
        result['type'] = 'text'
    elif file_name.endswith('.ipynb'):
        content = clean_and_format_ipynb(content)
    elif file_name.endswith('.sh'):
        content = clean_shell_script(content)
    elif file_name.startswith('dockerfile'):
        content = clean_dockerfile(content)
    # print('-------------------------')
    # print('-------------------------')
    # print(blob['path'])
    # print(content)
    result['context'] = get_comments(content)
    return result

def get_cummlative(data):
    raw = {}
    raw['total_LOC'] = 0
    raw['md'] = False
    raw['test_cases'] = False

    for d in data:
        if d['type'] == 'Markdown':
            raw['md'] = True
        elif d['type'] == 'python':
            raw['total_LOC'] += d['LOC']
        elif d['type'] == 'test':
            raw['test_cases'] = True
        
    data['meta_data'] = raw
    return data

repo = '1md3nd/materials_backend'
main_branch = get_repo_main_branch(repo)
sha = get_sha(main_branch)
res = extract_blobs_lists(repo,sha)
data = extract_blobs_data(res)
cummlative_data = get_cummlative(data)

print(cummlative_data)

# print(res)
