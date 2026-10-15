import pytest

INVALID_STAKES = [
    pytest.param(0.99, "invalid_stake_min", id="below-minimum-0.99"),
    pytest.param(0, "invalid_stake_min", id="zero"),
    pytest.param(
        -5,
        "invalid_stake_min",
        id="negative",
        marks=pytest.mark.xfail(strict=True, raises=AssertionError, reason="BUG-02: negative stake accepted, balance grows"),
    ),
    pytest.param(100.01, "invalid_stake_max", id="above-maximum-100.01"),
    pytest.param(1.234, "invalid_stake_precision", id="three-decimal-places"),
    pytest.param("10", "invalid_stake_type", id="numeric-string"),
    pytest.param(None, "invalid_stake_type", id="null"),
]


@pytest.mark.api
@pytest.mark.parametrize("stake, expected_error", INVALID_STAKES)
def test_invalid_stake_is_rejected_and_balance_unchanged(
    api_client, fresh_balance, upcoming_match, stake, expected_error
):
    response = api_client.place_bet(upcoming_match["id"], "HOME", stake)

    assert response.status_code == 422, response.text
    assert response.json()["error"] == expected_error
    assert api_client.get_balance_amount() == fresh_balance, "A rejected bet must not move money"


@pytest.mark.api
@pytest.mark.xfail(
    strict=True, raises=AssertionError, reason="BUG-01: API accepts stakes above balance, balance goes negative"
)
def test_stake_exceeding_available_balance_is_rejected(api_client, fresh_balance, upcoming_match):
    drain_stake = min(100, round(fresh_balance - 10, 2))
    assert api_client.place_bet(upcoming_match["id"], "HOME", drain_stake).status_code == 200
    balance = api_client.get_balance_amount()

    response = api_client.place_bet(upcoming_match["id"], "HOME", round(balance + 1, 2))

    assert response.status_code == 422, response.text
    assert response.json()["error"] == "insufficient_balance"
    assert api_client.get_balance_amount() == balance
