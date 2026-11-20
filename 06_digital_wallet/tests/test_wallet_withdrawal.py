"""Unit tests for withdraw() in wallet_withdrawal.py.

Expected results come from the Digital Wallet Requirements Specification
(section 3.1), NOT from what the code currently does.
"""
import pytest

from wallet_withdrawal import withdraw


# ---------- Valid inputs: the remaining balance is returned ----------
@pytest.mark.parametrize(
    "balance, amount, expected",
    [
        (1000, 400, 600),   # normal withdrawal
        (1000, 1, 999),     # smallest valid amount
        (1000, 999, 1),     # one cent short of the balance
    ],
)
def test_withdraw_valid_amount_returns_remaining_balance(balance, amount, expected):
    assert withdraw(balance, amount) == expected


# ---------- Boundary: withdrawing the exact balance is allowed ----------
@pytest.mark.parametrize("balance, amount", [(1000, 1000), (1, 1)])
def test_withdraw_exact_balance_returns_zero(balance, amount):
    assert withdraw(balance, amount) == 0


def test_withdraw_returns_an_int():
    result = withdraw(1000, 400)
    assert type(result) is int


# ---------- ValueError: right type, value outside the permitted range ----------
@pytest.mark.parametrize(
    "balance, amount",
    [
        (1000, 1001),   # amount above balance
        (0, 1),         # nothing to withdraw from
        (1000, 0),      # zero amount
        (1000, -1),     # negative amount
        (0, 0),         # zero amount, zero balance
        (-1, 100),      # negative balance
    ],
)
def test_withdraw_out_of_range_raises_value_error(balance, amount):
    with pytest.raises(ValueError):
        withdraw(balance, amount)


# ---------- TypeError: wrong data type (bool is NOT a valid int) ----------
@pytest.mark.parametrize("bad_balance", [1000.0, "1000", None, True])
def test_withdraw_invalid_balance_type_raises_type_error(bad_balance):
    with pytest.raises(TypeError):
        withdraw(bad_balance, 100)


@pytest.mark.parametrize("bad_amount", [100.5, "100", None, True])
def test_withdraw_invalid_amount_type_raises_type_error(bad_amount):
    with pytest.raises(TypeError):
        withdraw(1000, bad_amount)
