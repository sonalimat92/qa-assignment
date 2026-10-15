from decimal import Decimal

from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage
from framework.utils.money import parse_money

SELECTION_TO_ID_SUFFIX = {"HOME": "home", "DRAW": "draw", "AWAY": "away"}


class MatchListPage(BasePage):
    HEADER_BALANCE = (By.ID, "header-balance")
    MATCH_LIST = (By.ID, "match-list")

    def open(self, base_url: str, user_id: str) -> "MatchListPage":
        self.driver.get(f"{base_url}/?user-id={user_id}")
        self.find_visible(self.MATCH_LIST)
        return self

    def header_balance(self) -> Decimal:
        return parse_money(self.text_of(self.HEADER_BALANCE))

    def select_odds(self, match_id: str, selection: str) -> None:
        suffix = SELECTION_TO_ID_SUFFIX[selection]
        self.click((By.ID, f"odds-{match_id}-{suffix}"))
