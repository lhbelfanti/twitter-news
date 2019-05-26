import time
import constants

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.ui import WebDriverWait

from driver import Driver
from driver.elements import WebElement
from exceptions import ElementNotFound

from config import Configuration


class TwitterDriver(Driver):
    def __init__(self):
        super().__init__()
        self._config = None
        self._driver = None
        self._element = WebElement

    def _define_dependencies(self):
        self._add_dependency(Configuration)

    def construct(self, dependencies):
        self._config = self._get_dependency(Configuration, dependencies)
        self.create_driver()

    def create_driver(self):
        # Load the Chrome webdriver
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")

        # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads
        # and put it as an environment variable
        self._driver = webdriver.Chrome(options=chrome_options, executable_path="chromedriver")

    def get_element(self, element_id, by=By.CLASS_NAME, from_item=None, force_default=False):
        from_item = self._driver if from_item is None else from_item
        elements = from_item.find_elements(by, element_id)
        size = len(elements)

        if size > 0:
            e = elements[0]
            return self._create_element(e, e.tag_name)
        elif force_default:
            return self._create_element(None, "tag")
        else:
            raise ElementNotFound()

    def get_elements(self, element_id, by=By.CLASS_NAME, from_item=None):
        from_item = self._driver if from_item is None else from_item
        items = from_item.find_elements(by, element_id)
        elements = self._create_elements(items)
        return elements

    def wait_until_load(self, element_id, by=By.CLASS_NAME):
        return WebDriverWait(self._driver,
                             self._config.get_prop("loading_timeout", constants.DE_CFG)
                             ).until(Ec.element_to_be_clickable((by, element_id)))

    def navigate_to(self, url):
        self._driver.get(url)
        return self._driver.title

    def scroll_to_bottom(self, times):
        # Get scroll height
        last_height = self._driver.execute_script("return document.body.scrollHeight")

        for i in range(0, times):
            # Scroll down to bottom
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(self._config.get_prop("scroll_pause_time", constants.DE_CFG))
            # Calculate new scroll height and compare with last scroll height
            new_height = self._driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def _create_element(self, e, tag):
        return self._element(e, self, tag)

    def _create_elements(self, items):
        elements = []
        for e in items:
            elements.append(self._create_element(e, e.tag_name))

        return elements

    def close(self):
        self._driver.close()

    # Getters and setters
    @property
    def driver(self):
        return self._driver

    @property
    def config(self, value):
        self._config = value

    @config.setter
    def config(self, value):
        self._config = value
