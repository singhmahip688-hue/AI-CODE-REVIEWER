def detect_code_smells(code):
    issues = []

    lines = code.split('\n')

    # Long function detection
    if len(lines) > 50:
        issues.append("Function too long (>50 lines)")

    # Deep nesting detection
    indent_levels = [len(line) - len(line.lstrip()) for line in lines]
    if max(indent_levels, default=0) > 12:
        issues.append("Deep nesting detected")

    # Too many variables
    if code.count('=') > 20:
        issues.append("Too many variables")

    return issues