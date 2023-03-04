from random import randrange as r


def get_color():
    """Get a random color as (r,g,b)

    Returns:
        tuple: tuple of an RGB color represented as (r,g,b)
    """
    return (r(0, 255), r(0, 255), r(0, 255))