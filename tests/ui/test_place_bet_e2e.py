from decimal import Decimal

import pytest

from framework.pages.bet_slip import BetSlip
from framework.pages.match_list_page import MatchListPage
from framework.utils.money import expected_payout

STAKE = Decimal("10.00")
SELECTION = "HOME"


@pytest.mark.ui
@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason=(
        "Known defects: BUG-04 receipt payout is stake x 2, BUG-05 receipt lists teams "
        "away-vs-home, BUG-08 header balance not refreshed after a bet"
    ),
)
def test_place_single_bet_end_to_end(driver, config, api_client, fresh_balance, upcoming_match):
    match = upcoming_match
    odds = Decimal(str(match["odds"]["home"]))
    starting_balance = Decimal(str(fresh_balance))

    page = MatchListPage(driver, config.explicit_wait_seconds).open(config.base_url, config.user_id)
    assert page.header_balance() == starting_balance

    page.select_odds(match["id"], SELECTION)
    slip = BetSlip(driver, config.explicit_wait_seconds)
    slip.enter_stake(str(STAKE))
    assert slip.potential_payout() == expected_payout(STAKE, odds)

    receipt = slip.place_bet()
    assert receipt.bet_id(), "Receipt should show a bet id"
    assert receipt.placed_at(), "Receipt should show a placement timestamp"

    actual_receipt = {
        "match": receipt.match(),
        "stake": receipt.stake(),
        "odds": receipt.odds(),
        "payout": receipt.payout(),
    }
    expected_receipt = {
        "match": f"{match['homeTeam']} vs {match['awayTeam']}",
        "stake": STAKE,
        "odds": odds,
        "payout": expected_payout(STAKE, odds),
    }
    assert actual_receipt == expected_receipt

    receipt.close()
    expected_balance = starting_balance - STAKE
    assert Decimal(str(api_client.get_balance_amount())) == expected_balance, "Server balance"
    assert page.header_balance() == expected_balance, "Header balance shown to the user"
    assert slip.selection_count() == 0, "Closing the receipt should clear the selection"
