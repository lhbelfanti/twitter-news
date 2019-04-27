import unittest
from unittest.mock import MagicMock

from selenium.webdriver.common.by import By

from driver import TwitterDriver
from driver.elements import WebElement as OwnWebElement


class ElementTest(unittest.TestCase):
    def setUp(self):
        self._driver = TwitterDriver()
        attrs = {'get.return_value': 10}
        config_mock = MagicMock(**attrs)
        self._driver.config = config_mock

    def setup_test(self):
        self._driver.create_driver()
        self._driver.navigate_to("https://www.python.org/")

    def _assert_element_obtained(self, element):
        self.assertIsInstance(element, OwnWebElement)
        self.assertIsNotNone(element)

    def test_should_get_element_from_element(self):
        self.setup_test()
        element = self._driver.get_element("options-bar")
        self._assert_element_obtained(element)
        # Get element from another element than the driver
        element2 = element.get_element("search-the-site")
        self._assert_element_obtained(element2)

    def test_should_get_elements_from_element(self):
        self.setup_test()
        element = self._driver.get_element("ul[aria-label='Main Navigation']", None, By.CSS_SELECTOR)
        elements = element.get_elements("tier-1", By.CLASS_NAME)
        size = len(elements)
        self.assertEqual(size, 7)
        for e in elements:
            self._assert_element_obtained(e)

    def test_should_get_attribute(self):
        self.setup_test()
        element = self._driver.get_element("a[title='The Python Programming Language']", None, By.CSS_SELECTOR)
        link_attr = element.get_attribute("href")
        self.assertEqual(link_attr, "https://www.python.org/")

    def test_should_be_able_to_write_into_text_field(self):
        self.setup_test()
        text_field = self._driver.get_element("input[type='search']", None, By.CSS_SELECTOR)
        text_field.write("Testing")
        self.assertEqual(text_field.get_attribute("value"), "Testing")

    def test_should_be_able_to_click_on_button(self):
        self.setup_test()
        button = self._driver.get_element("search-button")
        button.click()
        self.assertEqual(self._driver.driver.current_url, "https://www.python.org/search/?q=&submit=")
