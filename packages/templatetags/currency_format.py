"""Template filters for INR-style number display (Indian comma grouping)."""
from decimal import Decimal, ROUND_HALF_UP

from django import template

register = template.Library()


def _to_int(value):
    if value is None:
        return 0
    if isinstance(value, Decimal):
        return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return 0


def _indian_commas(n: int) -> str:
    """Group digits as ...,XX,XX,XXX (last group 3, then pairs from the right)."""
    n = abs(int(n))
    s = str(n)
    if len(s) <= 3:
        return s
    last_three = s[-3:]
    rest = s[:-3]
    pairs = []
    while rest:
        pairs.insert(0, rest[-2:])
        rest = rest[:-2]
    return ",".join(pairs) + "," + last_three


@register.filter(name="inr_commas")
def inr_commas(value):
    """
    Format a numeric amount with Indian-style thousands separators.
    Example: 1234567 -> '12,34,567'
    """
    return _indian_commas(_to_int(value))
