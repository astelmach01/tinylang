def evaluate_expression(expression: str) -> float | str:
    """
    Useful when needed for mathematical calculations.
    Evaluates a mathematical expression such as '(10 + 2) ** 2' and return the result as a float.

    Args:
        expression (str): The mathematical expression to evaluate.

    Returns:
        float or string: The result of the evaluated expression, or an error message if the expression is invalid.
    """
    try:
        result = eval(expression)
        return float(result)
    except Exception as e:
        return f"Error: {str(e)}"
