from config import Configuration
from exceptions import ElementNotFound
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from .driver_utils import DriverUtils


# Selenium WebDriver
class WebDriverUtils(DriverUtils):
    def get_element_by(self, by, element_id, from_item):
        elements = from_item.find_elements(by, element_id)
        size = len(elements)

        if size > 0:
            return elements[0]
        else:
            raise ElementNotFound()

    def get_elements_by(self, by, element_id, from_item):
        elements = from_item.find_elements(by, element_id)
        return elements

    def wait_until_load(self, by, element_id, driver):
        return WebDriverWait(driver, Configuration.config["loading_timeout"]).until(
            Ec.element_to_be_clickable((by, element_id)))
