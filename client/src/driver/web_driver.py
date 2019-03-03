import time

from selenium.webdriver.common.by import By

from driver import Driver
from config import Configuration
from exceptions import ElementNotFound
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec


class WebDriver(Driver):
    def __init__(self, driver, element):
        super().__init__(driver, element)

    def get_element(self, element_id, from_item=None, by=By.CLASS_NAME):
        from_item = self.driver if from_item is None else from_item
        elements = from_item.find_elements(by, element_id)
        size = len(elements)

        if size > 0:
            e = elements[0]
            return self.create_element(e, e.tag_name)
        else:
            raise ElementNotFound()

    def get_elements(self, element_id, from_item=None, by=By.CLASS_NAME):
        from_item = self.driver if from_item is None else from_item
        items = from_item.find_elements(by, element_id)
        elements = self.create_elements(items)
        return elements

    def wait_until_load(self, element_id, by=By.CLASS_NAME):
        return WebDriverWait(self.driver, Configuration.config["loading_timeout"]).until(
            Ec.element_to_be_clickable((by, element_id)))

    def navigate_to(self, url):
        self.driver.get(url)
        return self.driver.title

    def scroll_to_bottom(self, times):
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        for i in range(0, times):
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(Configuration.config["scroll_pause_time"])
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def create_element(self, e, tag):
        return self.element(e, self, tag)

    def create_elements(self, items):
        elements = []
        for e in items:
            elements.append(self.create_element(e, e.tag_name))

        return elements

    def close(self):
        self.driver.close()
