import sys

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

Locator = tuple[str, str]
SELECT_ALL_MODIFIER = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find_visible(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator: Locator) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()

    def text_of(self, locator: Locator) -> str:
        return self.find_visible(locator).text.strip()

    def type_into(self, locator: Locator, value: str) -> None:
        element = self.find_visible(locator)
        element.send_keys(SELECT_ALL_MODIFIER, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(value)
