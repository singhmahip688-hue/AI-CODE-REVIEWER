function showLoading(show) {
    document.getElementById("loading").style.display = show ? "block" : "none";
}


// 🔹 Analyze Code
function analyze() {
    const code = document.getElementById("code").value;

    showLoading(true);

    fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ code })
    })
    .then(res => res.json())
    .then(data => {
        showLoading(false);
        displayResult(data);
    })
    .catch(() => {
        showLoading(false);
        alert("Error analyzing code");
    });
}


function analyzeRepo() {
    const repo = document.getElementById("repo").value;

    showLoading(true);

    fetch("http://127.0.0.1:5000/analyze_repo", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ repo_url: repo })
    })
    .then(res => res.json())
    .then(data => {
        showLoading(false);

        // 🔥 Show dashboard
        document.getElementById("repoDashboard").style.display = "block";

        // 🔹 RAW OUTPUT (optional)
        document.getElementById("output").innerText =
            JSON.stringify(data, null, 2);

        // 🔹 SUMMARY
        const summary = data.summary;

        document.getElementById("summary").innerHTML = `
            <div>⭐ Score: ${summary.repo_score}</div>
            <div>📁 Files: ${summary.total_files}</div>
            <div>🐞 Bugs: ${summary.total_bugs}</div>
            <div>⚠️ Smells: ${summary.total_smells}</div>
        `;

        // 🔹 TABLE
        const tbody = document.querySelector("#fileTable tbody");
        tbody.innerHTML = "";

        data.files.forEach(file => {
            tbody.innerHTML += `
                <tr onclick='showFileDetail(${JSON.stringify(file)})'>
                    <td>${file.file}</td>
                    <td>${file.score}</td>
                    <td>${file.bugs.length}</td>
                    <td>${file.code_smells.length}</td>
                </tr>
            `;
        });

        // 🔹 WORST FILES
        document.getElementById("worstFiles").innerHTML =
            data.worst_files.length > 0
                ? data.worst_files.map(f => `<p class="bug">❌ ${f}</p>`).join("")
                : "<p class='good'>No critical files ✅</p>";

    })
    .catch(err => {
        showLoading(false);
        console.error(err);
        alert("Error analyzing repo");
    });
}

// 🔥 Display result
function displayResult(data) {
    document.getElementById("output").innerText =
        JSON.stringify(data, null, 2);

    let html = "";

    if (data.bugs?.length) {
        html += "<h3 class='bug'>Bugs:</h3>";
        data.bugs.forEach(b => html += `<p class='bug'>• ${b}</p>`);
    }

    if (data.code_smells?.length) {
        html += "<h3 class='smell'>Code Smells:</h3>";
        data.code_smells.forEach(s => html += `<p class='smell'>• ${s}</p>`);
    }

    if (data.complexity?.length) {
        html += "<h3>Complexity:</h3>";
        data.complexity.forEach(c =>
            html += `<p>${c.name} → ${c.complexity}</p>`
        );
    }

    if (data.score !== undefined) {
        let cls = data.score >= 80 ? "high" : data.score >= 50 ? "medium" : "low";
        html += `<h2 class="score ${cls}">Score: ${data.score}/100</h2>`;
    }

    if (!html) {
        html = "<h3 class='good'>No issues found ✅</h3>";
    }

    document.getElementById("issues").innerHTML = html;
}
function showFileDetail(file) {
    document.getElementById("fileDetail").style.display = "block";

    document.getElementById("fileDetail").scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

    let html = `
        <h2>${file.file}</h2>
        <p><b>Score:</b> ${file.score}/100</p>
    `;

    if (file.bugs.length > 0) {
        html += "<h3 class='bug'>Bugs:</h3>";
        file.bugs.forEach(b => html += `<p class='bug'>• ${b}</p>`);
    } else {
        html += "<p class='good'>No bugs ✅</p>";
    }

    if (file.code_smells.length > 0) {
        html += "<h3 class='smell'>Code Smells:</h3>";
        file.code_smells.forEach(s => html += `<p class='smell'>• ${s}</p>`);
    } else {
        html += "<p class='good'>No code smells ✅</p>";
    }

    document.getElementById("fileContent").innerHTML = html;
}