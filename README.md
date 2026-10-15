# QA Home Assignment – Single Bet Placement

Manual testing, bug reports and automation for the sports betting test application.

## Deliverables

| Deliverable | File |
|-------------|------|
| Test plan (scenarios + test cases) | [docs/01_Test_Plan.docx](docs/01_Test_Plan.docx) |
| Test execution report (Pass / Fail) | [docs/02_Test_Execution_Report.docx](docs/02_Test_Execution_Report.docx) |
| Bug reports (with screenshots) | [docs/03_Bug_Reports.docx](docs/03_Bug_Reports.docx) |
| Automation strategy and recommendations | [docs/04_Automation_Strategy.docx](docs/04_Automation_Strategy.docx) |
| Screenshots | [docs/evidence/](docs/evidence/) |
| Automation framework and 2 tests | `framework/`, `tests/` |

## Results at a Glance
- 57 test cases executed: 36 passed, 21 failed
- 19 bugs logged: 2 Critical, 6 High, 6 Medium, 5 Low

## Tech Stack
- Python 3.10+
- pytest – test runner
- Selenium – UI tests
- requests – API tests
- python-dotenv – reads settings from `.env`

## Project Structure
```
config/settings.py           Settings (URL, user ID, headless, timeouts)
framework/api/client.py      API client
framework/pages/             Page objects
framework/utils/money.py     Money helpers
tests/conftest.py            Fixtures
tests/api/                   API test
tests/ui/                    UI test
docs/                        Test plan, execution report, bug reports, strategy (.docx)
```

## Setup
You need Python 3.10+ and Google Chrome. Selenium downloads the right ChromeDriver automatically.

```bash
git clone https://github.com/sonalimat92/qa-assignment.git
cd qa-assignment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then put your user ID in .env
```

`.env` example:
```
BASE_URL=https://qae-assignment-tau.vercel.app
USER_ID=your-user-id
HEADLESS=true
```

Optional settings (only needed if Chrome is not found automatically, for example in a Docker/CI container):
```
CHROME_BINARY=/path/to/chrome
CHROMEDRIVER_PATH=/path/to/chromedriver
CHROME_ARGS=--no-sandbox --disable-dev-shm-usage
```

## Run the Tests
```bash
pytest                       # run all tests
pytest -m api                # API tests only
pytest -m ui                 # UI test only
HEADLESS=false pytest -m ui  # see the browser while the test runs
```
Run tests one at a time (not in parallel), because all tests use the same user.

## Understanding the Results
Some tests check bugs that are already logged. They are marked as `xfail` with the bug ID.

| Result | Meaning |
|--------|---------|
| `passed` | Test passed |
| `xfailed` | Known bug is still there (expected) |
| `XPASS` (run fails) | Known bug is fixed – remove the `xfail` mark from the test |
| `failed` | New problem – investigate |

The `xfail` marks only accept an `AssertionError`. If the browser cannot start, a page element is missing, or the API is down, the test shows as `failed` / `error` – it is never hidden as a known bug.

**Expected result today: 6 passed, 3 xfailed**
- `test_stake_exceeding_available_balance_is_rejected` → BUG-01
- `test_invalid_stake_is_rejected_and_balance_unchanged[negative]` → BUG-02
- `test_place_single_bet_end_to_end` → BUG-04, BUG-05, BUG-08

If a UI test fails, a screenshot is saved in `reports/screenshots/`.
