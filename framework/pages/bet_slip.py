from decimal import Decimal

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from framework.pages.base_page import BasePage
from framework.pages.modals import ErrorModal, SuccessReceiptModal
from framework.utils.money import parse_money


class BetSlip(BasePage):
    STAKE_INPUT = (By.ID, "bet-slip-stake-input")
    TOTAL_STAKE = (By.ID, "bet-slip-total-stake")
    POTENTIAL_PAYOUT = (By.ID, "bet-slip-potential-payout")
    PLACE_BET = (By.ID, "bet-slip-place-bet")
    SELECTION_COUNT = (By.ID, "bet-slip-count")

    def enter_stake(self, stake: str) -> None:
        self.type_into(self.STAKE_INPUT, stake)

    def potential_payout(self) -> Decimal:
        return parse_money(self.text_of(self.POTENTIAL_PAYOUT))

    def selection_count(self) -> int:
        return int(self.text_of(self.SELECTION_COUNT))

    def place_bet(self, max_retries: int = 2) -> SuccessReceiptModal:
        self.click(self.PLACE_BET)
        success, error = SuccessReceiptModal(self.driver), ErrorModal(self.driver)

        for attempt in range(max_retries + 1):
            outcome = WebDriverWait(self.driver, 15).until(
                EC.any_of(
                    EC.visibility_of_element_located(SuccessReceiptModal.ROOT),
                    EC.visibility_of_element_located(ErrorModal.ROOT),
                )
            )
            if outcome.get_attribute("id") == "modal-success":
                return success
            if attempt < max_retries:
                error.rebet()
        raise TimeoutException(f"Bet still failing after {max_retries} Rebet attempts")
