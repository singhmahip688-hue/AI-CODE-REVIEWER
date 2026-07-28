def detect_bugs(code):
    bugs = []

    if "== None" in code:
        bugs.append("Use 'is None' instead of '== None'")

    if "/ 0" in code:
        bugs.append("Possible division by zero")

    if "while True" in code:
        bugs.append("Possible infinite loop")

    return bugs