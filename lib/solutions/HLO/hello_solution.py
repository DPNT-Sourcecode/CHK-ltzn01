def hello(friend_name: str) -> str:
    """
    Returns a greeting message.

    Args:
        friend_name (str): A name to be included in the greeting.
    
    Returns:
        str: A greeting message.
    """
    if not friend_name:
        raise ValueError("Friend name cannot be empty")
    return f"Hello, {friend_name}!"
