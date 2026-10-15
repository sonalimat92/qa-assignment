from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from framework.pages.base_page import BasePage
from framework.utils.money import parse_money


class SuccessReceiptModal(BasePage):
    ROOT = (By.ID, "modal-success")
    BET_ID = (By.ID, "modal-success-bet-id")
    MATCH = (By.ID, "modal-success-match")
    STAKE = (By.ID, "modal-success-stake")
    ODDS = (By.ID, "modal-success-odds")
    PAYOUT = (By.ID, "modal-success-payout")
    PLACED_AT = (By.ID, "modal-success-placed-at")
    CLOSE = (By.ID, "modal-success-close")

    def bet_id(self) -> str:
        return self.text_of(self.BET_ID)

    def match(self) -> str:
        return self.text_of(self.MATCH)

    def stake(self) -> Decimal:
        return parse_money(self.text_of(self.STAKE))

    def odds(self) -> Decimal:
        return Decimal(self.text_of(self.ODDS))

    def payout(self) -> Decimal:
        return parse_money(self.text_of(self.PAYOUT))

    def placed_at(self) -> str:
        return self.text_of(self.PLACED_AT)

    def close(self) -> None:
        self.click(self.CLOSE)
        self.wait.until(EC.invisibility_of_element_located(self.ROOT))


class ErrorModal(BasePage):
    ROOT = (By.ID, "modal-error")
    REBET = (By.ID, "modal-error-rebet")
    CLOSE = (By.ID, "modal-error-close")

    def rebet(self) -> None:
        self.click(self.REBET)
        self.wait.until(EC.invisibility_of_element_located(self.ROOT))
