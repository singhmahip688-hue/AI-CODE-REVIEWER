from radon.complexity import cc_visit

def analyze_complexity(code):
    try:
        results = cc_visit(code)
        output = []

        for block in results:
            output.append({
                "name": block.name,
                "complexity": block.complexity,
                "lineno": block.lineno
            })

        return output
    except:
        return []