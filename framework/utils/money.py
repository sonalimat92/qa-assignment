import re
from decimal import ROUND_HALF_UP, Decimal

_NON_NUMERIC = re.compile(r"[^\d.\-]")


def parse_money(text: str) -> Decimal:
    cleaned = _NON_NUMERIC.sub("", text.replace(",", ""))
    if not cleaned:
        raise ValueError(f"No amount found in {text!r}")
    return Decimal(cleaned)


def expected_payout(stake: Decimal, odds: Decimal) -> Decimal:
    return (stake * odds).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
