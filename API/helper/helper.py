import requests
from functools import wraps
from helper.utils import fix_url,is_ignored_files,is_ignored_folder, comments_file_filter
from helper.vars import import_patterns
from helper.vars import comment_patterns as comment_file_dict
from dotenv import load_dotenv
import os
import base64
from helper.utils import filter_files
from collections import defaultdict
import chardet
import re


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
    """ 
    Given the owner and repo names, this function returns the main branch of the repository. 
    If there are multiple branches and none of them are named 'main' or 'master', 
    then it returns the first branch. 
    """ 

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
    """
      Given the owner and repo names, and SHA of a git tree, 
      this function returns the json response containing the corresponding git tree details. 
    """
    return f'{BASE_URL}/repos/{owner}/{repo}/git/trees/{sha}'

@handle_request_exception
def get_blob(owner,repo,sha):
    """ 
    Given the owner and repo names, and SHA of a git blob, 
    this function returns the json response containing the corresponding git blob details. 
    """
    return f'{BASE_URL}/repos/{owner}/{repo}/git/blobs/{sha}'

@handle_request_exception
def get_url(url):
    """ 
    Given the URL, this function returns the json response corresponding to the URL. 
    """ 
    return url

@handle_request_exception
def is_forked(owner,repo):
    """ 
    Given the owner and repo names, 
    this function returns the json response containing the details of the repository, 
    including whether it is forked or not. 
    """
    return f'{BASE_URL}/repos/{owner}/{repo}'

def get_sha(paths):
    """ 
    Given a dictionary containing commit details, 
    this function returns the SHA of the commit. 
    """
    return paths['commit']['sha']


def extract_blobs_lists(owner,repo,sha):
    """ 
    Given the owner and repo names, and SHA of a git tree, 
    this function returns a list of all the blobs in the tree. 
    The function uses a BFS search to traverse the git tree of given SHA, 
    adding blobs to the list as they are found. 
    """ 
    # Initialize variables 
    tree_stack = [sha]
    # List to store git tree SHAs 
    # List to store all blobs in tree 
    t = ['root'] 
    # List to keep track of paths in tree 
    blobs = []
    t = ['root']
    # Loop until the list of git tree SHAs to be traversed is empty 
    while tree_stack:
    # Get current git tree SHA from list 
        curr_sha = tree_stack.pop(0) 
        # Get details of current git tree 
        curr_tree = get_tree(owner,repo,curr_sha)
        # Get current path in tree
        curr_path = t.pop(0)
        # Loop through contents of current git tree
        for curr in curr_tree['tree']:
            # If content type is blob, append it to blobs list 
            if curr['type'] == 'blob':
                curr['file_path'] = curr_path+ '/' + curr['path']
                blobs.append(curr)
            # If content type is tree, append its SHA to tree_stack and add its path to t list 
            elif not is_ignored_folder(curr['path']):
                t.append(curr_path+'/'+curr['path'])
                tree_stack.append(curr['sha'])
    return blobs


def extract_blobs_data(blobs):
    """ 
    Given a list of blobs, this function extracts the data from each blob 
    and returns a list of data dictionary for each of the blob files, 
    skipping any files that are ignored by the `is_ignored_files` function. 
    """ 
    # Initialize variables 
    # List to store data dictionary for each file 
    data_res = []
    # Loop through blobs list 
    for blob in blobs: 
        # Skip ignored files 
        if not is_ignored_files(blob['path']): 
        # Extract data from blob file 
           res = process_blob(blob) 
           # Append data dictionary to data_res list 
           data_res.append(res) 
    return data_res


def count_comments(file_text,file_type):
    """
    Count the number of single-line comments in a given file text.

    Parameters:
    file_text (str): The text content of the file.

    Returns:
    int: The number of single-line comments found in the file text.
    """
    pattern = comments_file_filter(file_type)
    if not pattern:
        return -1
    comments = re.findall(pattern, file_text, re.MULTILINE)
    return len(comments)


def count_imports(file_text, file_type):
    """
    Count the number of files imported in a given file text based on the programming language.

    Parameters:
    file_text (str): The text content of the file.
    file_type (str): The programming language of the file.

    Returns:
    int: The number of files imported in the file text.
    """
    if file_type in import_patterns:
        pattern = import_patterns[file_type]
        imports = re.findall(pattern, file_text)
        modules = [module for pair in imports for module in pair if module]
        return (len(modules),modules)
    else:
        return (-1,[])
    
