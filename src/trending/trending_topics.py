import constants
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TrendingTopics:
    def __init__(self, driver, callback):
        self.driver = driver
        self.trends = []
        self.callback = callback

    def start(self):
        try:
            wait = WebDriverWait(self.driver, constants.TRENDS_TIMEOUT)
            element_loaded = Ec.presence_of_element_located((By.CLASS_NAME, constants.TRENDS_CONTAINER))
            wait.until(element_loaded)
            self.get_trends()
        except TimeoutException:
            print("Loading took too much time!")

    def get_trends(self):
        # Get all of the items of the list
        items = self.driver.find_elements(By.CLASS_NAME, constants.TREND_ITEM)
        for item in items:
            item_obj = {}
            # Get information of each item
            a_element = item.find_element(By.CLASS_NAME, constants.TREND_A_TAG)
            title_element = a_element.find_element(By.CLASS_NAME, constants.TRENDS_TITLE)
            desc_element = a_element.find_element(By.CLASS_NAME, constants.TRENDS_DESC)
            item_obj["title"] = title_element.text
            item_obj["desc"] = desc_element.text

            try:
                tweets_element = a_element.find_element(By.CLASS_NAME, constants.TRENDS_TWEETS)
            except NoSuchElementException:
                item_obj["tweets"] = ""

            item_obj["tweets"] = tweets_element.text

            items.append(item_obj)
            print("Adding")
            print(items)

        self.callback(items)
