from flask import Flask, request, jsonify
from flask_cors import CORS

# 🔹 Analyzer imports
from analyzer.complexity import analyze_complexity
from analyzer.code_smells import detect_code_smells
from analyzer.bug_detector import detect_bugs
from analyzer.score import calculate_score

# 🔹 Utils
from utils.github_fetcher import fetch_repo_files

app = Flask(__name__)
CORS(app)


# 🔹 Home Route
@app.route('/')
def home():
    return "AI Code Reviewer is running 🚀"


# 🔹 Analyze Direct Code
@app.route('/analyze', methods=['POST'])
def analyze_code():
    code = request.json.get("code")

    complexity = analyze_complexity(code)
    smells = detect_code_smells(code)
    bugs = detect_bugs(code)

    # ⭐ Score calculation
    score = calculate_score(complexity, smells, bugs)

    return jsonify({
        "complexity": complexity,
        "code_smells": smells,
        "bugs": bugs,
        "score": score
    })


# 🔹 Analyze GitHub Repository
@app.route('/analyze_repo', methods=['POST'])
def analyze_repo():
    repo_url = request.json.get("repo_url")

    print("Repo URL:", repo_url)

    # ✅ Try-catch (important)
    try:
        files = fetch_repo_files(repo_url)
        print("Fetched files:", len(files))
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

    # ✅ Empty repo handling
    if not files:
        return jsonify({
            "summary": {
                "repo_score": 0,
                "total_files": 0,
                "total_bugs": 0,
                "total_smells": 0
            },
            "files": [],
            "worst_files": []
        })

    all_results = []

    # 🔥 MAIN LOOP
    for file in files:
        code = file["code"]
        lang = file["language"]

        # 🔥 SMART MULTI-LANGUAGE LOGIC
        if lang == "python":
            complexity = analyze_complexity(code)
            smells = detect_code_smells(code)
            bugs = detect_bugs(code)
        else:
            complexity = []
            smells = [f"Basic analysis only for {lang}"]
            bugs = []

        score = calculate_score(complexity, smells, bugs)

        all_results.append({
            "file": file["file"],
            "language": lang,
            "complexity": complexity,
            "code_smells": smells,
            "bugs": bugs,
            "score": score
        })

    # 🔥 SUMMARY CALCULATION
    total_files = len(all_results)
    total_bugs = sum(len(f["bugs"]) for f in all_results)
    total_smells = sum(len(f["code_smells"]) for f in all_results)
    avg_score = int(sum(f["score"] for f in all_results) / total_files)

    # 🔥 WORST FILES
    worst_files = sorted(all_results, key=lambda x: x["score"])[:3]

    return jsonify({
        "summary": {
            "repo_score": avg_score,
            "total_files": total_files,
            "total_bugs": total_bugs,
            "total_smells": total_smells
        },
        "files": all_results,
        "worst_files": [f["file"] for f in worst_files]
    })


# 🔹 Run Server
if __name__ == "__main__":
    app.run(debug=True)
