import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.ui import WebDriverWait

from driver import Driver
from driver.elements import WebElement
from exceptions import ElementNotFound

from config import Configuration


class WebDriver(Driver):
    def __init__(self):
        super().__init__()
        self.config = None
        self.driver = None
        self.element = None

    def define_dependencies(self):
        self.add_dependency(Configuration)

    def construct(self, dependencies):
        self.config = self.get_dependency(Configuration, dependencies)
        self.driver = self.create_driver()
        self.element = WebElement

    def create_driver(self):
        # Load the Chrome webdriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")

        # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads
        # and put it as an environment variable
        return webdriver.Chrome(options=chrome_options, executable_path="chromedriver")

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
        return WebDriverWait(self.driver, self.config.get("loading_timeout")).until(
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
            time.sleep(self.config.get("scroll_pause_time"))
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
