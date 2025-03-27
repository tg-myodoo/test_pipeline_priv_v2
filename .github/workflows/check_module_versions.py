# Script to compare Odoo module versions between a pull request and any branch.
# by Tomasz Golaszewski
# 2025.03.27

import os           # for connection with action environment (installed for python by default)
import sys          # for returning failure (installed for python by default)
import base64       # decoding data (installed for python by default)
import json         # for converting json into dict (installed for python by default)
import ast          # for running python inside python (installed for python by default)
import requests     # api (installed by pip)


API_KEY = os.environ['THE_GITHUB_TOKEN']
REPOSITORY = os.environ['REPOSITORY']
PULL_REQUEST_URL = os.environ['PULL_REQUEST_URL']
PULL_REQUEST_TARGET = os.environ['PULL_REQUEST_TARGET']
GITHUB_WORKSPACE = os.environ['GITHUB_WORKSPACE']

if PULL_REQUEST_TARGET == 'client_stage': COMPARASION_BASE = 'dev_stage'
elif PULL_REQUEST_TARGET in ['main', 'master']: COMPARASION_BASE = 'client_stage'
else: COMPARASION_BASE = 'dev_stage'


def extract_manifest_info(manifest_str: str) -> dict:
    """Converts text Odoo module manifest from string into dictionary."""
    
    # default odoo manifest
    manifest_dict = {
        'version': '1.0',
    }
    # convert str to dict by running str via eval (this is odoo official way) 
    manifest_dict.update(ast.literal_eval(manifest_str))
    return manifest_dict

def handle_connection(url: str) -> dict:
    """Common function to handle request.
    Returns: structure with request response
    """
    headers = {
        'authorization': f"Bearer {API_KEY}",
        'content-type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(url)
        print(f"[{response.status_code}]: {response.text}")
    return response

def get_structure(url: str) -> list[dict]:
    """Gets by url and next processes json-like structure. 
    Returns python list of dicts.
    """
    response = handle_connection(url)
    if response.status_code == 200:
        return json.loads(response.text)
    return []

def get_file(url: str) -> str:
    """Get by url and next process text files. 
    Returns text files as str.
    """
    response = handle_connection(url)
    if response.status_code == 200:
        return response.text
    return ""

def get_pull_request_commits_sha_list(pull_request_url: str) -> list[tuple[str, str]]:
    commit_list = get_structure(pull_request_url) 
    return [(commit['sha'], commit['commit']['message']) for commit in commit_list]

def get_modules_list_by_sha(sha: str) -> list:
    commit_url = f"https://api.github.com/repos/{REPOSITORY}/contents?ref={sha}"
    commit_content_list = get_structure(commit_url) 
    modules_list = []
    for commit in commit_content_list:
        if commit["type"] == "dir":
            modules_list.append(commit['name'])
    return modules_list

def get_modules_list_by_workspace() -> list:
    return [f.name for f in os.scandir(GITHUB_WORKSPACE) if f.is_dir()]

def get_module_version(manifest_url: str) -> str:
    """
    Gets file by commit sha:
    url = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{COMMIT_SHA}/{PATH_TO_FILE}"
    e.g.
    url = "https://raw.githubusercontent.com/tg-myodoo/test_pipeline/858f26378801c9f086eef1a9e2705665bf79a959/module_name/__manifest__.py"
    ...or by branch:
    url = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/refs/heads/{BRANCH}/{PATH_TO_FILE}"
    e.g.
    url = "https://raw.githubusercontent.com/tg-myodoo/test_pipeline/refs/heads/module_name/module_name/__manifest__.py"
    
    Returns module version as str.
    """
    manifest_raw = get_file(manifest_url) 
    if manifest_raw:
        manifest_dict = extract_manifest_info(manifest_raw)
        return manifest_dict['version']
    return "0.0.0.0.0"

def get_module_version_by_commit(sha: str, module: str) -> str:
    manifest_url = f"https://raw.githubusercontent.com/{REPOSITORY}/{sha}/{module}/__manifest__.py"
    return get_module_version(manifest_url)

def get_module_version_by_branch(module: str) -> str:
    manifest_url = f"https://raw.githubusercontent.com/{REPOSITORY}/refs/heads/{COMPARASION_BASE}/{module}/__manifest__.py"
    return get_module_version(manifest_url)

def get_module_version_by_workspace(module: str) -> str:
    # prepares path to file
    path = os.path.join(GITHUB_WORKSPACE, module, "__manifest__.py")
    # open and read file
    with open(path) as file:
        manifest_raw = file.read()
    # get module version from file
    manifest_dict = extract_manifest_info(manifest_raw)
    return manifest_dict['version']

def compare_versions(version_lower: str, version_higher: str) -> bool:
    """
    Checks if version_higher is higher or equal than version_lower.

    Args:
        version_lower (str): Older version of the module e.g. '18.0.1.0.0'.
        version_higher (str): Newer version of the module e.g '18.0.2.0.0'.

    Returns:
        bool: True if version_higher is higher or equal than version_lower, False if lower.
    """

    if version_lower == version_higher:
        return True
    
    version_lower_splited = version_lower.split(".")
    version_higher_splited = version_higher.split(".")

    if len(version_lower_splited) != len(version_higher_splited):
        print("DIFFERENT VERSION FORMATS!!!")
        return False

    for i in range(len(version_higher_splited)):
        if version_higher_splited[i] > version_lower_splited[i]:
            return True
    return False
    
def run_script():
    """Main function."""
    is_pull_correct = True
    modules_list = get_modules_list_by_workspace()
    for module in modules_list:
        module_version_from_pull_request = get_module_version_by_workspace(module)
        module_version_from_branch = get_module_version_by_branch(module)
        print(f"{module}: pull_request: {module_version_from_pull_request}, {COMPARASION_BASE}: {module_version_from_branch}")
        is_pull_correct &= compare_versions(module_version_from_pull_request, module_version_from_branch)
    if is_pull_correct:
        print("ALLES GUT!")
    else:
        print("INCORRECT MODULE VERSIONS!!!")
        sys.exit(1) # trigger failure


if __name__ == '__main__':
    run_script()