def get_loc(content):
    """ 
    Given the content of a file as a string, 
    this function counts the number of lines of code (LOC) in the file. 
    It skips empty lines and lines that start with '#' (assumed to be comments). 
    Returns the count of lines of code. 
    """
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
    """ 
    Given the content of a file as a string, 
    this function returns a placeholder string 'no comments'. 
    This function can be updated to retrieve and process comments from the file. 
    """
    return 'no comments'

def process_blob(blob,file_type):
    """
    Given a blob and its file type, 
    this function processes the blob to extract relevant information. 
    Returns a dictionary with the following information: 
    - 'path': The file path 
    - 'LOC': The count of lines of code in the file 
    - 'comment_count': A placeholder for counting comments (can be updated) 
    - 'import_count': The count of imports in the file (if applicable) 
    - 'imported_modules': A list of imported modules (if applicable) 
    - 'context': A placeholder
     for comments (can be updated) 
    """
    result = {}
    result['path'] = blob['file_path']
    url = blob['url']
    res = get_url(url)
    content = base64.b64decode(res['content'])
    encoding = chardet.detect(content)['encoding']
    # print(blob['path'],encoding)
    if encoding == 'UTF-16':
        content = content.decode('utf-16')
    else:
        content = content.decode('utf-8')
    result['LOC'] = get_loc(content)
    result['comment_count'] = count_comments(content,file_type)
    imports_tuple = count_imports(content,file_type)
    if imports_tuple[0] != -1:
        result['import_count'] = imports_tuple[0]
        result['imported_modules'] = imports_tuple[1]
    result['context'] = get_comments(content)
    return result

def get_cummlative(filtered_files_dict):
    """ 
    Given a filtered list of file dictionaries, 
    this function calculates the cumulative LOC and comment count for each file type. 
    Returns a dictionary with keys 'LOC' and 'comment_count', 
    where the value of each key is another dictionary containing the cumulative count of that metric for each file type. 
    """
    raw_metadata_loc = defaultdict(int)
    raw_metadata_comment_count = defaultdict(int)
    # Loop through each file type and all files associated with it to calculate LOC and comment count
    for file_type, files in filtered_files_dict.items():
        for file in files:
            raw_metadata_loc[file_type] += file['LOC']
            if file_type in comment_file_dict:
                raw_metadata_comment_count[file_type] += file['comment_count']
        
    return {'LOC': raw_metadata_loc, 'comment_count': raw_metadata_comment_count}

def process_files(files_dict: dict):
    """ 
    Given a dictionary of files where keys are file types, 
    this function processes each file using 'process_blob' function 
    and returns a dictionary where keys are file types and values are lists of processed file dictionaries. 
    """
    file_type_res = defaultdict(list)
    for file_type, files in files_dict.items():
        for file in files:
            res = process_blob(file,file_type)
            file_type_res[file_type].append(res)    
    return file_type_res
        

def process_repo(owner,repo):
    """ 
    Given the owner and repo names, 
    this function retrieves information about the repo and each file it contains. 
    Returns two dictionaries: 
    - The first dictionary is the filtered files dictionary returned by 'filter_files' function, 
        where keys are file types and values are lists of file dictionaries. 
    - The second dictionary contains the cumulative LOC and comment count for each file type, 
        returned by the 'get_cummlative' function. 
        It also contains a boolean key 'forked' to indicate if the repo is a fork. 
    """
    main_branch = get_repo_main_branch(owner,repo)
    # print(owner,repo,main_branch)
    sha = get_sha(main_branch)
    res = extract_blobs_lists(owner,repo,sha)
    forked = is_forked(owner,repo)["fork"]
    # Filter files by file type 
    filtered_files = filter_files(res)
    # Process each file using 'process_blob' function 
    filtered_files_res = process_files(filtered_files)
    # data = extract_blobs_data(res)
    # Calculate cumulative LOC and comment count across all files of each file type
    cummlative_data = get_cummlative(filtered_files_res)
    cummlative_data['forked'] = forked
    return filtered_files_res,cummlative_data
