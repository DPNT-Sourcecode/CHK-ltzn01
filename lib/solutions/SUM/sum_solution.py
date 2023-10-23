def compute(x: int, y: int) -> int:
    """
    Adds two positive integers.

    Args:
        x (int): A positive integer between 0 and 100.
        y (int): A positive integer between 0 and 100.

    Returns:
        int: The sum of x and y.

    Raises:
        ValueError: If x or y is not between 0 and 100 inclusive.
    """
    if not (0 <= x <= 100) or not (0 <= y <= 100):
        raise ValueError("x and y must be between 0 and 100")
    return x + y
