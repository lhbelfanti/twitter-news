import unittest
from unittest.mock import MagicMock, patch

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from driver import TwitterDriver
from driver.elements import WebElement as OwnWebElement
from exceptions import ElementNotFound


class DriverTest(unittest.TestCase):
    def setUp(self):
        self._driver = TwitterDriver()
        attrs = {'get.return_value': 10}
        config_mock = MagicMock(**attrs)
        self._driver.config = config_mock

    def setup_test(self):
        self._driver.create_driver()
        self._driver.navigate_to("https://www.python.org/")

    def test_should_create_driver(self):
        self._driver.create_driver()
        self.assertIsInstance(self._driver.driver, WebDriver)

    def test_navigate_to(self):
        self._driver.create_driver()
        self._driver.navigate_to("https://www.python.org/")
        self.assertIn("Python", self._driver.driver.title)

        with self.assertRaises(WebDriverException):
            self._driver.navigate_to("non-existent-url")

    def test_should_wait_element_to_be_loaded(self):
        self.setup_test()
        element = self._driver.wait_until_load("python-logo")
        self.assertIsInstance(element, WebElement)
        self.assertIsNotNone(element)

    @patch("selenium.webdriver.support.ui.WebDriverWait.until", side_effect=TimeoutException)
    def test_should_throw_timeout_exception(self, wd_mock):
        self.setup_test()
        with self.assertRaises(TimeoutException):
            self._driver.wait_until_load("python-logo")

    def test_should_get_element(self):
        self.setup_test()
        # Basic case
        element = self._driver.get_element("options-bar",,
        self._assert_element_obtained(element)
        # Get element by css selector
        element2 = self._driver.get_element("img[class='python-logo']", By.CSS_SELECTOR, None)
        self._assert_element_obtained(element2)

    def test_get_element_should_throw_exception(self):
        self.setup_test()
        with self.assertRaises(ElementNotFound) as cm:
            self._driver.get_element("non-existent-element",,
        print(cm.exception.args[0])

    def test_should_get_elements(self):
        self.setup_test()
        elements = self._driver.get_elements("tier-1",,
        size = len(elements)
        self.assertEqual(size, 22)
        for element in elements:
            self._assert_element_obtained(element)

    def test_get_elements_should_be_empty(self):
        self.setup_test()
        elements = self._driver.get_elements("non-existent-element",,
        size = len(elements)
        self.assertEqual(size, 0)

    def _assert_element_obtained(self, element):
        self.assertIsInstance(element, OwnWebElement)
        self.assertIsNotNone(element)

    def test_scroll_to_bottom(self):
        attrs = {'get.return_value': 2}
        config_mock = MagicMock(**attrs)
        self._driver.config = config_mock
        self.setup_test()
        y1 = self._driver.driver.execute_script("return window.pageYOffset;")
        self._driver.scroll_to_bottom(1)
        y2 = self._driver.driver.execute_script("return window.pageYOffset;")
        self.assertGreater(y2, y1)

    def tearDown(self):
        self._driver.config = None
        self._driver.close()
