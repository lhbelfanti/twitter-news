import constants
import utils
from exceptions import ElementNotFound, LoadingTimeout
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.common.exceptions import TimeoutException


class TrendingTopics:
    def __init__(self, driver, callback):
        self.driver = driver
        self.trends = []
        self.callback = callback

    def start(self):
        try:
            wait = WebDriverWait(self.driver, constants.LOADING_TIMEOUT)
            element_loaded = Ec.presence_of_element_located((By.CLASS_NAME, constants.TRENDS_CONTAINER))
            wait.until(element_loaded)
            self.get_trends()
        except TimeoutException:
            raise LoadingTimeout()

    def get_trends(self):
        # Get all of the items of the list
        items = utils.get_elements_by(By.CLASS_NAME, constants.TREND_ITEM, self.driver)
        for item in items:
            item_obj = {}

            # Get information of each item
            try:
                a_element = utils.get_element_by(By.CLASS_NAME, constants.TREND_A_TAG, item)
                title_element = utils.get_element_by(By.CLASS_NAME, constants.TRENDS_TITLE, a_element)
                desc_element = utils.get_element_by(By.CLASS_NAME, constants.TRENDS_DESC, a_element)
                tweets_element = utils.get_element_by(By.CLASS_NAME, constants.TRENDS_TWEETS, a_element)
            except ElementNotFound:
                continue

            item_obj["title"] = title_element.text
            item_obj["desc"] = desc_element.text
            item_obj["tweets"] = tweets_element.text

            items.append(item_obj)
            print("Adding")
            print(items)

        self.callback(items)
