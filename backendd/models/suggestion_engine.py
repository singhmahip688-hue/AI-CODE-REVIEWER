def generate_suggestions(smells, complexity):
    suggestions = []

    if smells:
        suggestions.append("Refactor code to reduce complexity and improve readability")

    for item in complexity:
        if item["complexity"] > 10:
            suggestions.append(f"Reduce complexity in function '{item['name']}'")

    return suggestions