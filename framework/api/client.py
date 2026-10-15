from datetime import date
from typing import Any

import requests


class BettingApiClient:
    def __init__(self, base_url: str, user_id: str, timeout: int = 15) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"x-user-id": user_id, "Content-Type": "application/json"})

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def get_matches(self) -> requests.Response:
        return self.session.get(self._url("/api/matches"), timeout=self.timeout)

    def get_balance(self) -> requests.Response:
        return self.session.get(self._url("/api/balance"), timeout=self.timeout)

    def place_bet(self, match_id: str, selection: str, stake: Any) -> requests.Response:
        payload = {"matchId": match_id, "selection": selection, "stake": stake}
        return self.session.post(self._url("/api/place-bet"), json=payload, timeout=self.timeout)

    def reset_balance(self) -> requests.Response:
        return self.session.post(self._url("/api/reset-balance"), timeout=self.timeout)

    def get_balance_amount(self) -> float:
        response = self.get_balance()
        response.raise_for_status()
        return float(response.json()["balance"])

    def upcoming_matches(self) -> list[dict]:
        response = self.get_matches()
        response.raise_for_status()
        today = date.today().isoformat()
        return [m for m in response.json() if m["kickoffDate"] >= today]
