def calculate_score(complexity, smells, bugs):
    score = 100

    score -= len(smells) * 5
    score -= len(bugs) * 10

    for item in complexity:
        if item["complexity"] > 10:
            score -= 5

    return max(score, 0)