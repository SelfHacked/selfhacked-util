from typing import Union


def format_price(
        price: Union[float, int]
) -> str:
    """
    Format price.
    If integer, format without decimals;
    otherwise, format with 2 decimals.
    """

    if isinstance(price, int) or int(price) == price:
        return f"{price:.0f}"
    else:
        return f"{price:.2f}"
