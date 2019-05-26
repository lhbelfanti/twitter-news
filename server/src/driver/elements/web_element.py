from selenium.webdriver.common.by import By

from driver.elements import Element


class WebElement(Element):
    def __init__(self, element, driver, tag=""):
        super().__init__(element, driver, tag)

    def get_element(self, element_id, by=By.CLASS_NAME, force_default=False):
        return self.driver.get_element(element_id, by, self.element, force_default)

    def get_elements(self, element_id, by=By.TAG_NAME):
        return self.driver.get_elements(element_id, by, self.element)

    def get_attribute(self, attr_id):
        return self.element.get_attribute(attr_id)

    def write(self, text):
        self.element.send_keys(text)

    def click(self):
        self.element.click()

    @property
    def text(self):
        return self.element.text if self.element is not None else ""
