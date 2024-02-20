import fnmatch
import ast
import astor
import markdown
import nbformat

def fix_url(url):
    # Remove leading and trailing spaces and slashes
    url = url.strip().strip('/')
    return url

def clean_and_format_python_code(data):
    # Decode the data if it's in bytes format
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    # Parse the Python code
    parsed_ast = ast.parse(data)
    # Pretty-print the AST to a string
    formatted_code = astor.to_source(parsed_ast)

    return formatted_code

def clean_and_format_markdown(data):
    # Decode the data if it's in bytes format
    if isinstance(data, bytes):
        data = data.decode('utf-8')

    # Parse Markdown and convert it to HTML
    html = markdown.markdown(data)

    return html

def clean_and_format_text(data):
    # Decode the data if it's in bytes format
    if isinstance(data, bytes):
        data = data.decode('utf-8')

    # Remove leading and trailing whitespace
    cleaned_data = data.strip()

    return cleaned_data

def clean_and_format_ipynb(data):
    # Decode the data if it's in bytes format
    if isinstance(data, bytes):
        data = data.decode('utf-8')

    # Load the notebook from the data
    notebook = nbformat.reads(data, as_version=4)

    # Process the notebook cells
    for cell in notebook.cells:
        # Clean and format each cell
        if cell.cell_type == 'code':
            # Example: Remove leading and trailing whitespace from code cells
            cell.source = cell.source.strip()
        elif cell.cell_type == 'markdown':
            # Example: Remove leading and trailing whitespace from Markdown cells
            cell.source = cell.source.strip()

    # Serialize the notebook back to JSON format
    formatted_notebook = nbformat.writes(notebook)

    return formatted_notebook

def clean_dockerfile(data):
    # Decode the data if it's in bytes format
    if isinstance(data, bytes):
        data = data.decode('utf-8')

    # Split the Dockerfile into lines
    lines = data.split('\n')

    # Remove comments and leading/trailing whitespace from each line
    cleaned_lines = [line.split('#')[0].strip() for line in lines]

    # Remove empty lines
    cleaned_data = '\n'.join(line for line in cleaned_lines if line)

    return cleaned_data

def clean_shell_script(data):
    # Decode the data if it's in bytes format
    if isinstance(data, bytes):
        data = data.decode('utf-8')

    # Split the script into lines
    lines = data.split('\n')

    # Remove comments and leading/trailing whitespace from each line
    cleaned_lines = [line.split('#')[0].strip() for line in lines]

    # Remove empty lines
    cleaned_data = '\n'.join(line for line in cleaned_lines if line)

    return cleaned_data

FOLDERS_TO_EXCLUDE = ['migrations','__pycache__/', 'build/', 'develop-eggs/', 'dist/', 'downloads/',
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