import requests

def fetch_repo_files(repo_url):
    parts = repo_url.strip("/").split("/")
    owner = parts[-2]
    repo = parts[-1].replace(".git", "")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # 🔥 Step 1: Get default branch
    repo_api = f"https://api.github.com/repos/{owner}/{repo}"
    repo_data = requests.get(repo_api, headers=headers).json()

    branch = repo_data.get("default_branch", "main")

    # 🔥 Step 2: Get full tree (RECURSIVE)
    tree_api = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    tree_data = requests.get(tree_api, headers=headers).json()

    code_files = []

    for item in tree_data.get("tree", []):
        if item["type"] == "blob" and item["path"].endswith(".py", ".js", ".java", ".cpp", ".c"):
            file_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{item['path']}"

            try:
                file_data = requests.get(file_url, headers=headers).text
                code_files.append({
                    "file": item["path"],
                    "code": file_data
                })
            except:
                continue

    print("Fetched files:", len(code_files))  # DEBUG

    return code_files
