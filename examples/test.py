def calculate_operation(operand1: float, operand2: float, operation: str) -> float:
    """
    Perform a basic arithmetic operation on two numbers.

    Args:
        operand1 (float): The first numeric operand.
        operand2 (float): The second numeric operand.
        operation (str): The arithmetic operation to perform.
            Supported operations are:
            - "add": addition
            - "sub": subtraction
            - "mul": multiplication
            - "div": division

    Returns:
        float: The result of the arithmetic operation.

    Raises:
        ValueError: If the operation is unknown.
        ZeroDivisionError: If division by zero is attempted.

    Example:
        >>> calculate_operation(4, 2, "add")
        6.0
        >>> calculate_operation(4, 0, "div")
        Traceback (most recent call last):
          ...
        ZeroDivisionError: Cannot divide by zero.

    """
    if operation == "add":
        return operand1 + operand2
    elif operation == "sub":
        return operand1 - operand2
    elif operation == "mul":
        return operand1 * operand2
    elif operation == "div":
        if operand2 == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return operand1 / operand2
    else:
        raise ValueError(f"Unknown operation: {operation}")

print(calculate_operation(4, 2, "add"))