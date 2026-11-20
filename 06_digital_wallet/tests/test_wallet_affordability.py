"""Unit tests for can_afford() in wallet_affordability.py.

Expected results come from the Digital Wallet Requirements Specification
(section 3.2), NOT from what the code currently does.
"""
import pytest

from wallet_affordability import can_afford


# ---------- Logic: is the purchase affordable? ----------
# (== is used here on purpose: this group checks the LOGIC only.
#  The return TYPE is checked separately below.)
@pytest.mark.parametrize(
    "balance, price",
    [
        (500, 400),   # balance above price
        (500, 500),   # boundary: balance equals price
        (500, 499),   # boundary: one cent above price
        (0, 0),       # zero price, zero balance
        (500, 0),     # zero price, positive balance
    ],
)
def test_can_afford_balance_covers_price_is_true(balance, price):
    assert can_afford(balance, price) == True  # noqa: E712


@pytest.mark.parametrize(
    "balance, price",
    [
        (400, 500),   # balance below price
        (499, 500),   # boundary: one cent below price
        (0, 1),       # empty balance
    ],
)
def test_can_afford_balance_too_low_is_false(balance, price):
    assert can_afford(balance, price) == False  # noqa: E712


# ---------- Return type: must be a real bool (1 and 0 are not accepted) ----------
@pytest.mark.parametrize("balance, price, expected", [(500, 400, True), (400, 500, False)])
def test_can_afford_returns_real_bool(balance, price, expected):
    result = can_afford(balance, price)
    assert result is expected


# ---------- ValueError: right type, negative value ----------
@pytest.mark.parametrize("balance, price", [(-1, 100), (100, -1), (-1, -1)])
def test_can_afford_negative_value_raises_value_error(balance, price):
    with pytest.raises(ValueError):
        can_afford(balance, price)


# ---------- TypeError: wrong data type (bool is NOT a valid int) ----------
@pytest.mark.parametrize("bad_balance", [100.0, "100", None, True])
def test_can_afford_invalid_balance_type_raises_type_error(bad_balance):
    with pytest.raises(TypeError):
        can_afford(bad_balance, 50)


@pytest.mark.parametrize("bad_price", [50.5, "50", None, True])
def test_can_afford_invalid_price_type_raises_type_error(bad_price):
    with pytest.raises(TypeError):
        can_afford(100, bad_price)
