import fnmatch
import collections
import re


def fix_url(url):
    # Remove leading and trailing spaces and slashes
    url = url.strip().strip('/')
    return url

FOLDERS_TO_EXCLUDE = ['migrations','__pycache__/', 'build/', 'develop-eggs/', 'dist/', 'downloads/','.vscode/',
    'eggs/', '.eggs/', 'lib/', 'lib64/', 'parts/', 'sdist/', 'var/',
    'wheels/', 'share/python-wheels/', 'htmlcov/', '.tox/', '.nox/',
    '.cache/', '.hypothesis/', '.pytest_cache/', '__pypackages__/',
    '.spyderproject/', '.spyproject/', '.ropeproject/', 'site/',
    '.mypy_cache/', '.pyre/', '.pytype/', 'cython_debug/', '.idea/']

FILES_TO_EXCLUDE = ['csv','__init__','*.pyc', '*.pyo', '*.pyd', '*.so', '.Python', '*.manifest', '*.spec',
    'pip-log.txt', 'pip-delete-this-directory.txt', 'nosetests.xml',
    'coverage.xml', '*.cover', '*.py,cover', '*.mo', '*.pot', '*.log',
    'local_settings.py', 'db.sqlite3', 'db.sqlite3-journal', '*.sage.py',
    '.installed.cfg', '*.egg', 'MANIFEST', '.dmypy.json', 'dmypy.json',
    'coverage.*']



def is_ignored(name,patterns):
    for pattern in patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
    return False

def is_ignored_files(name,patterns=FILES_TO_EXCLUDE):
    return is_ignored(name,patterns)

def is_ignored_folder(name,patterns=FOLDERS_TO_EXCLUDE):
    return is_ignored(name,patterns)

file_extension_to_language = {
    '.c': 'C',
    '.h': 'C',
    '.cpp': 'C++',
    '.hpp': 'C++',
    '.java': 'Java',
    '.py': 'Python',
    '.rb': 'Ruby',
    '.js': 'JavaScript',
    '.html': 'HTML',
    '.css': 'CSS',
    '.php': 'PHP',
    '.swift': 'Swift',
    '.cs': 'C#',
    '.pl': 'Perl',
    '.r': 'R',
    '.sql': 'SQL',
    '.go': 'Go',
    '.lua': 'Lua',
    '.rs': 'Rust',
    '.sh': 'Shell',
    '.asm': 'Assembly',
    '.json': 'JSON',
    '.xml': 'XML',
    '.yaml': 'YAML',
    '.toml': 'TOML',
    '.jsx': 'React JSX',
    '.tsx': 'React TSX',
    '.coffee': 'CoffeeScript',
    '.ts': 'TypeScript',
    '.scss': 'Sass',
    '.less': 'Less',
    '.kt': 'Kotlin',
    '.dart': 'Dart',
    '.jl': 'Julia',
    '.m': 'Objective-C',
    '.ipa': 'iOS App',
    '.apk': 'Android App',
    '.dll': 'Dynamic Link Library',
    '.exe': 'Executable',
    '.jar': 'Java Archive',
    '.war': 'Java Web Archive',
    '.ear': 'Enterprise Archive',
    '.deb': 'Debian Package',
    '.rpm': 'Red Hat Package Manager',
    '.tar.gz': 'Tarball',
    '.zip': 'Zip Archive',
    '.gz': 'Gzip Compressed File',
    '.bz2': 'Bzip2 Compressed File',
    '.xz': 'xz Compressed File',
    '.rar': 'RAR Archive',
    '.7z': '7-Zip Archive',
    '.tgz': 'Tar Gzipped Archive',
    '.lz': 'Lzip Compressed File',
    '.lzma': 'LZMA Compressed File',
    '.lz4': 'LZ4 Compressed File',
    '.zst': 'Zstandard Compressed File',
    '.csv': 'CSV',
    '.tsv': 'TSV',
    '.xlsx': 'Excel',
    '.xls': 'Excel',
    '.pdf': 'PDF',
    '.docx': 'Word',
    '.doc': 'Word',
    '.txt': 'Text',
    '.md': 'Markdown',
    '.rtf': 'Rich Text Format',
    '.pptx': 'PowerPoint',
    '.ppt': 'PowerPoint',
    '.key': 'Keynote',
    '.numbers': 'Numbers',
    '.odt': 'OpenDocument Text',
    '.ods': 'OpenDocument Spreadsheet',
    '.odp': 'OpenDocument Presentation',
    '.odg': 'OpenDocument Graphics',
    '.odf': 'OpenDocument Formula',
}

def filter_files(file_list):
    filtered_files = collections.defaultdict(list)
    for file_ in file_list:
        file = file_['path']
        file_extension = '.' + file.split('.')[-1]
        if file_extension in file_extension_to_language:
            language = file_extension_to_language[file_extension]
            filtered_files[language].append(file_)
    return filtered_files


def extract_owner_and_repo(url):
    # Remove leading/trailing whitespace and trailing slashes
    url = url.strip("'").strip().rstrip('/')

    # Define regular expressions for different GitHub URL formats
    patterns = [
        r'^https?://github.com/([^/]+)/([^/]+)',
        r'^git@github.com:([^/]+)/([^/]+)',
        r'^github.com/([^/]+)/([^/]+)'
    ]

    # Loop through patterns and match against the URL
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            owner = match.group(1)
            repo = match.group(2)
            return owner, repo

    # Return None if no match is found
    return None, None

