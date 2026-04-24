import requests

def fetch_repo_files(repo_url):
    parts = repo_url.strip("/").split("/")
    owner = parts[-2]
    repo = parts[-1].replace(".git", "")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # 🔥 Step 1: Get repo info
    repo_api = f"https://api.github.com/repos/{owner}/{repo}"
    repo_res = requests.get(repo_api, headers=headers)

    if repo_res.status_code != 200:
        raise Exception("Invalid repository URL or API limit exceeded")

    repo_data = repo_res.json()
    branch = repo_data.get("default_branch", "main")

    # 🔥 Step 2: Get all files recursively
    tree_api = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    tree_res = requests.get(tree_api, headers=headers)

    if tree_res.status_code != 200:
        raise Exception("Unable to fetch repository files")

    tree_data = tree_res.json()

    code_files = []

    for item in tree_data.get("tree", []):
        if item["type"] == "blob":

            file_path = item["path"]

            # 🔥 Language detection
            if file_path.endswith(".py"):
                lang = "python"
            elif file_path.endswith(".js"):
                lang = "javascript"
            elif file_path.endswith(".java"):
                lang = "java"
            elif file_path.endswith(".cpp"):
                lang = "cpp"
            elif file_path.endswith(".c"):
                lang = "c"
            else:
                continue  # skip unsupported

            file_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"

            try:
                file_data = requests.get(file_url, headers=headers).text

                code_files.append({
                    "file": file_path,
                    "code": file_data,
                    "language": lang
                })

            except:
                continue

    print("Fetched files:", len(code_files))  # 🔥 DEBUG

    return code_files
